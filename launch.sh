#!/bin/bash

# ==============================================================================
# Robust Launcher for the AI HAT+ Box Counter System
# - Cleans up previous runs
# - Checks for required configuration variables
# - Sets camera exposure for better low-light performance
# - Enables Hailo monitoring for hailo-stats
# - Launches the web app and the Hailo AI pipeline
# - Manages shutdown of all processes on exit
# ==============================================================================

echo "--- Preparing to launch Box Counter System ---"

# Function to clean up background processes on exit
cleanup() {
    echo ""
    echo "--- Shutting down all services... ---"
    # Kill all child processes of this script using the process group ID
    if [ -n "$UVICORN_PID" ]; then kill $UVICORN_PID; fi
    if [ -n "$PIPELINE_PID" ]; then kill $PIPELINE_PID; fi
    echo "--- Shutdown complete. ---"
}

# Trap Ctrl+C (SIGINT) and other exit signals to run the cleanup function
trap cleanup SIGINT SIGTERM EXIT

# --- Initial Cleanup ---
echo "[Launcher] Performing initial cleanup of any old processes..."
pkill -f uvicorn
pkill -f hailo_pipeline_service.py
pkill -f rpicam-vid
sleep 1

# --- Activate Environment and Load Config ---
source venv/bin/activate
if [ -f .env ]; then
    set -o allexport
    source .env
    set +o allexport
else
    echo "FATAL: .env file not found. Please create one from .env.example."
    exit 1
fi

# --- DEFINITIVE FIX: Check for required variables ---
if [ -z "$CAMERA_WIDTH" ] || [ -z "$CAMERA_HEIGHT" ] || [ -z "$CAMERA_FRAMERATE" ]; then
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "FATAL ERROR: One or more camera variables are missing from your .env file."
    echo "Please ensure CAMERA_WIDTH, CAMERA_HEIGHT, and CAMERA_FRAMERATE are set."
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    exit 1
fi

# --- 1. Enable Hailo Monitoring ---
export HAILO_MONITOR=1
echo "[Launcher] Hailo monitoring ENABLED."

# --- 2. Launch the FastAPI Web Application ---
echo "[Launcher] Starting FastAPI server in the background..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
UVICORN_PID=$!
sleep 5

# --- 3. Launch the Camera-to-AI Pipeline ---
echo "[Launcher] Starting Camera-to-AI pipeline..."
EXPOSURE_SETTINGS="--shutter 30000 --gain 10"
echo "[Launcher] Camera settings: ${CAMERA_WIDTH}x${CAMERA_HEIGHT} @ ${CAMERA_FRAMERATE}fps, Gain/Exposure Enabled"

# Run the pipeline and store its PID
( rpicam-vid --camera 0 --width $CAMERA_WIDTH --height $CAMERA_HEIGHT --framerate $CAMERA_FRAMERATE --codec yuv420 -t 0 --inline $EXPOSURE_SETTINGS -o - | python3 services/hailo_pipeline_service.py ) &
PIPELINE_PID=$!

# Wait for either process to exit. The trap will handle cleanup.
wait -n $UVICORN_PID $PIPELINE_PID