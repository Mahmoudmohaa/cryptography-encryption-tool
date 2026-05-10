"""
Application entry for the modernized GUI.
"""

from __future__ import annotations

import tkinter as tk

from gui.styles import apply_dark_style
from gui.windows import MainWindow


def run() -> None:
    """Run the desktop application."""
    root = tk.Tk()
    root.title("Cryptography Encryption Tool")
    root.geometry("980x680")
    root.minsize(880, 620)

    apply_dark_style(root)
    MainWindow(root)

    root.mainloop()

