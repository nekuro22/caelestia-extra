#!/usr/bin/env python3
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
from PIL import Image, ImageTk

# Deaktiviere Bombenschutz – nur für eigene Bilder sicher
from PIL import Image as PILImage
PILImage.MAX_IMAGE_PIXELS = None

WALLPAPER_DIR = Path.home() / "Pictures" / "Wallpapers"
SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

class WallpaperManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Wallpaper Manager")
        self.root.geometry("760x600")
        self.root.minsize(500, 400)

        # Modernes Theme, wenn verfügbar
        try:
            self.root.tk.call("source", "/usr/share/tk8.6/ttk/fonts.tcl")
            self.root.tk.call("set", "tk::classic::photo", "false")
        except:
            pass

        style = ttk.Style()
        try:
            style.theme_use('clam')  # moderner als 'default'
        except:
            pass
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))

        # Header
        header = ttk.Label(root, text="🖼️ Wallpaper Manager", font=("Segoe UI", 14, "bold"))
        header.pack(pady=(12, 6))

        hint = ttk.Label(root, text="Klicke auf ein Bild, um es mit Caelestia zu setzen", foreground="#555")
        hint.pack(pady=(0, 12))

        # Listbox mit Scrollbar
        frame = ttk.Frame(root)
        frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.listbox = tk.Listbox(
            frame,
            font=("Monospace", 10),
            activestyle="none",
            selectbackground="#4a86e8",
            selectforeground="white",
            highlightthickness=0,
            bd=1,
            relief="solid"
        )
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.listbox.bind("<Double-1>", self.on_double_click)
        self.listbox.bind("<Return>", self.on_double_click)

        self.load_filenames()

    def load_filenames(self):
        if not WALLPAPER_DIR.exists():
            self.listbox.insert("end", f"[FEHLER] Ordner nicht gefunden: {WALLPAPER_DIR}")
            self.listbox.itemconfig(0, {"fg": "red"})
            return

        image_files = sorted([
            f for f in WALLPAPER_DIR.rglob("*")
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS
        ])

        if not image_files:
            self.listbox.insert("end", "[INFO] Keine Bilder in ~/Pictures/Wallpapers/")
            self.listbox.itemconfig(0, {"fg": "gray"})
            return

        for img in image_files:
            self.listbox.insert("end", img.name)
            # Optional: Icon hinzufügen – aber das verlangsamt
        self.root.after(100, lambda: self.listbox.focus_set())

    def on_double_click(self, event=None):
        selection = self.listbox.curselection()
        if not selection:
            return
        filename = self.listbox.get(selection[0])
        if filename.startswith("["):
            return  # Info-Zeile

        filepath = WALLPAPER_DIR / filename
        if not filepath.exists():
            messagebox.showerror("Fehler", "Datei nicht gefunden!")
            return

        try:
            subprocess.run(["caelestia", "wallpaper", "-f", str(filepath)], check=True)
            self.root.after(100, self.root.destroy)  # Optional: Schließen nach Setzen
        except FileNotFoundError:
            messagebox.showerror("Fehlt", "Caelestia nicht gefunden!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Fehler", f"Konnte Wallpaper nicht setzen:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*tearOff", False)  # Keine Menü-Trennleisten
    app = WallpaperManager(root)
    root.mainloop()