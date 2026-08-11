"""
pc_svg_renderer.py — Render SUDS PC board layouts as multi-layer SVG files.

Produces an SVG image with separate groups per layer, suitable for
visual inspection and debugging of board layouts. Each layer can be
toggled via CSS visibility controls.

Layer groups:
  - board-outline   — CRD board outline (if provided)
  - dip-bodies      — DIP component rectangles with pin numbers
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


# ============================================================================
# Default rendering parameters (mils)
# ============================================================================

DEFAULT_PAD_RADIUS = 25      # Standard DIP pad radius
DEFAULT_VIA_RADIUS = 20      # Feed-through via radius
DEFAULT_TRACE_WIDTH = 10     # Default trace width
DEFAULT_PIN1_RADIUS = 30     # Pin 1 square pad half-size
BODY_STROKE_WIDTH = 4        # DIP body outline width
FINGER_WIDTH = 12            # Edge connector finger width

# Colors
COLORS = {
    'board_outline': '#333333',
    'board_fill': '#F5F0E0',          # PCB substrate color
    'body_stroke': '#444444',
    'body_fill': '#2A2A2A',
    'body_text': '#FFFFFF',
    'side1_trace': '#CC0000',          # Component side = red
    'side1_pad': '#990000',
    'side2_trace': '#0000CC',          # Solder side = blue
    'side2_pad': '#000099',
    'feed_through': '#009900',         # Vias = green
    'pin1_marker': '#FF6600',          # Pin 1 = orange
    'finger': '#FFD700',              # Gold fingers
    'bar': '#C0C0C0',                 # Silver shorting bars
    'label': '#666666',
}


class PCSVGRenderer:
    """Render a parsed PCFile (and optional CRDFile) to SVG.

    Usage:
        from .pc_parser import parse_pc_file
        from .crd_parser import parse_crd_file

        pc = parse_pc_file("mouse.pc.O")
        crd = parse_crd_file("multi0.crd.O")  # optional

        renderer = PCSVGRenderer(pc, crd=crd)
        renderer.render("mouse_board.svg")
    """

    def __init__(self, pc: PCFile, crd: CRDFile | None = None,
                 scale: float = 1.0, margin: int = 200):
        """
        Args:
            pc: Parsed PC board layout
            crd: Optional card definition for board outline
            scale: Scale factor (1.0 = 1 mil per SVG unit)
            margin: Margin around the board in mils
        """
        self.pc = pc
        self.crd = crd
        self.scale = scale
        self.margin = margin

        # Compute bounding box from all points
        self._compute_bounds()

    def _compute_bounds(self) -> None:
        """Compute the bounding box of all geometry."""
        all_x: list[int] = []
        all_y: list[int] = []

        for pt in self.pc.all_points:
            all_x.append(pt.loc[0])
            all_y.append(pt.loc[1])

        for body in self.pc.bodies:
            all_x.append(body.loc[0])
            all_y.append(body.loc[1])

        if self.crd:
            for pt in self.crd.outline:
                all_x.append(pt[0])
                all_y.append(pt[1])

        if not all_x:
            self.min_x = self.min_y = 0
            self.max_x = self.max_y = 1000
            return

        self.min_x = min(all_x) - self.margin
        self.min_y = min(all_y) - self.margin
        self.max_x = max(all_x) + self.margin
        self.max_y = max(all_y) + self.margin

    def _sx(self, x: int) -> float:
        """Scale X coordinate."""
        return (x - self.min_x) * self.scale

    def _sy(self, y: int) -> float:
        """Scale and flip Y coordinate (SUDS Y-up → SVG Y-down)."""
        return (self.max_y - y) * self.scale

    def _build_point_index(self) -> dict[int, PCPoint]:
        """Build a lookup from point_id to PCPoint for neighbor resolution."""
        idx: dict[int, PCPoint] = {}
        for pt in self.pc.all_points:
            idx[pt.point_id] = pt
        return idx

    def render(self, output_path: str | Path) -> None:
        """Render the board to an SVG file."""
        width = (self.max_x - self.min_x) * self.scale
        height = (self.max_y - self.min_y) * self.scale

        # Create SVG root
        svg = ET.Element('svg')
        svg.set('xmlns', 'http://www.w3.org/2000/svg')
        svg.set('width', f'{width:.0f}')
        svg.set('height', f'{height:.0f}')
        svg.set('viewBox', f'0 0 {width:.0f} {height:.0f}')

        # Add CSS styles
        self._add_styles(svg)

        # Add title
        title = ET.SubElement(svg, 'title')
        title.text = f"SUDS PC Board: {Path(self.pc.source_path).stem}"

        # Background
        bg = ET.SubElement(svg, 'rect')
        bg.set('width', '100%')
        bg.set('height', '100%')
        bg.set('fill', '#1A1A1A')

        # Build point index for trace drawing
        point_idx = self._build_point_index()

        # Layer groups (back to front rendering order)
        if self.crd:
            self._render_board_outline(svg)
        self._render_traces(svg, self.pc.side2_points, 'side2', point_idx)
        self._render_traces(svg, self.pc.side1_points, 'side1', point_idx)
        self._render_pads(svg, self.pc.side2_points, 'side2')
        self._render_pads(svg, self.pc.side1_points, 'side1')
        self._render_feed_throughs(svg, point_idx)
        self._render_bodies(svg)
        self._render_labels(svg)

        # Write SVG
        tree = ET.ElementTree(svg)
        ET.indent(tree, space='  ')
        tree.write(str(output_path), encoding='unicode', xml_declaration=True)

    def _add_styles(self, svg: ET.Element) -> None:
        """Add CSS styles for layer toggling."""
        style = ET.SubElement(svg, 'style')
        style.text = """
            .board-outline { fill: """ + COLORS['board_fill'] + """; stroke: """ + COLORS['board_outline'] + """; stroke-width: 4; }
            .dip-body { fill: """ + COLORS['body_fill'] + """; stroke: """ + COLORS['body_stroke'] + """; stroke-width: """ + str(BODY_STROKE_WIDTH) + """; }
            .body-label { fill: """ + COLORS['body_text'] + """; font-family: monospace; font-size: 28px; text-anchor: middle; dominant-baseline: middle; }
            .side1-trace { stroke: """ + COLORS['side1_trace'] + """; stroke-width: """ + str(DEFAULT_TRACE_WIDTH * self.scale) + """; fill: none; stroke-linecap: round; }
            .side2-trace { stroke: """ + COLORS['side2_trace'] + """; stroke-width: """ + str(DEFAULT_TRACE_WIDTH * self.scale) + """; fill: none; stroke-linecap: round; }
            .side1-pad { fill: """ + COLORS['side1_pad'] + """; stroke: none; }
            .side2-pad { fill: """ + COLORS['side2_pad'] + """; stroke: none; }
            .feed-through { fill: """ + COLORS['feed_through'] + """; stroke: #00CC00; stroke-width: 2; }
            .pin1-marker { fill: """ + COLORS['pin1_marker'] + """; stroke: none; }
            .finger { fill: """ + COLORS['finger'] + """; stroke: #B8860B; stroke-width: 1; }
            .shorting-bar { stroke: """ + COLORS['bar'] + """; stroke-width: 8; fill: none; }
            .label { fill: """ + COLORS['label'] + """; font-family: monospace; font-size: 16px; }
        """

    def _render_board_outline(self, svg: ET.Element) -> None:
        """Render the CRD board outline."""
        if not self.crd or not self.crd.outline:
            return

        g = ET.SubElement(svg, 'g')
        g.set('id', 'board-outline')

        # Draw outline polygon
        points_str = " ".join(
            f"{self._sx(x):.1f},{self._sy(y):.1f}"
            for x, y in self.crd.outline
        )
        poly = ET.SubElement(g, 'polygon')
        poly.set('points', points_str)
        poly.set('class', 'board-outline')

        # Draw fingers
        for finger in self.crd.front_fingers + self.crd.back_fingers:
            line = ET.SubElement(g, 'line')
            line.set('x1', f'{self._sx(finger.start[0]):.1f}')
            line.set('y1', f'{self._sy(finger.start[1]):.1f}')
            line.set('x2', f'{self._sx(finger.end[0]):.1f}')
            line.set('y2', f'{self._sy(finger.end[1]):.1f}')
            line.set('class', 'finger')
            line.set('stroke-width', str(FINGER_WIDTH * self.scale))

        # Draw shorting bars
        for bar in self.crd.front_bars + self.crd.back_bars:
            line = ET.SubElement(g, 'line')
            line.set('x1', f'{self._sx(bar.start[0]):.1f}')
            line.set('y1', f'{self._sy(bar.start[1]):.1f}')
            line.set('x2', f'{self._sx(bar.end[0]):.1f}')
            line.set('y2', f'{self._sy(bar.end[1]):.1f}')
            line.set('class', 'shorting-bar')

    def _render_traces(self, svg: ET.Element, points: list[PCPoint],
                       side: str, point_idx: dict[int, PCPoint]) -> None:
        """Render trace segments for one side.

        Traces are drawn by following neighbor links from each point.
        To avoid duplicate lines, we only draw from points with lower
        IDs to higher IDs.
        """
        g = ET.SubElement(svg, 'g')
        g.set('id', f'{side}-traces')

        css_class = f'{side}-trace'
        drawn: set[tuple[int, int]] = set()

        for pt in points:
            for nb_id in pt.neighbors:
                # Avoid drawing same line twice
                pair = (min(pt.point_id, nb_id), max(pt.point_id, nb_id))
                if pair in drawn:
                    continue
                drawn.add(pair)

                nb = point_idx.get(nb_id)
                if nb is None:
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

            cx = self._sx(pt.loc[0])
            cy = self._sy(pt.loc[1])

            if pt.pad_type == 3:
                # Pin 1 square pad
                half = DEFAULT_PIN1_RADIUS * self.scale
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
        """Render feed-through vias."""
        g = ET.SubElement(svg, 'g')
        g.set('id', 'feed-throughs')

        rendered: set[int] = set()

        for pt in self.pc.all_points:
            if not pt.is_feed_through:
                continue
            if pt.point_id in rendered:
                continue
            rendered.add(pt.point_id)
            rendered.add(pt.feed_through_id)

            cx = self._sx(pt.loc[0])
            cy = self._sy(pt.loc[1])
            r = DEFAULT_VIA_RADIUS * self.scale

            circle = ET.SubElement(g, 'circle')
            circle.set('cx', f'{cx:.1f}')
            circle.set('cy', f'{cy:.1f}')
            circle.set('r', f'{r:.1f}')
            circle.set('class', 'feed-through')

    def _render_bodies(self, svg: ET.Element) -> None:
        """Render DIP component outlines."""
        g = ET.SubElement(svg, 'g')
        g.set('id', 'dip-bodies')

        for body in self.pc.bodies:
            # Estimate body dimensions from pin count and orientation
            if body.num_pins <= 2:
                # Two-pin component (capacitor/resistor)
                self._render_2pin_body(g, body)
            else:
                # DIP IC
                self._render_dip_body(g, body)

    def _render_dip_body(self, g: ET.Element, body: PCBody) -> None:
        """Render a DIP IC outline."""
        # DIP dimensions: 300 mil wide, 100 mil per pin pair
        pin_rows = body.num_pins // 2
        body_length = pin_rows * 100  # mils

        # Orientation: 0=normal, 1=90°CW, 2=180°, 3=90°CCW
        # For orientation 0/2: body is vertical (length along Y)
        # For orientation 1/3: body is horizontal (length along X)

        if body.orientation in (0, 2):
            w = 300
            h = body_length
        else:
            w = body_length
            h = 300

        cx = self._sx(body.loc[0])
        cy = self._sy(body.loc[1])

        rect = ET.SubElement(g, 'rect')
        rect.set('x', f'{cx - w * self.scale / 2:.1f}')
        rect.set('y', f'{cy - h * self.scale / 2:.1f}')
        rect.set('width', f'{w * self.scale:.1f}')
        rect.set('height', f'{h * self.scale:.1f}')
        rect.set('class', 'dip-body')
        rect.set('rx', f'{10 * self.scale:.1f}')

        # Label with body ID
        label = ET.SubElement(g, 'text')
        label.set('x', f'{cx:.1f}')
        label.set('y', f'{cy:.1f}')
        label.set('class', 'body-label')
        label.set('font-size', f'{min(24, body_length // 4) * self.scale:.0f}')
        label.text = f'L{body.dip_lib_index}N{body.sequence_num}'

    def _render_2pin_body(self, g: ET.Element, body: PCBody) -> None:
        """Render a 2-pin component (resistor/capacitor)."""
        spacing = body.spacing_5mil * 5  # Convert to mils

        cx = self._sx(body.loc[0])
        cy = self._sy(body.loc[1])

        # Small rectangle centered on body location
        w = max(spacing, 60) * self.scale
        h = 40 * self.scale

        if body.orientation in (1, 3):
            w, h = h, w

        rect = ET.SubElement(g, 'rect')
        rect.set('x', f'{cx - w / 2:.1f}')
        rect.set('y', f'{cy - h / 2:.1f}')
        rect.set('width', f'{w:.1f}')
        rect.set('height', f'{h:.1f}')
        rect.set('class', 'dip-body')

    def _render_labels(self, svg: ET.Element) -> None:
        """Render text annotations from points."""
        g = ET.SubElement(svg, 'g')
        g.set('id', 'labels')

        for pt in self.pc.all_points:
            if pt.text_size == 0 or not pt.text:
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
                  scale: float = 1.0, margin: int = 200) -> None:
    """Render a parsed PCFile to SVG.

    Args:
        pc: Parsed PC board layout
        output_path: Path for the output SVG file
        crd: Optional card definition for board outline
        scale: Scale factor (1.0 = 1 mil per SVG unit)
        margin: Margin around the board in mils
    """
    renderer = PCSVGRenderer(pc, crd=crd, scale=scale, margin=margin)
    renderer.render(output_path)


def render_pc_html(pc: PCFile, output_path: str | Path,
                   crd: CRDFile | None = None,
                   scale: float = 1.0, margin: int = 200) -> None:
    """Render a parsed PCFile to an interactive HTML file with layer toggles.

    Produces an HTML file embedding the SVG with checkboxes to toggle
    visibility of each layer group.
    """
    import io

    # Generate SVG content
    renderer = PCSVGRenderer(pc, crd=crd, scale=scale, margin=margin)
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
    bg.set('fill', '#1A1A1A')

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

    # Layer definitions for toggle controls
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

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SUDS PC Board: {board_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: #111; color: #eee; font-family: 'Consolas', 'Monaco', monospace; }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 16px 24px;
            border-bottom: 1px solid #333;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .header h1 {{ font-size: 18px; color: #e94560; }}
        .header .stats {{ font-size: 12px; color: #888; }}
        .controls {{
            background: #1a1a2e;
            padding: 12px 24px;
            display: flex; gap: 16px; flex-wrap: wrap;
            border-bottom: 1px solid #222;
        }}
        .layer-toggle {{
            display: flex; align-items: center; gap: 6px;
            font-size: 13px; cursor: pointer;
        }}
        .layer-toggle input {{ cursor: pointer; }}
        .svg-container {{
            overflow: auto; padding: 20px;
            display: flex; justify-content: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SUDS PC Board: {board_name}</h1>
        <div class="stats">
            {len(pc.bodies)} bodies | {s1_pts} side1 pts | {s2_pts} side2 pts | {ft} vias | v{pc.version}
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
