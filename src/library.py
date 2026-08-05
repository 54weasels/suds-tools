from typing import Dict, Iterable
from src.drw_model import BodyDefinition
from src.drw_parser import parse_drw_file

def load_library(path: str) -> Dict[str, BodyDefinition]:
    """Load a single DRW library file and return a dictionary of body definitions by name."""
    drw = parse_drw_file(path)
    return {bd.name: bd for bd in drw.body_defs}

def load_libraries(*paths: str) -> Dict[str, BodyDefinition]:
    """Load multiple DRW library files."""
    defs = {}
    for path in paths:
        defs.update(load_library(path))
    return defs
