#!/bin/bash
set -e

USERNAME="${USER}"
BIN_DIR="/home/$USERNAME/.local/bin"
APP_DIR="/home/$USERNAME/.local/share/wallpaper-manager"
KEYBINDS_FILE="/home/$USERNAME/.config/hypr/hyprland/keybinds.conf"

echo "🚀 Wallpaper Manager – Installing with EXACT user syntax"

# 1. Install dependencies (one-time setup)
echo "📥 Installing dependencies..."
sudo pacman -S --needed --noconfirm python tk python-pillow

# 2. Ensure directories exist
echo "📁 Creating directories..."
mkdir -p "$BIN_DIR" "$APP_DIR" "$(dirname "$KEYBINDS_FILE")"
mkdir -p "/home/$USERNAME/Pictures/Wallpapers"

# 3. Copy Python script
echo "📦 Copying application files..."
cp "src/wallpaper-manager.py" "$APP_DIR/main.py"
chmod +x "$APP_DIR/main.py"

# 4. Create terminal launcher
cat > "$BIN_DIR/wallpaper-manager" << EOF
#!/bin/bash
exec /usr/bin/python3 "$APP_DIR/main.py" "\$@"
EOF
chmod +x "$BIN_DIR/wallpaper-manager"

# 5. Copy uninstaller
cp "uninstall.sh" "$APP_DIR/"
chmod +x "$APP_DIR/uninstall.sh"

# 6. 🔥 Add EXACT keybinds as requested (verbatim)
{
    echo "# Wallpaper Manager – EXACT user syntax (may cause Hyprland errors)"
    echo "bind = CTRL SUPER, SPACE, exec, wallpaper-manager"
    echo "bind = SUPER, SPACE, exec, caelestia wallpaper -r"
} >> "$KEYBINDS_FILE"

# 7. Add to PATH for terminal use
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
    if [ -n "$fish" ]; then
        fish_add_path "$BIN_DIR"
        echo "✅ Added ~/.local/bin to fish PATH."
    else
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        export PATH="$BIN_DIR:$PATH"
        echo "✅ Added ~/.local/bin to shell PATH."
    fi
fi

echo
echo "⚠️  WARNING: Keybinds use your exact syntax."
echo "   → Hyprland may show 'Invalid dispatcher' errors."
echo "   → For working keys, use: bind = CTRL, SUPER, space, exec, /full/path"
echo
echo "✅ Installation complete!"
echo "   Terminal: wallpaper-manager"
echo "   Keybinds: in $KEYBINDS_FILE (EXACT syntax)"