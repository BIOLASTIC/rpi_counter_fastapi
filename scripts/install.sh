#!/bin/bash
#
# Main installation script for the Box Counter System on a Raspberry Pi.
# This script should be run with sudo.

set -e # Exit immediately if a command exits with a non-zero status.
echo "--- Starting Box Counter System Installation ---"

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root using sudo."
  exit 1
fi

# Get the directory of the script to find other scripts
SCRIPT_DIR=$(dirname "$(realpath "$0")")
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
INSTALL_USER="pi" # Change if you use a different user
APP_DIR="/opt/box_counter_system"

# --- Step 1: System and Hardware Setup ---
echo "Running Pi 5 specific setup..."
bash "${SCRIPT_DIR}/setup_pi5.sh"

# --- Step 2: Install Dependencies ---
echo "Installing system and Python dependencies..."
bash "${SCRIPT_DIR}/install_dependencies.sh"

# --- Step 3: Application Setup ---
echo "Setting up application directory and virtual environment..."
mkdir -p ${APP_DIR}
cp -r "${PROJECT_ROOT}/" "${APP_DIR}/"
chown -R ${INSTALL_USER}:${INSTALL_USER} ${APP_DIR}

# Create Python virtual environment as the target user
sudo -u ${INSTALL_USER} bash -c "cd ${APP_DIR} && python3 -m venv .venv"
# Install Python packages into the venv
sudo -u ${INSTALL_USER} bash -c "source ${APP_DIR}/.venv/bin/activate && pip install --no-cache-dir -r ${APP_DIR}/requirements.txt"

# --- Step 4: Database Setup ---
echo "Setting up the database..."
bash "${SCRIPT_DIR}/setup_database.sh"

# --- Step 5: Create systemd Service ---
echo "Creating and enabling systemd service..."
bash "${SCRIPT_DIR}/create_service.sh"

echo "--- Installation Complete! ---"
echo "The service has been enabled and will start on boot."
echo "You can start it now with: sudo systemctl start box_counter"
echo "Check its status with: sudo systemctl status box_counter"
echo "View logs with: journalctl -u box_counter -f"
