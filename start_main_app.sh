#!/bin/bash
# This script is a helper to launch the main FastAPI web server.

# Navigate to the project directory first
cd /home/kobidkunda/applications/rpi_counter_fastapi

# Activate the virtual environment and run the server
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# Keep the terminal open after the script finishes
exec bash