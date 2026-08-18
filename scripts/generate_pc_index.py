#!/usr/bin/env python3
"""Generate an HTML index page for rendered SUDS PC board files.

Scans data/pc_boards/ for rendered board HTML files, collects metadata
from the source PC files, and generates an interactive index page
grouped by card form factor.

Usage:
    python3 scripts/generate_pc_index.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.unpack import read_file
from src.pc_parser import PCParser
from src.crd_parser import parse_crd_file
from src.dip_type_map import build_dip_type_map


# ── Data source maps (shared with render_pc_boards.py) ──────────────

PRT_MAP = {
    '25': '25.prt', '60': '60.prt',
    'a': 'a.prt', 'b': 'b.prt', 'back': 'back.prt',
    'cg': 'cg.prt', 'd': 'd.prt',
    'em': 'em.prt', 'ep': 'ep.prt', 'ev': 'ev.prt',
    'f': 'f.prt', 'fm': 'fm.prt', 'foo': 'foo.prt',
    'g': 'g.prt',
    'm1': 'm1.prt', 'm11': 'm11.prt', 'm16': 'm16.prt',
    'p': 'p.prt', 'pc': 'pc.prt',
    'q': 'q.prt', 'sio': 'sio.prt',
    'ti': 'ti.prt', 've1': 've1.prt',
    'vme3x2': 'vme3x2.prt',
    'vmem': 'vmem.prt', 'vmep': 'vmep.prt', 'vmes': 'vmes.prt',
    'vmxpig': 'vmxpig.prt',
    'x': 'x.prt', 'xc': 'xc.prt', 'xm': 'xm.prt',
    'xx': 'xx.prt', 'xy': 'xy.prt', 'y': 'y.prt',
}

STF_MAP = {
    'a': 'a.stf', 'cg': 'cg.stf',
    'foo': 'foo.stf', 'g': 'g.stf',
    'mouse': 'mouse.stf', 'p': 'p.stf', 'q': 'q.stf',
    'sio': 'sio.stf',
    'vme3x2': 'vme3x2.stf', 'vmxpig': 'vmxpig.stf',
    'x': 'x.stf', 'y': 'y.stf',
}

NO_CRD_BOARDS = {
    'mouse', 'mousef', 'mupac', 'msilk', 'm2silk',
    'm2sola', 'ether', 'ratsht', 'a20', 'ax', 'back', 'p', 'mouse2',
    'vmemb',  # Corrupt data: S2 X-shifted, non-45° traces
}

CRD_OVERRIDES: dict[str, str | None] = {'mouse2': None}

CRD_LABELS = {
    'multi0.crd.O': 'Multibus',
    'vme.crd.O': 'VME',
    'vme3x2.crd.O': 'VME 3U×2',
    'vmx.crd.O': 'VMX',
    'e220.crd.O': 'Eurocard 220mm',
    'e280.crd.O': 'Eurocard 280mm',
    'at.crd.O': 'AT Card',
}

# Form factor display order
FF_ORDER = ['VME 3U×2', 'Multibus', 'VME', 'Eurocard 280mm', 'AT Card', 'No Card Outline']


def extract_board_title(name: str, smi_dir: Path) -> str:
    """Extract a human-readable board description from the PRT file."""
    if name not in PRT_MAP:
        return ''
    prt_path = smi_dir / PRT_MAP[name]
    if not prt_path.exists():
        return ''

    keywords = {'SUN', 'SMI', 'FERRARI', 'TAPE', 'MEMORY', 'GRAPHICS',
                'ETHERNET', 'VIDEO', 'MOUSE', 'CPU', 'COLOR', 'SCSI',
                'SERIAL', 'DISK', 'TIMER', 'FRAME', 'DATA', 'NETWORK',
                'CONNECTORS', 'INTERFACE'}
    prefixes = [
        'PROPRIETARY SMI, ', '(C) 1982 MSI, ', '(C) 1982 SMI, ',
        '(C) 1982 MSI ', '(C) 1983 SMI, ', '(C) 1984 SMI, ',
        '(C) 1985 SMI, ', '(C) 1986 SMI, ', 'PROPRIETARY ',
    ]

    with open(prt_path) as fp:
        lines = fp.readlines()
    for line in lines[6:15]:
        upper = line.upper()
        if any(kw in upper for kw in keywords):
            title = line.strip().split('\t')[0].strip()
            for prefix in prefixes:
                if title.startswith(prefix):
                    title = title[len(prefix):]
            return title.rstrip(',').strip()
    return ''


def auto_detect_crd(pc, crd_list):
    """Find smallest CRD that fits this board's components."""
    bx = [b.loc[0] for b in pc.bodies if abs(b.loc[0]) < 50000]
    by = [b.loc[1] for b in pc.bodies if abs(b.loc[1]) < 50000]
    if not bx or len(pc.bodies) < 3:
        return None
    for crd_name, crd, area in crd_list:
        ox = [p[0] for p in crd.outline]
        oy = [p[1] for p in crd.outline]
        orig = crd.pc_origin
        if max(bx) + orig[0] <= max(ox) + 50 and max(by) + orig[1] <= max(oy) + 50:
            return crd_name
    return None


