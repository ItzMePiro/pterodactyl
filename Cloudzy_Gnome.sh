#!/bin/bash
# This script will install xFCE on Ubuntu with RDP support
echo '

Welcome to Cloudzy :)
We are installing Gnome and RDP on your server now..

'
sleep 2
apt update
apt install tasksel -y
echo '
.
.
Installing Gnome Desktop Environment..
.
.'
sleep 2

OS=$(lsb_release -si)

if [[ "$OS" == "Debian"* ]]; then
        tasksel install --new-install gnome-desktop
elif [[ "$OS" == "Ubuntu"* ]]; then
        tasksel install --new-install ubuntu-desktop
else
        echo "OS not Supported!"
        exit 1
fi

echo '
.
.
Installing xRDP package..
.
.'
sleep 2
apt install xrdp -y
echo '
.
.
Rebooting in 5 seconds
.
.'
sleep 5
reboot
