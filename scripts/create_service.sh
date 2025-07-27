#!/bin/bash
# Creates and enables the systemd service file for the application.

set -e
APP_DIR="/opt/box_counter_system"
SERVICE_NAME="box_counter"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
INSTALL_USER="pi"

echo "Creating systemd service file at ${SERVICE_FILE}..."

# Create the service file content
cat <<EOL > ${SERVICE_FILE}
[Unit]
Description=Box Counter System FastAPI Application
After=network.target
# Add After= for database if it's a separate service, e.g., After=postgresql.service

[Service]
# User and Group that will run the service
User=${INSTALL_USER}
Group=${INSTALL_USER}

# Set the working directory
WorkingDirectory=${APP_DIR}

# Set environment variables for production
# Copy .env.example to .env and customize for production first!
EnvironmentFile=${APP_DIR}/.env

# Command to start the uvicorn server
# Use the absolute path to the uvicorn in the virtual environment
ExecStart=${APP_DIR}/.venv/bin/uvicorn main:app --factory --host 0.0.0.0 --port 8000

# Restart policy
Restart=always
RestartSec=10

# Standard output and error logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=box-counter

[Install]
WantedBy=multi-user.target
EOL

echo "Reloading systemd daemon and enabling service..."
systemctl daemon-reload
systemctl enable ${SERVICE_NAME}.service

echo "--- Systemd service created and enabled ---"
