"""
drw_parser.py — Parse SUDS DRW files into a structured data model.

CRITICAL DESIGN NOTE:
  SUDS DRW files are structured as streams of 18-bit HALFWORDS, not full
  36-bit words. Each 36-bit PDP-10 word contains two halfwords:
    word = (left_half << 18) | right_half

  String encodings (7-bit ASCIZ, 6-bit SIXBIT) pack characters across
  halfword boundaries, not word boundaries. The reference parser soap.c
  stores the entire file as an array of 18-bit unsigned ints (up[])
  and indexes by halfword position.

  Our parser converts the 36-bit word array to a halfword array internally
  to match this behavior exactly.

Reference documents:
  - suds.txt (Rich Alderson, 2000) — format specification
  - soap.c (Brad Parker, 2004) — reference parser
  - IN.FAI, CLOSE.FAI (DRAW source) — authoritative PDP-10 implementation
"""

from __future__ import annotations

import logging
from pathlib import Path

from .word36 import left_half, right_half, int18, SENTINEL, HALF_MASK
from .drw_model import (
    DRWFile, BodyDefinition, BodyText, Pin, LineSegment, Property,
    BodyPlacement, Point, SetCenter, Trailer, Macro,
    ExtraPart, Signal, LibraryRef,
)

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Raised on unrecoverable parse errors."""
    pass


class HalfwordStream:
    """A stream of 18-bit halfwords extracted from 36-bit PDP-10 words.

    This mirrors soap.c's `unsigned int *up` array. Two halfwords per word:
      up[2*n]   = left_half(word[n])
      up[2*n+1] = right_half(word[n])

    String reading functions (grab_7bit_ascii, grab_6bit_ascii) operate
    at the halfword level, matching soap.c exactly.
    """

    def __init__(self, words: list[int]):
        self.up: list[int] = []
        for w in words:
            self.up.append(left_half(w))
            self.up.append(right_half(w))
        self.size = len(self.up)
        self.p = 0  # Current halfword position

    def at_end(self) -> bool:
        return self.p >= self.size

    def remaining(self) -> int:
        return self.size - self.p

    def peek(self) -> int:
        """Peek at current halfword."""
        if self.p >= self.size:
            return 0
        return self.up[self.p]

    def peek2(self) -> tuple[int, int]:
        """Peek at current halfword pair (one 36-bit word)."""
        lh = self.up[self.p] if self.p < self.size else 0
        rh = self.up[self.p + 1] if self.p + 1 < self.size else 0
        return (lh, rh)

    def read_hw(self) -> int:
        """Read one halfword and advance."""
        if self.p >= self.size:
            raise ParseError(f"EOF at halfword {self.p}")
        v = self.up[self.p]
        self.p += 1
        return v

    def read_word(self) -> tuple[int, int]:
        """Read a halfword pair (one 36-bit word). Returns (left, right)."""
        lh = self.read_hw()
        rh = self.read_hw()
        return (lh, rh)

    def read_full_word(self) -> int:
        """Read a halfword pair and return as a single 36-bit int."""
        lh, rh = self.read_word()
        return (lh << 18) | rh

    def read_signed_hw(self) -> int:
        """Read one halfword as a signed 18-bit integer."""
        return int18(self.read_hw())

    def read_xy(self) -> tuple[int, int]:
        """Read an X,Y coordinate pair (two signed halfwords = one word)."""
        x = self.read_signed_hw()
        y = self.read_signed_hw()
        return (x, y)

    def check_zero_word(self) -> bool:
        """Check if next word (two halfwords) is zero."""
        if self.p + 1 >= self.size:
            return True
        return self.up[self.p] == 0 and self.up[self.p + 1] == 0

    def check_sentinel_word(self) -> bool:
        """Check if next word is the sentinel (0,,400000)."""
        if self.p + 1 >= self.size:
            return True
        return self.up[self.p] == 0 and self.up[self.p + 1] == SENTINEL

    def skip_zero_word(self) -> bool:
        """If next word is zero, skip it (advance by 2 halfwords)."""
        if self.check_zero_word():
            self.p += 2
            return True
        return False

    def skip_sentinel_word(self) -> bool:
        """If next word is sentinel, skip it."""
        if self.check_sentinel_word():
            self.p += 2
            return True
        return False

    # ------------------------------------------------------------------
    # String reading — PDP-10 authoritative RSTRZ (IN.FAI:3161-3175)
    # ------------------------------------------------------------------

    def rstrz(self) -> tuple[str, bool]:
        """Read a 7-bit ASCIZ string using PDP-10 RSTRZ word-level semantics.

        Matches IN.FAI:3161-3175 exactly:
        1. Read first full word. If zero → return ("", False) (empty/failure).
        2. Otherwise, decode 7-bit characters from the word.
        3. Check if word's low 8 bits are zero → string done (success).
        4. Read next word. If zero → done. If non-zero, decode and repeat.

        Returns:
            (text, success): The decoded string and whether it was non-empty.
            success=False means the string was empty (first word was zero),
            which in RSTRZ corresponds to the CPOPJ (no-skip) return.
        """
        if self.p + 1 >= self.size:
            raise ParseError(f"EOF at halfword {self.p}")

        # Read first word
        w = self.read_full_word()
        if w == 0:
            # JUMPE TTT,CPOPJ — empty string
            return ("", False)

        # Non-empty: read words and decode 7-bit chars
        chars: list[str] = []
        while True:
            # Extract 5 characters from the 36-bit word (bits 35-1)
            for shift in (29, 22, 15, 8, 1):
                c = (w >> shift) & 0x7F
                if c == 0:
                    # NUL character — stop decoding this word's chars
                    # but the WORD-level termination is what matters below
                    break
                chars.append(chr(c))

            # TRNN TTT,377: check if low 8 bits are zero → string terminated
            if (w & 0o377) == 0:
                break

            # Read next word
            if self.p + 1 >= self.size:
                break
            w = self.read_full_word()

            # JUMPN TTT,RS1: if word is zero, string ended (padding)
            if w == 0:
                break

        return ("".join(chars), True)

    # ------------------------------------------------------------------
    # String reading — soap.c compatible (byte-level, kept for non-body sections)
    # ------------------------------------------------------------------

    def grab_7bit_ascii(self) -> str:
        """Read a 7-bit ASCIZ string from the halfword stream.

        Exact port of soap.c grab_7bit_ascii(). Characters are packed
        5 per 36-bit word (spanning two halfwords), with a NUL terminator.
        After reading, position is aligned to the next word boundary.
        """
        result: list[str] = []
        state = 0
        off = self.p

        while off < self.size:
            if state == 0:
                c = self.up[off] >> 11
            elif state == 1:
                c = self.up[off] >> 4
            elif state == 2:
                c = ((self.up[off] & 0xF) << 3)
                if off + 1 < self.size:
                    c |= (self.up[off + 1] >> 15) & 7
                off += 1
            elif state == 3:
                c = self.up[off] >> 8
            elif state == 4:
                c = self.up[off] >> 1
                off += 1
                state = -1

            c &= 0x7F
            state += 1

            if c == 0:
                break
            result.append(chr(c))

        # Alignment: advance past partially consumed halfword, then word-align
        if state > 0 and state < 3:
            off += 1
        if off & 1:
            off += 1

        self.p = off
        return "".join(result)

    def grab_6bit_ascii(self) -> str:
        """Read a 6-bit (SIXBIT) encoded string from the halfword stream.

        Exact port of soap.c grab_6bit_ascii(). Characters are packed
        3 per halfword (6 per word). Code 0 terminates.
        Character value = sixbit_code + 0o40 (space).
        """
        result: list[str] = []
        state = 0
        off = self.p

        while off < self.size:
            if state == 0:
                c = self.up[off] >> 12
            elif state == 1:
                c = self.up[off] >> 6
            elif state == 2:
                c = self.up[off]
                off += 1
                state = -1

            c &= 0o77
            state += 1

            if c == 0:
                break
            result.append(chr(c + 0o40))

        if state > 0 and state < 3:
            off += 1
        if off & 1:
            off += 1

        self.p = off
        return "".join(result)

    def grab_9bit(self) -> list[int]:
        """Read a sequence of 9-bit values from the halfword stream.

        Used for macro bodies. Two 9-bit values per halfword pair.
        Terminated by a zero byte.
        """
        result: list[int] = []
        state = 0
        off = self.p

        while off < self.size:
            if state == 0:
                c = self.up[off] >> 9
            elif state == 1:
                c = self.up[off]
                off += 1
                state = -1

            c &= 0o777
            state += 1

            if c == 0:
                break
            result.append(c)

        if state == 1:
            off += 1
        if off & 1:
            off += 1

        self.p = off
        return result

    def read_sixbit_word(self) -> str:
        """Read one 36-bit SIXBIT word (6 characters from 2 halfwords).

        SIXBIT encodes 6 characters per word, 6 bits each.
        Character value = sixbit_code + 0o40 (space).
        Code 0 means padding (ignored).
        """
        lh = self.read_hw()
        rh = self.read_hw()
        chars: list[str] = []
        for half in (lh, rh):
            c = (half >> 12) & 0o77
            if c:
                chars.append(chr(c + 0o40))
            c = (half >> 6) & 0o77
            if c:
                chars.append(chr(c + 0o40))
            c = half & 0o77
            if c:
                chars.append(chr(c + 0o40))
        return ''.join(chars)


class DRWParser:
    """Parse a SUDS DRW file from a list of 36-bit words."""

    def __init__(self, words: list[int], source_path: str = "",
                 debug: bool = False):
        self.stream = HalfwordStream(words)
        self.source_path = source_path
        self.debug = debug
        self.result = DRWFile(
            source_path=source_path,
            word_count=len(words),
        )

    def _warn(self, msg: str):
        full_msg = f"[hw {self.stream.p}] {msg}"
        logger.warning(full_msg)
        self.result.parse_warnings.append(full_msg)

    def _dbg(self, msg: str):
        if self.debug:
            print(f"  [p={self.stream.p}] {msg}")

    # ------------------------------------------------------------------
    # Header sub-parsers
    # ------------------------------------------------------------------

    def _looks_like_sixbit_filespec(self) -> bool:
        """Check if data at current position looks like a SIXBIT filespec.

        Library filespecs are 3-word SIXBIT blocks: NAME, EXT, PPN.
        The extension (2nd word) is always 'DRW' or 'DRW0' in this archive.

        We use the extension word as the primary discriminator because:
        - Both SIXBIT filenames and 7-bit type names can start with
          uppercase letters, making the first word ambiguous.
        - The extension 'DRW' is unambiguous — type name data in this
          position would decode as random SIXBIT chars, not 'DRW'.
        """
        s = self.stream
        if s.p + 5 >= s.size:
            return False

        # Decode the 2nd word (extension position) as SIXBIT
        ext_lh, ext_rh = s.up[s.p + 2], s.up[s.p + 3]
        ext_chars: list[str] = []
        for half in (ext_lh, ext_rh):
            c = (half >> 12) & 0o77
            if c:
                ext_chars.append(chr(c + 0o40))
            c = (half >> 6) & 0o77
            if c:
                ext_chars.append(chr(c + 0o40))
            c = half & 0o77
            if c:
                ext_chars.append(chr(c + 0o40))
        ext = ''.join(ext_chars)

        # Check extension starts with 'DRW' (case-insensitive)
        return ext.upper().startswith('DRW')

    def _read_library_filespecs(self):
        """Read library filespecs as 3-word SIXBIT blocks.

        Each entry: NAME (6-char SIXBIT), EXT (6-char SIXBIT),
                    PPN (6-char SIXBIT encoding [proj,prog]).
        Terminated when the first word of a block is zero.
        """
        s = self.stream
        while not s.at_end():
            if s.check_zero_word():
                s.p += 2
                break
            name = s.read_sixbit_word()
            ext = s.read_sixbit_word()
            ppn = s.read_sixbit_word()
            filespec = name
            if ext:
                filespec += '.' + ext
            if ppn:
                filespec += '[' + ppn + ']'
            ref = LibraryRef(filespec=filespec)
            self.result.library_refs.append(ref)
            self._dbg(f"  lib_ref: '{filespec}'")

    def _read_type_names_and_filespecs(self):
        """Read type names and library filespecs, auto-detecting order.

        The canonical format (version >= 13) has:
        1. Used library type names (7-bit ASCIZ, zero-terminated)
        2. Library filespecs (3-word SIXBIT blocks, zero-terminated)

        Some files omit section 1 entirely and start with SIXBIT filespecs.
        We detect this by checking encoding at the current position.
        """
        s = self.stream

        if s.at_end():
            return

        # Case 1: zero word — empty type names, check what follows
        if s.check_zero_word():
            s.p += 2
            self._dbg("  type_names: (empty)")

            # After empty type names, check for filespecs
            if not s.at_end() and not s.check_zero_word():
                if self._looks_like_sixbit_filespec():
                    self._read_library_filespecs()
                    return
                # else: not SIXBIT — next section (body defs) starts
            elif not s.at_end():
                # Another zero word — empty filespecs too
                s.p += 2
                self._dbg("  lib_refs: (empty)")
            return

        # Case 2: non-zero data — is it SIXBIT filespecs or 7-bit names?
        if self._looks_like_sixbit_filespec():
            # SIXBIT filespecs come first (no type names section)
            self._dbg("  type_names: (absent)")
            self._read_library_filespecs()
            return

        # Case 3: 7-bit type names, then filespecs
        while not s.at_end():
            if s.check_zero_word():
                s.p += 2
                break
            name = s.grab_7bit_ascii()
            if name:
                self.result.type_names.append(name)
                self._dbg(f"  type_name: '{name}'")

        # Now read library filespecs
        if not s.at_end():
            if s.check_zero_word():
                # Empty filespecs
                s.p += 2
                self._dbg("  lib_refs: (empty)")
            elif self._looks_like_sixbit_filespec():
                self._read_library_filespecs()
            # else: no filespecs section (body defs start)

    # ------------------------------------------------------------------
    # Section parsers
    # ------------------------------------------------------------------

    def _parse_header(self):
        """Parse header: version, nomenclature, board type, type names, lib filespecs."""
        s = self.stream
        self._dbg("parse_header")

        # Version number is in up[1] (right half of first word)
        s.read_hw()  # skip up[0] (left half, unused)
        self.result.version = s.read_hw()  # up[1]

        # Nomenclature type (7-bit ASCIZ)
        self.result.nomenclature_type, _ = s.rstrz()

        # Board type (7-bit ASCIZ)
        self.result.board_type, _ = s.rstrz()

        self._dbg(f"version={self.result.version}, "
                  f"nom='{self.result.nomenclature_type}', "
                  f"board='{self.result.board_type}'")

        # --- Type names and library filespecs ---
        # Per IN.FAI (version >= 13): used-library-type-names (zero-term),
        # then library filespecs as 3-word SIXBIT blocks (zero-term).
        #
        # HOWEVER: some files omit the type-names zero-word terminator and
        # jump straight to SIXBIT filespecs. We detect this by checking
        # whether the data at the current position is SIXBIT or 7-bit ASCIZ.

        self._read_type_names_and_filespecs()

    def _parse_property(self) -> Property:
        """Parse a single property record."""
        s = self.stream
        prop = Property()
        prop.value_text = s.grab_7bit_ascii()
        prop.prop_name_text = s.grab_7bit_ascii()
        # TEXT SIZE: soap.c reads up[p+1] (right half of word)
        s.read_hw()  # skip left half
        prop.text_size = s.read_hw()
        # Text location (X, Y)
        prop.text_loc = s.read_xy()
        # Constant offset (X, Y)
        prop.xy_const_offset = s.read_xy()
        return prop

    def _parse_body_defs(self):
        """Parse body definitions (component symbols).

        Implements RDTYPX from IN.FAI:915-1200. Uses word-level RSTRZ
        for string reading and correct version-gated field reading.

        Version gates (constants are OCTAL as in the assembly source):
          - DIP type string: 0o10 <= RDVER < 0o27   (IN.FAI:922-926)
          - BITS word:       RDVER >= 0o13           (IN.FAI:933)
          - DEFOFF word:     RDVER >= 0o12           (IN.FAI:938)
          - DEFOF1 word:     RDVER > 0o23            (IN.FAI:942, CAILE)
          - Pin format v2:   RDVER >= 0o17           (IN.FAI:960, NWPND1)
          - BTEXT format:    RDVER < 0o23            (IN.FAI:1051, CAIL C,23)
          - PROPIN format:   RDVER >= 0o23           (via JRST RBTXTN)

        Note: 0o23 = 19 decimal. Version 21 (0o25) >= 19 → uses PROPIN.
        """
        s = self.stream
        ver = self.result.version
        self._dbg("parse_body_defs")

        while not s.at_end():
            # RDTYPX: RSTRZ reads type name. Empty (zero word) = end.
            name, ok = s.rstrz()
            if not ok:
                # Zero word: end of body definitions
                break

            bd = BodyDefinition()
            bd.name = name
            self._dbg(f"  body_def: '{bd.name}'")

            # DIP type string (IN.FAI:922-928): 0o10 <= ver < 0o23
            # CAIGE TT,10 + CAIL TT,23 + JRST ISTYPN
            if 0o10 <= ver < 0o23:
                bd.name2, _ = s.rstrz()

            # BITS word (IN.FAI:933-937): ver >= 0o13
            if ver >= 0o13:
                bits_word = s.read_full_word()
                # TLZ TTT,FOUNDL!DTMP1 clears mark bits in left half
                bd.bits = (bits_word >> 18) & 0o777777  # left half = bits

            # DEFOFF word (IN.FAI:938-939): ver >= 0o12
            if ver >= 0o12:
                defoff = s.read_full_word()
                bd.loc_offset = (int18((defoff >> 18) & 0o777777),
                                 int18(defoff & 0o777777))

            # DEFOF1 word (IN.FAI:942-944): ver > 0o23
            if ver > 0o23:
                defof1 = s.read_full_word()
                bd.loc_char_offset = (int18((defof1 >> 18) & 0o777777),
                                      int18(defof1 & 0o777777))

            # --- Pins (IN.FAI:947-1036, sentinel-terminated) ---
            # For ver >= 0o17 (NWPND1): 3 words per pin (LOC, ID/bits, name/pos)
            while not s.at_end():
                loc_word = s.read_full_word()
                if loc_word == 0o400000:
                    break  # CAIN TTT,400000
                pin = Pin()
                pin.loc = (int18((loc_word >> 18) & 0o777777),
                           int18(loc_word & 0o777777))
                if ver >= 0o17:
                    # NWPND1: read ID/bits word, then name/pos word
                    id_word = s.read_full_word()
                    pin.bits = (id_word >> 18) & 0o777777
                    pin.pin_id = id_word & 0o777777
                    name_word = s.read_full_word()
                    pin.pin_pos = (name_word >> 18) & 0o777777
                    pin.pin_name = name_word & 0o777777
                else:
                    # Older format: 2 additional words with different packing
                    w2 = s.read_full_word()
                    pin.bits = (w2 >> 18) & 0o777777
                    pin.pin_id = w2 & 0o777777
                bd.pins.append(pin)

            # --- Lines (IN.FAI:1040-1048, sentinel-terminated) ---
            while not s.at_end():
                loc_word = s.read_full_word()
                if loc_word == 0o400000:
                    break
                x_raw = (loc_word >> 18) & 0o777777
                y_raw = loc_word & 0o777777
                invisible = bool(y_raw & 1)
                seg = LineSegment(x=int18(x_raw), y=int18(y_raw),
                                  invisible=invisible)
                bd.lines.append(seg)

            # --- BTEXT or Properties (IN.FAI:1049-1144) ---
            # CAIL C,23: if ver < 0o23 (19), use BTEXT; else PROPIN
            if ver < 0o23:
                # BTEXT format (IN.FAI:1054-1119): sentinel-terminated
                self._parse_btext(bd, ver)
            else:
                # PROPIN format (IN.FAI:1121-1144): RSTRZ-terminated
                self._parse_propin(bd)

            self.result.body_defs.append(bd)

    def _parse_btext(self, bd: BodyDefinition, ver: int):
        """Parse BTEXT entries for body definition (version < 0o27).

        Implements RBTEXT loop from IN.FAI:1054-1119:
        1. WORDIN → LOC (XY packed). If 0o400000 → done.
        2. WORDIN → SIZE_INFO (char/line counts + text size).
        3. WORDIN → CONST_OFFSET (if ver > 3).
        4. RSTRZ → TEXT string. If fails (empty), entry is discarded.
        """
        s = self.stream
        while not s.at_end():
            loc = s.read_full_word()
            if loc == 0o400000:
                break  # CAIN TTT,400000 → BTXTDN

            size_info = s.read_full_word()

            if ver > 3:
                const_offset = s.read_full_word()
            else:
                const_offset = 0

            text, ok = s.rstrz()
            if not ok:
                # RSTRZ failure: entry discarded (IN.FAI:1108-1113)
                continue

            bt = BodyText(loc=loc, size_info=size_info,
                          const_offset=const_offset, text=text)
            bd.btext_entries.append(bt)

    def _parse_propin(self, bd: BodyDefinition):
        """Parse PROPIN property entries for body definition (version >= 0o27).

        Implements PROPIN from IN.FAI:1124-1144:
        1. RSTRZ → property value. If fails → done (end of properties).
        2. RSTRZ → property name.
        3. WORDIN → info word 1 (text size / flags).
        4. WORDIN → info word 2 (text location XY).
        5. WORDIN → info word 3 (constant offset XY).
        """
        s = self.stream
        while not s.at_end():
            value, ok = s.rstrz()
            if not ok:
                break

            name, _ = s.rstrz()

            w1 = s.read_full_word()
            w2 = s.read_full_word()
            w3 = s.read_full_word()

            prop = Property(
                value_text=value,
                prop_name_text=name,
                text_size=w1 & 0o777777,
                text_loc=(int18((w2 >> 18) & 0o777777),
                          int18(w2 & 0o777777)),
                xy_const_offset=(int18((w3 >> 18) & 0o777777),
                                 int18(w3 & 0o777777)),
            )
            bd.properties.append(prop)

    def _parse_macros(self):
        """Parse macro definitions."""
        s = self.stream
        self._dbg("parse_macros")

        while not s.at_end():
            if s.check_zero_word():
                s.p += 2
                break

            macro = Macro()
            macro.name = s.grab_7bit_ascii()
            macro.body = s.grab_9bit()
            self.result.macros.append(macro)
            self._dbg(f"  macro: '{macro.name}'")

    def _parse_body_placements(self):
        """Parse body placements (component instances).

        Implements RDBOD from IN.FAI:1324-1586.

        The orientation word is read as a full word at IN.FAI:1338.
        TRNN TT,400000 (IN.FAI:1349) tests bit 17 of the RIGHT HALF:
          - If set: location fields (LETTER, NUMBER, NUMBR1) follow
          - If clear: skip directly to NNFORM (BITS/ID)
        """
        s = self.stream
        ver = self.result.version
        self._dbg("parse_body_placements")

        while not s.at_end():
            if s.check_sentinel_word():
                s.p += 2
                break

            bp = BodyPlacement()

            # Location of body (X, Y) — IN.FAI:1324
            bp.loc = s.read_xy()

            # Orientation word — IN.FAI:1338
            orient_lh = s.read_hw()
            orient_rh = s.read_hw()
            bp.orientation = orient_rh

            # TRNN TT,400000 — IN.FAI:1349: test bit 17 of RH for location data
            if orient_rh & 0o400000:
                bp.has_location = True

                # LNNEWS (IN.FAI:3770-3773): WORDIN → LETTER, WORDIN → NUMBER
                # For version ≥ 7, just two words:
                #   LETTER: card/body location info
                #   NUMBER: constant offset XY
                bp.card_body_loc = s.read_full_word()   # LETTER
                bp.xy_const_offset = s.read_xy()        # NUMBER (X,Y)

                # NUMBR1 — IN.FAI:1355-1357: only for version > 0o23 (19 decimal)
                # CAILE A,23 / PUSHJ P,WORDIN — skip WORDIN if version ≤ 19
                if ver > 0o23:
                    s.read_full_word()  # NUMBR1
            else:
                bp.has_location = False

            # BODY BITS ,, BODY ID — IN.FAI:1370-1374
            bp.body_bits = s.read_hw()
            bp.body_id = s.read_hw()

            # Name of body definition — IN.FAI:1384
            bp.body_name = s.grab_7bit_ascii()

            self._dbg(f"  body: '{bp.body_name}' id={bp.body_id} "
                      f"loc=({bp.loc[0]},{bp.loc[1]}) orient={bp.orientation}")

            # Properties — IN.FAI:1404-1405 (PROPIN, zero-word terminated)
            if ver >= 0o23:
                while not s.at_end():
                    if s.check_zero_word():
                        s.p += 2
                        break
                    prop = self._parse_property()
                    bp.properties.append(prop)

            self.result.body_placements.append(bp)

    def _parse_points(self):
        """Parse connection points (wiring nodes).

        CRITICAL: The bits field is a COMPOUND BITFIELD, not an enumeration!
        Individual bits have independent meanings (from WLFST.FAI / LOWCOR.FAN):

            ISPIN   = 0o200000  This point is a pin
            FIXTXT  = 0o040000  Fixing text offset
            FIXRHT  = 0o020000  When fixing, move line right
            FIXCON  = 0o010000  Fix connector to text
            CPNBTS  = 0o006000  Terminator rule bits (CPINS only)
            DEFPIN  = 0o004000  Defaulted pin name (WD output)
            CPIN    = 0o001000  Connector pin (I/O pin)

        Variable-length data after the base record:
        1. IF text_size (right half) != 0:
               Read constant_offset, ASCIZ string
        2. IF CPIN bit (0o1000) is set:
               Read CPIN location, CPIN constant offset
        
        These conditions are INDEPENDENT — both can be true simultaneously.
        """
        s = self.stream
        self._dbg("parse_points")

        CPIN = 0o1000    # Connector pin bit

        while not s.at_end():
            if s.check_sentinel_word():
                s.p += 2
                break

            pnt = Point()

            # Location (X, Y)
            pnt.loc = s.read_xy()

            # Point ID
            pnt.point_id = (s.read_hw(), s.read_hw())

            # Neighbor IDs: down, up, left, right
            pnt.down = (s.read_hw(), s.read_hw())
            pnt.up = (s.read_hw(), s.read_hw())
            pnt.left = (s.read_hw(), s.read_hw())
            pnt.right = (s.read_hw(), s.read_hw())

            # BITS ,, PIN NAME
            pnt.bits = s.read_hw()
            pnt.pin_name = s.read_hw()

            # SIZE OF TEXT — the right half is the actual text size
            tsz_word = s.read_word()
            pnt.text_size = tsz_word

            # 1. Text data: if text size (right half) is non-zero
            if tsz_word[1] != 0:
                pnt.xy_const_offset = s.read_xy()
                pnt.name = s.grab_7bit_ascii()

            # 2. CPIN data: if CPIN bit is set in bits field
            if pnt.bits & CPIN:
                pnt.io_loc = s.read_xy()
                pnt.io_offset = s.read_xy()

            self.result.points.append(pnt)

    def _parse_set_centers(self):
        """Parse set center groupings."""
        s = self.stream
        self._dbg("parse_set_centers")

        while not s.at_end():
            if s.check_sentinel_word():
                s.p += 2
                break

            sc = SetCenter()
            sc.loc = s.read_xy()

            # Body IDs (terminated by zero word)
            while not s.at_end():
                if s.check_zero_word():
                    s.p += 2
                    break
                sc.body_ids.append((s.read_hw(), s.read_hw()))

            # Point IDs (terminated by zero word)
            while not s.at_end():
                if s.check_zero_word():
                    s.p += 2
                    break
                sc.point_ids.append((s.read_hw(), s.read_hw()))

            self.result.set_centers.append(sc)

    def _parse_trailer(self):
        """Parse the complete trailer (title block) — all 18 fields."""
        s = self.stream
        self._dbg("parse_trailer")

        t = Trailer()

        def _safe_str() -> str:
            if s.at_end():
                return ""
            return s.grab_7bit_ascii()

        t.drawn_by = _safe_str()
        t.title_line_1 = _safe_str()
        t.title_line_2 = _safe_str()

        # Card location (one full word)
        if not s.at_end():
            t.card_loc = s.read_full_word()

        t.revision = _safe_str()
        t.module = _safe_str()
        t.variable = _safe_str()
        t.prefix = _safe_str()
        t.project = _safe_str()
        t.page = _safe_str()
        t.of_string = _safe_str()
        t.drawing_code = _safe_str()
        t.site_line_1 = _safe_str()
        t.site_line_2 = _safe_str()
        t.next_higher_assy = _safe_str()
        t.drawn_by_filespec = _safe_str()
        t.checked_by_filespec = _safe_str()
        t.engineered_by_filespec = _safe_str()

        self.result.trailer = t
        self._dbg(f"  trailer: title='{t.title_line_1}' by='{t.drawn_by}' "
                  f"project='{t.project}' page='{t.page} of {t.of_string}'")

    def _parse_extra_parts(self):
        """Parse extra parts declarations."""
        s = self.stream
        self._dbg("parse_extra_parts")

        while not s.at_end():
            if s.check_zero_word():
                s.p += 2
                break
            ep = ExtraPart()
            ep.description = s.grab_7bit_ascii()
            ep.part_number = s.grab_7bit_ascii()
            while not s.at_end():
                if s.check_zero_word():
                    s.p += 2
                    break
                count = s.read_hw()
                loc = s.read_hw()
                ep.instances.append((count, loc))
            self.result.extra_parts.append(ep)

    def _parse_signals(self):
        """Parse signal name declarations."""
        s = self.stream
        self._dbg("parse_signals")

        while not s.at_end():
            if s.check_zero_word():
                s.p += 2
                break
            sig = Signal()
            sig.name = s.grab_7bit_ascii()
            sig.prop_name = s.grab_7bit_ascii()
            sig.prop_value = s.grab_7bit_ascii()
            self.result.signals.append(sig)

    def _parse_dip_filespecs(self):
        """Parse DIP definition filespecs."""
        s = self.stream
        self._dbg("parse_dip_filespecs")

        while not s.at_end():
            if s.check_zero_word():
                s.p += 2
                break
            fs = s.grab_7bit_ascii()
            self.result.dip_filespecs.append(fs)

    def _parse_wire_rule_filespecs(self):
        """Parse wire rule check filespecs."""
        s = self.stream
        self._dbg("parse_wire_rule_filespecs")

        while not s.at_end():
            if s.check_zero_word():
                s.p += 2
                break
            fs = s.grab_7bit_ascii()
            self.result.wire_rule_filespecs.append(fs)

    # ------------------------------------------------------------------
    # Main parse entry point
    # ------------------------------------------------------------------

    def parse(self) -> DRWFile:
        """Parse the complete DRW file."""
        if len(self.stream.up) == 0:
            self._warn("Empty file")
            return self.result

        try:
            self._parse_header()
        except ParseError as e:
            self._warn(f"Header parse error: {e}")
            return self.result

        # Body defs, macros, body placements, and points are the core
        # sections. If any section fails, attempt to recover by scanning
        # for the next section's delimiter.
        try:
            self._parse_body_defs()
        except ParseError as e:
            self._warn(f"Body defs parse error at hw {self.stream.p}: {e}")
            self._recover_to_next_section()

        try:
            self._parse_macros()
        except ParseError as e:
            self._warn(f"Macros parse error at hw {self.stream.p}: {e}")
            self._recover_to_next_section()

        try:
            self._parse_body_placements()
        except ParseError as e:
            self._warn(f"Body placements parse error at hw {self.stream.p}: {e}")
            self._recover_to_next_section()

        try:
            self._parse_points()
        except ParseError as e:
            self._warn(f"Points parse error at hw {self.stream.p}: {e}")
            self._recover_to_next_section()

        try:
            self._parse_set_centers()
            self._parse_trailer()

            # Post-trailer optional sections
            if not self.stream.at_end():
                self._parse_extra_parts()
            if not self.stream.at_end():
                self._parse_signals()
            if not self.stream.at_end():
                self._parse_dip_filespecs()
            if not self.stream.at_end():
                self._parse_wire_rule_filespecs()
        except ParseError as e:
            self._warn(f"Post-placement parse error: {e}")
        except Exception as e:
            self._warn(f"Unexpected error at hw {self.stream.p}: {e}")

        remaining = self.stream.remaining()
        if remaining > 0:
            all_zeros = all(
                self.stream.up[i] == 0
                for i in range(self.stream.p, self.stream.size)
            )
            if not all_zeros:
                self._warn(f"Unparsed non-zero data: {remaining} "
                          f"halfwords remaining at position "
                          f"{self.stream.p}")

        return self.result

    def _recover_to_next_section(self):
        """Attempt to recover stream position after a section parse error.

        Scans forward through the halfword stream looking for the
        pattern that starts the next expected section. The DRW file
        format has sections delimited by sentinel words (0,,400000)
        and zero words (0,,0). After a desync, we look for a sequence
        of two consecutive zero words (which typically separates body
        defs → macros → body placements sections) or a sentinel
        followed by reasonable-looking data.
        """
        s = self.stream
        # Scan for a plausible section boundary: look for patterns
        # like two consecutive zero words or a sentinel followed by data.
        original_p = s.p
        best_p = s.size  # default: give up at end

        for i in range(s.p, min(s.size - 3, s.p + 10000)):
            # Pattern: zero word, then zero word (empty section + start)
            if (s.up[i] == 0 and s.up[i + 1] == 0 and
                    s.up[i + 2] == 0 and s.up[i + 3] == 0):
                # Two consecutive zero words — could be section boundary
                # But need to check if this is within a data area
                # Use heuristic: after two zero words, is there non-zero data?
                look_ahead = i + 4
                while look_ahead < s.size and s.up[look_ahead] == 0:
                    look_ahead += 1
                if look_ahead < s.size:
                    best_p = i
                    break

        if best_p < s.size:
            self._dbg(f"  recovery: jumping from p={original_p} to p={best_p}")
            s.p = best_p


# ============================================================================
# Convenience functions
# ============================================================================

def parse_drw_file(path: str | Path, debug: bool = False) -> DRWFile:
    """Parse a DRW file from disk."""
    from .unpack import read_file
    words = read_file(str(path))
    parser = DRWParser(words, source_path=str(path), debug=debug)
    return parser.parse()


def parse_drw_words(words: list[int], source_path: str = "",
                    debug: bool = False) -> DRWFile:
    """Parse a DRW file from a pre-loaded word list."""
    parser = DRWParser(words, source_path=source_path, debug=debug)
    return parser.parse()
