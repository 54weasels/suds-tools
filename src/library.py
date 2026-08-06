"""Library file loader for SUDS DRW body definitions.

Loads body definitions from library DRW files and indexes them by name.
Supports loading multiple libraries with priority ordering (later files
override earlier ones, inline defs override all).
"""
from typing import Dict, List
from src.drw_model import BodyDefinition
from src.drw_parser import parse_drw_file


def load_library(path: str) -> Dict[str, BodyDefinition]:
    """Load a single DRW library file and return body defs indexed by name."""
    drw = parse_drw_file(path, debug=False)
    return {bd.name: bd for bd in drw.body_defs}


def load_libraries(*paths: str) -> Dict[str, BodyDefinition]:
    """Load multiple DRW library files. Later files override earlier ones."""
    defs: Dict[str, BodyDefinition] = {}
    for path in paths:
        defs.update(load_library(path))
    return defs


def auto_discover_libraries(octal_dir: str) -> List[str]:
    """Auto-discover all library files in the octal directory.

    Returns paths in priority order (general libraries first,
    then supplementary libraries, then large component files).
    """
    import os

    # Known library files in priority order
    LIBRARY_FILES = [
        'lib.drw.O',       # Primary library (252 defs)
        'micro.drw.O',     # Microcode library (119 defs)
        'libold.drw.O',    # Older library (143 defs)
        'libs.drw.O',      # Supplementary (37 defs)
        'ecllib.drw.O',    # ECL library (27 defs)
        'nlib.drw.O',      # New library (7 defs)
        'tnlib.drw.O',     # TN library (7 defs)
        'nlibt.drw.O',     # NL test library (5 defs)
        'lib1.drw.O',      # Library 1 (2 defs)
        'libpal.drw.O',    # PAL library (2 defs)
        '5380.drw.O',      # Large component file with many defs
        'el2003.drw.O',    # Large ECL schematic with defs
        'old.drw.O',       # Older version with defs
    ]

    found = []
    for name in LIBRARY_FILES:
        path = os.path.join(octal_dir, name)
        if os.path.exists(path):
            found.append(path)
    return found


def load_all_defs(octal_dir: str) -> Dict[str, BodyDefinition]:
    """Load ALL available body definitions: DRW libraries + synthetic DIPs.

    This provides maximum body resolution. Priority order:
    1. Synthetic DIP defs (lowest priority, used as fallback)
    2. DRW library file defs (override synthetics)
    """
    from src.dip_generator import get_synthetic_defs

    # Start with synthetic DIPs as fallback
    defs = get_synthetic_defs()

    # Override with real library defs (higher fidelity)
    lib_paths = auto_discover_libraries(octal_dir)
    defs.update(load_libraries(*lib_paths))

    return defs

