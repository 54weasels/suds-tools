"""SVG renderer for SUDS DRW schematic files.

Converts a parsed DRWFile into an SVG document. Handles:
- Body definition symbol rendering (IC outlines, pin dots, pin numbers)
- Body placement with orientation transforms (rotation + mirror)
- Wire routing from point connectivity graph
- Signal/pin name labels
- Title block from trailer
- Drawing border frame

Coordinate system notes:
- SUDS uses a 12.5 mil grid (1 unit = 0.0125 inches)
- DIP pin spacing = 8 units = 100 mils (standard)
- Text size 1 ≈ 6 units tall (75 mils, standard schematic text)
- The SVG uses a Y-flip (scale(1,-1)) to match screen coordinates

Reference: Calibrated against original SUDS plotter output (harscn PNGs)
to match text sizing, line weights, and overall appearance.
"""
import xml.etree.ElementTree as ET
from typing import Dict, Optional
from src.drw_model import (DRWFile, BodyDefinition, BodyPlacement,
                           Point, Property, Trailer)

# --- Styling constants ---
# Matched to original SUDS plotter output appearance
BODY_STROKE = "#000000"
BODY_STROKE_W = "0.8"
WIRE_STROKE = "#000000"
WIRE_STROKE_W = "0.8"
PIN_FILL = "#000000"
PIN_R = "0.6"
JUNCTION_FILL = "#000000"
JUNCTION_R = "1.0"
TEXT_FONT = "'Courier New', monospace"
LABEL_COLOR = "#000000"
SIGNAL_COLOR = "#000000"
REFDES_COLOR = "#000000"
PIN_NUM_COLOR = "#000000"
TITLE_COLOR = "#000000"
BG_COLOR = "#ffffff"
BORDER_STROKE = "#000000"
BORDER_STROKE_W = "1.0"
PADDING = 20

# Text size scaling: SUDS text_size=1 → ~5 drawing units tall
# Calibrated to match the original plotter where text fits cleanly
# inside standard 24-unit wide DIP body outlines.
TEXT_SCALE = 4.0  # multiplier: text_size * TEXT_SCALE = font-size in drawing units

# Pin number text is slightly smaller than body/signal text
PIN_NUM_FONT_SIZE = 3.0  # drawing units


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
    if sz <= 0:
        return 0  # don't render
    return max(4.0, sz * TEXT_SCALE)


def _make_text(parent: ET.Element, x: float, y: float, text: str,
               font_size: str, fill: str,
               anchor: str = 'start',
               baseline: str = 'auto') -> ET.Element:
    """Create a text element with Y-flip compensation.

    All text in the drawing lives inside a scale(1,-1) group, so we
    must negate Y and add a local scale(1,-1) to un-flip the glyphs.
    """
    txt = ET.SubElement(parent, 'text',
                        x=str(x), y=str(-y))
    txt.set('fill', fill)
    txt.set('font-family', TEXT_FONT)
    txt.set('font-size', font_size)
    txt.set('text-anchor', anchor)
    if baseline != 'auto':
        txt.set('dominant-baseline', baseline)
    txt.set('transform', 'scale(1,-1)')
    txt.text = text
    return txt


def _body_box(bd: BodyDefinition):
    """Compute bounding box of body's line segments.

    Returns (min_x, max_x, min_y, max_y) or None if no lines.
    """
    if not bd.lines:
        return None
    xs = [s.draw_x for s in bd.lines]
    ys = [s.draw_y for s in bd.lines]
    return (min(xs), max(xs), min(ys), max(ys))


