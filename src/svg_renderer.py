"""SVG renderer for SUDS DRW schematic files.

Converts a parsed DRWFile into an SVG document. Handles:
- Body definition symbol rendering (IC outlines, pin dots)
- Body placement with orientation transforms (rotation + mirror)
- Wire routing from point connectivity graph
- Signal/pin name labels
- Title block from trailer
"""
import xml.etree.ElementTree as ET
from typing import Dict, Optional
from src.drw_model import (DRWFile, BodyDefinition, BodyPlacement,
                           Point, Property, Trailer)

# --- Styling constants ---
BODY_STROKE = "#333333"
BODY_STROKE_W = "0.5"
WIRE_STROKE = "#1a5fb4"
WIRE_STROKE_W = "0.7"
PIN_FILL = "#333333"
PIN_R = "0.8"
JUNCTION_FILL = "#1a5fb4"
JUNCTION_R = "1.2"
TEXT_FONT = "'Courier New', monospace"
LABEL_COLOR = "#555555"
SIGNAL_COLOR = "#1a5fb4"
REFDES_COLOR = "#000000"
TITLE_COLOR = "#000000"
BG_COLOR = "#ffffff"
PADDING = 40


def _clean_text(s: str) -> str:
    """Strip non-printable chars and leading/trailing whitespace."""
    return ''.join(c for c in s.strip() if ord(c) >= 32)


def _text_size_px(text_size) -> float:
    """Convert SUDS text_size to SVG font-size in drawing units."""
    if isinstance(text_size, tuple):
        sz = text_size[1] if text_size[1] else text_size[0]
    elif isinstance(text_size, int):
        sz = text_size
    else:
        sz = 0
    # SUDS text sizes are small integers (typically 1-3).
    # Map to readable SVG sizes in the coordinate space.
    if sz <= 0:
        return 0  # don't render
    return max(2.5, sz * 2.5)


def _make_symbol(defs_el: ET.Element, name: str, bd: BodyDefinition):
    """Create an SVG <symbol> for a body definition."""
    safe_id = name.replace('\\', '_').replace('*', '_').replace('.', '_')
    sym = ET.SubElement(defs_el, 'symbol', id=f"bd_{safe_id}", overflow="visible")

    # --- Lines (IC outline / symbol shape) ---
    if bd.lines:
        parts = []
        for i, seg in enumerate(bd.lines):
            x, y = seg.draw_x, seg.draw_y
            if i == 0 or seg.invisible:
                parts.append(f"M{x},{y}")
            else:
                parts.append(f"L{x},{y}")
        path = ET.SubElement(sym, 'path', d=" ".join(parts))
        path.set('stroke', BODY_STROKE)
        path.set('stroke-width', BODY_STROKE_W)
        path.set('fill', 'none')

    # --- Pin dots ---
    for pin in bd.pins:
        px, py = pin.loc
        ET.SubElement(sym, 'circle',
                      cx=str(px), cy=str(py),
                      r=PIN_R, fill=PIN_FILL)

    # --- Body-level property text ---
    for prop in bd.properties:
        text_val = _clean_text(prop.value_text)
        if not text_val:
            continue
        sz = _text_size_px(prop.text_size)
        if sz <= 0:
            continue  # hidden property (text_size=0)
        tx, ty = prop.text_loc
        # Text needs to be un-flipped since we're inside a scale(1,-1) context
        txt = ET.SubElement(sym, 'text',
                            x=str(tx), y=str(-ty),
                            fill=LABEL_COLOR)
        txt.set('font-family', TEXT_FONT)
        txt.set('font-size', f"{sz}px")
        txt.set('transform', 'scale(1,-1)')
        txt.text = text_val

    return safe_id


def _orientation_transform(bp: BodyPlacement) -> str:
    """Build SVG transform string for a body placement.

    Orientation encoding (from IN.FAI):
    - 0o400000 bit: has_location flag (not rotation)
    - Bits 0-1: rotation (0=0°, 1=90°CCW, 2=180°, 3=270°CCW)
    - Bit 2: mirror (horizontal flip)
    """
    x, y = bp.loc
    rot_val = bp.orientation & 0x3
    mirror = bool(bp.orientation & 0x4)
    rot_deg = rot_val * 90

    parts = [f"translate({x},{y})"]
    if rot_deg:
        parts.append(f"rotate({rot_deg})")
    if mirror:
        parts.append("scale(-1,1)")
    return " ".join(parts)