def generate_index(boards: list[dict], output_path: Path) -> None:
    """Generate the HTML index page."""
    # Group by form factor
    groups: dict[str, list[dict]] = {}
    for b in boards:
        ff = b['crd_label'] or 'No Card Outline'
        groups.setdefault(ff, []).append(b)

    sorted_groups = []
    for ff in FF_ORDER:
        if ff in groups:
            sorted_groups.append((ff, groups.pop(ff)))
    for ff in sorted(groups.keys()):
        sorted_groups.append((ff, groups[ff]))

    total_bodies = sum(b['bodies'] for b in boards)
    total_pts = sum(b['s1_pts'] + b['s2_pts'] for b in boards)

    crd_css = {
        'Multibus': 'crd-multi', 'VME': 'crd-vme', 'VME 3U×2': 'crd-vme3',
        'Eurocard 220mm': 'crd-euro', 'Eurocard 280mm': 'crd-euro',
        'AT Card': 'crd-at', 'No Card Outline': 'crd-none',
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SUDS PC Board Index — {len(boards)} Boards</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0a0a0a; color: #ddd;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            line-height: 1.5;
        }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            padding: 32px 40px; border-bottom: 2px solid #e94560;
        }}
        .header h1 {{ font-size: 28px; color: #fff; font-weight: 300; letter-spacing: 1px; margin-bottom: 8px; }}
        .header h1 span {{ color: #e94560; font-weight: 600; }}
        .header .subtitle {{ font-size: 14px; color: #8899aa; }}
        .stats-bar {{
            background: #111; padding: 12px 40px;
            display: flex; gap: 32px; font-size: 13px; color: #888;
            border-bottom: 1px solid #222;
        }}
        .stats-bar .val {{ color: #e94560; font-weight: 600; }}
        .content {{ padding: 24px 40px 60px; }}
        .form-factor {{ margin-bottom: 32px; }}
        .ff-header {{
            font-size: 18px; color: #5dade2; font-weight: 500;
            margin-bottom: 12px; padding-bottom: 6px;
            border-bottom: 1px solid #2a2a3a;
            display: flex; align-items: baseline; gap: 12px;
        }}
        .ff-header .count {{ font-size: 12px; color: #666; font-weight: 400; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
        th {{
            text-align: left; padding: 8px 12px;
            background: #1a1a2a; color: #8899aa;
            font-weight: 500; font-size: 11px;
            text-transform: uppercase; letter-spacing: 0.5px;
            border-bottom: 1px solid #333;
            position: sticky; top: 0;
        }}
        td {{ padding: 7px 12px; border-bottom: 1px solid #1a1a1a; }}
        tr:hover td {{ background: #151525; }}
        .board-link {{ color: #e94560; text-decoration: none; font-weight: 600; font-size: 14px; }}
        .board-link:hover {{ color: #ff6b81; text-decoration: underline; }}
        .title-col {{ color: #aaa; max-width: 280px; }}
        .num {{ text-align: right; font-family: 'Consolas','Monaco',monospace; color: #bbb; }}
        .dim {{ color: #777; font-family: 'Consolas','Monaco',monospace; font-size: 12px; }}
        .src {{ font-size: 11px; }}
        .src span {{ display: inline-block; padding: 1px 6px; border-radius: 3px; margin-right: 3px; font-family: monospace; }}
        .src .prt {{ background: #1a3a2a; color: #4ade80; }}
        .src .wd  {{ background: #2a2a1a; color: #fbbf24; }}
        .src .stf {{ background: #1a2a3a; color: #60a5fa; }}
        .src .dip {{ background: #2a1a2a; color: #c084fc; }}
        .crd-tag {{ font-size: 11px; padding: 2px 8px; border-radius: 3px; font-family: monospace; }}
        .crd-multi {{ background: #2a1a1a; color: #f87171; }}
        .crd-vme   {{ background: #1a2a1a; color: #4ade80; }}
        .crd-vme3  {{ background: #1a3a1a; color: #22c55e; }}
        .crd-euro  {{ background: #1a1a3a; color: #818cf8; }}
        .crd-at    {{ background: #3a2a1a; color: #fb923c; }}
        .crd-none  {{ background: #1a1a1a; color: #555; }}
        .filter-bar {{ margin-bottom: 16px; display: flex; gap: 12px; align-items: center; }}
        .filter-bar input {{
            background: #1a1a2a; border: 1px solid #333; color: #ddd;
            padding: 8px 14px; border-radius: 6px; font-size: 14px;
            width: 300px; outline: none;
        }}
        .filter-bar input:focus {{ border-color: #e94560; }}
        .filter-bar .count-display {{ font-size: 13px; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SUDS <span>PC Board</span> Index</h1>
        <div class="subtitle">Stanford University Drawing System — Sun Microsystems PCB Layout Archive</div>
    </div>
    <div class="stats-bar">
        <span>Boards: <span class="val">{len(boards)}</span></span>
        <span>Components: <span class="val">{total_bodies:,}</span></span>
        <span>Trace Points: <span class="val">{total_pts:,}</span></span>
        <span>Form Factors: <span class="val">{len([g for g in sorted_groups if g[0] != 'No Card Outline'])}</span></span>
    </div>
    <div class="content">
        <div class="filter-bar">
            <input type="text" id="search" placeholder="Filter boards..." oninput="filterBoards(this.value)">
            <span class="count-display" id="filter-count"></span>
        </div>
"""

    for ff_name, ff_boards in sorted_groups:
        css_cls = crd_css.get(ff_name, 'crd-none')
        html += f"""
        <div class="form-factor" data-ff="{ff_name}">
            <div class="ff-header">
                <span class="crd-tag {css_cls}">{ff_name}</span>
                <span class="count">{len(ff_boards)} board{'s' if len(ff_boards) != 1 else ''}</span>
            </div>
            <table>
                <tr>
                    <th>Board</th><th>Description</th>
                    <th style="text-align:right">Bodies</th>
                    <th style="text-align:right">S1 Pts</th>
                    <th style="text-align:right">S2 Pts</th>
                    <th style="text-align:right">Vias</th>
                    <th>Size</th><th>Data Sources</th><th>Ver</th>
                </tr>
"""
        for b in sorted(ff_boards, key=lambda x: x['name']):
            srcs = []
            if b['prt']: srcs.append(f'<span class="prt">PRT {b["prt"]}</span>')
            if b['wd']:  srcs.append(f'<span class="wd">WD {b["wd"]}</span>')
            if b['stf']: srcs.append(f'<span class="stf">STF {b["stf"]}</span>')
            if not srcs:  srcs.append('<span class="dip">DIP lib</span>')

            html += f"""                <tr class="board-row" data-name="{b['name']}" data-title="{b['title'].lower()}">
                    <td><a class="board-link" href="{b['name']}_board.html">{b['name']}</a></td>
                    <td class="title-col">{b['title']}</td>
                    <td class="num">{b['bodies']}</td>
                    <td class="num">{b['s1_pts']:,}</td>
                    <td class="num">{b['s2_pts']:,}</td>
                    <td class="num">{b['vias']}</td>
                    <td class="dim">{b['w_in']}×{b['h_in']}"</td>
                    <td class="src">{' '.join(srcs)}</td>
                    <td class="dim">v{b['version']}</td>
                </tr>
"""
        html += """            </table>
        </div>
"""

    html += """
    </div>
    <script>
        function filterBoards(query) {
            const q = query.toLowerCase();
            const rows = document.querySelectorAll('.board-row');
            let visible = 0;
            rows.forEach(r => {
                const match = r.dataset.name.includes(q) || r.dataset.title.includes(q);
                r.style.display = match ? '' : 'none';
                if (match) visible++;
            });
            document.querySelectorAll('.form-factor').forEach(ff => {
                const vis = ff.querySelectorAll('.board-row:not([style*="display: none"])');
                ff.style.display = vis.length ? '' : 'none';
            });
            document.getElementById('filter-count').textContent =
                q ? `${visible} of ${rows.length} boards` : '';
        }
    </script>
</body>
</html>
"""
    output_path.write_text(html, encoding='utf-8')


def main():
    smi_dir = PROJECT_ROOT / '..' / 'smi'
    octal_dir = smi_dir / 'octal'
    output_dir = PROJECT_ROOT / 'data' / 'pc_boards'

    # Load CRD files sorted by area
    crd_list = []
    for f in sorted(octal_dir.iterdir()):
        if f.name.endswith('.crd.O'):
            try:
                crd = parse_crd_file(str(f))
                ox = [p[0] for p in crd.outline]
                oy = [p[1] for p in crd.outline]
                area = (max(ox) - min(ox)) * (max(oy) - min(oy))
                crd_list.append((f.name, crd, area))
            except Exception:
                pass
    crd_list.sort(key=lambda x: x[2])

    # Collect metadata for all rendered boards
    boards = []
    pc_files = sorted(f.name for f in octal_dir.iterdir() if f.name.endswith('.pc.O'))

    for f in pc_files:
        name = f.replace('.pc.O', '')
        html_file = output_dir / f'{name}_board.html'
        if not html_file.exists():
            continue

        pc = PCParser(read_file(str(octal_dir / f)), source_path=f).parse()

        bx = [b.loc[0] for b in pc.bodies if abs(b.loc[0]) < 50000]
        by = [b.loc[1] for b in pc.bodies if abs(b.loc[1]) < 50000]

        # Detect CRD
        crd_name = None
        if name not in NO_CRD_BOARDS and name not in CRD_OVERRIDES:
            crd_name = auto_detect_crd(pc, crd_list)
        elif name in CRD_OVERRIDES:
            crd_name = CRD_OVERRIDES[name]

        # DIP type counts
        stf = smi_dir / STF_MAP[name] if name in STF_MAP else None
        prt = smi_dir / PRT_MAP[name] if name in PRT_MAP else None
        if stf and not stf.exists(): stf = None
        if prt and not prt.exists(): prt = None
        dip = build_dip_type_map(name, str(octal_dir),
                                 stf_path=str(stf) if stf else None,
                                 prt_path=str(prt) if prt else None)

        boards.append({
            'name': name,
            'bodies': len(pc.bodies),
            's1_pts': len(pc.side1_points),
            's2_pts': len(pc.side2_points),
            'vias': len(pc.feed_through_pairs),
            'w_in': round((max(bx) - min(bx)) / 1000, 1) if bx else 0,
            'h_in': round((max(by) - min(by)) / 1000, 1) if by else 0,
            'crd': crd_name,
            'crd_label': CRD_LABELS.get(crd_name, '') if crd_name else '',
            'prt': dip.prt_count,
            'wd': dip.wd_count,
            'stf': dip.stf_count,
            'version': pc.version,
            'title': extract_board_title(name, smi_dir),
        })

    index_path = output_dir / 'index.html'
    generate_index(boards, index_path)
    print(f'Index: {index_path}  ({len(boards)} boards)')


if __name__ == '__main__':
    main()