def _make_symbol(defs_el: ET.Element, name: str, bd: BodyDefinition):
    """Create an SVG <symbol> for a body definition.

    The symbol is drawn in body-local coordinates (origin at body center).
    Pin labels, pin numbers, and IC outline are all included.

    Line segments use invisible=True as a pen-up flag: when invisible,
    the pen moves without drawing (SVG 'M'). When visible, the pen draws
    a line to the next point (SVG 'L'). The first segment is always
    treated as a move-to regardless of its invisible flag.
    """
    safe_id = name.replace('\\', '_').replace('*', '_').replace('.', '_')
    sym = ET.SubElement(defs_el, 'symbol', id=f"bd_{safe_id}", overflow="visible")

    # --- Compute body box extent for text alignment decisions ---
    box = _body_box(bd)
    if box:
        box_minx, box_maxx, box_miny, box_maxy = box
        box_cx = (box_minx + box_maxx) / 2.0
        box_w = box_maxx - box_minx
    else:
        box_minx = box_maxx = box_miny = box_maxy = 0
        box_cx = 0
        box_w = 0

    # --- Lines (IC outline / symbol shape) ---
    if bd.lines:
        # Build path segments, correctly handling pen-up (invisible) as moves
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

    # --- Pin dots + pin numbers ---
    # Pin number offset: push numbers outside the body box and slightly
    # above pin center so they don't collide with horizontal signal wires.
    PIN_NUM_OFFSET_X = 1.5    # horizontal offset from pin dot
    PIN_NUM_OFFSET_Y = 1.8    # vertical offset above pin center to clear wires
    for pin in bd.pins:
        px, py = pin.loc
        ET.SubElement(sym, 'circle',
                      cx=str(px), cy=str(py),
                      r=PIN_R, fill=PIN_FILL)

        # Render pin number if available
        if pin.pin_name and pin.pin_name > 0:
            pin_text = str(pin.pin_name)
            # pin_pos encodes the text placement direction:
            #   0 = right of pin, 2 = left of pin, 4 = below pin, 6 = above pin
            pos = pin.pin_pos
            pin_fs = f"{PIN_NUM_FONT_SIZE}px"
            if pos == 2:        # Left-side pin → number goes left of dot, above wire
                _make_text(sym, px - PIN_NUM_OFFSET_X, py + PIN_NUM_OFFSET_Y, pin_text,
                           pin_fs, PIN_NUM_COLOR,
                           anchor='end', baseline='auto')
            elif pos == 4:      # Bottom pin → number goes below dot, left of wire
                _make_text(sym, px - PIN_NUM_OFFSET_Y, py - 2.5, pin_text,
                           pin_fs, PIN_NUM_COLOR,
                           anchor='end', baseline='auto')
            elif pos == 6:      # Top pin → number goes above dot, left of wire
                _make_text(sym, px - PIN_NUM_OFFSET_Y, py + 2.5, pin_text,
                           pin_fs, PIN_NUM_COLOR,
                           anchor='end', baseline='auto')
            else:               # Right-side pin (pos=0 or default) → above wire
                _make_text(sym, px + PIN_NUM_OFFSET_X, py + PIN_NUM_OFFSET_Y, pin_text,
                           pin_fs, PIN_NUM_COLOR,
                           anchor='start', baseline='auto')

    # --- Body-level property text (pin names like A0, Q0, DIPTYPE) ---
    # Determine text anchor based on position relative to body box center.
    # This ensures left-side labels read rightward into the body,
    # right-side labels end at the right edge, and centered labels
    # (like body type name) are centered.
    for prop in bd.properties:
        text_val = _clean_text(prop.value_text)
        if not text_val:
            continue
        sz = _text_size_px(prop.text_size)
        if sz <= 0:
            continue  # hidden property (text_size=0)
        tx, ty = prop.text_loc

        # Smart anchor detection based on text position within body box
        if box_w > 0:
            # Relative position of text within body box (0=left edge, 1=right edge)
            rel_x = (tx - box_minx) / box_w if box_w > 0 else 0.5
            if rel_x < 0.35:
                # Left region: text starts here, reads rightward
                anchor = 'start'
            elif rel_x > 0.65:
                # Right region: text ends here
                anchor = 'end'
            else:
                # Center region: text is centered
                anchor = 'middle'
        else:
            anchor = 'start'

        _make_text(sym, tx, ty, text_val,
                   f"{sz}px", LABEL_COLOR,
                   anchor=anchor, baseline='central')

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
    if mirror:
        parts.append("scale(-1,1)")
    if rot_deg:
        parts.append(f"rotate({rot_deg})")
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
        # Skip outlier points (likely corrupted data)
        if abs(p.loc[0]) > 5000 or abs(p.loc[1]) > 5000:
            continue
        expand(p.loc[0], p.loc[1])

    for bp in drw.body_placements:
        bx, by = bp.loc
        expand(bx, by)
        if bp.body_name in all_defs:
            bd = all_defs[bp.body_name]
            for seg in bd.lines:
                expand(bx + seg.draw_x, by + seg.draw_y)
            for pin in bd.pins:
                expand(bx + pin.loc[0], by + pin.loc[1])
        else:
            # Unresolved body — expand by a default IC-sized box
            expand(bx - 16, by - 24)
            expand(bx + 16, by + 24)

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

    # No drawing border frame — matches user preference for clean output

    # --- Body placements ---
    g_bodies = ET.SubElement(g, 'g', id="bodies")
    for bp in drw.body_placements:
        x, y = bp.loc
        if bp.body_name in symbol_ids:
            xform = _orientation_transform(bp)
            use = ET.SubElement(g_bodies, 'use')
            use.set('href', f"#bd_{symbol_ids[bp.body_name]}")
            use.set('transform', xform)
        elif bp.body_name.strip():
            # Unresolved body with a real name → draw placeholder
            _render_placeholder(g_bodies, x, y, bp.body_name)

    # --- Placement property text (ref des, values) ---
    # Designators (like Q2, U4) are centered above the body for IC-sized
    # components. Smaller passives (R, C) keep their original text offset.
    g_labels = ET.SubElement(g, 'g', id="labels")
    for bp in drw.body_placements:
        bd = all_defs.get(bp.body_name)
        box = _body_box(bd) if bd else None
        for prop in bp.properties:
            text_val = _clean_text(prop.value_text)
            if not text_val:
                continue
            sz = _text_size_px(prop.text_size)
            if sz <= 0:
                continue
            # xy_const_offset is the XY offset from the body placement location
            tx = bp.loc[0] + prop.xy_const_offset[0]
            ty = bp.loc[1] + prop.xy_const_offset[1]
            anchor = 'start'
            if box:
                box_minx, box_maxx, box_miny, box_maxy = box
                box_w = box_maxx - box_minx
                box_cx = (box_minx + box_maxx) / 2.0
                # Only center designators for IC-sized bodies (width >= 20)
                if box_w >= 20:
                    tx = bp.loc[0] + box_cx
                    # Place designator above the body top
                    ty = bp.loc[1] + box_maxy + sz * 0.6
                    anchor = 'middle'
            _make_text(g_labels, tx, ty, text_val,
                       f"{sz}px", REFDES_COLOR, anchor=anchor)

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
        # Use const_offset for text positioning, fall back to small offset
        ox, oy = pt.xy_const_offset if pt.xy_const_offset != (0, 0) else (1, 1)
        # Use text_size from point data if available
        sz_val = pt.text_size
        if isinstance(sz_val, tuple):
            sz = sz_val[1] if sz_val[1] else sz_val[0]
        elif isinstance(sz_val, int):
            sz = sz_val
        else:
            sz = 1
        font_sz = max(4.0, sz * TEXT_SCALE)
        _make_text(g_signals, x + ox, y + oy, name_val,
                   f"{font_sz}px", SIGNAL_COLOR)

    # --- Title block ---
    if drw.trailer:
        _render_title_block(g, drw.trailer, min_x, min_y, width, height)

    # Serialize
    ET.indent(root, space='  ')
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode')


