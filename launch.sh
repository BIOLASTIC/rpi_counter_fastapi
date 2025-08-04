#!/bin/bash
# Box Counter System Launcher - COMPLETE MJPEG VERSION
# Uses direct MJPEG streaming for reliable video feeds

set -e

echo "--- Preparing to launch Box Counter System ---"

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"
MAIN_APP_PID_FILE="/tmp/box_counter_main.pid"
CAMERA_PID_FILE="/tmp/box_counter_camera.pid"
AI_PID_FILE="/tmp/box_counter_ai.pid"
MONITOR_PID_FILE="/tmp/hailo_monitor.pid"

# Load environment variables with proper quote stripping
if [ -f "$SCRIPT_DIR/.env" ]; then
    echo "[Launcher] Loading environment variables from .env file..."
    while IFS='=' read -r key value; do
        # Skip empty lines and comments
        [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
        # Skip lines without = or with invalid variable names
        [[ "$key" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || continue
        
        # Strip surrounding quotes from value
        value=$(echo "$value" | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/")
        
        # Export the variable
        export "$key"="$value"
        
        # Special handling for Hailo monitor
        if [ "$key" = "HAILO_MONITOR_ENABLED" ] && [ "$value" = "true" ]; then
            export HAILO_MONITOR=1
            echo "[Launcher] Hailo monitoring enabled via environment"
        fi
    done < <(grep -E '^[A-Za-z_][A-Za-z0-9_]*=' "$SCRIPT_DIR/.env")
    echo "[Launcher] Environment variables loaded successfully."
else
    echo "[Launcher] No .env file found at $SCRIPT_DIR/.env"
fi

# Camera configuration - WORKING MJPEG VALUES  
FRAME_WIDTH=${CAMERA_CAMERA_WIDTH:-640}
FRAME_HEIGHT=${CAMERA_CAMERA_HEIGHT:-480}
FRAMERATE=${CAMERA_FRAMERATE:-30}
JPEG_QUALITY=${CAMERA_JPEG_QUALITY:-90}
AWB_MODE=${CAMERA_AWB_MODE:-auto}
AWB_GAINS=${CAMERA_AWB_GAINS:-1.5,1.2}
EXPOSURE_TIME=${CAMERA_EXPOSURE_TIME:-33000}  
ANALOG_GAIN=${CAMERA_ANALOG_GAIN:-1.0}
SATURATION=${CAMERA_SATURATION:-0}
CONTRAST=${CAMERA_CONTRAST:-0}
BRIGHTNESS=${CAMERA_BRIGHTNESS:-0}

echo "[Launcher] DATABASE_URL format check: ${DATABASE_URL:0:50}..."

# Enhanced cleanup function
cleanup() {
    echo "--- Shutting down all services... ---"
    
    # Kill processes if PID files exist
    for pid_file in "$MAIN_APP_PID_FILE" "$CAMERA_PID_FILE" "$AI_PID_FILE" "$MONITOR_PID_FILE"; do
        if [ -f "$pid_file" ]; then
            pid=$(cat "$pid_file")
            if kill -0 "$pid" 2>/dev/null; then
                echo "Stopping process $pid"
                kill "$pid" 2>/dev/null || true
                sleep 2
                kill -9 "$pid" 2>/dev/null || true
            fi
            rm -f "$pid_file"
        fi
    done
    
    # Kill processes by name
    pkill -f "rpicam-vid" || true
    pkill -f "simple_mjpeg_publisher" || true
    pkill -f "hailo_pipeline_service.py" || true
    pkill -f "hailortcli monitor" || true
    
    # Clean up temporary files
    rm -f /tmp/camera_error.log || true
    
    echo "--- Shutdown complete. ---"
}

# Set up signal handlers
trap cleanup EXIT INT TERM

echo "[Launcher] Performing initial cleanup of any old processes..."
cleanup

# Check if Hailo AI should be enabled
if [ "${AI_HAT_ENABLED:-true}" = "true" ]; then
    echo "[Launcher] Hailo AI processing ENABLED."
    HAILO_ENABLED=true
else
    echo "[Launcher] Hailo AI processing DISABLED."
    HAILO_ENABLED=false
fi

# Start Hailo monitor if requested
if [ "${HAILO_MONITOR_ENABLED:-false}" = "true" ] && [ "$HAILO_ENABLED" = true ]; then
    echo "[Launcher] Starting Hailo device monitor..."
    hailortcli monitor > /tmp/hailo_monitor.log 2>&1 &
    MONITOR_PID=$!
    echo $MONITOR_PID > "$MONITOR_PID_FILE"
    echo "[Launcher] Hailo monitor started with PID $MONITOR_PID (log: /tmp/hailo_monitor.log)"
    sleep 2
fi

# Activate virtual environment
if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
    echo "[Launcher] Virtual environment activated."
else
    echo "[Launcher] WARNING: Virtual environment not found at $VENV_PATH"
fi

# Create data directory
mkdir -p "$SCRIPT_DIR/data"

echo "[Launcher] Starting FastAPI server in the background..."

# Start main FastAPI application
cd "$SCRIPT_DIR"
uvicorn main:app --host 0.0.0.0 --port 8000 --env-file .env &
MAIN_PID=$!
echo $MAIN_PID > "$MAIN_APP_PID_FILE"
echo "[Launcher] Main application started with PID $MAIN_PID"

# Wait for main app to start
sleep 5

# Test camera availability first
echo "[Launcher] Testing camera availability..."
if ! rpicam-hello --list-cameras &>/dev/null; then
    echo "[Launcher] ERROR: Camera not detected or accessible"
    echo "[Launcher] Please check camera connection and permissions"
    exit 1
fi
echo "[Launcher] Camera detected successfully"

if [ "$HAILO_ENABLED" = true ]; then
    echo "[Launcher] Starting MJPEG Dual-Stream Pipeline (with AI)..."
    echo "[Launcher] Camera settings: ${FRAME_WIDTH}x${FRAME_HEIGHT} @ ${FRAMERATE}fps"
    echo "[Launcher] MJPEG Quality: ${JPEG_QUALITY}%, Color: AWB=$AWB_MODE"
    echo "[Launcher] Using direct MJPEG codec for maximum compatibility"
    
    # WORKING MJPEG PIPELINE: Camera -> MJPEG -> Python Publisher -> Redis -> FastAPI
    echo "[Launcher] Starting MJPEG camera stream with AI processing..."
    
    # Start camera with MJPEG output piped to both AI and raw publisher
    rpicam-vid \
        --timeout 0 \
        --width $FRAME_WIDTH \
        --height $FRAME_HEIGHT \
        --framerate $FRAMERATE \
        --nopreview \
        --codec mjpeg \
        --quality $JPEG_QUALITY \
        --awb $AWB_MODE \
        --awbgains $AWB_GAINS \
        --shutter $EXPOSURE_TIME \
        --analoggain $ANALOG_GAIN \
        --saturation $SATURATION \
        --contrast $CONTRAST \
        --brightness $BRIGHTNESS \
        --verbose 0 \
        --output - 2>/tmp/camera_error.log | \
    tee >(python3 "$SCRIPT_DIR/services/hailo_pipeline_service.py" 2>/tmp/ai_error.log &) | \
    python3 "$SCRIPT_DIR/services/simple_mjpeg_publisher.py" &
    
    CAMERA_PID=$!
    echo $CAMERA_PID > "$CAMERA_PID_FILE"
    echo "[Launcher] MJPEG dual-stream pipeline started with PID $CAMERA_PID"
    
    echo "[Launcher] Both AI and raw feeds using MJPEG from single camera source"
    
else
    echo "[Launcher] Starting camera-only MJPEG pipeline..."
    
    # Camera-only mode without AI processing
    rpicam-vid \
        --timeout 0 \
        --width $FRAME_WIDTH \
        --height $FRAME_HEIGHT \
        --framerate $FRAMERATE \
        --nopreview \
        --codec mjpeg \
        --quality $JPEG_QUALITY \
        --awb $AWB_MODE \
        --awbgains $AWB_GAINS \
        --shutter $EXPOSURE_TIME \
        --analoggain $ANALOG_GAIN \
        --saturation $SATURATION \
        --contrast $CONTRAST \
        --brightness $BRIGHTNESS \
        --verbose 0 \
        --output - 2>/tmp/camera_error.log | \
    python3 "$SCRIPT_DIR/services/simple_mjpeg_publisher.py" &
    
    CAMERA_PID=$!
    echo $CAMERA_PID > "$CAMERA_PID_FILE"
    echo "[Launcher] Camera-only MJPEG service started with PID $CAMERA_PID"
fi

echo "[Launcher] All services started successfully."
echo "[Launcher] Web interface available at: http://$(hostname -I | awk '{print $1}'):8000"

# Direct streaming endpoints for testing
echo "[Launcher] Direct video streams:"
echo "[Launcher]   Raw Camera: http://$(hostname -I | awk '{print $1}'):8000/api/v1/camera/stream/rpi"
echo "[Launcher]   AI Detection: http://$(hostname -I | awk '{print $1}'):8000/api/v1/camera/ai_stream/rpi"

if [ "${HAILO_MONITOR_ENABLED:-false}" = "true" ]; then
    echo "[Launcher] Hailo monitor running - check /tmp/hailo_monitor.log for device utilization"
    echo "[Launcher] To view monitor output: tail -f /tmp/hailo_monitor.log"
fi

echo "[Launcher] To view camera status: tail -f /tmp/camera_error.log"
if [ "$HAILO_ENABLED" = true ]; then
    echo "[Launcher] To view AI status: tail -f /tmp/ai_error.log"
fi
echo "[Launcher] Press Ctrl+C to stop all services."

# Monitor processes and restart if needed
while true; do
    sleep 10
    
    # Check if main app is still running
    if ! kill -0 $MAIN_PID 2>/dev/null; then
        echo "[Launcher] Main application stopped unexpectedly"
        break
    fi
    
    # Check camera process if enabled
    if [ -f "$CAMERA_PID_FILE" ]; then
        camera_pid=$(cat "$CAMERA_PID_FILE")
        if ! kill -0 $camera_pid 2>/dev/null; then
            echo "[Launcher] Camera process stopped unexpectedly"
            echo "[Launcher] Check /tmp/camera_error.log for details"
        fi
    fi
done

# Wait for main process
wait $MAIN_PID
