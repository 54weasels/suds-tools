"""
pc_model.py — Data model for SUDS PC board layout files.

All structures here represent the parsed content of a single PC file.
Field names and semantics follow the SUDS format specification.

Coordinates are 18-bit signed integers from the PDP-10 word layout.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PCMacro:
    """A named macro definition (same format as DRW macros)."""
    name: str = ""
    body: list[int] = field(default_factory=list)  # 9-bit encoded macro body


@dataclass
class PCBody:
    """A DIP component placement on the PC board.
    
    Unlike DRW body definitions, PC bodies do not carry symbol graphics.
    They are DIP references identified by the L field in the orientation
    word, which indexes into the DIP library (DIPS.DIP).
    """
    loc: tuple[int, int] = (0, 0)       # X,Y position in mils
    dip_type_name: str = ""             # ASCIZ DIP type (empty in version 0o21)
    dip_lib_index: int = 0              # L field from BYTE(6)L(12)N(18)ORIENT
    sequence_num: int = 0               # N field from orientation word
    orientation: int = 0                 # Rotation (18-bit field)
    body_bits: int = 0                   # Body attribute bits
    body_id: int = 0                     # Generated body ID
    spacing_5mil: int = 0                # Pin spacing * 5 mils (for 2-pin DIPs)
    num_pins: int = 0                    # Number of pins on this DIP


@dataclass
class PCPoint:
    """A trace point, pad, or via on one side of the PC board.
    
    Points form a connectivity graph via their variable-length neighbor
    lists. Each point has an X,Y location, a pad type, and optionally
    links to a feed-through point on the other board side.
    
    Point ID is either a generated sequential number or
    XWD PIN_ID, BODY_ID for DIP pins.
    """
    loc: tuple[int, int] = (0, 0)       # X,Y position in mils
    point_id: int = 0                    # Point ID (full 36-bit word)
    neighbors: list[int] = field(default_factory=list)  # IDs of connected neighbor points
    bits: int = 0                        # Point attribute bits (left half of bits word)
    pad_type: int = 0                    # Pad type number (right half of bits word)
                                         #   0=none, 1=standard DIP, 2=clearance, 3=pin-1 square
    text_size: int = 0                   # Text size (0 if no text)
    text_offset: tuple[int, int] = (0, 0)  # X,Y text offset (if text_size != 0)
    text: str = ""                       # Text annotation (if text_size != 0)
    feed_through_id: int = 0             # ID of corresponding point on other side (0 if none)

    @property
    def is_pin(self) -> bool:
        """True if this is a DIP pin (has a body ID in upper half)."""
        return (self.point_id >> 18) != 0
    
    @property
    def pin_id(self) -> int:
        """Pin ID (left half of point_id)."""
        return (self.point_id >> 18) & 0o777777
    
    @property
    def body_id(self) -> int:
        """Body ID (right half of point_id), only valid when is_pin is True."""
        return self.point_id & 0o777777
    
    @property
    def is_feed_through(self) -> bool:
        """True if this point has a feed-through to the other side."""
        return self.feed_through_id != 0
    
    @property
    def has_pad(self) -> bool:
        """True if this point has a physical pad."""
        return self.pad_type != 0
    
    @property
    def plane_connections(self) -> list[int]:
        """Inner plane numbers this point connects to (from bits).
        Plane 0=GND, 1=VCC, 2=power2, 3=power3.
        Encoded in bits as flags."""
        # TODO: The exact bit positions need to be verified from the PC source.
        # We don't hallucinate bit layouts without verification.
        planes = []
        # Example logic, pending actual bit layout verification:
        # for i in range(4):
        #     if self.bits & (1 << i):
        #         planes.append(i)
        return planes


@dataclass
class PCSetCenter:
    """A set center groups related bodies and points together."""
    loc: tuple[int, int] = (0, 0)
    body_ids: list[int] = field(default_factory=list)
    point_ids: list[int] = field(default_factory=list)


@dataclass
class PCCardInfo:
    """Board metadata from the PC file trailer."""
    board_type: str = ""                 # ASCIZ board type (e.g., "DECPC")
    card_location: int = 0               # Card location word BYTE(4)N(5)L(3)X(6)N(18)0
    card_filename: str = ""              # Card definition filename (or empty)
    card_ext: str = ""                   # Card definition extension
    card_ppn: int = 0                    # Card definition PPN


@dataclass
class PCDiagnostic:
    """A parse-time or analysis diagnostic."""
    severity: str = 'info'               # 'error', 'warning', 'info'
    category: str = 'format'             # 'format', 'connectivity', 'drc', 'netlist'
    message: str = ""
    word_offset: int = -1                # Word offset in file where issue occurred
    location: tuple[int, int] | None = None  # X,Y if applicable


@dataclass
class PCFile:
    """Complete parsed representation of a SUDS PC board layout file."""
    # Source info
    source_path: str = ""
    word_count: int = 0
    
    # Header
    version: int = 0
    board_type: str = ""                 # Nomenclature/board type from header (e.g., "DECPC")
    
    # Content
    macros: list[PCMacro] = field(default_factory=list)
    bodies: list[PCBody] = field(default_factory=list)
    side1_points: list[PCPoint] = field(default_factory=list)  # Component side
    side2_points: list[PCPoint] = field(default_factory=list)  # Solder side
    set_centers: list[PCSetCenter] = field(default_factory=list)
    
    # Trailer
    card_info: Optional[PCCardInfo] = None
    
    # Diagnostics
    diagnostics: list[PCDiagnostic] = field(default_factory=list)
    
    @property
    def all_points(self) -> list[PCPoint]:
        """All points from both sides."""
        return self.side1_points + self.side2_points

    @property
    def feed_through_pairs(self) -> list[tuple[int, int]]:
        """List of (side1_id, side2_id) feed-through pairs."""
        pairs = []
        for pt in self.side1_points:
            if pt.is_feed_through:
                pairs.append((pt.point_id, pt.feed_through_id))
        return pairs

    @property
    def pin_points(self) -> list[PCPoint]:
        """All points that are DIP pins."""
        return [pt for pt in self.all_points if pt.is_pin]

    @property
    def trace_points(self) -> list[PCPoint]:
        """All points that are trace junction points (not pins)."""
        return [pt for pt in self.all_points if not pt.is_pin]

    def summary(self) -> str:
        """Return a human-readable summary of the file."""
        num_feed_throughs = len(self.feed_through_pairs)
        num_pads = sum(1 for pt in self.all_points if pt.has_pad)
        num_text = sum(1 for pt in self.all_points if pt.text_size != 0)
        
        lines = [
            f"SUDS PC File: {self.source_path}",
            f"  Version: {self.version}",
            f"  Board type: {self.board_type}",
            f"  Words: {self.word_count}",
            f"  Macros: {len(self.macros)}",
            f"  Bodies: {len(self.bodies)}",
            f"  Side 1 points: {len(self.side1_points)}",
            f"  Side 2 points: {len(self.side2_points)}",
            f"  Set centers: {len(self.set_centers)}",
            f"  DIP pins: {len(self.pin_points)}",
            f"  Trace points: {len(self.trace_points)}",
            f"  Feed-throughs: {num_feed_throughs}",
            f"  Pads: {num_pads}",
            f"  Text annotations: {num_text}",
        ]
        
        if self.card_info:
            lines.append(f"  Card type: {self.card_info.board_type}")
            if self.card_info.card_filename:
                lines.append(f"  Card definition: {self.card_info.card_filename}.{self.card_info.card_ext}")
                
        errors = [d for d in self.diagnostics if d.severity == 'error']
        warnings = [d for d in self.diagnostics if d.severity == 'warning']
        
        if errors or warnings:
            lines.append(f"  Diagnostics: {len(errors)} errors, {len(warnings)} warnings")
            for d in (errors + warnings)[:5]:
                lines.append(f"    - [{d.severity.upper()}] {d.message}")
                
        return "\n".join(lines)
