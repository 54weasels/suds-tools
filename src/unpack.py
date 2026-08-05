"""
unpack.py — Decode PDP-10 36-bit word files in various formats.

Supported input formats
-----------------------
- **octal text** (.O files from SAILDART):
      Plain text, one 12-digit octal number per line.

- **ITS evacuated** (binary, as produced by `cat36 -Woct -Xits`):
      Alan Bawden's encoding of 36-bit words in 8-bit bytes.
      See unpack.c in the SUDS repository for the reference implementation.

Both readers produce the same output: a Python list of ints, each in [0, 2^36).
"""

from __future__ import annotations

import struct
from pathlib import Path

from .word36 import WORD_MASK


# ============================================================================
# Octal text format  (.O files)
# ============================================================================

def read_octal_file(path: str | Path) -> list[int]:
    """Read a SAILDART octal-text file into a list of 36-bit words.

    Each line is expected to be exactly 12 octal digits (no prefix).
    Blank lines and lines that don't parse are silently skipped.
    """
    words: list[int] = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                word = int(line, 8) & WORD_MASK
                words.append(word)
            except ValueError:
                continue
    return words


# ============================================================================
# ITS evacuated binary format
# ============================================================================

# Lookup tables ported from unpack.c (Alan Bawden's encoding)
# first[c]  — first 7-bit output code for input byte c  (0 ≤ c ≤ 0xEF)
# second[c] — second 7-bit output code, or _NONE if only one

_NONE = 0x100  # sentinel: "no second byte"

_FIRST = [
    # 0o000 - 0o007
    0o000, 0o001, 0o002, 0o003, 0o004, 0o005, 0o006, 0o007,
    # 0o010 - 0o017  (0o012 = '\n' → CR,LF pair: first=CR=0o015)
    0o010, 0o011, 0o015, 0o013, 0o014, 0o012, 0o016, 0o017,
    # 0o020 - 0o027
    0o020, 0o021, 0o022, 0o023, 0o024, 0o025, 0o026, 0o027,
    # 0o030 - 0o037
    0o030, 0o031, 0o032, 0o033, 0o034, 0o035, 0o036, 0o037,
    # 0o040 - 0o047
    0o040, 0o041, 0o042, 0o043, 0o044, 0o045, 0o046, 0o047,
    # 0o050 - 0o057
    0o050, 0o051, 0o052, 0o053, 0o054, 0o055, 0o056, 0o057,
    # 0o060 - 0o067
    0o060, 0o061, 0o062, 0o063, 0o064, 0o065, 0o066, 0o067,
    # 0o070 - 0o077
    0o070, 0o071, 0o072, 0o073, 0o074, 0o075, 0o076, 0o077,
    # 0o100 - 0o107
    0o100, 0o101, 0o102, 0o103, 0o104, 0o105, 0o106, 0o107,
    # 0o110 - 0o117
    0o110, 0o111, 0o112, 0o113, 0o114, 0o115, 0o116, 0o117,
    # 0o120 - 0o127
    0o120, 0o121, 0o122, 0o123, 0o124, 0o125, 0o126, 0o127,
    # 0o130 - 0o137
    0o130, 0o131, 0o132, 0o133, 0o134, 0o135, 0o136, 0o137,
    # 0o140 - 0o147
    0o140, 0o141, 0o142, 0o143, 0o144, 0o145, 0o146, 0o147,
    # 0o150 - 0o157
    0o150, 0o151, 0o152, 0o153, 0o154, 0o155, 0o156, 0o157,
    # 0o160 - 0o167
    0o160, 0o161, 0o162, 0o163, 0o164, 0o165, 0o166, 0o167,
    # 0o170 - 0o177
    0o170, 0o171, 0o172, 0o173, 0o174, 0o175, 0o176, 0o177,
    # 0o200 - 0o207  (all produce 0o177 first)
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o210 - 0o217
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o220 - 0o227
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o230 - 0o237
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o240 - 0o247
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o250 - 0o257
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o260 - 0o267
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o270 - 0o277
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o300 - 0o307
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o310 - 0o317
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o320 - 0o327
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o330 - 0o337
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o340 - 0o347
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o177,
    # 0o350 - 0o357
    0o177, 0o177, 0o177, 0o177, 0o177, 0o177, 0o015, 0o177,
]

_SECOND = [
    # 0o000 - 0o007
    _NONE, _NONE, _NONE, _NONE, _NONE, _NONE, _NONE, _NONE,
    # 0o010 - 0o017  (0o012 = '\n' → second = LF = 0o012)
    _NONE, _NONE, 0o012, _NONE, _NONE, _NONE, _NONE, _NONE,
    # 0o020 - 0o177: all _NONE
    *([_NONE] * (0o200 - 0o020)),
    # 0o200 - 0o207
    0o000, 0o001, 0o002, 0o003, 0o004, 0o005, 0o006, 0o177,
    # 0o210 - 0o217
    0o010, 0o011, 0o015, 0o013, 0o014, 0o012, 0o016, 0o017,
    # 0o220 - 0o227
    0o020, 0o021, 0o022, 0o023, 0o024, 0o025, 0o026, 0o027,
    # 0o230 - 0o237
    0o030, 0o031, 0o032, 0o033, 0o034, 0o035, 0o036, 0o037,
    # 0o240 - 0o247
    0o040, 0o041, 0o042, 0o043, 0o044, 0o045, 0o046, 0o047,
    # 0o250 - 0o257
    0o050, 0o051, 0o052, 0o053, 0o054, 0o055, 0o056, 0o057,
    # 0o260 - 0o267
    0o060, 0o061, 0o062, 0o063, 0o064, 0o065, 0o066, 0o067,
    # 0o270 - 0o277
    0o070, 0o071, 0o072, 0o073, 0o074, 0o075, 0o076, 0o077,
    # 0o300 - 0o307
    0o100, 0o101, 0o102, 0o103, 0o104, 0o105, 0o106, 0o107,
    # 0o310 - 0o317
    0o110, 0o111, 0o112, 0o113, 0o114, 0o115, 0o116, 0o117,
    # 0o320 - 0o327
    0o120, 0o121, 0o122, 0o123, 0o124, 0o125, 0o126, 0o127,
    # 0o330 - 0o337
    0o130, 0o131, 0o132, 0o133, 0o134, 0o135, 0o136, 0o137,
    # 0o340 - 0o347
    0o140, 0o141, 0o142, 0o143, 0o144, 0o145, 0o146, 0o147,
    # 0o350 - 0o357
    0o150, 0o151, 0o152, 0o153, 0o154, 0o155, _NONE, _NONE,
]