def render_svg(drw: DRWFile,
               library: Optional[Dict[str, BodyDefinition]] = None) -> str:
    """Render a DRW file to an SVG string.

    Args:
        drw: Parsed DRW file
        library: Dict of body definition name -> BodyDefinition from library files

    Returns:
        SVG document as a string
    """
    if library is None:
        library = {}

    # Build combined body def index (inline defs override library)
    all_defs: Dict[str, BodyDefinition] = {}
    all_defs.update(library)
    for bd in drw.body_defs:
        all_defs[bd.name] = bd

    # --- SVG root ---
    root = ET.Element('svg')
    root.set('xmlns', 'http://www.w3.org/2000/svg')

    # --- <defs> with body symbols ---
    defs_el = ET.SubElement(root, 'defs')

    # Only create symbols for body defs that are actually USED
    used_names = {bp.body_name for bp in drw.body_placements}
    symbol_ids: Dict[str, str] = {}  # body_name -> safe SVG id
    for name in used_names:
        if name in all_defs:
            safe_id = _make_symbol(defs_el, name, all_defs[name])
            symbol_ids[name] = safe_id

    # --- Compute bounding box ---
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    def expand(x, y):
        nonlocal min_x, max_x, min_y, max_y
        if x < min_x: min_x = x
        if x > max_x: max_x = x
        if y < min_y: min_y = y
        if y > max_y: max_y = y

    for p in drw.points:
        expand(p.loc[0], p.loc[1])

    for bp in drw.body_placements:
        bx, by = bp.loc
        expand(bx, by)
        # Expand by body def extents
        if bp.body_name in all_defs:
            bd = all_defs[bp.body_name]
            for seg in bd.lines:
                expand(bx + seg.draw_x, by + seg.draw_y)
            for pin in bd.pins:
                expand(bx + pin.loc[0], by + pin.loc[1])

    if min_x == float('inf'):
        min_x, max_x, min_y, max_y = 0, 100, 0, 100

    min_x -= PADDING
    max_x += PADDING
    min_y -= PADDING
    max_y += PADDING
    width = max_x - min_x
    height = max_y - min_y

    # viewBox: Y-flip → negate Y and swap min/max
    root.set('viewBox', f"{min_x} {-max_y} {width} {height}")
    root.set('width', '100%')
    root.set('height', '100%')

    # Main group with Y-flip
    g = ET.SubElement(root, 'g', transform="scale(1,-1)")

    # Background
    ET.SubElement(g, 'rect',
                  x=str(min_x), y=str(min_y),
                  width=str(width), height=str(height),
                  fill=BG_COLOR)

    # --- Body placements ---
    g_bodies = ET.SubElement(g, 'g', id="bodies")
    for bp in drw.body_placements:
        if bp.body_name not in symbol_ids:
            continue
        xform = _orientation_transform(bp)
        use = ET.SubElement(g_bodies, 'use')
        use.set('href', f"#bd_{symbol_ids[bp.body_name]}")
        use.set('transform', xform)

    # --- Placement property text (ref des, values) ---
    g_labels = ET.SubElement(g, 'g', id="labels")
    for bp in drw.body_placements:
        for prop in bp.properties:
            text_val = _clean_text(prop.value_text)
            if not text_val:
                continue
            sz = _text_size_px(prop.text_size)
            if sz <= 0:
                continue
            # Property text_loc is relative to the placement
            tx = bp.loc[0] + prop.text_loc[0]
            ty = bp.loc[1] + prop.text_loc[1]
            txt = ET.SubElement(g_labels, 'text',
                                x=str(tx), y=str(-ty),
                                fill=REFDES_COLOR)
            txt.set('font-family', TEXT_FONT)
            txt.set('font-size', f"{sz}px")
            txt.set('transform', 'scale(1,-1)')
            txt.text = text_val

    # --- Wiring ---
    g_wires = ET.SubElement(g, 'g', id="wires")
    g_junctions = ET.SubElement(g, 'g', id="junctions")

    points_by_id = {p.point_id: p for p in drw.points}
    ZERO = (0, 0)

    for pt in drw.points:
        x1, y1 = pt.loc
        neighbor_count = 0
        for n_id in (pt.up, pt.down, pt.left, pt.right):
            if n_id == ZERO:
                continue
            n_pt = points_by_id.get(n_id)
            if n_pt is None:
                continue
            neighbor_count += 1
            # Draw wire only once: from lower ID to higher ID
            if pt.point_id < n_id:
                x2, y2 = n_pt.loc
                wire = ET.SubElement(g_wires, 'line',
                                    x1=str(x1), y1=str(y1),
                                    x2=str(x2), y2=str(y2))
                wire.set('stroke', WIRE_STROKE)
                wire.set('stroke-width', WIRE_STROKE_W)

        # Junction dot at 3+ connections
        if neighbor_count >= 3:
            ET.SubElement(g_junctions, 'circle',
                          cx=str(x1), cy=str(y1),
                          r=JUNCTION_R, fill=JUNCTION_FILL)

    # --- Signal/pin name labels ---
    g_signals = ET.SubElement(g, 'g', id="signals")
    for pt in drw.points:
        if not pt.name:
            continue
        name_val = _clean_text(pt.name)
        if not name_val:
            continue
        x, y = pt.loc
        # Offset text slightly from the point
        ox, oy = pt.xy_const_offset if pt.xy_const_offset != (0, 0) else (2, 1)
        txt = ET.SubElement(g_signals, 'text',
                            x=str(x + ox), y=str(-(y + oy)),
                            fill=SIGNAL_COLOR)
        txt.set('font-family', TEXT_FONT)
        txt.set('font-size', '2.5px')
        txt.set('transform', 'scale(1,-1)')
        txt.text = name_val

    # --- Title block ---
    if drw.trailer:
        _render_title_block(g, drw.trailer, min_x, min_y, width)

    # Serialize
    ET.indent(root, space='  ')
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode')


def _render_title_block(g: ET.Element, trailer: Trailer,
                        min_x: float, min_y: float, width: float):
    """Render the title block in the lower-left corner."""
    g_title = ET.SubElement(g, 'g', id="title_block")

    title = f"{trailer.title_line_1}"
    if trailer.title_line_2:
        title += f" — {trailer.title_line_2}"

    lines = []
    if title.strip():
        lines.append(title.strip())
    if trailer.revision:
        lines.append(f"Rev: {trailer.revision}")
    if trailer.page:
        page_str = f"Page {trailer.page}"
        if trailer.of_string:
            page_str += f" of {trailer.of_string}"
        lines.append(page_str)
    if trailer.drawn_by:
        lines.append(f"Drawn by: {trailer.drawn_by}")

    base_y = min_y + 8
    for i, line in enumerate(lines):
        ty = base_y + i * 6
        txt = ET.SubElement(g_title, 'text',
                            x=str(min_x + 10), y=str(-ty),
                            fill=TITLE_COLOR)
        txt.set('font-family', TEXT_FONT)
        txt.set('font-size', '4px')
        txt.set('transform', 'scale(1,-1)')
        txt.text = line
