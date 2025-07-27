#!/bin/bash
# Sets up the database directory and permissions.

set -e
APP_DIR="/opt/box_counter_system"
DATA_DIR="${APP_DIR}/data"
INSTALL_USER="pi"

echo "Creating data directory at ${DATA_DIR}..."
mkdir -p "${DATA_DIR}"
# The database file itself will be created by the application on first run.
# We just need to ensure the directory exists and has the correct owner.
chown -R ${INSTALL_USER}:${INSTALL_USER} "${DATA_DIR}"
chmod 755 "${DATA_DIR}"

echo "--- Database setup complete ---"
