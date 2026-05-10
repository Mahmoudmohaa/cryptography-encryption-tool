"""
Caesar cipher implementation.

Preserves behavior from the original single-file version.
"""


def encrypt(text: str, shift: int) -> str:
    """Encrypt text using Caesar cipher with the given shift value."""
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result


def decrypt(text: str, shift: int) -> str:
    """Decrypt text using Caesar cipher with the given shift value."""
    return encrypt(text, -shift)

