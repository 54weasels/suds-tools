"""
crd_model.py — Data model for SUDS CRD (Card Definition) files.

CRD files define the physical characteristics of a printed circuit board
card type: outline shape, edge connector finger positions, and shorting bars.
These are production files referenced by PC board layouts to determine
physical boundaries and connector locations.

Coordinates are in mils (thousandths of an inch).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CRDFinger:
    """An edge connector finger (contact) on one side of the board.

    Each finger is defined by two X,Y endpoints:
      start: the connection end (where the signal meets the board)
      end: the tip end (where the connector inserts)
    The location encoding uses BYTE(6) format matching body location.
    """
    start: tuple[int, int] = (0, 0)      # X,Y start (connection end), mils
    end: tuple[int, int] = (0, 0)        # X,Y end (tip end), mils
    location: int = 0                     # BYTE(6)0,0,0,L,L,N location encoding


@dataclass
class CRDBar:
    """A shorting bar segment on one side of the board.

    Shorting bars connect multiple fingers together electrically
    (typically for ground or power buses on the card edge).
    Each bar is defined by start and end X,Y coordinates.
    """
    start: tuple[int, int] = (0, 0)      # X,Y start of shorting bar, mils
    end: tuple[int, int] = (0, 0)        # X,Y end of shorting bar, mils


@dataclass
class CRDFile:
    """Complete parsed representation of a SUDS CRD card definition file.

    The CRD format is organized in sections separated by FMARK (400000,,0)
    and terminated by CMARK (0,,400000):

    1. Board outline (X,Y polygon)
    2. Front (component side) fingers
    3. Back (solder side) fingers
    4. Front shorting bars
    5. Back shorting bars
    6. Mounting holes and targets (hardware marks)
    """
    # Source info
    source_path: str = ""
    word_count: int = 0
    version: int = 0  # CRDVER (currently 1)

    # Board outline as polygon vertices (X,Y pairs in SUDS units = 0.4 mil)
    outline: list[tuple[int, int]] = field(default_factory=list)

    # Edge connector fingers, by side
    front_fingers: list[CRDFinger] = field(default_factory=list)
    back_fingers: list[CRDFinger] = field(default_factory=list)

    # Shorting bars, by side
    front_bars: list[CRDBar] = field(default_factory=list)
    back_bars: list[CRDBar] = field(default_factory=list)

    # Hardware marks: mounting holes then targets (from CMARK section)
    mounting_holes: list[tuple[int, int]] = field(default_factory=list)
    targets: list[tuple[int, int]] = field(default_factory=list)

    @property
    def total_fingers(self) -> int:
        """Total finger count (front + back)."""
        return len(self.front_fingers) + len(self.back_fingers)

    @property
    def total_bars(self) -> int:
        """Total shorting bar count (front + back)."""
        return len(self.front_bars) + len(self.back_bars)

    @property
    def pc_origin(self) -> tuple[int, int]:
        """PC coordinate origin in CRD space (stored units).

        The PC file coordinate system has its origin at the bottom-left
        mounting hole.  This is defined by lever(0,0) in pcdvi.sai's
        card() function.  Returns (0, 0) if no mounting holes are
        available — meaning PC and CRD share the same origin.
        """
        if self.mounting_holes:
            return self.mounting_holes[0]
        return (0, 0)

    @property
    def board_extents(self) -> tuple[int, int, int, int]:
        """Bounding box of the board outline: (min_x, min_y, max_x, max_y)."""
        if not self.outline:
            return (0, 0, 0, 0)
        xs = [p[0] for p in self.outline]
        ys = [p[1] for p in self.outline]
        return (min(xs), min(ys), max(xs), max(ys))

    @property
    def board_size_mils(self) -> tuple[int, int]:
        """Board width and height in mils."""
        min_x, min_y, max_x, max_y = self.board_extents
        return (max_x - min_x, max_y - min_y)

    @property
    def board_size_inches(self) -> tuple[float, float]:
        """Board width and height in inches."""
        w, h = self.board_size_mils
        return (w / 1000.0, h / 1000.0)

    def summary(self) -> str:
        """Return a human-readable summary of the card definition."""
        w_mils, h_mils = self.board_size_mils
        w_in, h_in = self.board_size_inches
        lines = [
            f"SUDS CRD File: {self.source_path}",
            f"  Words: {self.word_count}",
            f"  Board outline: {len(self.outline)} vertices",
            f"  Board size: {w_mils} x {h_mils} mils ({w_in:.3f}\" x {h_in:.3f}\")",
            f"  Front fingers: {len(self.front_fingers)}",
            f"  Back fingers: {len(self.back_fingers)}",
            f"  Front shorting bars: {len(self.front_bars)}",
            f"  Back shorting bars: {len(self.back_bars)}",
        ]
        return "\n".join(lines)
