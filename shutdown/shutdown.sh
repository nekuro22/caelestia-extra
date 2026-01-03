#!/bin/bash
# Dieses Skript gibt "Press Enter to Shutdown" aus und fährt das System herunter, wenn Enter gedrückt wird.

echo "Press Enter to Shutdown"
read -r # Warten auf Benutzereingabe
sudo shutdown now
