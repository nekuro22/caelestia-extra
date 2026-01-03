#!/bin/bash
set -e

# === Arch-Check ===
if ! grep -q '^ID.*=.*arch' /etc/os-release && ! grep -q -i 'manjaro\|cachy\|endeavouros\|garuda\|arco\|reborn' /etc/os-release; then
    echo "❌ Dieses Skript unterstützt nur Arch-basierte Distributionen (Arch, Manjaro, CachyOS, etc.)."
    echo "   Erkanntes System: $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '"')"
    exit 1
fi

echo "✅ Arch-basiertes System erkannt."

# === Caelestia-Abfrage ===
if command -v caelestia &>/dev/null; then
    echo "✨ Caelestia wurde gefunden – Wallpaper-Wechsel wird funktionieren."
    CAELIAVAILABLE="yes"
else
    echo
    echo "❓ Caelestia (z. B. aus Caelestia.dots) wurde NICHT gefunden."
    read -p "Ist Caelestia bereits manuell installiert oder wirst du es später installieren? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "🛑 Ohne Caelestia kann der Hintergrund nicht gewechselt werden."
        echo "   Du kannst das Tool trotzdem installieren, aber die Wallpaper-Funktion bleibt deaktiviert."
        read -p "Trotzdem fortfahren? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Abbruch durch Benutzer."
            exit 0
        fi
    fi
    CAELIAVAILABLE="no"
fi

# === Pfade ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/wallpaper-manager"
DESKTOP_DIR="$HOME/.local/share/applications"

mkdir -p "$BIN_DIR" "$APP_DIR" "$DESKTOP_DIR"

# === Abhängigkeiten prüfen (nur Python/GTK) ===
echo "🔍 Prüfe Python/GTK-Abhängigkeiten..."

missing=()
for pkg in python gtk3 python-gobject; do
    if ! pacman -Q "$pkg" &>/dev/null; then
        missing+=("$pkg")
    fi
done

if [[ ${#missing[@]} -gt 0 ]]; then
    echo "📥 Installiere benötigte Laufzeitumgebung: ${missing[*]}"
    if command -v sudo &>/dev/null; then
        sudo pacman -S --needed --noconfirm "${missing[@]}"
    else
        echo "❌ Kein sudo-Zugriff. Bitte manuell installieren:"
        echo "   pacman -S ${missing[*]}"
        exit 1
    fi
fi

# === Dateien kopieren ===
echo "📦 Installiere Wallpaper Manager..."

cp "$SCRIPT_DIR/src/wallpaper-manager.py" "$APP_DIR/main.py"
chmod +x "$APP_DIR/main.py"

# Wrapper-Skript – optional mit Warnung, falls caelestia fehlt
WRAPPER="$BIN_DIR/wallpaper-manager"
cat > "$WRAPPER" << EOF
#!/bin/bash
exec python3 "$APP_DIR/main.py" "\$@"
EOF
chmod +x "$WRAPPER"

# Desktop-Datei
cp "$SCRIPT_DIR/wallpaper-manager.desktop" "$DESKTOP_DIR/"
chmod +x "$DESKTOP_DIR/wallpaper-manager.desktop"

# === Hinweis zur PATH-Umgebung ===
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo
    echo "⚠️  ~/.local/bin ist nicht im PATH."
    echo "   Füge diese Zeile zu deiner ~/.bashrc oder ~/.zshrc hinzu:"
    echo "   export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo
if [[ "$CAELIAVAILABLE" == "no" ]]; then
    echo "ℹ️  HINWEIS: Caelestia wurde nicht gefunden."
    echo "   Ohne Caelestia wird das Klicken auf Wallpapers keine Wirkung zeigen."
    echo "   Installiere Caelestia manuell (z. B. aus Caelestia.dots), dann funktioniert alles."
fi

echo "✅ Installation abgeschlossen!"
echo "Starte mit: wallpaper-manager"