"""
word36.py — 36-bit PDP-10 word manipulation utilities.

A 36-bit word is stored as a Python int.
The PDP-10 divides each word into two 18-bit "halfwords":
    [LEFT_HALF (bits 35-18)] [RIGHT_HALF (bits 17-0)]

ASCIZ strings pack 5 × 7-bit ASCII characters per word (35 bits, LSB=0):
    [c1:7][c2:7][c3:7][c4:7][c5:7][0:1]
"""

WORD_MASK = (1 << 36) - 1       # 0o777777_777777
HALF_MASK = (1 << 18) - 1       # 0o777777
SENTINEL  = 0o400000            # 0x20000 — section boundary marker


def left_half(word: int) -> int:
    """Extract the left (upper) 18 bits of a 36-bit word."""
    return (word >> 18) & HALF_MASK


def right_half(word: int) -> int:
    """Extract the right (lower) 18 bits of a 36-bit word."""
    return word & HALF_MASK


def int18(value: int) -> int:
    """Sign-extend an 18-bit value to a Python signed integer."""
    if value & (1 << 17):
        return value - (1 << 18)
    return value


def make_word(left: int, right: int) -> int:
    """Construct a 36-bit word from two 18-bit halfwords."""
    return ((left & HALF_MASK) << 18) | (right & HALF_MASK)


def word_to_octal(word: int) -> str:
    """Format a 36-bit word as a 12-digit octal string."""
    return f"{word:012o}"


def octal_to_word(s: str) -> int:
    """Parse a 12-digit octal string into a 36-bit word."""
    return int(s, 8) & WORD_MASK


# ---------------------------------------------------------------------------
# ASCIZ string extraction
# ---------------------------------------------------------------------------

def _extract_7bit_chars(word: int) -> list[int]:
    """Extract five 7-bit characters from a 36-bit word.

    Layout:  [c1:7][c2:7][c3:7][c4:7][c5:7][pad:1]
    c1 is in bits 35-29, c5 is in bits 7-1, bit 0 is padding.
    """
    chars = []
    chars.append((word >> 29) & 0x7F)
    chars.append((word >> 22) & 0x7F)
    chars.append((word >> 15) & 0x7F)
    chars.append((word >>  8) & 0x7F)
    chars.append((word >>  1) & 0x7F)
    return chars


def read_asciz(words: list[int], offset: int) -> tuple[str, int]:
    """Read an ASCIZ string starting at *offset* in the word array.

    Returns (string, next_offset) where next_offset points to the word
    after the NUL terminator.  The NUL may appear anywhere within a word;
    the remaining characters in that word are ignored.
    """
    result: list[str] = []
    pos = offset
    while pos < len(words):
        chars = _extract_7bit_chars(words[pos])
        pos += 1
        for c in chars:
            if c == 0:
                return ("".join(result), pos)
            result.append(chr(c))
    # Unterminated string — return what we have
    return ("".join(result), pos)


def read_sixbit(words: list[int], offset: int) -> tuple[str, int]:
    """Read a SIXBIT-encoded string starting at *offset*.

    SIXBIT packs 6 characters per word (6 × 6 bits = 36 bits).
    Character code 0 = space (0o40 in ASCII), so add 0o40 to convert.
    A NUL (code 0 → space) terminates when context dictates.

    Returns (string, next_offset).
    """
    result: list[str] = []
    pos = offset
    while pos < len(words):
        w = words[pos]
        pos += 1
        all_zero = True
        for shift in (30, 24, 18, 12, 6, 0):
            c = (w >> shift) & 0o77
            if c != 0:
                all_zero = False
            ch = chr(c + 0o40) if c != 0 else '\0'
            if ch == '\0':
                return ("".join(result).rstrip(), pos)
            result.append(ch)
        if all_zero:
            return ("".join(result).rstrip(), pos)
    return ("".join(result).rstrip(), pos)


def is_zero(words: list[int], offset: int) -> bool:
    """Check if the word at offset is zero."""
    if offset >= len(words):
        return True
    return words[offset] == 0


def is_sentinel(words: list[int], offset: int) -> bool:
    """Check if the word at offset is the section sentinel (0o400000)."""
    if offset >= len(words):
        return True
    return words[offset] == SENTINEL
