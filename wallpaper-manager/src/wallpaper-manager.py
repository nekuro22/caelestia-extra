#!/usr/bin/env python3
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
from PIL import Image, ImageTk

from PIL import Image as PILImage
PILImage.MAX_IMAGE_PIXELS = None

WALLPAPER_DIR = Path.home() / "Pictures" / "Wallpapers"
CONFIG_DIR = Path.home() / ".config" / "wallpaper-manager"
FAVORITES_FILE = CONFIG_DIR / "favorites.txt"
SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

CONFIG_DIR.mkdir(parents=True, exist_ok=True)

SIZES = {
    "small":  (600, 480),
    "medium": (800, 620),
    "large":  (1080, 740)
}

class WallpaperManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Wallpaper Manager")
        self.root.geometry(f"{SIZES['medium'][0]}x{SIZES['medium'][1]}")
        self.root.minsize(550, 420)

        self.is_dark_mode = self.detect_dark_mode()
        self.apply_theme()

        # Header
        header = ttk.Label(root, text="🖼️ Wallpaper Manager", font=("Sans", 14, "bold"))
        header.pack(pady=(12, 6))

        hint = ttk.Label(
            root,
            text="Click = Select | Space = Add to Favorites | Backspace = Remove | Double-click = Set",
            foreground="#aaa" if self.is_dark_mode else "#555"
        )
        hint.pack(pady=(0, 10))

        # Add current wallpaper button
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=(0, 8))
        self.add_current_btn = ttk.Button(
            btn_frame,
            text="➕ Add Current Wallpaper to Favorites",
            command=self.add_current_to_favorites
        )
        self.add_current_btn.pack()

        # Main area
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # List
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(side="left", fill="y", padx=(0, 12))

        self.listbox = tk.Listbox(
            list_frame,
            width=34,
            font=("Monospace", 10),
            activestyle="none",
            selectbackground=self.fg_color,
            selectforeground=self.bg_color,
            highlightthickness=0,
            bd=1,
            relief="solid",
            bg=self.entry_bg,
            fg=self.text_fg
        )
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")

        self.listbox.bind("<Button-1>", self.on_click_select)
        self.listbox.bind("<Double-1>", self.on_double_click)
        self.listbox.bind("<Return>", self.on_double_click)
        self.listbox.bind("<space>", self.add_to_favorites)        # Space = immer hinzufügen
        self.listbox.bind("<BackSpace>", self.remove_from_favorites)  # Backspace = entfernen
        self.listbox.bind("<KeyRelease>", self.on_key_release)

        # Preview
        preview_frame = tk.Frame(main_frame, bg=self.bg_color)
        preview_frame.pack(side="right", fill="both", expand=True)

        self.preview_label = tk.Label(
            preview_frame,
            text="No image selected",
            anchor="center",
            bg=self.bg_color,
            fg=self.text_fg,
            font=("Sans", 12)
        )
        self.preview_label.pack(expand=True, padx=15, pady=15)

        self.root.bind("<t>", self.cycle_size)
        self.root.bind("<T>", self.cycle_size)

        self.current_image_ref = None
        self.selected_path = None
        self.favorite_paths = self.load_favorites()
        self.load_filenames()
        self.current_size = "medium"

    def cycle_size(self, event=None):
        order = ["small", "medium", "large"]
        idx = (order.index(self.current_size) + 1) % len(order)
        self.current_size = order[idx]
        w, h = SIZES[self.current_size]
        self.root.geometry(f"{w}x{h}")
        if self.selected_path:
            self.show_preview()

    def detect_dark_mode(self):
        if "dark" in os.getenv("GTK_THEME", "").lower():
            return True
        try:
            out = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
                capture_output=True, text=True
            )
            return "dark" in out.stdout.lower()
        except:
            return False

    def apply_theme(self):
        if self.is_dark_mode:
            self.bg_color = "#1e1e1e"
            self.fg_color = "#3a7ca5"
            self.text_fg = "#e0e0e0"
            self.entry_bg = "#2d2d2d"
        else:
            self.bg_color = "#ffffff"
            self.fg_color = "#4a86e8"
            self.text_fg = "#202020"
            self.entry_bg = "#f8f8f8"

        self.root.configure(bg=self.bg_color)
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass
        style.configure("TLabel", foreground=self.text_fg, background=self.bg_color)
        style.configure("TFrame", background=self.bg_color)
        style.configure("TButton", foreground=self.text_fg, background=self.entry_bg)

    def load_favorites(self):
        if FAVORITES_FILE.exists():
            with open(FAVORITES_FILE, "r") as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    def save_favorites(self):
        with open(FAVORITES_FILE, "w") as f:
            for path in sorted(self.favorite_paths):
                f.write(path + "\n")

    def load_filenames(self):
        all_files = []
        if WALLPAPER_DIR.exists():
            all_files = sorted([
                f for f in WALLPAPER_DIR.rglob("*")
                if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS
            ])

        fav_files = [f for f in all_files if str(f) in self.favorite_paths]
        other_files = [f for f in all_files if str(f) not in self.favorite_paths]

        self.listbox.delete(0, "end")

        if fav_files:
            self.listbox.insert("end", "🌟 FAVORITES")
            self.listbox.itemconfig(self.listbox.size() - 1, {"fg": "#FFD700" if self.is_dark_mode else "#D4AF37"})
            for f in fav_files:
                self.listbox.insert("end", f"⭐ {f.name}")
            self.listbox.insert("end", "")

        self.listbox.insert("end", "📚 ALL WALLPAPERS")
        self.listbox.itemconfig(self.listbox.size() - 1, {"fg": "#888" if self.is_dark_mode else "#666"})
        for f in other_files:
            self.listbox.insert("end", f.name)

        self.root.after(100, lambda: self.listbox.focus_set())

    def get_real_path_from_index(self, index):
        lines = self.listbox.get(0, "end")
        if index >= len(lines):
            return None
        line = lines[index]
        if line in ("", "🌟 FAVORITES", "📚 ALL WALLPAPERS"):
            return None
        filename = line.replace("⭐ ", "")
        for path in self.favorite_paths:
            if Path(path).name == filename:
                return Path(path)
        return WALLPAPER_DIR / filename

    def on_click_select(self, event=None):
        self.root.after(50, self.select_and_preview)

    def select_and_preview(self):
        index = self.listbox.nearest(self.listbox.winfo_pointery() - self.listbox.winfo_rooty())
        if index < 0 or index >= self.listbox.size():
            return
        line = self.listbox.get(index)
        if line in ("", "🌟 FAVORITES", "📚 ALL WALLPAPERS"):
            return
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(index)
        self.selected_path = self.get_real_path_from_index(index)
        self.show_preview()

    def on_key_release(self, event=None):
        sel = self.listbox.curselection()
        if sel:
            self.selected_path = self.get_real_path_from_index(sel[0])
            self.show_preview()

    def show_preview(self):
        if not self.selected_path or not self.selected_path.exists():
            self.preview_label.config(image="", text="File not found", bg=self.bg_color, fg=self.text_fg)
            self.current_image_ref = None
            return

        try:
            available_width = self.preview_label.winfo_width()
            available_height = self.preview_label.winfo_height()

            if available_width < 100 or available_height < 100:
                win_w = self.root.winfo_width()
                win_h = self.root.winfo_height()
                available_width = max(300, win_w - 350)
                available_height = max(250, win_h - 150)

            img = Image.open(self.selected_path)
            img_ratio = img.width / img.height
            frame_ratio = available_width / available_height

            if frame_ratio > img_ratio:
                new_height = available_height
                new_width = int(available_height * img_ratio)
            else:
                new_width = available_width
                new_height = int(available_width / img_ratio)

            new_width = min(new_width, img.width)
            new_height = min(new_height, img.height)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            self.preview_label.config(image=photo, text="", bg=self.bg_color)
            self.preview_label.image = photo
            self.current_image_ref = photo
        except Exception as e:
            self.preview_label.config(image="", text=f"Error:\n{str(e)[:50]}", bg=self.bg_color, fg=self.text_fg)
            self.current_image_ref = None

    def add_to_favorites(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return "break"
        path = self.get_real_path_from_index(sel[0])
        if not path or not path.exists():
            return "break"

        path_str = str(path)
        if path_str not in self.favorite_paths:
            self.favorite_paths.add(path_str)
            self.save_favorites()
            self.load_filenames()
            self.root.after(100, lambda: self.reselect_after_reload(path_str))
        return "break"

    def remove_from_favorites(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return "break"
        path = self.get_real_path_from_index(sel[0])
        if not path or not path.exists():
            return "break"

        path_str = str(path)
        if path_str in self.favorite_paths:
            self.favorite_paths.discard(path_str)
            self.save_favorites()
            self.load_filenames()
            self.root.after(100, lambda: self.reselect_after_reload(path_str))
        return "break"

    def reselect_after_reload(self, target_path):
        lines = self.listbox.get(0, "end")
        for i, line in enumerate(lines):
            clean_name = line.replace("⭐ ", "")
            if line in ("", "🌟 FAVORITES", "📚 ALL WALLPAPERS"):
                continue
            for p in self.favorite_paths:
                if Path(p).name == clean_name:
                    self.listbox.selection_set(i)
                    self.selected_path = Path(p)
                    self.show_preview()
                    return
            if (WALLPAPER_DIR / clean_name).exists() and str(WALLPAPER_DIR / clean_name) == target_path:
                self.listbox.selection_set(i)
                self.selected_path = WALLPAPER_DIR / clean_name
                self.show_preview()
                return

    def on_double_click(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        path = self.get_real_path_from_index(sel[0])
        if not path or not path.exists():
            messagebox.showerror("Error", "File not found!")
            return

        try:
            subprocess.run(["caelestia", "wallpaper", "-f", str(path)], check=True)
            self.root.after(100, self.root.destroy)
        except FileNotFoundError:
            messagebox.showerror("Error", "Caelestia not found!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to set wallpaper:\n{e}")

    def add_current_to_favorites(self):
        try:
            result = subprocess.run(["caelestia", "wallpaper"], capture_output=True, text=True, check=True)
            current_path = result.stdout.strip()
            if not current_path:
                messagebox.showinfo("Info", "No current wallpaper detected.")
                return

            wallpaper_path = Path(current_path)
            if not wallpaper_path.exists():
                messagebox.showerror("Error", f"Current wallpaper file does not exist:\n{current_path}")
                return

            # Add to favorites
            path_str = str(wallpaper_path)
            if path_str in self.favorite_paths:
                messagebox.showinfo("Info", "Already in favorites!")
            else:
                self.favorite_paths.add(path_str)
                self.save_favorites()
                self.load_filenames()
                messagebox.showinfo("Success", "Added current wallpaper to favorites!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to get current wallpaper from Caelestia.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Caelestia not found!")

if __name__ == "__main__":
    root = tk.Tk()
    root.option_add("*tearOff", False)
    app = WallpaperManager(root)
    root.mainloop()