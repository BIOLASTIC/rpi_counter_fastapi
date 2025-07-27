#!/bin/bash
#
# Configures Raspberry Pi 5 specific settings for the application.
# This script assumes a recent version of Raspberry Pi OS (Bookworm).

set -e
echo "--- Configuring Raspberry Pi 5 Hardware Interfaces ---"

# Enable Camera Interface (libcamera)
echo "Enabling camera interface..."
raspi-config nonint do_camera 0

# Add user to the gpio, i2c, and video groups to access hardware without root
INSTALL_USER="pi"
echo "Adding user '${INSTALL_USER}' to hardware groups..."
usermod -a -G gpio,i2c,video ${INSTALL_USER}

# Setup udev rule for the USB-RS485 converter
# This ensures it gets consistent permissions when plugged in.
echo "Setting up udev rule for USB-RS485 converter..."
cat <<EOL > /etc/udev/rules.d/99-usb-serial.rules
# Rule for Waveshare USB to RS485 converter and other common chips
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", GROUP="dialout", MODE="0666"
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", GROUP="dialout", MODE="0666"
EOL
udevadm control --reload-rules && udevadm trigger

echo "--- Pi 5 Setup Complete ---"
echo "A reboot is recommended to apply all changes, especially group memberships."
