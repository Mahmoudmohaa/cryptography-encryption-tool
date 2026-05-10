# Cryptography Encryption Tool (Python)

A beginner-friendly desktop app for **encrypting and decrypting text** using classic cryptography ciphers.
Built with **Python + Tkinter (ttk)** and refactored into a clean, portfolio-ready structure.

## Features

- Dark-mode **modern ttk UI**
- Encrypt & decrypt tabs
- Dropdown algorithm selection
- Dynamic key input (shift / keyword / rails)
- Status messages
- Copy output to clipboard
- Clear input/output
- Optional **chaining** (apply multiple algorithms in sequence)
- Basic history (last 20 operations)

## Included Algorithms

- Caesar Cipher
- Vigenere Cipher
- Mono Alphabetical Cipher
- Playfair Cipher
- Zigzag (Rail Fence) Cipher
- Row Column (Transposition) Cipher

## Screenshots

Add screenshots to `screenshots/` and reference them here:

- `screenshots/main.png`
- `screenshots/encrypt.png`
- `screenshots/decrypt.png`

## Installation

Requirements:
- Python 3.10+ recommended (Tkinter included with standard Python on Windows)

Steps:

```bash
git clone https://github.com/Mahmoudmohaa/cryptography-encryption-tool.git
cd cryptography-encryption-tool
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Usage

1. Choose an algorithm from the dropdown.
2. Switch to **Encrypt** or **Decrypt** tab.
3. Enter input text.
4. Enter the key:
   - Caesar: shift (e.g., `3`)
   - Zigzag: number of rails (e.g., `3`)
   - Vigenere/Playfair/Row Column: keyword (e.g., `SECRET`)
   - Monoalphabetic:
     - Encrypt: key auto-generated (shown after run)
     - Decrypt: provide the 26-letter key
5. Click **Encrypt/Decrypt**.
6. (Optional) accept the chaining prompt to apply another algorithm to the result.

## Project Structure

```text
cryptography-encryption-tool/
│
├── main.py
├── gui/
│   ├── app.py
│   ├── windows.py
│   └── styles.py
│
├── algorithms/
│   ├── caesar.py
│   ├── vigenere.py
│   ├── monoalphabetic.py
│   ├── playfair.py
│   ├── zigzag.py
│   └── rowcolumn.py
│
├── utils/
│   └── helpers.py
│
├── screenshots/
├── README.md
├── requirements.txt
└── .gitignore
```

## Example

- Caesar Encrypt:
  - Text: `Hello World`
  - Shift: `3`
  - Output: `Khoor Zruog`

## Technologies Used

- Python
- Tkinter / ttk

## Future Improvements

- Export history to file (CSV/JSON)
- Per-algorithm help panel
- Optional file encryption mode (for learning use-cases)
- Input validation hints (live)
- Better history viewer (dockable panel)

