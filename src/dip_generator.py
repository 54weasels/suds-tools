"""Generate synthetic body definitions for standard DIP IC packages.

When a DRW file references a body that isn't in any library, we can
synthesize a basic DIP outline based on the pin count from the DIPS
database. This gives us a generic IC rectangle with pin dots at the
correct positions instead of nothing at all.

Pin count data extracted from DIPS.LSD[LIB,DRW] in the SAILDART archive.
"""
from dataclasses import dataclass, field
from src.drw_model import BodyDefinition, Pin, LineSegment, Property

# Pin count database from DIPS.LSD[LIB,DRW] (SAILDART archive)
# Maps component name → pin count
DIP_PIN_COUNTS = {
    # ALS series (Advanced Low-power Schottky)
    'ALS00': 14, 'ALS00\\': 14, 'ALS02': 14, 'ALS02\\': 14,
    'ALS04': 14, 'ALS04\\': 14, 'ALS08': 14, 'ALS08\\': 14,
    'ALS10': 14, 'ALS11': 14, 'ALS20': 14, 'ALS27': 14,
    'ALS30': 14, 'ALS32': 14, 'ALS32\\': 14, 'ALS74': 14,
    'ALS86': 14,
    'ALS138': 16, 'ALS157': 16, 'ALS158': 16, 'ALS163': 16,
    'ALS257': 16, 'ALS258': 16,
    'ALS244': 20, 'ALS2441': 20, 'ALS245': 20,
    'ALS273': 20, 'ALS373': 20, 'ALS374': 20, 'ALS534': 20,
    # FAST series
    'F00': 14, 'F02': 14, 'F04': 14, 'F04\\': 14,
    'F08': 14, 'F10': 14, 'F11': 14, 'F20': 14, 'F32': 14,
    'F74': 14, 'F86': 14,
    'F138': 16, 'F157': 16, 'F158': 16, 'F163': 16,
    'F240': 20, 'F240.': 20, 'F241': 20, 'F244': 20, 'F245': 20,
    'F253': 16, 'F257': 16, 'F258': 16,
    'F273': 20, 'F373': 20, 'F374': 20, 'F381': 20,
    # LS series
    'LS00': 14, 'LS02': 14, 'LS04': 14, 'LS08': 14, 'LS10': 14,
    'LS20': 14, 'LS27': 14, 'LS30': 14, 'LS32': 14, 'LS74': 14,
    'LS86': 14,
    'LS138': 16, 'LS139': 16, 'LS153': 16, 'LS157': 16,
    'LS158': 16, 'LS163': 16, 'LS174': 16, 'LS175': 16,
    'LS240': 20, 'LS240.': 20, 'LS244': 20, 'LS245': 20,
    'LS273': 20, 'LS373': 20, 'LS374': 20,
    # Processors
    '68000': 64, '68010': 64, '68020': 128, '68881': 68,
    '8031': 40, '8080': 40, '8748': 40, '82586': 48,
    # Memory / special
    '8308': 20, 'VRAM': 28, 'S10.T': 20,
    # Passives
    'DIODE': 16, 'RT': 2, 'LM385': 2,
    # Connectors
    'J.2': 2, 'J.4': 4, 'J.6': 6, 'J.8': 8, 'J.10': 10,
    'J.12': 12, 'J.14': 14, 'J.16': 16, 'J.20': 20,
    'J.26': 26, 'J.32': 32, 'J.36': 36, 'J.40': 40,
    'J.50': 50, 'J.60': 60,
}


def make_dip_body(name: str, pin_count: int) -> BodyDefinition:
    """Create a synthetic DIP body definition with standard dimensions.

    DIP pin spacing: 8 units between pins vertically
    DIP body width: 24 units (12 from center to edge)
    """
    bd = BodyDefinition()
    bd.name = name

    if pin_count <= 2:
        # Simple 2-pin component (resistor, cap, diode, LED)
        bd.pins = [
            Pin(loc=(0, 8)),
            Pin(loc=(0, -8)),
        ]
        bd.lines = [
            LineSegment(x=0, y=6, invisible=False),
            LineSegment(x=0, y=-6, invisible=False),
        ]
        return bd

    # Standard DIP layout
    half_w = 12  # Half-width of body
    pin_spacing = 8
    pins_per_side = pin_count // 2
    half_h = (pins_per_side - 1) * pin_spacing // 2

    # Create outline rectangle
    bd.lines = [
        LineSegment(x=-half_w, y=-half_h - 4, invisible=False),
        LineSegment(x=half_w, y=-half_h - 4, invisible=False),
        LineSegment(x=half_w, y=half_h + 4, invisible=False),
        LineSegment(x=-half_w, y=half_h + 4, invisible=False),
        LineSegment(x=-half_w, y=-half_h - 4, invisible=False),
    ]

    # Create pins: left side bottom-to-top, right side top-to-bottom
    bd.pins = []
    for i in range(pins_per_side):
        y = -half_h + i * pin_spacing
        bd.pins.append(Pin(loc=(-half_w, y)))   # Left side

    for i in range(pins_per_side):
        y = half_h - i * pin_spacing
        bd.pins.append(Pin(loc=(half_w, y)))    # Right side

    return bd


def get_synthetic_defs() -> dict[str, BodyDefinition]:
    """Generate synthetic body definitions for all known DIP packages."""
    defs = {}
    for name, pin_count in DIP_PIN_COUNTS.items():
        defs[name] = make_dip_body(name, pin_count)
    return defs


def guess_pin_count(name: str) -> int | None:
    """Try to guess pin count from component name patterns."""
    # Check database first
    if name in DIP_PIN_COUNTS:
        return DIP_PIN_COUNTS[name]

    # Strip trailing backslash (inverted output marker)
    clean = name.rstrip('\\')
    if clean in DIP_PIN_COUNTS:
        return DIP_PIN_COUNTS[clean]

    # Try common prefixes
    import re
    # 74-series: base part number determines pin count
    m = re.match(r'(?:74)?(?:LS|ALS|F|S|AS|HC|HCT)?(\d+)', clean)
    if m:
        base = m.group(1)
        # Look up base part number
        for prefix in ['74LS', '74F', '74S', '74ALS', '74', 'ALS', 'F', 'LS']:
            key = prefix + base
            if key in DIP_PIN_COUNTS:
                return DIP_PIN_COUNTS[key]

    return None
