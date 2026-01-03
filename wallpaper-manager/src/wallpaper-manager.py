#!/usr/bin/env python3
import os
import gi
import subprocess
from pathlib import Path

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

# Nutze aktuellen Benutzernamen (robuster als hartes "niklas")
USERNAME = os.getenv("USER") or os.path.basename(os.path.expanduser("~"))
WALLPAPER_DIR = Path.home() / "Pictures" / "Wallpapers"

class WallpaperManager:
    def __init__(self):
        self.build_ui()

    def build_ui(self):
        self.window = Gtk.Window(title="Wallpaper Manager")
        self.window.set_default_size(900, 650)
        self.window.set_border_width(12)
        self.window.connect("destroy", Gtk.main_quit)

        # Scrollbar
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_shadow_type(Gtk.ShadowType.IN)

        # FlowBox für Bilder
        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_max_children_per_line(6)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        flowbox.set_row_spacing(10)
        flowbox.set_column_spacing(10)

        if WALLPAPER_DIR.exists():
            valid_extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
            for img_path in sorted(WALLPAPER_DIR.rglob("*")):
                if img_path.suffix.lower() in valid_extensions:
                    try:
                        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                            str(img_path), 220, 160, True
                        )
                        image = Gtk.Image.new_from_pixbuf(pixbuf)
                        button = Gtk.Button()
                        button.set_image(image)
                        button.set_always_show_image(True)
                        button.set_relief(Gtk.ReliefStyle.NONE)
                        button.connect("clicked", self.set_wallpaper, str(img_path))
                        flowbox.add(button)
                    except Exception:
                        continue

        scrolled.add(flowbox)
        self.window.add(scrolled)

    def set_wallpaper(self, button, filepath):
        try:
            subprocess.run(["caelestia", "wallpaper", "-f", filepath], check=True)
        except subprocess.CalledProcessError:
            dialog = Gtk.MessageDialog(
                transient_for=self.window,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Fehler beim Setzen des Hintergrunds",
                secondary_text=f"Konnte '{filepath}' nicht mit 'caelestia' setzen."
            )
            dialog.run()
            dialog.destroy()

    def run(self):
        self.window.show_all()
        Gtk.main()

if __name__ == "__main__":
    app = WallpaperManager()
    app.run()