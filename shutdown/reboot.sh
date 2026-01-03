#!/bin/bash
# Dieses Skript gibt "Press Enter to Reboot" aus und startet das System neu, wenn Enter gedrückt wird.

echo "Press Enter to Reboot"
read -r # Warten auf Benutzereingabe
sudo reboot
