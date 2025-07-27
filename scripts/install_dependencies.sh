#!/bin/bash
# Installs system-level and Python dependencies.

set -e
echo "--- Updating package list and installing system dependencies ---"
apt-get update
# python3-venv is needed to create virtual environments.
# libatlas-base-dev is often needed for numpy performance.
# libcamera-apps provides utilities for testing the camera.
apt-get install -y python3-venv python3-pip libatlas-base-dev libcamera-apps

echo "--- System dependencies installed ---"
