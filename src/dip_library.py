"""
dip_library.py — Parse the SUDS DIPS.DIP library file.

The DIPS.DIP file is a sequential database of DIP (Dual Inline Package)
IC definitions. Each entry contains a pin count, component name, optional
part number, and per-pin electrical data (loading, use, section info).

PC board body placements reference entries by L-index (sequential position
in this file) to identify the component type.

Format (from dscr.txt lines 806-822):
    Header word (777777,,xxxxxx)
    --------
    !   # OF PINS
    !   ASCIZ/DIPNAME/
    !   ASCIZ/PART NUMBER STRING/
    !   --------
    !   !   XWD BITS,PS #
    !   !   XWD HI,LOW LOADING
    !   !   SIXBIT/USE/
    !   !   SECT BITS,,1ST SECT PIN#
    !   --------
    --------
    0

Between entries: zero-word separators and flag/marker words (nonzero left half)
are skipped. The pin count word always has left_half == 0.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .word36 import left_half, right_half


@dataclass
class DIPEntry:
    """A DIP component type from the DIPS.DIP library."""
    index: int = 0           # L-index (position in file)
    name: str = ""           # Component name (e.g., "8T97", "74LS283")
    part_number: str = ""    # Part number string (often empty)
    num_pins: int = 0        # Number of pins


class DIPLibrary:
    """Parsed DIPS.DIP library providing L-index → component name lookup."""

    def __init__(self):
        self.entries: dict[int, DIPEntry] = {}

    def get_name(self, l_index: int) -> str:
        """Get component name by L-index. Returns 'L{n}' if not found."""
        entry = self.entries.get(l_index)
        if entry and entry.name:
            return entry.name
        return f"L{l_index}"

    def get_entry(self, l_index: int) -> DIPEntry | None:
        """Get full DIP entry by L-index."""
        return self.entries.get(l_index)

    def __len__(self) -> int:
        return len(self.entries)

    def __contains__(self, l_index: int) -> bool:
        return l_index in self.entries


def _read_asciz(words: list[int], pos: int) -> tuple[str, int]:
    """Read a 7-bit ASCIZ string from the word stream."""
    name = ''
    while pos < len(words):
        w = words[pos]
        pos += 1
        for shift in [29, 22, 15, 8, 1]:
            ch = (w >> shift) & 0o177
            if ch == 0:
                return name, pos
            name += chr(ch)
        if (w & 0o177) == 0:
            return name, pos
    return name, pos


def parse_dip_library(path: str | Path) -> DIPLibrary:
    """Parse a DIPS.DIP library file and return a DIPLibrary.

    Args:
        path: Path to the .dip.O file (octal text format).

    Returns:
        DIPLibrary with all entries indexed by L-number.
    """
    from .unpack import read_file
    words = read_file(str(path))

    lib = DIPLibrary()
    pos = 0

    # Skip header word (777777,,xxxxxx)
    if pos < len(words) and left_half(words[pos]) == 0o777777:
        pos = 1

    index = 0

    while pos < len(words) and index < 2000:
        # Pin count is right_half of current word
        # (left half may contain flags — ignore it)
        numpins = right_half(words[pos])
        if numpins <= 0 or numpins > 200:
            break
        pos += 1

        name, pos = _read_asciz(words, pos)
        part, pos = _read_asciz(words, pos)

        # Skip per-pin data (4 words per pin)
        pos += numpins * 4

        entry = DIPEntry(index=index, name=name, part_number=part,
                         num_pins=numpins)
        lib.entries[index] = entry
        index += 1

        # Skip exactly 1 separator word between entries
        if pos < len(words):
            pos += 1

    return lib
