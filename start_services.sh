#!/bin/bash

# Script to start all RPI Counter FastAPI services in separate terminals
# Each service runs in its own terminal window and stays open

BASE_DIR="/home/kobidkunda/applications/rpi_counter_fastapi"

# Function to create a command that activates venv and runs the service
create_command() {
    local service_command="$1"
    local title="$2"
    echo "cd '$BASE_DIR' && source venv/bin/activate && $service_command; exec bash"
}

# Start FastAPI server
gnome-terminal --title="FastAPI Server" -- bash -c "$(create_command 'uvicorn main:app --host 0.0.0.0 --port 8000 --env-file .env --reload' 'FastAPI Server')" &

# Start AI Processor
gnome-terminal --title="AI Processor" -- bash -c "$(create_command 'python services/ai_processor.py' 'AI Processor')" &

# Start RPI Camera Service
gnome-terminal --title="RPI Camera Service" -- bash -c "$(create_command 'python services/camera_service_rpi.py' 'RPI Camera Service')" &

# Start USB Camera Service
gnome-terminal --title="USB Camera Service" -- bash -c "$(create_command 'python services/camera_service_usb.py' 'USB Camera Service')" &

echo "All services started in separate terminals!"
echo "Each terminal will remain open even after Ctrl+C"
echo "To stop all services, close the terminal windows individually"
