#!/bin/bash
set -e

USERNAME="${USER}"
BIN_DIR="/home/$USERNAME/.local/bin"
APP_DIR="/home/$USERNAME/.local/share/wallpaper-manager"
KEYBINDS_FILE="/home/$USERNAME/.config/hypr/hyprland/keybinds.conf"

echo "🗑️  Removing Wallpaper Manager..."

# Remove files
rm -f "$BIN_DIR/wallpaper-manager"
rm -rf "$APP_DIR"

# Remove exact keybind lines
if [ -f "$KEYBINDS_FILE" ]; then
    sed -i '/CTRL SUPER, SPACE, exec, wallpaper-manager/d' "$KEYBINDS_FILE"
    sed -i '/SUPER, SPACE, exec, caelestia wallpaper -r/d' "$KEYBINDS_FILE"
    sed -i '/# Wallpaper Manager – EXACT user syntax/d' "$KEYBINDS_FILE"
    echo "✅ Removed your exact syntax from keybinds.conf."
fi

echo "✅ Cleanup complete. Goodbye!"