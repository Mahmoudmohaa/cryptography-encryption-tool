"""
Centralized ttk styling for a modern dark UI (no external deps).
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class Palette:
    bg = "#0f172a"  # slate-900
    panel = "#111c33"
    panel_2 = "#0b1224"
    fg = "#e5e7eb"  # gray-200
    muted = "#9ca3af"  # gray-400
    border = "#243049"
    accent = "#38bdf8"  # sky-400
    accent_2 = "#22c55e"  # green-500
    danger = "#ef4444"  # red-500
    warn = "#f59e0b"  # amber-500


def apply_dark_style(root: tk.Tk) -> ttk.Style:
    """
    Apply a dark theme on top of ttk 'clam' so it works cross-platform.
    Returns the configured ttk.Style instance.
    """
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    root.configure(background=Palette.bg)

    style.configure(
        ".",
        background=Palette.bg,
        foreground=Palette.fg,
        fieldbackground=Palette.panel_2,
        bordercolor=Palette.border,
        lightcolor=Palette.border,
        darkcolor=Palette.border,
        troughcolor=Palette.panel_2,
        focuscolor=Palette.accent,
        font=("Segoe UI", 10),
    )

    style.configure("TFrame", background=Palette.bg)
    style.configure("Card.TFrame", background=Palette.panel, relief="flat")

    style.configure(
        "TLabel",
        background=Palette.bg,
        foreground=Palette.fg,
    )
    style.configure("Muted.TLabel", foreground=Palette.muted)
    style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
    style.configure("H2.TLabel", font=("Segoe UI", 12, "bold"))

    style.configure(
        "TLabelFrame",
        background=Palette.bg,
        foreground=Palette.fg,
        bordercolor=Palette.border,
        padding=10,
    )
    style.configure("TLabelFrame.Label", background=Palette.bg, foreground=Palette.muted, font=("Segoe UI", 9, "bold"))

    style.configure(
        "TButton",
        padding=(12, 8),
        relief="flat",
        background=Palette.panel,
        foreground=Palette.fg,
        bordercolor=Palette.border,
        focusthickness=2,
        focuscolor=Palette.accent,
    )
    style.map(
        "TButton",
        background=[("active", "#162443"), ("pressed", "#0b1328")],
        foreground=[("disabled", "#6b7280")],
    )

    style.configure(
        "Accent.TButton",
        background=Palette.accent,
        foreground="#06101c",
        bordercolor=Palette.accent,
        font=("Segoe UI", 10, "bold"),
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#55d1ff"), ("pressed", "#1fb8f4")],
    )

    style.configure(
        "Danger.TButton",
        background=Palette.danger,
        foreground="#0b0b0b",
        bordercolor=Palette.danger,
        font=("Segoe UI", 10, "bold"),
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#ff6464"), ("pressed", "#d83b3b")],
    )

    style.configure(
        "TCombobox",
        padding=6,
        relief="flat",
    )

    style.configure(
        "TEntry",
        padding=6,
        relief="flat",
        fieldbackground=Palette.panel_2,
    )

    style.configure(
        "TSpinbox",
        padding=6,
        relief="flat",
        fieldbackground=Palette.panel_2,
    )

    style.configure("TNotebook", background=Palette.bg, bordercolor=Palette.border)
    style.configure("TNotebook.Tab", padding=(12, 8), background=Palette.panel_2)
    style.map(
        "TNotebook.Tab",
        background=[("selected", Palette.panel), ("active", "#132042")],
        foreground=[("selected", Palette.fg), ("active", Palette.fg)],
    )

    style.configure(
        "Horizontal.TSeparator",
        background=Palette.border,
    )

    return style

