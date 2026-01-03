#!/bin/bash
set -e

echo "🗑️  Entferne Wallpaper Manager..."

# Pfade
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/wallpaper-manager"
DESKTOP_FILE="$HOME/.local/share/applications/wallpaper-manager.desktop"

# Dateien löschen
rm -f "$BIN_DIR/wallpaper-manager"
rm -rf "$APP_DIR"
rm -f "$DESKTOP_FILE"

echo "✅ Wallpaper Manager wurde deinstalliert."

# Optional: Desktop-Cache aktualisieren (damit das Menü-Eintrag verschwindet)
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$HOME/.local/share/applications" &>/dev/null || true
fi

# Optional: Selbst löschen – aber nicht während der Ausführung!
# Wir kopieren uns kurz und führen die Kopie aus, dann löschen wir Original + Kopie.
if [[ -f "$0" ]]; then
    echo "🧹 Entferne Uninstall-Skript..."
    SCRIPT_PATH="$0"
    # In den meisten Fällen ist dies ein lokaler Pfad – also sicher löschen nach Ausführung
    # Aber: nicht während der Ausführung löschen → erst nach exit
    (
        sleep 0.2
        rm -f "$SCRIPT_PATH"
    ) &
fi

echo "👋 Alles aufgeräumt. Tschüss!"