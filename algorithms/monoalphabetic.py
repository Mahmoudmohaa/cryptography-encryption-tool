"""
Monoalphabetic substitution cipher implementation.

Preserves behavior from the original single-file version.
"""

import random
import string


def generate_key() -> str:
    """Generate a random substitution key (26 uppercase letters)."""
    alphabet = list(string.ascii_uppercase)
    shuffled = alphabet.copy()
    random.shuffle(shuffled)
    return "".join(shuffled)


def encrypt(text: str, key: str) -> str:
    """Encrypt text using mono alphabetical cipher with the given key."""
    result = ""
    alphabet = string.ascii_uppercase

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char_idx = alphabet.index(char.upper())
            encrypted_char = key[char_idx]

            if not is_upper:
                encrypted_char = encrypted_char.lower()

            result += encrypted_char
        else:
            result += char
    return result


def decrypt(text: str, key: str) -> str:
    """Decrypt text using mono alphabetical cipher with the given key."""
    result = ""
    alphabet = string.ascii_uppercase

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char_upper = char.upper()

            if char_upper in key:
                char_idx = key.index(char_upper)
                decrypted_char = alphabet[char_idx]

                if not is_upper:
                    decrypted_char = decrypted_char.lower()

                result += decrypted_char
            else:
                result += char
        else:
            result += char
    return result

