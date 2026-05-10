"""
Vigenère cipher implementation.

Preserves behavior from the original single-file version.
"""


def encrypt(text: str, key: str) -> str:
    """Encrypt text using Vigenere cipher with the given key."""
    result = ""
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(k) - ord("A") for k in key]

    for i, char in enumerate(text):
        if char.isalpha():
            key_index = i % key_length
            shift = key_as_int[key_index]

            ascii_offset = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result


def decrypt(text: str, key: str) -> str:
    """Decrypt text using Vigenere cipher with the given key."""
    result = ""
    key = key.upper()
    key_length = len(key)
    key_as_int = [ord(k) - ord("A") for k in key]

    for i, char in enumerate(text):
        if char.isalpha():
            key_index = i % key_length
            shift = key_as_int[key_index]

            ascii_offset = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    return result

