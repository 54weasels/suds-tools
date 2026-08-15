"""Unified DIP type lookup aggregating WD, PRT, STF, and DIP library sources.

Provides a single ``get_type(designator)`` interface that the SVG renderer
uses to label components with their real chip part numbers (e.g. 74LS374,
4164, AM9513) instead of internal DIP library codes.

Priority order:
  1. PRT mapping     (from parts list, uses PC-board designator namespace)
  2. WD body name    (from per-sheet wirelist data — schematic namespace)
  3. STF dip_type    (from stuffing file, if available)
  4. DIP library     (internal package codes like 8T97, least specific)

PRT is highest priority because it uses the same designator namespace
as the PC board file (U100, C10, etc.), while WD files use schematic-
local designators (A104, B91) that may differ from the PC layout.
"""

from __future__ import annotations

import glob
import re
from pathlib import Path
from typing import Optional

# SUDS custom alphabet (skips H, I, O, Q).
# SAIL uses 1-based indexing: DECALPH[l for 1].
SUDS_DECALPH = 'ABCDEFGJKLMNPRSTUVWXYZ'


def _loc_from_brsloc(brsloc: int) -> str:
    """Convert a WD body's brsloc field to a designator string."""
    rh = brsloc & 0x3FFFF
    l = (rh >> 12) & 0x3F
    n = rh & 0xFFF
    if 1 <= l <= len(SUDS_DECALPH):
        return SUDS_DECALPH[l - 1] + str(n)
    elif l == 0:
        return ''
    return f'?{l}:{n}'


class DIPTypeMap:
    """Unified designator → chip type lookup.

    Aggregates information from WD files, STF files, and the DIP library
    into a single lookup keyed by component designator (e.g. 'U704').
    """

    def __init__(self) -> None:
        self._prt_map: dict[str, str] = {}
        self._wd_map: dict[str, str] = {}
        self._stf_map: dict[str, str] = {}
        self._dip_lib_map: dict[str, str] = {}

    def add_wd_file(self, wd_file) -> None:
        """Add body data from a parsed WDFile.

        Args:
            wd_file: A parsed WDFile instance from wd_parser.
        """
        for body in wd_file.bodies:
            desig = _loc_from_brsloc(body.brsloc)
            if desig:
                dip_type = body.type_name.rstrip('\\')
                if dip_type:
                    self._wd_map[desig] = dip_type

    def add_prt_data(self, prt_map: dict[str, str]) -> None:
        """Add designator data from a parsed PRT file.

        Args:
            prt_map: Dict mapping designator → dip_type from prt_parser.
        """
        for desig, dip_type in prt_map.items():
            if desig and dip_type:
                self._prt_map[desig] = dip_type

    def add_stf_file(self, stf_file) -> None:
        """Add designator data from a parsed STFFile.

        Args:
            stf_file: A parsed STFFile instance from stf_parser.
        """
        for entry in stf_file.entries:
            if entry.designator and entry.dip_type:
                self._stf_map[entry.designator] = entry.dip_type.rstrip('\\')

    def get_type(self, designator: str) -> str:
        """Look up the chip type for a component designator.

        Returns the most specific type available, checking WD first,
        then STF, then DIP library.  Returns empty string if no data.

        Args:
            designator: Component designator (e.g. 'U704', 'C109').
        """
        return (
            self._prt_map.get(designator, '') or
            self._wd_map.get(designator, '') or
            self._stf_map.get(designator, '') or
            self._dip_lib_map.get(designator, '')
        )

    @property
    def wd_count(self) -> int:
        """Number of designators with WD-sourced types."""
        return len(self._wd_map)

    @property
    def prt_count(self) -> int:
        """Number of designators with PRT-sourced types."""
        return len(self._prt_map)

    @property
    def stf_count(self) -> int:
        """Number of designators with STF-sourced types."""
        return len(self._stf_map)


def build_dip_type_map(
    board_prefix: str,
    octal_dir: str | Path,
    stf_path: str | Path | None = None,
    prt_path: str | Path | None = None,
) -> DIPTypeMap:
    """Build a DIPTypeMap for a board by loading all available data sources.

    Discovers and parses all WD files (e.g. g1.wd.O through g5.wd.O),
    and optionally loads PRT and STF files.

    Args:
        board_prefix: Board name prefix (e.g. 'g', 'qx', 'd', 'ti').
        octal_dir: Path to the octal directory containing .wd.O files.
        stf_path: Optional path to an .stf file.
        prt_path: Optional path to a .prt file (parts list).

    Returns:
        A DIPTypeMap ready for lookup.
    """
    from .wd_parser import parse_wd_file

    dip_map = DIPTypeMap()

    # PRT file (highest priority — uses PC board designators)
    if prt_path:
        from .prt_parser import parse_prt_file
        try:
            prt_map = parse_prt_file(str(prt_path))
            dip_map.add_prt_data(prt_map)
        except Exception:
            pass

    # Discover and parse all WD files for this board
    octal_path = Path(octal_dir)
    wd_pattern = re.compile(
        rf'^{re.escape(board_prefix)}\d+\.wd\.O$', re.IGNORECASE)
    wd_files = sorted(
        p for p in octal_path.iterdir()
        if wd_pattern.match(p.name)
    )

    for wd_path in wd_files:
        try:
            wd = parse_wd_file(wd_path)
            dip_map.add_wd_file(wd)
        except Exception:
            pass  # Skip malformed WD files

    # Add STF as fallback
    if stf_path:
        from .stf_parser import parse_stf_file
        try:
            stf = parse_stf_file(str(stf_path))
            dip_map.add_stf_file(stf)
        except Exception:
            pass

    return dip_map
