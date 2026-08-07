#!/usr/bin/env python3
"""Generate a provenance-rich HTML index for rendered SUDS boards.

Includes:
- Version recovery information (which files were replaced from version history)
- WL authority data (which wirelist defines the board)
- Coherence scoring breakdown
- Per-page provenance (source file, version, metadata)
"""
import argparse
import glob
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.drw_parser import parse_drw_file
from src.version_coherence import (
    analyze_board_versions, extract_board_designator,
    _extract_page_versions, print_diagnostic_table
)
from src.board_registry import discover_boards


def load_recovery_data(path='data/version_recovery.json'):
    """Load the version recovery report."""
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {'mismatches': [], 'summary': {}}


def load_wl_authority(path='data/wl_authority.json'):
    """Load the WL authority map."""
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def load_canonical_sets(path='data/canonical_board_sets.json'):
    """Load the canonical board sets analysis."""
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {'boards': {}, 'metadata': {}}


def load_manifest(path='data/drw_provenance_manifest.json'):
    """Load the provenance manifest (which version was actually used)."""
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
        # Build lookup: basename -> manifest entry
        return {e['basename']: e for e in data.get('files', [])}
    return {}

def generate_provenance_index(output_dir, drw_dir, wl_dir):
    """Generate the full provenance-rich HTML index."""

    boards = discover_boards(drw_dir, wl_dir=wl_dir)
    recovery = load_recovery_data()
    wl_auth = load_wl_authority()
    canonical = load_canonical_sets()
    manifest = load_manifest()

    canonical_meta = canonical.get('metadata', {})

    # Build recovery lookup: filename -> recovery info
    recovery_map = {}
    for m in recovery.get('mismatches', []):
        recovery_map[m['filename']] = m

    # Generate board sections
    board_sections = []
    total_pages = 0
    total_versions = 0

    for board in boards:
        prefix = board.board_id.rstrip('_0123456789')
        if not prefix:
            prefix = board.board_id

        # Get versions
        all_page_versions = _extract_page_versions(drw_dir, prefix)
        wl_count = None
        if board.wirelist:
            wl_data = wl_auth.get(board.wirelist, {})
            wl_count = wl_data.get('page_count')

        versions = analyze_board_versions(prefix, drw_dir, wl_page_count=wl_count)

        # Get WL page data for this board
        wl_pages = {}
        if board.wirelist and board.wirelist in wl_auth:
            wl_pages = wl_auth[board.wirelist].get('pages', {})

        # Build page rows
        page_rows = []
        for pv in sorted(all_page_versions, key=lambda x: x.page_num_int):
            # Find which version set this page belongs to
            assigned = None
            for vi, vs in enumerate(versions, 1):
                if pv in vs.pages:
                    assigned = vs
                    break

            # Check recovery status
            rec = recovery_map.get(f'{pv.name}.drw.O')
            recovery_note = ''
            if rec:
                old_title = rec.get('data_drw_meta', {}).get('title1', '')[:30]
                recovery_note = f'Recovered (was: "{old_title}")'

            # Check WL authority
            wl_info = wl_pages.get(pv.name.upper(), {})
            wl_note = ''
            if wl_info:
                wl_note = f'WL: {wl_info.get("board", "")} {wl_info.get("function", "")}'.strip()

            # Check provenance manifest (source version)
            mf = manifest.get(pv.name, {})
            source_note = ''
            if mf:
                ver = mf.get('version', 'latest')
                if ver != 'latest' and mf.get('action') == 'copied':
                    source_note = f'prev/v{ver}'
                elif mf.get('action') == 'copied':
                    source_note = 'latest (copied)'
                else:
                    source_note = 'latest'

            page_rows.append({
                'name': pv.name,
                'page': pv.page_num,
                'of': pv.of_total,
                'designator': pv.board_designator,
                'function': pv.page_function,
                'variant': pv.variant,
                'bodies': pv.bodies,
                'points': pv.points,
                'assigned_version': f'v{vi}' if assigned else '',
                'assigned_score': f'{assigned.score:.0%}' if assigned else '',
                'is_best': assigned.is_best if assigned else False,
                'recovery_note': recovery_note,
                'wl_note': wl_note,
                'source_note': source_note,
            })

        # Find PDFs
        board_dir = os.path.join(output_dir, board.board_id)
        pdfs = sorted(glob.glob(os.path.join(board_dir, '*.pdf'))) if os.path.isdir(board_dir) else []
        svgs = sorted(glob.glob(os.path.join(board_dir, '*.svg'))) if os.path.isdir(board_dir) else []

        total_pages += len(all_page_versions)
        total_versions += len(versions)

        board_sections.append({
            'board': board,
            'versions': versions,
            'page_rows': page_rows,
            'pdfs': pdfs,
            'svgs': svgs,
            'wl_name': board.wirelist or '',
        })

    # Generate HTML
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    rec_summary = recovery.get('summary', {})

    boards_html = ''
    for sec in board_sections:
        board = sec['board']
        versions = sec['versions']
        page_rows = sec['page_rows']
        pdfs = sec['pdfs']
        svgs = sec['svgs']

        # Version pills
        version_pills = ''
        for vi, vs in enumerate(versions, 1):
            best = ' best-version' if vs.is_best else ''
            star = ' ★' if vs.is_best else ''
            version_pills += (
                f'<span class="version-pill{best}">'
                f'v{vi} "{vs.board_designator}" '
                f'{len(vs.pages)}/{vs.of_total}p '
                f's={vs.score:.0%}{star}</span> '
            )

        # PDF links
        pdf_links = ''
        for pdf_path in pdfs:
            fname = os.path.basename(pdf_path)
            is_best = '_BEST' in fname
            cls = ' class="best-pdf"' if is_best else ''
            pdf_links += f'<a href="{board.board_id}/{fname}"{cls}>📄 {fname}</a><br>'

        # Page table
        page_table_rows = ''
        for pr in page_rows:
            cls = ' class="best-row"' if pr['is_best'] else ''
            recovery_td = f'<td class="recovery">{pr["recovery_note"]}</td>' if pr['recovery_note'] else '<td></td>'
            wl_td = f'<td class="wl-info">{pr["wl_note"]}</td>' if pr['wl_note'] else '<td></td>'
            svg_link = f'<a href="{board.board_id}/{pr["name"]}.svg">{pr["name"]}</a>'

            source_cls = ' class="from-prev"' if pr.get('source_note', '').startswith('prev/') else ''
            source_td = f'<td{source_cls}>{pr.get("source_note", "")}</td>'

            page_table_rows += (
                f'<tr{cls}>'
                f'<td>{svg_link}</td>'
                f'<td>{pr["page"]}/{pr["of"]}</td>'
                f'<td>{pr["designator"]}</td>'
                f'<td>{pr["function"]}</td>'
                f'<td>{pr["bodies"]}</td>'
                f'<td>{pr["assigned_version"]}</td>'
                f'<td>{pr["assigned_score"]}</td>'
                f'{source_td}'
                f'{recovery_td}'
                f'{wl_td}'
                f'</tr>\n'
            )

        boards_html += f'''
<div class="board-section" id="{board.board_id}">
    <h2>{board.name} <span class="board-id">({board.board_id})</span></h2>
    <div class="board-meta">
        <div><strong>Wirelist:</strong> {sec['wl_name'] or 'none'}</div>
        <div><strong>Pages:</strong> {len(page_rows)}</div>
        <div class="versions-row">{version_pills}</div>
    </div>
    <div class="pdf-links">{pdf_links}</div>
    <table class="page-table">
        <thead>
            <tr>
                <th>Page</th><th>Pg/Of</th><th>Board Designator</th><th>Function</th>
                <th>Bodies</th><th>Version</th><th>Score</th>
                <th>Source</th><th>Recovery</th><th>WL Authority</th>
            </tr>
        </thead>
        <tbody>{page_table_rows}</tbody>
    </table>
</div>
'''

    # Navigation
    nav_links = ''
    for sec in board_sections:
        b = sec['board']
        best = ''
        if sec['versions']:
            bv = sec['versions'][0]
            best = f' ({bv.board_designator} {bv.score:.0%})'
        nav_links += f'<a href="#{b.board_id}">{b.board_id}{best}</a> '

    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SUDS Schematic Board Index — with Provenance</title>
