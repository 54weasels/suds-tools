"""
pc_svg_renderer.py — Render SUDS PC board layouts as multi-layer SVG files.

Produces an SVG image with separate groups per layer, suitable for
visual inspection and debugging of board layouts. Each layer can be
toggled via CSS visibility controls.

Layer groups:
  - board-outline   — CRD board outline (if provided)
  - dip-bodies      — DIP component rectangles derived from actual pin positions
  - side1-traces    — Component side traces (red)
  - side2-traces    — Solder side traces (blue)
  - side1-pads      — Component side pads (dark red filled circles)
  - side2-pads      — Solder side pads (dark blue filled circles)
  - feed-throughs   — Via connections between sides (green)
  - labels          — Text annotations

Coordinate system: SUDS uses mils with Y increasing upward.
SVG uses Y increasing downward, so we flip the Y axis.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

from .pc_model import PCFile, PCPoint, PCBody
from .crd_model import CRDFile
from .dip_library import DIPLibrary


# ============================================================================
# Default rendering parameters (mils)
# ============================================================================

DEFAULT_PAD_RADIUS = 8       # Standard DIP pad radius (mils)
DEFAULT_VIA_RADIUS = 7       # Feed-through via radius (mils)
DEFAULT_TRACE_WIDTH = 6      # Default trace width (mils) — KiCad narrow
DEFAULT_PIN1_SIZE = 10       # Pin 1 square pad half-size (mils)
BODY_PAD_MARGIN = 10         # Margin around pin bbox for body outline (mils)
BODY_STROKE_WIDTH = 2        # DIP body outline width
FINGER_WIDTH = 12            # Edge connector finger width

# Colors
COLORS = {
    'board_outline': '#555555',
    'board_fill': '#2B3320',           # Dark PCB substrate green
    'body_stroke': '#888888',
    'body_fill': '#1A1A1A',
    'body_text': '#CCCCCC',
    'side1_trace': '#CC3333',          # Component side = red
    'side1_pad': '#BB2222',
    'side2_trace': '#3366CC',          # Solder side = blue
    'side2_pad': '#2244AA',
    'feed_through': '#22AA22',         # Vias = green
    'pin1_marker': '#DD7700',          # Pin 1 = orange
    'finger': '#FFD700',              # Gold fingers
    'bar': '#C0C0C0',                 # Silver shorting bars
    'label': '#999999',
}


class PCSVGRenderer:
    """Render a parsed PCFile (and optional CRDFile) to SVG.

    Body outlines are derived from actual pin positions (bounding box
    of all points belonging to each body), not estimated from pin count.
    This ensures bodies align precisely with their pin holes.
    """

    def __init__(self, pc: PCFile, crd: CRDFile | None = None,
                 dip_lib: DIPLibrary | None = None,
                 scale: float = 1.0, margin: int = 100):
        self.pc = pc
        self.crd = crd
        self.dip_lib = dip_lib
        self.scale = scale
        self.margin = margin

        # Pre-compute body pin bounding boxes
        self._body_pin_bboxes: dict[int, tuple[int, int, int, int]] = {}
        self._compute_body_bboxes()

        # Compute overall bounding box from actual geometry
        self._compute_bounds()

    def _compute_body_bboxes(self) -> None:
        """Compute bounding box of pins for each body from actual point data.

        Uses only side1 (component side) pins to avoid doubling the bbox
        from pins that exist on both sides at the same coordinates.
        """
        body_pins: dict[int, list[PCPoint]] = {}
        for pt in self.pc.side1_points:
            if pt.is_pin:
                bid = pt.body_id
                if bid not in body_pins:
                    body_pins[bid] = []
                body_pins[bid].append(pt)

        for bid, pins in body_pins.items():
            xs = [p.loc[0] for p in pins]
            ys = [p.loc[1] for p in pins]
            self._body_pin_bboxes[bid] = (min(xs), min(ys), max(xs), max(ys))

    def _compute_bounds(self) -> None:
        """Compute the bounding box of the actual board area.

        Derives the board area from body locations (which represent
        placed components) and the CRD outline (if available),
        with a generous margin. This excludes unplaced/garbage
        points that would otherwise inflate the SVG viewport.
        """
        # Stage 1: establish the board area from reliable anchors
        anchor_x: list[int] = []
        anchor_y: list[int] = []

        # Bodies are always placed at real board locations
        for body in self.pc.bodies:
            if abs(body.loc[0]) < 50000 and abs(body.loc[1]) < 50000:
                anchor_x.append(body.loc[0])
                anchor_y.append(body.loc[1])

        # CRD outline defines the physical board edge
        if self.crd:
            for pt in self.crd.outline:
                anchor_x.append(pt[0])
                anchor_y.append(pt[1])

        if not anchor_x:
            # Fallback: use all points with loose filter
            for pt in self.pc.all_points:
                if abs(pt.loc[0]) < 50000 and abs(pt.loc[1]) < 50000:
                    anchor_x.append(pt.loc[0])
                    anchor_y.append(pt.loc[1])

        if not anchor_x:
            self.min_x = self.min_y = 0
            self.max_x = self.max_y = 1000
            self._board_min_x = self._board_min_y = -500
            self._board_max_x = self._board_max_y = 1500
            return

        # Board area with 300 mil margin (covers traces near edges)
        BOARD_MARGIN = 300
        self._board_min_x = min(anchor_x) - BOARD_MARGIN
        self._board_min_y = min(anchor_y) - BOARD_MARGIN
        self._board_max_x = max(anchor_x) + BOARD_MARGIN
        self._board_max_y = max(anchor_y) + BOARD_MARGIN

        # Stage 2: compute viewport from in-area points + CRD
        all_x: list[int] = list(anchor_x)
        all_y: list[int] = list(anchor_y)

        for pt in self.pc.all_points:
            if self._pt_in_board_area(pt.loc):
                all_x.append(pt.loc[0])
                all_y.append(pt.loc[1])

        self.min_x = min(all_x) - self.margin
        self.min_y = min(all_y) - self.margin
        self.max_x = max(all_x) + self.margin
        self.max_y = max(all_y) + self.margin

    def _pt_in_board_area(self, loc: tuple[int, int]) -> bool:
        """Check if a coordinate is within the computed board area."""
        return (self._board_min_x <= loc[0] <= self._board_max_x and
                self._board_min_y <= loc[1] <= self._board_max_y)

    def _is_valid_point(self, pt: PCPoint) -> bool:
        """Check if a point is a valid renderable entity.

        Filters out unplaced entries at the origin (0,0) which appear
        in many PC files as uninitialized/sentinel data regardless
        of their point_id.
        """
        if pt.loc == (0, 0):
            return False
        return self._pt_in_board_area(pt.loc)

    def _sx(self, x: int | float) -> float:
        """Scale X coordinate."""
        return (x - self.min_x) * self.scale

    def _sy(self, y: int | float) -> float:
        """Scale and flip Y coordinate (SUDS Y-up → SVG Y-down)."""
        return (self.max_y - y) * self.scale

    def _build_point_index(self) -> dict[int, PCPoint]:
        """Build a lookup from point_id to PCPoint for neighbor resolution.

        Only includes valid points within the board area.
        """
        idx: dict[int, PCPoint] = {}
        for pt in self.pc.all_points:
            if pt.point_id not in idx and self._is_valid_point(pt):
                idx[pt.point_id] = pt
        return idx

    def render(self, output_path: str | Path) -> None:
        """Render the board to an SVG file."""
        width = (self.max_x - self.min_x) * self.scale
        height = (self.max_y - self.min_y) * self.scale

        svg = ET.Element('svg')
        svg.set('xmlns', 'http://www.w3.org/2000/svg')
        svg.set('width', f'{width:.0f}')
        svg.set('height', f'{height:.0f}')
        svg.set('viewBox', f'0 0 {width:.0f} {height:.0f}')

        self._add_styles(svg)

        title = ET.SubElement(svg, 'title')
        title.text = f"SUDS PC Board: {Path(self.pc.source_path).stem}"

        # Background
        bg = ET.SubElement(svg, 'rect')
        bg.set('width', '100%')
        bg.set('height', '100%')
        bg.set('fill', '#111111')

        point_idx = self._build_point_index()

        # Render layers back to front
        if self.crd:
            self._render_board_outline(svg)
        else:
            # No CRD: draw a filled rectangle from the body-derived board area
            self._render_inferred_board(svg)
        self._render_traces(svg, self.pc.side2_points, 'side2', point_idx)
        self._render_traces(svg, self.pc.side1_points, 'side1', point_idx)
        self._render_pads(svg, self.pc.side2_points, 'side2')
        self._render_pads(svg, self.pc.side1_points, 'side1')
        self._render_feed_throughs(svg, point_idx)
        self._render_bodies(svg)
        self._render_labels(svg)

        tree = ET.ElementTree(svg)
        ET.indent(tree, space='  ')
        tree.write(str(output_path), encoding='unicode', xml_declaration=True)

    def _add_styles(self, svg: ET.Element) -> None:
        """Add CSS styles for layer toggling."""
        s = self.scale
        style = ET.SubElement(svg, 'style')
        style.text = f"""
            .board-outline {{ fill: {COLORS['board_fill']}; stroke: {COLORS['board_outline']}; stroke-width: 3; }}
            .dip-body {{ fill: {COLORS['body_fill']}; stroke: {COLORS['body_stroke']}; stroke-width: {BODY_STROKE_WIDTH}; opacity: 0.85; }}
            .body-label {{ fill: {COLORS['body_text']}; font-family: monospace; font-size: 10px; text-anchor: middle; dominant-baseline: middle; }}
            .side1-trace {{ stroke: {COLORS['side1_trace']}; stroke-width: {DEFAULT_TRACE_WIDTH * s:.1f}; fill: none; stroke-linecap: round; }}
            .side2-trace {{ stroke: {COLORS['side2_trace']}; stroke-width: {DEFAULT_TRACE_WIDTH * s:.1f}; fill: none; stroke-linecap: round; }}
            .side1-pad {{ fill: {COLORS['side1_pad']}; stroke: #DD4444; stroke-width: 1; }}
            .side2-pad {{ fill: {COLORS['side2_pad']}; stroke: #4466DD; stroke-width: 1; }}
            .feed-through {{ fill: none; stroke: {COLORS['feed_through']}; stroke-width: 2; }}
            .pin1-marker {{ fill: {COLORS['pin1_marker']}; stroke: #FF9900; stroke-width: 1; }}
            .finger {{ fill: {COLORS['finger']}; stroke: #B8860B; stroke-width: 1; }}
            .shorting-bar {{ stroke: {COLORS['bar']}; stroke-width: 6; fill: none; }}
            .label {{ fill: {COLORS['label']}; font-family: monospace; font-size: 12px; }}
        """

    def _render_board_outline(self, svg: ET.Element) -> None:
        """Render the CRD board outline.

        Draws a filled rectangle from the CRD bounding box (ensuring
        the board fill covers the entire component area including
        the finger zone), then overlays the detailed CRD outline
        polygon as a stroke-only border.
        """
        if not self.crd or not self.crd.outline:
            return

        g = ET.SubElement(svg, 'g')
        g.set('id', 'board-outline')

        # 1. Filled rectangle covering the full board + finger zone
        ext = list(self.crd.board_extents)  # [min_x, min_y, max_x, max_y]

        # Extend to cover finger positions
        for finger in self.crd.front_fingers + self.crd.back_fingers:
            ext[0] = min(ext[0], finger.start[0], finger.end[0])
            ext[1] = min(ext[1], finger.start[1], finger.end[1])
            ext[2] = max(ext[2], finger.start[0], finger.end[0])
            ext[3] = max(ext[3], finger.start[1], finger.end[1])

        rx = self._sx(ext[0])
        ry = self._sy(ext[3])  # flip Y — max_y is top in board coords
        rw = (ext[2] - ext[0]) * self.scale
        rh = (ext[3] - ext[1]) * self.scale
        fill_rect = ET.SubElement(g, 'rect')
        fill_rect.set('x', f'{rx:.1f}')
        fill_rect.set('y', f'{ry:.1f}')
        fill_rect.set('width', f'{rw:.1f}')
        fill_rect.set('height', f'{rh:.1f}')
        fill_rect.set('fill', COLORS['board_fill'])
        fill_rect.set('stroke', 'none')

        # 2. Detailed outline polygon (stroke only, no fill)
        points_str = " ".join(
            f"{self._sx(x):.1f},{self._sy(y):.1f}"
            for x, y in self.crd.outline
        )
        poly = ET.SubElement(g, 'polygon')
        poly.set('points', points_str)
        poly.set('fill', 'none')
        poly.set('stroke', COLORS['board_outline'])
        poly.set('stroke-width', '3')

        # Fingers
        for finger in self.crd.front_fingers + self.crd.back_fingers:
            line = ET.SubElement(g, 'line')
            line.set('x1', f'{self._sx(finger.start[0]):.1f}')
            line.set('y1', f'{self._sy(finger.start[1]):.1f}')
            line.set('x2', f'{self._sx(finger.end[0]):.1f}')
            line.set('y2', f'{self._sy(finger.end[1]):.1f}')
            line.set('class', 'finger')
            line.set('stroke-width', str(FINGER_WIDTH * self.scale))

        # Shorting bars
        for bar in self.crd.front_bars + self.crd.back_bars:
            line = ET.SubElement(g, 'line')
            line.set('x1', f'{self._sx(bar.start[0]):.1f}')
            line.set('y1', f'{self._sy(bar.start[1]):.1f}')
            line.set('x2', f'{self._sx(bar.end[0]):.1f}')
            line.set('y2', f'{self._sy(bar.end[1]):.1f}')
            line.set('class', 'shorting-bar')

    def _render_inferred_board(self, svg: ET.Element) -> None:
        """Render a filled board rectangle when no CRD is available.

        Uses the body-derived board area (with margin stripped back
        to just the component extent) as the board fill.
        """
        g = ET.SubElement(svg, 'g')
        g.set('id', 'board-outline')

        # Use body positions with a small margin for the board fill
        bxs = [b.loc[0] for b in self.pc.bodies if abs(b.loc[0]) < 50000]
        bys = [b.loc[1] for b in self.pc.bodies if abs(b.loc[1]) < 50000]
        if not bxs:
            return

        m = 100  # Small margin around bodies
        bx1, by1 = min(bxs) - m, min(bys) - m
        bx2, by2 = max(bxs) + m, max(bys) + m

        rx = self._sx(bx1)
        ry = self._sy(by2)
        rw = (bx2 - bx1) * self.scale
        rh = (by2 - by1) * self.scale

        fill_rect = ET.SubElement(g, 'rect')
        fill_rect.set('x', f'{rx:.1f}')
        fill_rect.set('y', f'{ry:.1f}')
        fill_rect.set('width', f'{rw:.1f}')
        fill_rect.set('height', f'{rh:.1f}')
        fill_rect.set('fill', COLORS['board_fill'])
        fill_rect.set('stroke', COLORS['board_outline'])
        fill_rect.set('stroke-width', '3')
        fill_rect.set('rx', '8')

    def _render_traces(self, svg: ET.Element, points: list[PCPoint],
                       side: str, point_idx: dict[int, PCPoint]) -> None:
        """Render trace segments for one side."""
        g = ET.SubElement(svg, 'g')
        g.set('id', f'{side}-traces')

        css_class = f'{side}-trace'
        drawn: set[tuple[int, int]] = set()

        for pt in points:
            if not self._is_valid_point(pt):
                continue
            for nb_id in pt.neighbors:
                pair = (min(pt.point_id, nb_id), max(pt.point_id, nb_id))
                if pair in drawn:
                    continue
                drawn.add(pair)

                nb = point_idx.get(nb_id)
                if nb is None:
                    continue
                if not self._pt_in_board_area(nb.loc):
                    continue

                line = ET.SubElement(g, 'line')
                line.set('x1', f'{self._sx(pt.loc[0]):.1f}')
                line.set('y1', f'{self._sy(pt.loc[1]):.1f}')
                line.set('x2', f'{self._sx(nb.loc[0]):.1f}')
                line.set('y2', f'{self._sy(nb.loc[1]):.1f}')
                line.set('class', css_class)

    def _render_pads(self, svg: ET.Element, points: list[PCPoint],
                     side: str) -> None:
        """Render pads for one side."""
        g = ET.SubElement(svg, 'g')
        g.set('id', f'{side}-pads')

        for pt in points:
            if not pt.has_pad:
                continue
            if not self._is_valid_point(pt):
                continue

            cx = self._sx(pt.loc[0])
            cy = self._sy(pt.loc[1])

            if pt.pad_type == 3:
                # Pin 1 square pad
                half = DEFAULT_PIN1_SIZE * self.scale
                rect = ET.SubElement(g, 'rect')
                rect.set('x', f'{cx - half:.1f}')
                rect.set('y', f'{cy - half:.1f}')
                rect.set('width', f'{2 * half:.1f}')
                rect.set('height', f'{2 * half:.1f}')
                rect.set('class', 'pin1-marker')
            else:
                # Circular pad
                r = DEFAULT_PAD_RADIUS * self.scale
                circle = ET.SubElement(g, 'circle')
                circle.set('cx', f'{cx:.1f}')
                circle.set('cy', f'{cy:.1f}')
                circle.set('r', f'{r:.1f}')
                circle.set('class', f'{side}-pad')

    def _render_feed_throughs(self, svg: ET.Element,
                               point_idx: dict[int, PCPoint]) -> None:
        """Render feed-through vias as open circles.

        Deduplicates by location (X,Y tuple) since the same physical
        via appears as two points — one on each board side — with
        different point IDs but identical coordinates.
        """
        g = ET.SubElement(svg, 'g')
        g.set('id', 'feed-throughs')

        rendered_locs: set[tuple[int, int]] = set()

        for pt in self.pc.all_points:
            if not pt.is_feed_through:
                continue
            if pt.loc in rendered_locs:
                continue
            if not self._is_valid_point(pt):
                continue
            rendered_locs.add(pt.loc)

            cx = self._sx(pt.loc[0])
            cy = self._sy(pt.loc[1])
            r = DEFAULT_VIA_RADIUS * self.scale

            circle = ET.SubElement(g, 'circle')
            circle.set('cx', f'{cx:.1f}')
            circle.set('cy', f'{cy:.1f}')
            circle.set('r', f'{r:.1f}')
            circle.set('class', 'feed-through')

    def _render_bodies(self, svg: ET.Element) -> None:
        """Render DIP component outlines derived from actual pin positions.

        Body outlines are computed from the bounding box of all pins
        belonging to each body, with a small margin. This ensures
        bodies align precisely with their pin holes.
        """
        g = ET.SubElement(svg, 'g')
        g.set('id', 'dip-bodies')

        for body in self.pc.bodies:
            bbox = self._body_pin_bboxes.get(body.body_id)
            if bbox is None:
                continue

            min_px, min_py, max_px, max_py = bbox

            # Skip bodies with pins outside the board area
            if not self._pt_in_board_area((min_px, min_py)):
                continue

            # Add margin around pin bounding box, clamped to CRD bounds
            m = BODY_PAD_MARGIN
            bx1 = min_px - m
            by1 = min_py - m
            bx2 = max_px + m
            by2 = max_py + m

            # Clamp to CRD board outline if available
            if self.crd and self.crd.outline:
                crd_min_x, crd_min_y, crd_max_x, crd_max_y = self.crd.board_extents
                bx1 = max(bx1, crd_min_x)
                by1 = max(by1, crd_min_y)
                bx2 = min(bx2, crd_max_x)
                by2 = min(by2, crd_max_y)

            x1 = self._sx(bx1)
            y1 = self._sy(by2)  # flip Y
            x2 = self._sx(bx2)
            y2 = self._sy(by1)  # flip Y

            w = x2 - x1
            h = y2 - y1

            if w < 1 or h < 1:
                # Degenerate (all pins in a line) — make a thin rectangle
                if w < 1:
                    x1 -= 10 * self.scale
                    w = 20 * self.scale
                if h < 1:
                    y1 -= 10 * self.scale
                    h = 20 * self.scale

            rect = ET.SubElement(g, 'rect')
            rect.set('x', f'{x1:.1f}')
            rect.set('y', f'{y1:.1f}')
            rect.set('width', f'{w:.1f}')
            rect.set('height', f'{h:.1f}')
            rect.set('class', 'dip-body')
            rect.set('rx', f'{4 * self.scale:.1f}')

            # Label at center — show DIP type and pin count
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            font_size = min(12, max(5, min(w, h) / (3 * self.scale))) * self.scale

            if self.dip_lib:
                dip_name = self.dip_lib.get_name(body.dip_lib_index)
            else:
                dip_name = f'L{body.dip_lib_index}'

            # Show DIP name + pin count for clarity
            label_text = f'{dip_name}' if body.num_pins <= 2 else f'{dip_name}/{body.num_pins}'

            label = ET.SubElement(g, 'text')
            label.set('x', f'{cx:.1f}')
            label.set('y', f'{cy:.1f}')
            label.set('class', 'body-label')
            label.set('font-size', f'{font_size:.0f}')
            label.text = label_text

    def _render_labels(self, svg: ET.Element) -> None:
        """Render text annotations from points."""
        g = ET.SubElement(svg, 'g')
        g.set('id', 'labels')

        for pt in self.pc.all_points:
            if pt.text_size == 0 or not pt.text:
                continue
            if abs(pt.loc[0]) > 50000 or abs(pt.loc[1]) > 50000:
                continue

            x = self._sx(pt.loc[0] + pt.text_offset[0])
            y = self._sy(pt.loc[1] + pt.text_offset[1])

            text = ET.SubElement(g, 'text')
            text.set('x', f'{x:.1f}')
            text.set('y', f'{y:.1f}')
            text.set('class', 'label')
            text.set('font-size', f'{pt.text_size * self.scale:.0f}')
            text.text = pt.text


# ============================================================================
# Convenience functions
# ============================================================================

def render_pc_svg(pc: PCFile, output_path: str | Path,
                  crd: CRDFile | None = None,
                  dip_lib: DIPLibrary | None = None,
                  scale: float = 1.0, margin: int = 100) -> None:
    """Render a parsed PCFile to SVG."""
    renderer = PCSVGRenderer(pc, crd=crd, dip_lib=dip_lib, scale=scale, margin=margin)
    renderer.render(output_path)


def render_pc_html(pc: PCFile, output_path: str | Path,
                   crd: CRDFile | None = None,
                   dip_lib: DIPLibrary | None = None,
                   scale: float = 1.0, margin: int = 100) -> None:
    """Render a parsed PCFile to an interactive HTML file with layer toggles.

    Produces an HTML file embedding the SVG with checkboxes to toggle
    visibility of each layer group.
    """
    renderer = PCSVGRenderer(pc, crd=crd, dip_lib=dip_lib, scale=scale, margin=margin)
    width = (renderer.max_x - renderer.min_x) * scale
    height = (renderer.max_y - renderer.min_y) * scale

    svg = ET.Element('svg')
    svg.set('xmlns', 'http://www.w3.org/2000/svg')
    svg.set('width', '100%')
    svg.set('height', f'{height:.0f}')
    svg.set('viewBox', f'0 0 {width:.0f} {height:.0f}')
    svg.set('id', 'board-svg')

    renderer._add_styles(svg)

    title = ET.SubElement(svg, 'title')
    title.text = f"SUDS PC Board: {Path(pc.source_path).stem}"

    bg = ET.SubElement(svg, 'rect')
    bg.set('width', '100%')
    bg.set('height', '100%')
    bg.set('fill', '#111111')

    point_idx = renderer._build_point_index()

    if crd:
        renderer._render_board_outline(svg)
    renderer._render_traces(svg, pc.side2_points, 'side2', point_idx)
    renderer._render_traces(svg, pc.side1_points, 'side1', point_idx)
    renderer._render_pads(svg, pc.side2_points, 'side2')
    renderer._render_pads(svg, pc.side1_points, 'side1')
    renderer._render_feed_throughs(svg, point_idx)
    renderer._render_bodies(svg)
    renderer._render_labels(svg)

    ET.indent(ET.ElementTree(svg), space='  ')
    svg_str = ET.tostring(svg, encoding='unicode')

    layers = [
        ('board-outline', 'Board Outline', True),
        ('dip-bodies', 'DIP Bodies', True),
        ('side1-traces', 'Side 1 Traces (Component)', True),
        ('side2-traces', 'Side 2 Traces (Solder)', True),
        ('side1-pads', 'Side 1 Pads', True),
        ('side2-pads', 'Side 2 Pads', True),
        ('feed-throughs', 'Feed-throughs (Vias)', True),
        ('labels', 'Text Labels', True),
    ]

    board_name = Path(pc.source_path).stem
    s1_pts = len(pc.side1_points)
    s2_pts = len(pc.side2_points)
    ft = len(pc.feed_through_pairs)
    w_in = (renderer.max_x - renderer.min_x - 2 * renderer.margin) / 1000
    h_in = (renderer.max_y - renderer.min_y - 2 * renderer.margin) / 1000

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SUDS PC Board: {board_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: #0a0a0a; color: #eee; font-family: 'Consolas', 'Monaco', monospace; }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 14px 20px;
            border-bottom: 1px solid #333;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .header h1 {{ font-size: 16px; color: #e94560; letter-spacing: 0.5px; }}
        .header .stats {{ font-size: 11px; color: #888; }}
        .controls {{
            background: #141420;
            padding: 10px 20px;
            display: flex; gap: 14px; flex-wrap: wrap;
            border-bottom: 1px solid #222;
        }}
        .layer-toggle {{
            display: flex; align-items: center; gap: 5px;
            font-size: 12px; cursor: pointer; color: #bbb;
        }}
        .layer-toggle:hover {{ color: #fff; }}
        .layer-toggle input {{ cursor: pointer; accent-color: #e94560; }}
        .svg-container {{
            overflow: auto; padding: 16px;
            display: flex; justify-content: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SUDS PC Board: {board_name}</h1>
        <div class="stats">
            {len(pc.bodies)} bodies &middot; {s1_pts} s1 pts &middot; {s2_pts} s2 pts &middot; {ft} vias &middot; ~{w_in:.1f}&times;{h_in:.1f}" &middot; v{pc.version}
        </div>
    </div>
    <div class="controls">
"""

    for layer_id, label, checked in layers:
        chk = 'checked' if checked else ''
        html += f'        <label class="layer-toggle"><input type="checkbox" {chk} onchange="toggleLayer(\'{layer_id}\', this.checked)">{label}</label>\n'

    html += f"""    </div>
    <div class="svg-container">
{svg_str}
    </div>
    <script>
        function toggleLayer(id, visible) {{
            const el = document.getElementById(id);
            if (el) el.style.display = visible ? 'inline' : 'none';
        }}
    </script>
</body>
</html>"""

    Path(output_path).write_text(html, encoding='utf-8')