# Sanity: tables should have exactly 0o360 = 240 entries
assert len(_FIRST) == 0o360, f"_FIRST has {len(_FIRST)} entries, expected {0o360}"
assert len(_SECOND) == 0o360, f"_SECOND has {len(_SECOND)} entries, expected {0o360}"


def _flush_ascii_word(buf: list[int]) -> int:
    """Pack 5 × 7-bit characters into a single 36-bit word.

    Layout: [c1:7][c2:7][c3:7][c4:7][c5:7][0:1]
    """
    assert len(buf) == 5
    w = (buf[0] << 29) | (buf[1] << 22) | (buf[2] << 15) | (buf[3] << 8) | (buf[4] << 1)
    return w & WORD_MASK


def read_its_file(path: str | Path) -> list[int]:
    """Read an ITS evacuated-format binary file into a list of 36-bit words.

    This is a faithful port of the decoding algorithm from unpack.c.
    """
    data = Path(path).read_bytes()
    words: list[int] = []
    buf: list[int] = []      # accumulator for 7-bit chars (flushed every 5)
    idx = 0

    while idx < len(data):
        c = data[idx]
        idx += 1

        if c >= 0o360:  # 0xF0..0xFF — quoted binary word
            if idx + 4 > len(data):
                break  # truncated
            b0 = c & 0o17
            b1 = data[idx]
            b2 = data[idx + 1]
            b3 = data[idx + 2]
            b4 = data[idx + 3]
            idx += 4
            # Assemble 36-bit word from 5 bytes
            word = (b0 << 32) | (b1 << 24) | (b2 << 16) | (b3 << 8) | b4
            # buf must be empty at a word boundary
            if buf:
                raise ValueError(
                    f"Quoted binary word encountered mid-word at byte {idx - 5}"
                )
            words.append(word & WORD_MASK)
        else:
            # Lookup first character
            first_c = _FIRST[c]
            buf.append(first_c & 0x7F)
            if len(buf) == 5:
                words.append(_flush_ascii_word(buf))
                buf = []

            # Lookup second character (if any)
            second_c = _SECOND[c]
            if second_c != _NONE:
                buf.append(second_c & 0x7F)
                if len(buf) == 5:
                    words.append(_flush_ascii_word(buf))
                    buf = []

    # Pad remaining buffer with ^C (0o003) and flush
    if buf:
        while len(buf) < 5:
            buf.append(0o003)
        words.append(_flush_ascii_word(buf))

    return words


# ============================================================================
# Auto-detect format
# ============================================================================

def read_file(path: str | Path) -> list[int]:
    """Read a 36-bit word file, auto-detecting the format.

    - If the file extension is `.O` or the first bytes look like octal text
      (ASCII digits and newlines), use the octal reader.
    - Otherwise, try ITS evacuated binary.
    """
    p = Path(path)

    # Check extension
    if p.suffix.upper() == ".O":
        return read_octal_file(p)

    # Sniff first bytes
    with open(p, "rb") as f:
        head = f.read(64)

    # If first 13 bytes look like "NNNNNNNNNNNN\n" (octal digits + newline)
    if all(b in b"01234567\n\r" for b in head[:20]):
        return read_octal_file(p)

    # Default to ITS evacuated
    return read_its_file(p)


# ============================================================================
# Dump utilities
# ============================================================================

def dump_octal(words: list[int]) -> str:
    """Dump words as octal text (one 12-digit word per line)."""
    return "\n".join(f"{w:012o}" for w in words)


def dump_words(words: list[int], start: int = 0, count: int | None = None,
               fmt: str = "octal") -> str:
    """Pretty-print a range of words with addresses.

    *fmt* is one of "octal", "hex", "ascii".
    """
    if count is None:
        count = len(words) - start
    lines: list[str] = []
    for i in range(start, min(start + count, len(words))):
        w = words[i]
        lh = (w >> 18) & 0o777777
        rh = w & 0o777777
        if fmt == "hex":
            addr = f"{i:6d}"
            val = f"{w:09X}"
            halves = f"{lh:05X},{rh:05X}"
        else:
            addr = f"{i:6d}"
            val = f"{w:012o}"
            halves = f"{lh:06o},{rh:06o}"

        # Try to show ASCII
        ascii_repr = ""
        chars = []
        chars.append((w >> 29) & 0x7F)
        chars.append((w >> 22) & 0x7F)
        chars.append((w >> 15) & 0x7F)
        chars.append((w >>  8) & 0x7F)
        chars.append((w >>  1) & 0x7F)
        for c in chars:
            if 0x20 <= c <= 0x7E:
                ascii_repr += chr(c)
            else:
                ascii_repr += "."

        lines.append(f"{addr}  {val}  {halves}  |{ascii_repr}|")
    return "\n".join(lines)
