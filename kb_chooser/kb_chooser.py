#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
from pathlib import Path

# 🔧 Pfad (wie in deinem Setup)
CONFIG_FILE = Path.home() / ".config" / "hypr" / "hyprland" / "input.conf"

# Layout-Optionen
LAYOUTS = {
    "German (DE)": "de",
    "English (UK)": "gb",
    "English (US)": "us",
    "French (FR)": "fr",
    "Spanish (ES)": "es"
}

CONFIG_TEMPLATE = """input {{
    kb_layout = {layout}
    numlock_by_default = {numlock}
    repeat_delay = 250
    repeat_rate = 35

    focus_on_close = 1

    touchpad {{
        natural_scroll = true
        disable_while_typing = true
        scroll_factor = 1.0
    }}
}}

binds {{
    scroll_event_delay = 0
}}

cursor {{
    hotspot_padding = 1
}}
"""

def save_and_close():
    name = layout_combo.get()
    if name not in LAYOUTS:
        status_label.config(text="Error: Please select a valid layout.", fg="#f38ba8")
        return

    layout = LAYOUTS[name]
    numlock = "true" if numlock_var.get() else "false"

    try:
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            f.write(CONFIG_TEMPLATE.format(layout=layout, numlock=numlock))
        status_label.config(
            text="✅ Success! Saved.\nWindow will close in 1 second.",
            fg="#a6e3a1"
        )
        root.after(1000, root.destroy)
    except Exception as e:
        status_label.config(text=f"❌ Error:\n{str(e)}", fg="#f38ba8")

# === Fenster ===
root = tk.Tk()
root.title("Hyprland Keyboard Setup")
root.geometry("420x230")
root.resizable(False, False)

# 🎨 Farbpalette (dunkel, weich, modern)
BG = "#1e1e2e"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
SUCCESS = "#a6e3a1"
ERROR = "#f38ba8"
BUTTON_BG = "#313244"
BUTTON_HOVER = "#45475a"

root.configure(bg=BG)

# Titel
tk.Label(
    root,
    text="Hyprland Keyboard Layout",
    font=("Noto Sans", 13, "bold"),
    bg=BG,
    fg=ACCENT
).pack(pady=(12, 8))

# Layout-Auswahl
tk.Label(root, text="Select your keyboard layout:", bg=BG, fg=FG, font=("Noto Sans", 10)).pack(anchor="w", padx=30)

style = ttk.Style()
style.theme_use("default")
style.configure(
    "TCombobox",
    fieldbackground=BUTTON_BG,
    background=BUTTON_BG,
    foreground=FG,
    selectbackground=BUTTON_HOVER,
    selectforeground=FG,
    arrowcolor=FG,
    borderwidth=0
)
style.map(
    "TCombobox",
    fieldbackground=[("readonly", BUTTON_BG)],
    foreground=[("readonly", FG)]
)

layout_combo = ttk.Combobox(
    root,
    values=list(LAYOUTS.keys()),
    state="readonly",
    width=28,
    font=("Noto Sans", 10)
)
layout_combo.set("English (US)")
layout_combo.pack(pady=4)

# NumLock-Checkbox
numlock_var = tk.BooleanVar(value=False)
check = tk.Checkbutton(
    root,
    text="Enable Num Lock by default",
    variable=numlock_var,
    bg=BG,
    fg=FG,
    selectcolor=BUTTON_BG,
    activebackground=BG,
    activeforeground=FG,
    font=("Noto Sans", 10)
)
check.pack(pady=(10, 0))

# Button
btn = tk.Button(
    root,
    text="Save Configuration",
    command=save_and_close,
    bg=ACCENT,
    fg="#1e1e2e",
    font=("Noto Sans", 10, "bold"),
    relief="flat",
    padx=12,
    pady=6,
    cursor="hand2"
)
btn.pack(pady=12)

# Status
status_label = tk.Label(root, text="", bg=BG, fg=SUCCESS, font=("Noto Sans", 9), justify="center")
status_label.pack()

# Zentrieren
root.update_idletasks()
x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
root.geometry(f"+{x}+{y}")

root.mainloop()