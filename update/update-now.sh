#!/bin/bash
# Beispiel Update-Skript

echo "Starting system update..."

# Update mit Pacman
if command_exists pacman; then
  echo "Updating with pacman..."
  sudo pacman -Syu --noconfirm
else
  echo "pacman ist nicht installiert."
fi

# Update mit Yay (falls yay installiert ist)
if command_exists yay; then
  echo "Updating with yay..."
  yay -Syu --noconfirm
else
  echo "yay ist nicht installiert."
fi

# Update mit Pikaur (falls installiert)
if command_exists pikaur; then
  echo "Updating with pikaur..."
  pikaur -Syu --noconfirm
else
  echo "pikaur ist nicht installiert."
fi

# Optional: Update mit paru (falls installiert)
if command_exists paru; then
  echo "Updating with paru..."
  paru -Syu --noconfirm
else
  echo "paru ist nicht installiert."
fi

echo "System update abgeschlossen."
y