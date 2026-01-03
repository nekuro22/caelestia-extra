#!/bin/bash
set -e

echo "🗑️  Entferne Wallpaper Manager..."

rm -f "$HOME/.local/bin/wallpaper-manager"
rm -rf "$HOME/.local/share/wallpaper-manager"
rm -f "$HOME/.local/share/applications/wallpaper-manager.desktop"

# Desktop-Datenbank aktualisieren (optional)
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$HOME/.local/share/applications" &>/dev/null || true
fi

echo "✅ Alles entfernt."
echo "👋 Tschüss!"