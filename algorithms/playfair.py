"""
Playfair cipher implementation.

Preserves behavior from the original single-file version.
"""


def prepare_key(key: str) -> str:
    """Prepare the key for Playfair cipher."""
    key = key.upper().replace("J", "I")
    key = "".join(dict.fromkeys(key))  # Remove duplicates

    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # No J
    for char in key:
        alphabet = alphabet.replace(char, "")

    return key + alphabet


def _positions(matrix: str, char1: str, char2: str) -> tuple[int, int, int, int]:
    """Get positions of two characters in the Playfair matrix."""
    char1 = "I" if char1 == "J" else char1
    char2 = "I" if char2 == "J" else char2

    pos1 = matrix.index(char1)
    pos2 = matrix.index(char2)

    row1, col1 = pos1 // 5, pos1 % 5
    row2, col2 = pos2 // 5, pos2 % 5

    return row1, col1, row2, col2


def encrypt(text: str, key: str) -> str:
    """Encrypt text using Playfair cipher with the given key."""
    matrix = prepare_key(key)
    text = text.upper().replace("J", "I")

    text = "".join(char for char in text if char.isalpha())

    i = 0
    pairs: list[str] = []
    while i < len(text):
        if i == len(text) - 1:
            pairs.append(text[i] + "X")
            break

        if text[i] == text[i + 1]:
            pairs.append(text[i] + "X")
            i += 1
        else:
            pairs.append(text[i : i + 2])
            i += 2

    result = ""
    for pair in pairs:
        row1, col1, row2, col2 = _positions(matrix, pair[0], pair[1])

        if row1 == row2:
            result += matrix[row1 * 5 + (col1 + 1) % 5]
            result += matrix[row2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:
            result += matrix[((row1 + 1) % 5) * 5 + col1]
            result += matrix[((row2 + 1) % 5) * 5 + col2]
        else:
            result += matrix[row1 * 5 + col2]
            result += matrix[row2 * 5 + col1]

    return result


def decrypt(text: str, key: str) -> str:
    """Decrypt text using Playfair cipher with the given key."""
    matrix = prepare_key(key)
    text = text.upper()

    text = "".join(char for char in text if char.isalpha())
    pairs = [text[i : i + 2] for i in range(0, len(text), 2)]

    result = ""
    for pair in pairs:
        if len(pair) < 2:
            pair += "X"

        row1, col1, row2, col2 = _positions(matrix, pair[0], pair[1])

        if row1 == row2:
            result += matrix[row1 * 5 + (col1 - 1) % 5]
            result += matrix[row2 * 5 + (col2 - 1) % 5]
        elif col1 == col2:
            result += matrix[((row1 - 1) % 5) * 5 + col1]
            result += matrix[((row2 - 1) % 5) * 5 + col2]
        else:
            result += matrix[row1 * 5 + col2]
            result += matrix[row2 * 5 + col1]

    return result

