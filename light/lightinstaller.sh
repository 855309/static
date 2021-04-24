#!/usr/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "light installation script must be run as root."
    exit
fi

function removedir() {
    echo ":: Removing existing installation..."
    sudo rm -rf "/usr/share/light"
}

function removesymlink() {
    echo ":: Removing existing symlink..."
    sudo rm -rf "/usr/bin/light"
}

[ -d "/usr/share/light" ] && removedir

[ -L "/usr/bin/light" ] && removesymlink

[ -f "/tmp/light.zip" ] && sudo rm -rf "/tmp/light.zip"

echo ":: Fetching light..."

wget "https://raw.githubusercontent.com/fikret0/static/main/light/light.zip" -O "/tmp/light.zip"

echo ":: Extracting light..."

sudo unzip "/tmp/light.zip" -d "/usr/share/light"

echo ":: Creating symlinks..."

chmod +x "/usr/share/light/light.py"
sudo ln -s "/usr/share/light/light.py" "/usr/bin/light"

echo ":: Cleaning up..."

sudo rm -rf "/tmp/light.zip"

echo ":: Successfully installed light."