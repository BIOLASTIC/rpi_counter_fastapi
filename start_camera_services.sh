#!/bin/bash
# This script is a helper launched by the desktop shortcut.
# It starts both camera services in their own terminal windows.

PROJECT_DIR="/home/kobidkunda/applications/rpi_counter_fastapi"

# Command to run the RPi camera service
CMD_RPI_CAM="source venv/bin/activate && python services/camera_service_rpi.py; exec bash"

# Command to run the USB camera service
CMD_USB_CAM="source venv/bin/activate && python services/camera_service_usb.py; exec bash"

echo "-> Launching RPi Camera Service..."
gnome-terminal --title="RPi Camera" --working-directory="$PROJECT_DIR" -- /bin/bash -c "$CMD_RPI_CAM" &

echo "-> Launching USB Camera Service..."
gnome-terminal --title="USB Camera" --working-directory="$PROJECT_DIR" -- /bin/bash -c "$CMD_USB_CAM" &
