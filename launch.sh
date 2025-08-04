#!/bin/bash

# ==============================================================================
# Definitive Launcher for the AI HAT+ Box Counter System (Final Version)
# - Specifies the correct BGR888 raw video format from rpicam-vid
# - Creates a robust, fully-specified GStreamer pipeline for the raw feed
# - Launches all services in the correct order
# - Manages shutdown of all processes on exit
# ==============================================================================

echo "--- Preparing to launch Box Counter System ---"

# Function to clean up all child processes on exit
cleanup() {
    echo ""
    echo "--- Shutting down all services... ---"
    # Kill all processes in the script's process group
    pkill -P $$
    # A final, more forceful cleanup
    pkill -f uvicorn
    pkill -f hailo_pipeline_service.py
    pkill -f raw_frame_publisher.py
    pkill -f rpicam-vid
    echo "--- Shutdown complete. ---"
}

trap cleanup SIGINT SIGTERM EXIT

# --- Initial Cleanup ---
echo "[Launcher] Performing initial cleanup of any old processes..."
pkill -f uvicorn
pkill -f hailo_pipeline_service.py
pkill -f raw_frame_publisher.py
pkill -f rpicam-vid
sleep 1

# --- Activate Environment and Load Config ---
source venv/bin/activate
set -o allexport
source .env
set +o allexport

# --- 1. Enable Hailo Monitoring ---
export HAILO_MONITOR=1
echo "[Launcher] Hailo monitoring ENABLED."

# --- 2. Launch the FastAPI Web Application ---
echo "[Launcher] Starting FastAPI server in the background..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
sleep 5

# --- 3. Launch the new Dual-Stream Camera-to-AI Pipeline ---
echo "[Launcher] Starting Dual-Stream Camera-to-AI pipeline..."
EXPOSURE_SETTINGS="--shutter 30000 --gain 10"

FIFO_PIPE=/tmp/raw_pipe
rm -f $FIFO_PIPE
mkfifo $FIFO_PIPE

# Launch the Raw Feed Publisher in the background. It reads raw BGR888 frames
# from the named pipe and encodes them to JPEG before publishing.
echo "[Launcher] Raw Feed Publisher starting..."
python3 services/raw_frame_publisher.py < $FIFO_PIPE &

echo "[Launcher] AI Feed Pipeline starting..."

# --- DEFINITIVE FIX ---
# 1. Use '--format BGR888' to output raw, uncompressed frames that Python/OpenCV can directly use.
# 2. This single stream is then duplicated by 'tee'.
rpicam-vid --camera 0 --width $CAMERA_WIDTH --height $CAMERA_HEIGHT --framerate $CAMERA_FRAMERATE --format BGR888 -t 0 --inline $EXPOSURE_SETTINGS -o - \
    | tee $FIFO_PIPE \
    | python3 services/hailo_pipeline_service.py