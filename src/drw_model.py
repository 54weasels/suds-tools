"""
drw_model.py — Data model for SUDS DRW schematic drawing files.

All structures here represent the parsed content of a single DRW file.
Field names and semantics follow the SUDS format specification
(Rich Alderson, 2000; suds.txt) and the reference parser (soap.c, Brad Parker, 2004).

Coordinates are 18-bit signed integers from the PDP-10 word layout.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Property:
    """A named property attached to a body definition, body placement, or signal.

    Properties store text annotations like component values, part numbers, etc.
    """
    value_text: str = ""            # The property value (e.g., "4.7K")
    prop_name_text: str = ""        # The property name (e.g., "VALUE"), empty for text-only
    text_size: int = 0              # Display size (0 = not normally displayed)
    text_loc: tuple[int, int] = (0, 0)        # X,Y location for text display
    xy_const_offset: tuple[int, int] = (0, 0) # Constant offset from parent


@dataclass
class Pin:
    """A pin on a body definition (symbol).

    Pins define the connection points on a schematic symbol.
    """
    loc: tuple[int, int] = (0, 0)   # Pin location relative to body origin
    bits: int = 0                    # Pin attribute bits
    pin_id: int = 0                  # Generated pin ID
    pin_pos: int = 0                 # Pin position indicator
    pin_name: int = 0                # Default pin name (index/number)


@dataclass
class LineSegment:
    """A line segment in a body definition's graphical outline.

    The sequence of line segments defines the schematic symbol shape.
    Low bit of coordinate = pen control:
        0 = draw (visible line to this point)
        1 = move (invisible, pen up, move to this point)
    """
    x: int = 0                      # X coordinate (with pen bit in LSB)
    y: int = 0                      # Y coordinate
    invisible: bool = False          # True = move without drawing

    @property
    def draw_x(self) -> int:
        """X coordinate with pen bit cleared."""
        return self.x & ~1

    @property
    def draw_y(self) -> int:
        """Y coordinate with pen bit cleared."""
        return self.y & ~1


@dataclass
class BodyText:
    """A body text annotation entry (BTEXT format, version < 0o27).

    Used in older DRW versions instead of properties. Each entry
    describes a text annotation placed on the body symbol at a
    specific location.

    Read by RBTEXT in IN.FAI:1054-1119.
    """
    loc: int = 0                     # XY location packed in 36-bit word
    size_info: int = 0               # Char count, line count, text size packed
    const_offset: int = 0            # Constant offset for text placement
    text: str = ""                   # The annotation text (may be garbled for old data)

    @property
    def loc_x(self) -> int:
        """X coordinate (left half of loc word, signed 18-bit)."""
        from .word36 import int18
        return int18((self.loc >> 18) & 0o777777)

    @property
    def loc_y(self) -> int:
        """Y coordinate (right half of loc word, signed 18-bit)."""
        from .word36 import int18
        return int18(self.loc & 0o777777)


@dataclass
class BodyDefinition:
    """A body definition (schematic symbol / component type).

    Body definitions describe the graphical appearance and pin layout
    of a component type (e.g., a 74LS00 quad NAND gate).
    Multiple body placements can reference the same body definition.
    """
    name: str = ""                   # Body definition name (e.g., "74LS00")
    name2: str = ""                  # Secondary name / DIP type (often empty)
    bits: int = 0                    # Body definition attribute bits
    loc_offset: tuple[int, int] = (0, 0)       # DEFOFF: default location offset
    loc_char_offset: tuple[int, int] = (0, 0)  # DEFOF1: char offset (0o400000 = default)
    pins: list[Pin] = field(default_factory=list)
    lines: list[LineSegment] = field(default_factory=list)
    properties: list[Property] = field(default_factory=list)
    btext_entries: list[BodyText] = field(default_factory=list)


@dataclass
class BodyPlacement:
    """An instance of a body definition placed in the drawing.

    Each placement has a position, orientation, and reference designator.
    """
    loc: tuple[int, int] = (0, 0)       # X,Y position on the drawing
    orientation: int = 0                 # Rotation/mirror encoding
    has_location: bool = False           # True if CARD LOC field follows orientation
    card_body_loc: int = 0              # Card location encoding (slot, position)
    xy_const_offset: tuple[int, int] = (0, 0)  # Constant offset for location text
    xy_char_offset: tuple[int, int] = (0, 0)   # Character offset for location text
    body_bits: int = 0                   # Body instance attribute bits
    body_id: int = 0                     # Generated body ID
    body_name: str = ""                  # Reference to BodyDefinition.name
    properties: list[Property] = field(default_factory=list)

    @property
    def rotation(self) -> int:
        """Extract rotation from orientation field (0, 1, 2, 3 = 0°, 90°, 180°, 270°)."""
        return self.orientation & 0x3

    @property
    def mirrored(self) -> bool:
        """Extract mirror flag from orientation field."""
        return bool(self.orientation & 0x4)


@dataclass
class Point:
    """A connection point (wiring node) in the drawing.

    Points form a connectivity graph via their up/down/left/right links.
    Each point has an X,Y location and an ID that is either:
    - A simple sequential ID (for standalone wire points)
    - A compound <PIN_ID,,BODY_ID> (for pins on components)
    """
    loc: tuple[int, int] = (0, 0)       # X,Y position
    point_id: tuple[int, int] = (0, 0)  # (left_half, right_half) of ID word
    down: tuple[int, int] = (0, 0)      # ID of point below (0,0 if none)
    up: tuple[int, int] = (0, 0)        # ID of point above
    left: tuple[int, int] = (0, 0)      # ID of point to left
    right: tuple[int, int] = (0, 0)     # ID of point to right
    bits: int = 0                        # Point attribute bits
    pin_name: int = 0                    # Pin name index
    text_size: tuple[int, int] = (0, 0)  # Text size (if non-zero, text follows)
    xy_const_offset: tuple[int, int] = (0, 0)  # Text offset from point location
    name: str = ""                       # Signal/pin name text
    io_loc: tuple[int, int] = (0, 0)    # I/O pin location (if CPIN bit set)
    io_offset: tuple[int, int] = (0, 0) # I/O constant offset (if CPIN bit set)

    @property
    def is_pin(self) -> bool:
        """True if this point is a component pin (has a body ID)."""
        return self.point_id[0] != 0

    @property
    def body_id(self) -> int:
        """Body ID this pin belongs to (right half of point ID)."""
        return self.point_id[1]

    @property
    def has_connections(self) -> bool:
        """True if this point connects to any neighbor."""
        return (self.down != (0, 0) or self.up != (0, 0) or
                self.left != (0, 0) or self.right != (0, 0))


@dataclass
class SetCenter:
    """A set center groups related bodies and points together.

    Used for organizing related components on a schematic page.
    """
    loc: tuple[int, int] = (0, 0)
    body_ids: list[tuple[int, int]] = field(default_factory=list)
    point_ids: list[tuple[int, int]] = field(default_factory=list)


@dataclass
class Trailer:
    """Title block information for the drawing."""
    drawn_by: str = ""
    title_line_1: str = ""
    title_line_2: str = ""
    card_loc: int = 0               # Card location for whole drawing
    revision: str = ""
    module: str = ""
    variable: str = ""
    prefix: str = ""
    project: str = ""
    page: str = ""
    of_string: str = ""             # "of N" page count
    drawing_code: str = ""
    site_line_1: str = ""
    site_line_2: str = ""
    next_higher_assy: str = ""
    drawn_by_filespec: str = ""     # Filespec or literal (if starts with ")
    checked_by_filespec: str = ""
    engineered_by_filespec: str = ""


@dataclass
class Macro:
    """A named macro definition."""
    name: str = ""
    body: list[int] = field(default_factory=list)  # 9-bit encoded macro body


@dataclass
class ExtraPart:
    """An extra part declaration (BOM items not in the schematic)."""
    description: str = ""
    part_number: str = ""
    instances: list[tuple[int, int]] = field(default_factory=list)  # (count, location)


@dataclass
class Signal:
    """A named signal with optional properties."""
    name: str = ""
    prop_name: str = ""
    prop_value: str = ""


@dataclass
class LibraryRef:
    """A reference to a library file."""
    filespec: str = ""
    bits: int = 0


@dataclass
class DRWFile:
    """Complete parsed representation of a SUDS DRW drawing file."""
    # Source info
    source_path: str = ""
    word_count: int = 0

    # Header
    version: int = 0
    nomenclature_type: str = ""
    board_type: str = ""

    # Referenced types and libraries
    type_names: list[str] = field(default_factory=list)
    library_refs: list[LibraryRef] = field(default_factory=list)

    # Drawing content
    body_defs: list[BodyDefinition] = field(default_factory=list)
    macros: list[Macro] = field(default_factory=list)
    body_placements: list[BodyPlacement] = field(default_factory=list)
    points: list[Point] = field(default_factory=list)
    set_centers: list[SetCenter] = field(default_factory=list)

    # Metadata
    trailer: Optional[Trailer] = None

    # Extra data sections
    extra_parts: list[ExtraPart] = field(default_factory=list)
    signals: list[Signal] = field(default_factory=list)
    dip_filespecs: list[str] = field(default_factory=list)
    wire_rule_filespecs: list[str] = field(default_factory=list)

    # Parse diagnostics
    parse_warnings: list[str] = field(default_factory=list)

    def summary(self) -> str:
        """Return a human-readable summary of the file."""
        lines = [
            f"SUDS DRW File: {self.source_path}",
            f"  Version: {self.version}",
            f"  Nomenclature: {self.nomenclature_type}",
            f"  Board type: {self.board_type}",
            f"  Words: {self.word_count}",
            f"  Type names: {len(self.type_names)}",
            f"  Library refs: {len(self.library_refs)}",
            f"  Body definitions: {len(self.body_defs)}",
            f"  Macros: {len(self.macros)}",
            f"  Body placements: {len(self.body_placements)}",
            f"  Points: {len(self.points)}",
            f"  Set centers: {len(self.set_centers)}",
            f"  Signals: {len(self.signals)}",
            f"  Extra parts: {len(self.extra_parts)}",
        ]
        if self.trailer:
            lines.append(f"  Title: {self.trailer.title_line_1}")
            lines.append(f"  Drawn by: {self.trailer.drawn_by}")
            lines.append(f"  Project: {self.trailer.project}")
            lines.append(f"  Page: {self.trailer.page} of {self.trailer.of_string}")
        if self.parse_warnings:
            lines.append(f"  Warnings: {len(self.parse_warnings)}")
            for w in self.parse_warnings[:5]:
                lines.append(f"    - {w}")
        return "\n".join(lines)
