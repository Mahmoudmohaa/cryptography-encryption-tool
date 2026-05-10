"""
Zigzag (Rail Fence) cipher implementation.

Preserves behavior from the original single-file version.
"""


def encrypt(text: str, rails: int) -> str:
    """Encrypt text using Zigzag (Rail Fence) cipher with the given number of rails."""
    if rails <= 1:
        return text

    rail_rows: list[list[str]] = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        rail_rows[rail].append(char)

        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1

        rail += direction

    return "".join("".join(r) for r in rail_rows)


def decrypt(text: str, rails: int) -> str:
    """Decrypt text using Zigzag (Rail Fence) cipher with the given number of rails."""
    if rails <= 1 or len(text) <= 1:
        return text

    rail_lengths = [0] * rails
    rail = 0
    direction = 1

    for _ in range(len(text)):
        rail_lengths[rail] += 1

        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1

        rail += direction

    rail_slices: list[str] = []
    index = 0
    for length in rail_lengths:
        rail_slices.append(text[index : index + length])
        index += length

    result = ""
    rail = 0
    direction = 1

    for _ in range(len(text)):
        result += rail_slices[rail][0]
        rail_slices[rail] = rail_slices[rail][1:]

        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1

        rail += direction

    return result

