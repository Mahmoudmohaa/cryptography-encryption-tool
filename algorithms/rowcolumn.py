"""
Row-Column transposition cipher implementation.

Preserves behavior from the original single-file version.
"""

import math


def encrypt(text: str, key: str) -> str:
    """Encrypt text using Row-Column Transposition cipher with the given key."""
    text = "".join(char for char in text if char.isalpha() or char.isdigit())

    key_length = len(key)
    num_rows = math.ceil(len(text) / key_length)

    padded_length = num_rows * key_length
    text = text.ljust(padded_length, "X")

    grid: list[list[str]] = []
    for i in range(0, len(text), key_length):
        grid.append(list(text[i : i + key_length]))

    key_order: list[int] = []
    key_work = key
    for char in sorted(key_work):
        key_order.append(key_work.index(char))
        idx = key_work.index(char)
        key_work = key_work[:idx] + "." + key_work[idx + 1 :]  # Mark as used

    result = ""
    for col_idx in key_order:
        for row in grid:
            if col_idx < len(row):
                result += row[col_idx]

    return result


def decrypt(text: str, key: str) -> str:
    """Decrypt text using Row-Column Transposition cipher with the given key."""
    key_length = len(key)
    num_rows = math.ceil(len(text) / key_length)

    key_order: list[int] = []
    sorted_key = "".join(sorted(key))
    for char in key:
        key_order.append(sorted_key.index(char))
        idx = sorted_key.index(char)
        sorted_key = sorted_key[:idx] + "." + sorted_key[idx + 1 :]

    grid = [[""] * key_length for _ in range(num_rows)]

    col_lengths = [num_rows] * key_length
    remaining = len(text) % key_length
    if remaining > 0:
        for i in range(key_length - remaining, key_length):
            col_lengths[i] -= 1

    index = 0
    for col in range(key_length):
        col_idx = key_order.index(col)
        for row in range(col_lengths[col_idx]):
            grid[row][col_idx] = text[index]
            index += 1

    result = ""
    for row in grid:
        result += "".join(row)

    return result

