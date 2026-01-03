#!/bin/bash
echo "❗​Achtung Dieses Pogramm Funktioniert nur mit Caelestia Dots"
set -e

USERNAME="${USER}"
BIN_DIR="/home/$USERNAME/.local/bin"
APP_DIR="/home/$USERNAME/.local/share/wallpaper-manager"
KEYBINDS_FILE="/home/$USERNAME/.config/hypr/hyprland/keybinds.conf"

echo "🚀 Wallpaper Manager – Installiere mit EXAKTER Nutzer-Syntax"

# 1. Abhängigkeiten (einmalig nötig)
sudo pacman -S --needed --noconfirm python tk python-pillow

# 2. Wallpaper-Ordner
mkdir -p "$BIN_DIR" "$APP_DIR" "$(dirname "$KEYBINDS_FILE")"
mkdir -p "/home/$USERNAME/Pictures/Wallpapers"

# 3. Python-Skript kopieren
cp "src/wallpaper-manager.py" "$APP_DIR/main.py"
chmod +x "$APP_DIR/main.py"

# 4. Wrapper erstellen (für Terminal)
cat > "$BIN_DIR/wallpaper-manager" << EOF
#!/bin/bash
exec /usr/bin/python3 "$APP_DIR/main.py" "\$@"
EOF
chmod +x "$BIN_DIR/wallpaper-manager"

# 5. Deinstallations-Script
cp "uninstall.sh" "$APP_DIR/"
chmod +x "$APP_DIR/uninstall.sh"

# 6. 🔥 EXAKT DEINE SYNTAX in keybinds.conf einfügen (unverändert)
{
    echo "# Wallpaper Manager – EXAKTE Nutzer-Syntax (kann Fehler verursachen)"
    echo "bind = CTRL SUPER, SPACE, exec, wallpaper-manager"
    echo "bind = SUPER, SPACE, exec, caelestia wallpaper -r"
} >> "$KEYBINDS_FILE"

# 7. PATH für Terminal (einmalig)
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
    if [ -n "$fish" ]; then
        fish_add_path "$BIN_DIR"
    else
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        export PATH="$BIN_DIR:$PATH"
    fi
fi

echo
echo "✅ Installation abgeschlossen."
echo "   Terminal: wallpaper-manager"
echo "   Keybinds: in $KEYBINDS_FILE"
echo "⌨️​Keybinds sind: Strg+Super+Space zum Starten des Wallpaper Managers und Super+Space für einn zufälliges hintergrund Bild.