"""
crd_parser.py — Parse SUDS CRD (Card Definition) files.

CRD files define the physical board outline, edge connector fingers,
and shorting bars for a specific card type (e.g., Intel Multibus, VME,
Eurocard). These are production files compiled from CARD.FAI assembly
source and referenced by PC board layouts.

File format documented in dscr.txt lines 770-802.
Verified against multi0.crd.O, vme.crd.O, e220.crd.O, at.crd.O.

Section markers:
  FMARK = 400000,,0  (0o400000_000000) — separates sections
  CMARK = 0,,400000  (0o000000_400000) — terminates the file
"""

from __future__ import annotations

import logging
from pathlib import Path

from .word36 import left_half, right_half, int18
from .crd_model import CRDFile, CRDFinger, CRDBar

logger = logging.getLogger(__name__)

# Section markers
FMARK = 0o400000 << 18   # 400000,,0
CMARK = 0o400000          # 0,,400000


class CRDParseError(Exception):
    """Raised on unrecoverable CRD file parse errors."""
    pass


class CRDParser:
    """Parser for SUDS CRD card definition files.

    The CRD format has 5 sections, each separated by FMARK:
      1. Board outline (X,Y polygon)
      2. Front fingers (component side)
      3. Back fingers (solder side)
      4. Front shorting bars
      5. Back shorting bars
    The file is terminated by CMARK.

    Usage:
        from .unpack import read_file
        words = read_file("multi0.crd.O")
        parser = CRDParser(words, source_path="multi0.crd.O")
        crd = parser.parse()
        print(crd.summary())
    """

    def __init__(self, words: list[int], source_path: str = "",
                 debug: bool = False):
        self.words = words
        self.source_path = source_path
        self.debug = debug
        self.pos = 0
        self.result = CRDFile(source_path=source_path, word_count=len(words))

    def _dbg(self, msg: str) -> None:
        if self.debug:
            logger.debug(msg)

    def _at_end(self) -> bool:
        return self.pos >= len(self.words)

    def _read_word(self) -> int:
        if self.pos >= len(self.words):
            raise CRDParseError(f"Unexpected EOF at word {self.pos}")
        w = self.words[self.pos]
        self.pos += 1
        return w

    def _peek_word(self) -> int:
        if self.pos >= len(self.words):
            return 0
        return self.words[self.pos]

    def _read_xy(self) -> tuple[int, int]:
        """Read an X,Y coordinate pair from one word."""
        w = self._read_word()
        return (int18(left_half(w)), int18(right_half(w)))

    def _is_fmark(self) -> bool:
        if self._at_end():
            return False
        return self.words[self.pos] == FMARK

    def _is_cmark(self) -> bool:
        if self._at_end():
            return False
        return self.words[self.pos] == CMARK

    def _expect_fmark(self, section_name: str) -> None:
        """Skip an FMARK, raising if not found."""
        if self._at_end():
            raise CRDParseError(f"Expected FMARK before {section_name}, got EOF")
        w = self._read_word()
        if w != FMARK:
            raise CRDParseError(
                f"Expected FMARK before {section_name} at word {self.pos-1}, "
                f"got {oct(w)}"
            )

    def _parse_outline(self) -> None:
        """Parse the board outline (X,Y polygon vertices).

        The outline section starts with a CRDVER word (version number,
        currently 1) followed by X,Y coordinate pairs.  The first XY
        has an "initial point" flag (bit 0 set in the right half) which
        must be masked off to recover the true Y coordinate.

        Terminated by FMARK.
        """
        self._dbg(f"Parsing outline at word {self.pos}")

        # First word is CRDVER (version number), not a coordinate
        if not self._at_end() and not self._is_fmark():
            ver_word = self._read_word()
            version = right_half(ver_word)
            self.result.version = version
            self._dbg(f"  CRD version: {version}")

        first_point = True
        while not self._at_end():
            if self._is_fmark():
                self._read_word()  # consume FMARK
                break
            x, y = self._read_xy()

            if first_point:
                # Strip "initial point" flag (bit 0) from Y coordinate
                # The XY macro with I flag: 1!<X/5*2,,Y/5*2> ORs 1 into
                # the right half, setting bit 0.
                y = y & ~1
                first_point = False

            self.result.outline.append((x, y))
        self._dbg(f"  Outline: {len(self.result.outline)} vertices")

    def _parse_fingers(self, side_name: str) -> list[CRDFinger]:
        """Parse a finger section (front or back).

        Each finger: start X,Y + end X,Y + BYTE(6) location word.
        Terminated by FMARK.
        """
        self._dbg(f"Parsing {side_name} fingers at word {self.pos}")
        fingers: list[CRDFinger] = []

        while not self._at_end():
            if self._is_fmark():
                self._read_word()  # consume FMARK
                break
            if self._is_cmark():
                self._read_word()  # consume CMARK
                break

            start = self._read_xy()
            end = self._read_xy()
            location = self._read_word()

            finger = CRDFinger(start=start, end=end, location=location)
            fingers.append(finger)

        self._dbg(f"  {side_name} fingers: {len(fingers)}")
        return fingers

    def _parse_bars(self, side_name: str) -> list[CRDBar]:
        """Parse a shorting bar section (front or back).

        Each bar: start X,Y + end X,Y pair.
        Terminated by FMARK or CMARK.
        """
        self._dbg(f"Parsing {side_name} shorting bars at word {self.pos}")
        bars: list[CRDBar] = []

        while not self._at_end():
            if self._is_fmark():
                self._read_word()  # consume FMARK
                break
            if self._is_cmark():
                self._read_word()  # consume CMARK
                break

            start = self._read_xy()
            end = self._read_xy()

            bar = CRDBar(start=start, end=end)
            bars.append(bar)

        self._dbg(f"  {side_name} shorting bars: {len(bars)}")
        return bars

    def parse(self) -> CRDFile:
        """Parse the complete CRD file."""
        if len(self.words) < 3:
            raise CRDParseError(
                f"File too short: {len(self.words)} words (minimum 3)"
            )

        self._dbg(f"Parsing CRD file: {self.source_path} ({len(self.words)} words)")

        # 1. Board outline (terminated by FMARK)
        self._parse_outline()

        # 2. Front (component side) fingers (terminated by FMARK)
        self.result.front_fingers = self._parse_fingers("Front")

        # 3. Back (solder side) fingers (terminated by FMARK)
        self.result.back_fingers = self._parse_fingers("Back")

        # 4. Front shorting bars (terminated by FMARK)
        self.result.front_bars = self._parse_bars("Front")

        # 5. Back shorting bars (terminated by CMARK)
        self.result.back_bars = self._parse_bars("Back")

        # File should end with CMARK (already consumed above) or be at end
        if not self._at_end():
            # Check for final CMARK
            if self._is_cmark():
                self._read_word()

        self._dbg("CRD parse complete")
        return self.result


# ============================================================================
# Convenience functions
# ============================================================================

def parse_crd_file(path: str | Path, debug: bool = False) -> CRDFile:
    """Parse a CRD card definition file from disk."""
    from .unpack import read_file
    words = read_file(str(path))
    parser = CRDParser(words, source_path=str(path), debug=debug)
    return parser.parse()


def parse_crd_words(words: list[int], source_path: str = "",
                    debug: bool = False) -> CRDFile:
    """Parse a CRD card definition file from a pre-loaded word list."""
    parser = CRDParser(words, source_path=source_path, debug=debug)
    return parser.parse()
