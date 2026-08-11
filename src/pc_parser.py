"""
pc_parser.py — Parse SUDS PC board layout files into a structured data model.

PC files store printed circuit board layouts in 36-bit PDP-10 word format.
Unlike DRW files, PC bodies are DIP references (not full symbol definitions),
points have variable-length neighbor lists, and there are two separate point
sections for the component and solder sides of the board.

Reference documents:
  - dscr.txt lines 498-562 — PC file format specification
  - pio.307, in.501 (DRAW source) — I/O routines
  - Empirically verified against mouse.pc.O, x.pc.O, and other SMI files
"""

from __future__ import annotations

import logging
from pathlib import Path

from .word36 import left_half, right_half, int18, SENTINEL, HALF_MASK
from .pc_model import (
    PCFile, PCMacro, PCBody, PCPoint, PCSetCenter,
    PCCardInfo, PCDiagnostic,
)

logger = logging.getLogger(__name__)


class PCParseError(Exception):
    """Raised on unrecoverable PC file parse errors."""
    pass


class PCParser:
    """Parser for SUDS PC board layout files.

    Reads a list of 36-bit words and produces a PCFile model object.
    The file format is documented in dscr.txt lines 498-562.

    Usage:
        from .unpack import read_file
        words = read_file("board.pc.O")
        parser = PCParser(words, source_path="board.pc.O")
        pc = parser.parse()
        print(pc.summary())
    """

    # Section end sentinels
    SENTINEL_400000 = SENTINEL       # 0o400000 = 0,,400000 as right half
    SENTINEL_400001 = SENTINEL + 1   # 0o400001 = marks end of sets section

    def __init__(self, words: list[int], source_path: str = "",
                 debug: bool = False):
        self.words = words
        self.source_path = source_path
        self.debug = debug
        self.pos = 0  # Current word position
        self.result = PCFile(source_path=source_path, word_count=len(words))

    def _dbg(self, msg: str) -> None:
        if self.debug:
            logger.debug(msg)

    def _warn(self, msg: str, category: str = 'format') -> None:
        """Record a parse warning."""
        diag = PCDiagnostic(
            severity='warning',
            category=category,
            message=msg,
            word_offset=self.pos,
        )
        self.result.diagnostics.append(diag)
        logger.warning(f"PC parse [{self.pos}]: {msg}")

    def _error(self, msg: str, category: str = 'format') -> None:
        """Record a parse error."""
        diag = PCDiagnostic(
            severity='error',
            category=category,
            message=msg,
            word_offset=self.pos,
        )
        self.result.diagnostics.append(diag)
        logger.error(f"PC parse [{self.pos}]: {msg}")

    # ------------------------------------------------------------------
    # Word-level reading primitives
    # ------------------------------------------------------------------

    def _at_end(self) -> bool:
        return self.pos >= len(self.words)

    def _remaining(self) -> int:
        return len(self.words) - self.pos

    def _read_word(self) -> int:
        """Read one 36-bit word and advance."""
        if self.pos >= len(self.words):
            raise PCParseError(f"Unexpected EOF at word {self.pos}")
        w = self.words[self.pos]
        self.pos += 1
        return w

    def _peek_word(self) -> int:
        """Peek at current word without advancing."""
        if self.pos >= len(self.words):
            return 0
        return self.words[self.pos]

    def _read_xy(self) -> tuple[int, int]:
        """Read an X,Y coordinate pair (one word: left half = X, right half = Y)."""
        w = self._read_word()
        return (int18(left_half(w)), int18(right_half(w)))

    def _read_halves(self) -> tuple[int, int]:
        """Read one word as unsigned (left_half, right_half)."""
        w = self._read_word()
        return (left_half(w), right_half(w))

    def _is_sentinel(self, expected_rh: int | None = None) -> bool:
        """Check if the current word is a sentinel.

        A sentinel has left half = 0 and right half >= 0o400000.
        If expected_rh is given, check for that specific right half value.
        """
        if self.pos >= len(self.words):
            return True
        w = self.words[self.pos]
        lh = left_half(w)
        rh = right_half(w)
        if expected_rh is not None:
            return lh == 0 and rh == expected_rh
        return lh == 0 and rh >= SENTINEL

    def _skip_sentinel(self) -> int:
        """Skip a sentinel word and return its right half value."""
        w = self._read_word()
        return right_half(w)

    # ------------------------------------------------------------------
    # ASCIZ string reading (word-level, matching RSTRZ semantics)
    # ------------------------------------------------------------------

    def _read_asciz(self) -> tuple[str, bool]:
        """Read an ASCIZ string using word-level termination.

        Returns (string, success) where success=False if string was empty
        (first word was zero).
        """
        if self._at_end():
            return ("", False)

        w = self._read_word()
        if w == 0:
            return ("", False)

        chars: list[str] = []
        while True:
            for shift in (29, 22, 15, 8, 1):
                c = (w >> shift) & 0x7F
                if c == 0:
                    break
                chars.append(chr(c))

            # Word terminates when low 8 bits are zero
            if (w & 0o377) == 0:
                break

            if self._at_end():
                break
            w = self._read_word()
            if w == 0:
                break

        return ("".join(chars), True)

    # ------------------------------------------------------------------
    # Section parsers
    # ------------------------------------------------------------------

    def _parse_macros(self) -> None:
        """Parse the macro definitions section.

        Format:
            --------
            !  ASCIZ/MACRO NAME/
            !  BYTE(9)MACRO BODY ENDING WITH 0 BYTE
            --------
            0
        """
        self._dbg(f"Parsing macros at word {self.pos}")

        while not self._at_end():
            name, ok = self._read_asciz()
            if not ok:
                # Zero word — end of macros section
                break

            # Read BYTE(9) macro body — 4 nine-bit bytes per word
            body: list[int] = []
            while not self._at_end():
                w = self._read_word()
                for shift in (27, 18, 9, 0):
                    byte_val = (w >> shift) & 0o777
                    if byte_val == 0:
                        break
                    body.append(byte_val)
                else:
                    continue
                break

            macro = PCMacro(name=name, body=body)
            self.result.macros.append(macro)
            self._dbg(f"  Macro: '{name}' ({len(body)} bytes)")

        self._dbg(f"  Total macros: {len(self.result.macros)}")

    def _parse_bodies(self) -> None:
        """Parse the body placements section.

        Format per dscr.txt:
            --------
            !  LOC OF BODY (X,Y)
            !  ASCIZ STRING NAME OF DIP TYPE
            !  BYTE(6)L(12)N(18)ORIENTATION
            !  XWD BODY BITS, BODY ID
            !  XWD <SPACING * 5 MILS IF 2 PIN DIP>, # OF PINS
            --------
            400000
        """
        self._dbg(f"Parsing bodies at word {self.pos}")

        while not self._at_end():
            if self._is_sentinel(self.SENTINEL_400000):
                self._skip_sentinel()
                break

            # LOC OF BODY (X,Y)
            loc = self._read_xy()

            # ASCIZ STRING NAME OF DIP TYPE
            # In version 0o21, this is always empty (zero word)
            dip_name, _ = self._read_asciz()

            # BYTE(6)L(12)N(18)ORIENTATION
            orient_w = self._read_word()
            dip_lib_index = (orient_w >> 30) & 0o77
            sequence_num = (orient_w >> 18) & 0o7777
            orientation = orient_w & HALF_MASK

            # XWD BODY BITS, BODY ID
            body_bits, body_id = self._read_halves()

            # XWD SPACING, # PINS
            spacing_5mil, num_pins = self._read_halves()

            body = PCBody(
                loc=loc,
                dip_type_name=dip_name,
                dip_lib_index=dip_lib_index,
                sequence_num=sequence_num,
                orientation=orientation,
                body_bits=body_bits,
                body_id=body_id,
                spacing_5mil=spacing_5mil,
                num_pins=num_pins,
            )
            self.result.bodies.append(body)
            self._dbg(f"  Body {body_id}: loc={loc} L={dip_lib_index} "
                       f"N={sequence_num} pins={num_pins} spacing={spacing_5mil}")

        self._dbg(f"  Total bodies: {len(self.result.bodies)}")

    def _parse_points(self, side_name: str) -> list[PCPoint]:
        """Parse a point section (side 1 or side 2).

        Format per dscr.txt:
            --------
            !  LOC OF POINT (X,Y)
            !  POINT ID
            !  --------
            !  !  ID OF A NEIGHBOR
            !  --------
            !  0
            !  XWD BITS, PAD NUMBER
            !  SIZE OF TEXT (0 IF NONE)
            !      X,Y CONSTANT OFFSET FROM POINT LOC
            !      ASCIZ TEXT (IF ANY)
            !  ID OF FEED THROUGH (0 IF NONE)
            --------
            400000
        """
        self._dbg(f"Parsing {side_name} points at word {self.pos}")
        points: list[PCPoint] = []

        while not self._at_end():
            if self._is_sentinel(self.SENTINEL_400000):
                self._skip_sentinel()
                break

            # LOC OF POINT (X,Y)
            loc = self._read_xy()

            # POINT ID (full 36-bit word)
            point_id = self._read_word()

            # Neighbor list (terminated by 0)
            neighbors: list[int] = []
            while not self._at_end():
                w = self._read_word()
                if w == 0:
                    break
                neighbors.append(w)

            # XWD BITS, PAD NUMBER
            bits, pad_type = self._read_halves()

            # SIZE OF TEXT
            text_size_w = self._read_word()
            # The text size is in the left half of the word
            text_size = left_half(text_size_w)

            text_offset = (0, 0)
            text = ""
            if text_size != 0:
                # X,Y CONSTANT OFFSET FROM POINT LOC
                text_offset = self._read_xy()
                # ASCIZ TEXT
                text, _ = self._read_asciz()

            # ID OF FEED THROUGH (0 IF NONE)
            feed_through_id = self._read_word()

            pt = PCPoint(
                loc=loc,
                point_id=point_id,
                neighbors=neighbors,
                bits=bits,
                pad_type=pad_type,
                text_size=text_size,
                text_offset=text_offset,
                text=text,
                feed_through_id=feed_through_id,
            )
            points.append(pt)

        self._dbg(f"  {side_name}: {len(points)} points, "
                   f"{sum(1 for p in points if p.is_feed_through)} feed-throughs, "
                   f"{sum(1 for p in points if p.has_pad)} pads")
        return points

    def _parse_sets(self) -> None:
        """Parse the set centers section.

        Format per dscr.txt:
            --------
            !  LOC OF SET CENTER
            !  --------
            !  !  BODY ID
            !  --------
            !  0
            !  --------
            !  !  POINT ID
            !  --------
            !  0
            --------
            400001   (NOTE: 400001, not 400000!)
        """
        self._dbg(f"Parsing sets at word {self.pos}")

        while not self._at_end():
            if self._is_sentinel(self.SENTINEL_400001):
                self._skip_sentinel()
                break
            # Also handle unexpected 400000 sentinel
            if self._is_sentinel(self.SENTINEL_400000):
                self._warn("Expected 400001 sentinel for sets, got 400000")
                self._skip_sentinel()
                break

            # LOC OF SET CENTER
            loc = self._read_xy()

            # Body IDs (terminated by 0)
            body_ids: list[int] = []
            while not self._at_end():
                w = self._read_word()
                if w == 0:
                    break
                body_ids.append(w)

            # Point IDs (terminated by 0)
            point_ids: list[int] = []
            while not self._at_end():
                w = self._read_word()
                if w == 0:
                    break
                point_ids.append(w)

            sc = PCSetCenter(loc=loc, body_ids=body_ids, point_ids=point_ids)
            self.result.set_centers.append(sc)

        self._dbg(f"  Total sets: {len(self.result.set_centers)}")

    def _parse_trailer(self) -> None:
        """Parse the file trailer.

        Format per dscr.txt:
            ASCIZ BOARD TYPE
            CARD LOCATION  BYTE(4)N(5)L(3)X(6)N(18)0
            CARD FILENAME (FILNAM + EXT,,0 + PPN) or 0 if none
            0
        """
        self._dbg(f"Parsing trailer at word {self.pos}")

        if self._at_end():
            self._warn("No trailer data at end of file")
            return

        # ASCIZ BOARD TYPE
        board_type, _ = self._read_asciz()

        # CARD LOCATION
        card_location = 0
        if not self._at_end():
            card_location = self._read_word()

        # CARD FILENAME — 3-word block or 0
        card_filename = ""
        card_ext = ""
        card_ppn = 0
        if not self._at_end():
            w = self._peek_word()
            if w != 0:
                # FILNAM (SIXBIT, 1 word)
                filnam_w = self._read_word()
                # Decode SIXBIT filename from this word
                card_filename = self._decode_sixbit(filnam_w)
                # EXT,,0 (1 word)
                if not self._at_end():
                    ext_w = self._read_word()
                    card_ext = self._decode_sixbit_half(left_half(ext_w))
                # PPN (1 word)
                if not self._at_end():
                    card_ppn = self._read_word()
            else:
                self._read_word()  # skip the 0

        # Final 0 word
        if not self._at_end():
            self._read_word()

        self.result.card_info = PCCardInfo(
            board_type=board_type,
            card_location=card_location,
            card_filename=card_filename,
            card_ext=card_ext,
            card_ppn=card_ppn,
        )
        self._dbg(f"  Trailer: board_type='{board_type}' "
                   f"card='{card_filename}.{card_ext}'")

    def _decode_sixbit(self, word: int) -> str:
        """Decode a 6-char SIXBIT string from a 36-bit word."""
        chars: list[str] = []
        for shift in (30, 24, 18, 12, 6, 0):
            c = (word >> shift) & 0o77
            if c == 0:
                break
            chars.append(chr(c + 0o40))
        return "".join(chars).rstrip()

    def _decode_sixbit_half(self, half: int) -> str:
        """Decode a 3-char SIXBIT string from an 18-bit halfword."""
        chars: list[str] = []
        for shift in (12, 6, 0):
            c = (half >> shift) & 0o77
            if c == 0:
                break
            chars.append(chr(c + 0o40))
        return "".join(chars).rstrip()

    # ------------------------------------------------------------------
    # Main parse entry point
    # ------------------------------------------------------------------

    def parse(self) -> PCFile:
        """Parse the complete PC file."""
        if len(self.words) < 4:
            raise PCParseError(
                f"File too short: {len(self.words)} words (minimum 4)"
            )

        self._dbg(f"Parsing PC file: {self.source_path} ({len(self.words)} words)")

        # 1. IOVER (version)
        self.result.version = self._read_word()
        self._dbg(f"  Version: {self.result.version} (octal: {oct(self.result.version)})")

        # 2. ASCIZ board/nomenclature type
        board_type, ok = self._read_asciz()
        if ok:
            self.result.board_type = board_type
        self._dbg(f"  Board type: '{self.result.board_type}'")

        # 3. Macros
        self._parse_macros()

        # 4. Body placements
        self._parse_bodies()

        # 5. Side 1 points (component side)
        self.result.side1_points = self._parse_points("Side 1 (component)")

        # 6. Side 2 points (solder side)
        self.result.side2_points = self._parse_points("Side 2 (solder)")

        # 7. Set centers
        self._parse_sets()

        # 8. Trailer
        self._parse_trailer()

        # Validation: check remaining words
        if not self._at_end():
            remaining = self._remaining()
            # Check if remaining words are all zeros (trailing padding)
            non_zero = sum(1 for i in range(self.pos, len(self.words))
                          if self.words[i] != 0)
            if non_zero > 0:
                self._warn(f"{remaining} unparsed words remaining after trailer "
                           f"({non_zero} non-zero)")
            else:
                self._dbg(f"  {remaining} trailing zero-padding words (normal)")

        return self.result


# ============================================================================
# Convenience functions
# ============================================================================

def parse_pc_file(path: str | Path, debug: bool = False) -> PCFile:
    """Parse a PC board layout file from disk."""
    from .unpack import read_file
    words = read_file(str(path))
    parser = PCParser(words, source_path=str(path), debug=debug)
    return parser.parse()


def parse_pc_words(words: list[int], source_path: str = "",
                   debug: bool = False) -> PCFile:
    """Parse a PC board layout file from a pre-loaded word list."""
    parser = PCParser(words, source_path=source_path, debug=debug)
    return parser.parse()
