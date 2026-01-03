#!/bin/bash
set -e

# === Nur Arch-basierte Systeme erlauben ===
if ! grep -q '^ID.*=.*arch' /etc/os-release && ! grep -q -i 'manjaro\|cachy\|endeavouros\|garuda\|arco\|reborn\|archcraft' /etc/os-release; then
    echo "❌ Dieses Skript läuft nur auf Arch-basierten Distributionen."
    echo "   Erkannt: $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '"')"
    exit 1
fi

echo "✅ Arch-basiertes System erkannt."

# === Caelestia-Abfrage ===
if command -v caelestia &>/dev/null; then
    echo "✨ Caelestia gefunden – Wallpaper-Wechsel wird funktionieren."
else
    echo
    echo "❓ Caelestia (z. B. aus Caelestia.dots) wurde NICHT gefunden."
    read -p "Ist Caelestia bereits installiert oder wirst du es später manuell installieren? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "⚠️  Ohne Caelestia kann der Hintergrund nicht gewechselt werden."
        read -p "Trotzdem fortfahren? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Abbruch."
            exit 0
        fi
    fi
fi

# === Pfade ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/wallpaper-manager"
DESKTOP_DIR="$HOME/.local/share/applications"

mkdir -p "$BIN_DIR" "$APP_DIR" "$DESKTOP_DIR"

# === Abhängigkeiten installieren ===
echo "📥 Installiere benötigte Pakete..."
# Füge 'tk' zur Liste hinzu
missing=()
for pkg in python tk python-pillow; do
    if ! pacman -Q "$pkg" &>/dev/null; then
        missing+=("$pkg")
    fi
done

# Python ist meist schon da, aber sicherheitshalber
if ! command -v python3 &>/dev/null; then
    echo "Python3 fehlt – wird installiert..."
    sudo pacman -S --needed --noconfirm python
fi

# Pillow für Bildvorschau
if ! python3 -c "import PIL" &>/dev/null; then
    echo "Pillow (python-pillow) fehlt – wird installiert..."
    sudo pacman -S --needed --noconfirm python-pillow
fi

# === Dateien kopieren ===
echo "📦 Installiere Wallpaper Manager..."

# Python-Skript
cp "$SCRIPT_DIR/src/wallpaper-manager.py" "$APP_DIR/main.py"
chmod +x "$APP_DIR/main.py"

# Starter im PATH
cat > "$BIN_DIR/wallpaper-manager" << EOF
#!/bin/bash
exec python3 "$APP_DIR/main.py" "\$@"
EOF
chmod +x "$BIN_DIR/wallpaper-manager"

# Desktop-Datei (für Menü)
cp "$SCRIPT_DIR/wallpaper-manager.desktop" "$DESKTOP_DIR/"
chmod +x "$DESKTOP_DIR/wallpaper-manager.desktop"

# === PATH-Hinweis für fish/bash/zsh ===
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo
    echo "⚠️  ~/.local/bin ist nicht im PATH."
    if [ -n "$fish" ]; then
        echo "   Führe aus: fish_add_path ~/.local/bin"
    else
        echo "   Füge zu ~/.bashrc oder ~/.zshrc hinzu:"
        echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
fi

# === Deinstallations-Script bereitstellen ===
cp "$SCRIPT_DIR/uninstall.sh" "$APP_DIR/"
chmod +x "$APP_DIR/uninstall.sh"
echo
echo "ℹ️  Deinstallieren mit: ~/.local/share/wallpaper-manager/uninstall.sh"

echo
echo "✅ Installation abgeschlossen!"
echo "Starte mit: wallpaper-manager"