<style>
body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 20px 40px; }}
h1 {{ color: #f0f6fc; border-bottom: 2px solid #30363d; padding-bottom: 15px; }}
h2 {{ color: #f0f6fc; margin: 0 0 10px 0; }}

.summary {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px; padding: 20px; background: #161b22; border: 1px solid #30363d;
    border-radius: 8px; margin-bottom: 25px;
}}
.summary-item {{ text-align: center; }}
.summary-item .value {{ font-size: 2em; color: #58a6ff; font-weight: bold; }}
.summary-item .label {{ color: #8b949e; font-size: 0.9em; }}

.nav {{ background: #161b22; padding: 15px; border-radius: 8px; margin-bottom: 20px;
        border: 1px solid #30363d; line-height: 2; }}
.nav a {{ color: #58a6ff; margin-right: 10px; font-size: 0.85em; }}

.board-section {{
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 20px; margin-bottom: 25px;
}}
.board-id {{ color: #8b949e; font-size: 0.7em; }}
.board-meta {{ display: flex; gap: 20px; color: #8b949e; font-size: 0.9em; margin-bottom: 10px; flex-wrap: wrap; }}

.version-pill {{
    display: inline-block; padding: 3px 10px; border-radius: 12px;
    background: #21262d; border: 1px solid #30363d; font-size: 0.8em;
    color: #c9d1d9; margin: 2px;
}}
.version-pill.best-version {{
    background: #1b3826; border-color: #238636; color: #3fb950; font-weight: bold;
}}

.pdf-links {{ margin: 10px 0; }}
.pdf-links a {{ color: #58a6ff; margin-right: 15px; }}
.pdf-links a.best-pdf {{ color: #3fb950; font-weight: bold; }}

.page-table {{ width: 100%; border-collapse: collapse; font-size: 0.85em; margin-top: 10px; }}
.page-table th {{ background: #21262d; color: #f0f6fc; padding: 8px 10px; text-align: left; border-bottom: 2px solid #30363d; }}
.page-table td {{ padding: 5px 10px; border-bottom: 1px solid #21262d; }}
.page-table tr:hover {{ background: #1c2128; }}
.page-table tr.best-row {{ background: #1b3826; }}

.recovery {{ color: #d29922; font-size: 0.85em; }}
.wl-info {{ color: #79c0ff; font-size: 0.85em; }}
.from-prev {{ color: #d2a8ff; font-size: 0.85em; font-weight: bold; }}

.provenance-note {{
    background: #1c2128; border: 1px solid #30363d; border-radius: 6px;
    padding: 15px; margin-bottom: 20px; font-size: 0.9em; color: #8b949e;
}}
.provenance-note strong {{ color: #c9d1d9; }}

footer {{ margin-top: 40px; padding: 20px; color: #484f58; font-size: 0.85em; text-align: center; border-top: 1px solid #21262d; }}
</style>
</head>
<body>
<h1>🔧 SUDS Schematic Board Index</h1>

<div class="summary">
    <div class="summary-item"><div class="value">{len(board_sections)}</div><div class="label">Boards</div></div>
    <div class="summary-item"><div class="value">{total_pages}</div><div class="label">Total Pages</div></div>
    <div class="summary-item"><div class="value">{total_versions}</div><div class="label">Version Sets</div></div>
    <div class="summary-item"><div class="value">{canonical_meta.get('source_files', 0)}</div><div class="label">Source Files Indexed</div></div>
    <div class="summary-item"><div class="value">{canonical_meta.get('total_board_sets', 0)}</div><div class="label">Canonical Board Sets</div></div>
    <div class="summary-item"><div class="value">{canonical_meta.get('sets_using_prev_versions', 0)}</div><div class="label">Sets Using Prev/</div></div>
</div>

<div class="provenance-note">
    <strong>Provenance Information</strong><br>
    Generated: {timestamp}<br>
    Source: SAILDART SMI archive — {canonical_meta.get('source_files', 0)} DRW files indexed across octal/ and prev/ directories.<br>
    Grouping: Designator-first coherence algorithm — board identity from title block has maximum weight (0.35).<br>
    WL Authority: {len(wl_auth)} wirelists parsed for per-page board assignment.<br>
    Version Selection: Best version per page selected from all available versions (latest + history).<br>
    Scoring: Score = 0.35×C_desig + 0.20×C_of + 0.20×C_coverage + 0.15×C_wl + 0.10×C_size
</div>

<div class="nav"><strong>Boards:</strong> {nav_links}</div>

{boards_html}

<footer>
    SUDS (Stanford University Drawing System) Schematic Archive — Sun Microsystems Inc.<br>
    Recovered from SAILDART [1,SMI] archive. Algorithm: designator-first coherence scoring v2.<br>
    {timestamp}
</footer>
</body>
</html>'''

    return html


def main():
    parser = argparse.ArgumentParser(description="Generate provenance-rich HTML index")
    parser.add_argument("--output-dir", default="output/boards", help="Board output directory")
    parser.add_argument("--drw-dir", default="data/drw", help="DRW source directory")
    parser.add_argument("--wl-dir", default="data/wirelists", help="Wirelist directory")
    parser.add_argument("-o", "--output", default="output/boards/index.html", help="Output HTML file")

    args = parser.parse_args()

    print(f"Generating provenance index...")
    html = generate_provenance_index(args.output_dir, args.drw_dir, args.wl_dir)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(html)

    print(f"Index written to {args.output}")


if __name__ == "__main__":
    main()