def _render_title_block(g: ET.Element, trailer: Trailer,
                        vb_x: float, vb_y: float, vb_w: float, vb_h: float):
    """Render the title block matching original SUDS plotter layout.

    Title at bottom-left, page number at bottom-right.
    """
    g_title = ET.SubElement(g, 'g', id="title_block")
    fx, fy, fw, fh = vb_x, vb_y, vb_w, vb_h

    # Title text (bottom-left, inside frame)
    title = f"{trailer.title_line_1}"
    if trailer.title_line_2:
        title += f" — {trailer.title_line_2}"

    title_y = fy + 12
    title_x = fx + 10
    if title.strip():
        _make_text(g_title, title_x, title_y, title.strip(),
                   '6px', TITLE_COLOR)

    # Page info (bottom-left, second line)
    if trailer.page:
        page_str = f"Page {trailer.page}"
        if trailer.of_string:
            page_str += f" of {trailer.of_string}"
        _make_text(g_title, title_x, title_y + 8, page_str,
                   '5px', TITLE_COLOR)

    # Drawing name / page label (bottom-right)
    # The original shows ";  QX1" format at bottom-right
    if trailer.page:
        # Try to extract the drawing name from the file context
        # For now, show the copyright line
        pass


def _render_placeholder(parent: ET.Element, x: int, y: int, name: str):
    """Render a placeholder for an unresolved body definition.

    Draws a dashed red rectangle with the body name inside.
    """
    W, H = 24, 32  # default IC-sized box
    g = ET.SubElement(parent, 'g')
    g.set('transform', f"translate({x},{y})")

    rect = ET.SubElement(g, 'rect',
                         x=str(-W // 2), y=str(-H // 2),
                         width=str(W), height=str(H))
    rect.set('stroke', '#cc0000')
    rect.set('stroke-width', '0.5')
    rect.set('stroke-dasharray', '2,1')
    rect.set('fill', 'none')

    _make_text(g, 0, 0, name, '4px', '#cc0000',
               anchor='middle', baseline='central')
