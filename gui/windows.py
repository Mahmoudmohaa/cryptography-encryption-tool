"""
Main GUI window and widgets.

This refactor preserves all existing cipher behaviors and adds:
- Dropdown algorithm selection
- Tabs for Encrypt / Decrypt
- Status bar messages
- Copy-to-clipboard + Clear
- Optional chaining and basic history
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from algorithms import caesar, monoalphabetic, playfair, rowcolumn, vigenere, zigzag
from gui.styles import Palette
from utils.helpers import StatusMessage, normalize_key_26_upper, safe_int


ALGORITHMS: list[tuple[str, str]] = [
    ("caesar", "Caesar Cipher"),
    ("vigenere", "Vigenere Cipher"),
    ("mono", "Mono Alphabetical Cipher"),
    ("playfair", "Playfair Cipher"),
    ("zigzag", "Zigzag (Rail Fence) Cipher"),
    ("rowcolumn", "Row Column Cipher"),
]


class MainWindow(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master, padding=18, style="TFrame")
        self.master = master

        self.mode = tk.StringVar(value="encrypt")  # kept for parity
        self.algorithm = tk.StringVar(value="caesar")
        self.status_var = tk.StringVar(value="Ready.")

        self._chain_enabled = tk.BooleanVar(value=False)
        self._last_result: str = ""
        self._history: list[tuple[str, str, str]] = []  # (mode, algorithm, result)

        self._build_layout()
        self._on_algorithm_change()

    def _build_layout(self) -> None:
        self.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(self)
        header.pack(fill=tk.X)

        ttk.Label(header, text="Cryptography Encryption Tool", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            header,
            text="Encrypt / decrypt text using classic ciphers. Chaining supported.",
            style="Muted.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        ttk.Separator(self, orient="horizontal").pack(fill=tk.X, pady=14)

        top = ttk.Frame(self)
        top.pack(fill=tk.X)

        algo_box = ttk.Frame(top)
        algo_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Label(algo_box, text="Algorithm", style="H2.TLabel").pack(anchor=tk.W)
        self.algorithm_combo = ttk.Combobox(
            algo_box,
            values=[name for _, name in ALGORITHMS],
            state="readonly",
        )
        self.algorithm_combo.current(0)
        self.algorithm_combo.pack(fill=tk.X, pady=(6, 0))
        self.algorithm_combo.bind("<<ComboboxSelected>>", lambda _e: self._sync_algorithm_from_combo())

        options = ttk.Frame(top)
        options.pack(side=tk.RIGHT, padx=(16, 0))

        ttk.Label(options, text="Options", style="H2.TLabel").pack(anchor=tk.W)
        ttk.Checkbutton(
            options,
            text="Chain next run",
            variable=self._chain_enabled,
        ).pack(anchor=tk.W, pady=(6, 0))

        body = ttk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True, pady=(14, 0))

        self.notebook = ttk.Notebook(body)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.encrypt_tab = ttk.Frame(self.notebook, padding=12, style="Card.TFrame")
        self.decrypt_tab = ttk.Frame(self.notebook, padding=12, style="Card.TFrame")
        self.notebook.add(self.encrypt_tab, text="Encrypt")
        self.notebook.add(self.decrypt_tab, text="Decrypt")

        self._build_tab(self.encrypt_tab, mode="encrypt")
        self._build_tab(self.decrypt_tab, mode="decrypt")

        footer = ttk.Frame(self)
        footer.pack(fill=tk.X, pady=(12, 0))

        self.status_label = ttk.Label(footer, textvariable=self.status_var, style="Muted.TLabel")
        self.status_label.pack(side=tk.LEFT, anchor=tk.W)

        ttk.Label(footer, text="v2 (refactor)", style="Muted.TLabel").pack(side=tk.RIGHT)

    def _build_tab(self, parent: ttk.Frame, mode: str) -> None:
        grid = ttk.Frame(parent)
        grid.pack(fill=tk.BOTH, expand=True)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)
        grid.rowconfigure(1, weight=1)

        ttk.Label(grid, text="Key", style="H2.TLabel").grid(row=0, column=0, sticky="w")
        self._key_area = ttk.Frame(grid)
        self._key_area.grid(row=0, column=0, sticky="ew", pady=(28, 0))

        # We create per-tab key widgets so switching tabs doesn't lose state.
        key_container = ttk.Frame(grid)
        key_container.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(6, 12))
        key_container.columnconfigure(1, weight=1)

        ttk.Label(key_container, text="Key / Shift / Rails").grid(row=0, column=0, sticky="w", padx=(0, 10))
        key_widget = ttk.Entry(key_container)
        key_widget.grid(row=0, column=1, sticky="ew")

        # Store on parent for later lookup
        setattr(self, f"{mode}_key_widget", key_widget)

        ttk.Label(grid, text="Input", style="H2.TLabel").grid(row=1, column=0, sticky="w")
        ttk.Label(grid, text="Output", style="H2.TLabel").grid(row=1, column=1, sticky="w")

        input_frame = ttk.Frame(grid)
        input_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 8))
        output_frame = ttk.Frame(grid)
        output_frame.grid(row=2, column=1, sticky="nsew", padx=(8, 0))

        input_frame.rowconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)

        input_text = tk.Text(
            input_frame,
            height=10,
            bg=Palette.panel_2,
            fg=Palette.fg,
            insertbackground=Palette.fg,
            relief="flat",
            wrap="word",
            font=("Segoe UI", 10),
        )
        input_text.grid(row=0, column=0, sticky="nsew")
        in_scroll = ttk.Scrollbar(input_frame, orient="vertical", command=input_text.yview)
        in_scroll.grid(row=0, column=1, sticky="ns")
        input_text.configure(yscrollcommand=in_scroll.set)

        output_text = tk.Text(
            output_frame,
            height=10,
            bg=Palette.panel_2,
            fg=Palette.fg,
            insertbackground=Palette.fg,
            relief="flat",
            wrap="word",
            font=("Segoe UI", 10),
        )
        output_text.grid(row=0, column=0, sticky="nsew")
        out_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=output_text.yview)
        out_scroll.grid(row=0, column=1, sticky="ns")
        output_text.configure(yscrollcommand=out_scroll.set)
        output_text.configure(state="disabled")

        setattr(self, f"{mode}_input_text", input_text)
        setattr(self, f"{mode}_output_text", output_text)

        buttons = ttk.Frame(parent)
        buttons.pack(fill=tk.X, pady=(12, 0))

        run_btn = ttk.Button(
            buttons,
            text="Encrypt" if mode == "encrypt" else "Decrypt",
            style="Accent.TButton",
            command=lambda m=mode: self._run(m),
        )
        run_btn.pack(side=tk.LEFT)

        ttk.Button(buttons, text="Copy Output", command=lambda m=mode: self._copy_output(m)).pack(
            side=tk.LEFT, padx=(10, 0)
        )
        ttk.Button(buttons, text="Clear", style="Danger.TButton", command=lambda m=mode: self._clear(m)).pack(
            side=tk.LEFT, padx=(10, 0)
        )

        ttk.Button(buttons, text="View History", command=self._show_history).pack(side=tk.RIGHT)

    def _sync_algorithm_from_combo(self) -> None:
        selected = self.algorithm_combo.get()
        for algo_id, name in ALGORITHMS:
            if name == selected:
                self.algorithm.set(algo_id)
                break
        self._on_algorithm_change()

    def _on_algorithm_change(self) -> None:
        algo = self.algorithm.get()
        self._set_status(StatusMessage(f"Selected: {self._algo_name(algo)}", "info"))
        self._update_key_placeholders()

    def _update_key_placeholders(self) -> None:
        algo = self.algorithm.get()
        for mode in ("encrypt", "decrypt"):
            widget: ttk.Entry = getattr(self, f"{mode}_key_widget")
            widget.delete(0, tk.END)
            if algo == "caesar":
                widget.insert(0, "3")
            elif algo in ("vigenere", "playfair", "rowcolumn"):
                widget.insert(0, "")
            elif algo == "zigzag":
                widget.insert(0, "3")
            elif algo == "mono":
                if mode == "decrypt":
                    widget.insert(0, "")
                else:
                    widget.insert(0, "(auto)")

    def _algo_name(self, algo_id: str) -> str:
        for a, name in ALGORITHMS:
            if a == algo_id:
                return name
        return algo_id

    def _get_input_text(self, mode: str) -> str:
        if self._chain_enabled.get() and self._last_result:
            return self._last_result
        widget: tk.Text = getattr(self, f"{mode}_input_text")
        return widget.get("1.0", tk.END).strip()

    def _set_output_text(self, mode: str, value: str) -> None:
        widget: tk.Text = getattr(self, f"{mode}_output_text")
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
        widget.configure(state="disabled")

    def _get_key(self, mode: str):
        algo = self.algorithm.get()
        widget: ttk.Entry = getattr(self, f"{mode}_key_widget")
        raw = widget.get().strip()

        if algo in ("caesar", "zigzag"):
            num = safe_int(raw, None)
            if num is None:
                messagebox.showerror("Error", "Please enter a valid number.")
                return None
            return num

        if algo in ("vigenere", "playfair", "rowcolumn"):
            if not raw:
                messagebox.showerror("Error", "Please enter a key.")
                return None
            return raw

        if algo == "mono":
            if mode == "encrypt":
                return monoalphabetic.generate_key()
            key = normalize_key_26_upper(raw)
            if not key or len(key) != 26:
                messagebox.showerror("Error", "Please enter a valid 26-letter key.")
                return None
            return key

        return raw

    def _run(self, mode: str) -> None:
        self.mode.set(mode)
        algo = self.algorithm.get()
        text = self._get_input_text(mode)
        if not text:
            messagebox.showerror("Error", "Please enter text to process.")
            return

        key = self._get_key(mode)
        if key is None:
            return

        try:
            if mode == "encrypt":
                result = self._encrypt(algo, text, key)
            else:
                result = self._decrypt(algo, text, key)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self._set_status(StatusMessage("Error during processing.", "error"))
            return

        self._set_output_text(mode, result)
        self._last_result = result
        self._history.append((mode, self._algo_name(algo), result))
        self._set_status(StatusMessage("Done.", "success"))

        if algo == "mono" and mode == "encrypt":
            messagebox.showinfo("Key Generated", f"Generated key: {key}\nKeep this key for decryption!")

        # Preserve original behavior: prompt for chaining after each run.
        if messagebox.askyesno("Continue Processing", "Do you want to apply another algorithm to this result?"):
            self._chain_enabled.set(True)
            self._set_status(StatusMessage("Chaining enabled. Run another algorithm.", "info"))
        else:
            self._chain_enabled.set(False)

    def _encrypt(self, algo: str, text: str, key) -> str:
        if algo == "caesar":
            return caesar.encrypt(text, key)
        if algo == "vigenere":
            return vigenere.encrypt(text, key)
        if algo == "mono":
            return monoalphabetic.encrypt(text, key)
        if algo == "playfair":
            return playfair.encrypt(text, key)
        if algo == "zigzag":
            return zigzag.encrypt(text, key)
        if algo == "rowcolumn":
            return rowcolumn.encrypt(text, key)
        raise ValueError(f"Unsupported algorithm: {algo}")

    def _decrypt(self, algo: str, text: str, key) -> str:
        if algo == "caesar":
            return caesar.decrypt(text, key)
        if algo == "vigenere":
            return vigenere.decrypt(text, key)
        if algo == "mono":
            return monoalphabetic.decrypt(text, key)
        if algo == "playfair":
            return playfair.decrypt(text, key)
        if algo == "zigzag":
            return zigzag.decrypt(text, key)
        if algo == "rowcolumn":
            return rowcolumn.decrypt(text, key)
        raise ValueError(f"Unsupported algorithm: {algo}")

    def _copy_output(self, mode: str) -> None:
        widget: tk.Text = getattr(self, f"{mode}_output_text")
        value = widget.get("1.0", tk.END).strip()
        if not value:
            self._set_status(StatusMessage("Nothing to copy.", "warning"))
            return
        self.clipboard_clear()
        self.clipboard_append(value)
        self._set_status(StatusMessage("Copied output to clipboard.", "success"))

    def _clear(self, mode: str) -> None:
        in_widget: tk.Text = getattr(self, f"{mode}_input_text")
        out_widget: tk.Text = getattr(self, f"{mode}_output_text")
        key_widget: ttk.Entry = getattr(self, f"{mode}_key_widget")

        in_widget.delete("1.0", tk.END)
        out_widget.configure(state="normal")
        out_widget.delete("1.0", tk.END)
        out_widget.configure(state="disabled")

        key_widget.delete(0, tk.END)
        self._update_key_placeholders()
        self._last_result = ""
        self._chain_enabled.set(False)
        self._set_status(StatusMessage("Cleared.", "info"))

    def _show_history(self) -> None:
        if not self._history:
            messagebox.showinfo("History", "No history yet.")
            return
        lines = []
        for i, (mode, algo_name, result) in enumerate(self._history[-20:], start=1):
            lines.append(f"{i}. {mode.title()} • {algo_name}\n{result}\n")
        messagebox.showinfo("History (last 20)", "\n".join(lines).strip())

    def _set_status(self, msg: StatusMessage) -> None:
        self.status_var.set(msg.text)
        # We keep label style simple; color-coding can be added later without changing behavior.

