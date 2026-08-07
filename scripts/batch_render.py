#!/usr/bin/env python3
"""Batch render SUDS DRW schematic files.

Renders DRW files organized by board, with optional PDF generation and HTML index.
"""
import argparse
import glob
import os
import re
import subprocess
import sys
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.board_registry import discover_boards, Board, BoardPage
from src.drw_parser import parse_drw_file
from src.svg_renderer import render_svg
from src.drw_model import BodyDefinition
from src.wl_parser import parse_wl_netlist
from src.version_coherence import (
    analyze_board_versions, VersionSet, _extract_page_versions,
    print_diagnostic_table
)
from collections import defaultdict



def build_designator_map(drw, wl_components):
    """Map DRW body_id -> designator from WL components for this page."""
    designators = {}
    
    # Group WL components by normalized type name
    wl_by_type = defaultdict(list)
    for comp in wl_components:
        key = comp.body.rstrip('\\').rstrip("'")
        wl_by_type[key].append(comp)
    
    # Group DRW bodies by normalized type name
    drw_by_type = defaultdict(list)
    for bp in drw.body_placements:
        key = bp.body_name.rstrip('\\').rstrip("'")
        drw_by_type[key].append(bp)
    
    # Match: zip WL designators with DRW bodies (sorted by body_id)
    for type_name, wl_comps in wl_by_type.items():
        drw_bodies = drw_by_type.get(type_name, [])
        if not drw_bodies:
            continue
        drw_bodies.sort(key=lambda bp: bp.body_id)
        wl_comps.sort(key=lambda c: c.number)
        
        if len(wl_comps) == 1 and len(drw_bodies) > 1:
            desig = wl_comps[0].designator
            for bp in drw_bodies:
                designators[bp.body_id] = desig
        else:
            for i, bp in enumerate(drw_bodies):
                if i < len(wl_comps):
                    designators[bp.body_id] = wl_comps[i].designator
    
    return designators


def _generate_index_html(board_results, total_pages, total_bodies):
    """Generate a self-contained HTML index page."""
    boards_html = ""
    for b_res in board_results:
        board = b_res['board']
        pages_html = ""
        for p in b_res['pages_stats']:
            if p.get('png_file'):
                pages_html += (
                    f'<div class="page-card">'
                    f'<a href="{board.board_id}/{p["svg_file"]}"><img src="{board.board_id}/{p["png_file"]}" alt="{p["page_name"]}"></a>'
                    f'<div><strong><a href="{board.board_id}/{p["svg_file"]}">{p["page_name"]}</a></strong></div>'
                    f'<div class="stats">{p["title"]}<br>{p["bodies"]} bodies, {p["points"]} points</div>'
                    f'</div>\n'
                )
            else:
                pages_html += (
                    f'<div class="page-card">'
                    f'<div><strong><a href="{board.board_id}/{p["svg_file"]}">{p["page_name"]}</a></strong></div>'
                    f'<div class="stats">{p["title"]}<br>{p["bodies"]} bodies, {p["points"]} points</div>'
                    f'</div>\n'
                )

        pdf_link = ""
        if b_res.get('pdf_generated'):
            pdf_link = f'<div><a href="{board.board_id}/{board.board_id}.pdf">📄 Download PDF</a></div>'

        boards_html += (
            f'<div class="board-section">'
            f'<h2>{board.name} <span class="stats">({len(b_res["pages_stats"])} pages)</span></h2>'
            f'{pdf_link}'
            f'<div class="pages-grid">{pages_html}</div>'
            f'</div>\n'
        )

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SUDS Schematic Boards</title>
<style>
body {{ font-family: sans-serif; background-color: #1a1a1a; color: #f0f0f0; margin: 40px; }}
h1, h2, h3 {{ color: #fff; }}
.board-section {{ margin-bottom: 40px; border: 1px solid #333; padding: 20px; border-radius: 8px; background-color: #222; }}
.pages-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 20px; margin-top: 20px; }}
.page-card {{ background: #333; padding: 15px; border-radius: 6px; }}
.page-card img {{ max-width: 100%; height: auto; border: 1px solid #444; border-radius: 4px; margin-bottom: 10px; }}
.stats {{ font-family: monospace; color: #aaa; font-size: 0.9em; margin-top: 5px; }}
a {{ color: #5fb1ff; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.summary {{ font-family: monospace; background: #222; padding: 20px; border-radius: 8px; border: 1px solid #333; margin-bottom: 30px; }}
</style>
</head>
<body>
<h1>SUDS Schematic Boards</h1>
<div class="summary">
    <div><strong>Total Boards:</strong> {len(board_results)}</div>
    <div><strong>Total Pages:</strong> {total_pages}</div>
    <div><strong>Total Bodies:</strong> {total_bodies}</div>
</div>
{boards_html}
</body>
</html>"""




def load_all_body_defs(drw_dir: str) -> dict:
    """Load ALL body definitions from every DRW file in a directory.
    
    Priority: DRW library defs always override synthetic DIP defs.
    """
    all_defs: dict[str, BodyDefinition] = {}
    synthetic_names: set[str] = set()
    files = sorted(glob.glob(os.path.join(drw_dir, '*.drw.O')))
    
    # Load synthetic DIPs as lowest-priority fallback
    try:
        from src.dip_generator import get_synthetic_defs
        synth = get_synthetic_defs()
        all_defs.update(synth)
        synthetic_names = set(synth.keys())
    except ImportError:
        pass
    
    parse_errors = []
    for f in files:
        try:
            drw = parse_drw_file(f, debug=False)
            for bd in drw.body_defs:
                if bd.name and bd.name.strip():
                    existing = all_defs.get(bd.name)
                    if existing is None:
                        all_defs[bd.name] = bd
                    elif bd.name in synthetic_names:
                        # Always override synthetic defs with real library defs
                        all_defs[bd.name] = bd
                        synthetic_names.discard(bd.name)
                    elif len(bd.pins) > len(existing.pins) or len(bd.lines) > len(existing.lines):
                        # Among real defs, prefer the one with more detail
                        all_defs[bd.name] = bd
        except Exception as e:
            parse_errors.append((os.path.basename(f), str(e)))
    
    if parse_errors:
        print(f"  {len(parse_errors)} files had parse errors (non-fatal)")
    
    return all_defs


def main():
    parser = argparse.ArgumentParser(description="Batch render SUDS DRW schematic boards")
    parser.add_argument("--dir", default="data/drw", help="DRW source directory (default: data/drw)")
    parser.add_argument("--wl-dir", default="data/wirelists", help="Wirelist directory (default: data/wirelists)")
    parser.add_argument("--output-dir", default="output/boards", help="Output root (default: output/boards)")
    parser.add_argument("--list", action="store_true", help="List boards and exit")
    parser.add_argument("--board", help="Render single board by slug ID")
    parser.add_argument("--all", action="store_true", help="Render all boards")
    parser.add_argument("--pdf", action="store_true", help="Generate multi-page PDF per board")
    parser.add_argument("--png", action="store_true", help="Generate PNG files")
    parser.add_argument("--index", action="store_true", help="Generate HTML index page")
    parser.add_argument("--png-width", type=int, default=3000, help="PNG width in pixels (default: 3000)")
    parser.add_argument("--versions", action="store_true",
                        help="Use coherence scoring to identify design revisions. "
                             "With --pdf, generates a separate PDF per revision, "
                             "with version number and score in the filename.")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.dir):
        print(f"Error: directory not found: {args.dir}")
        sys.exit(1)
        
    boards = discover_boards(args.dir, wl_dir=args.wl_dir)
    
    if args.list:
        print(f"Discovered {len(boards)} boards:")
        wl_count = sum(1 for b in boards if b.source == 'wirelist')
        md_count = sum(1 for b in boards if b.source == 'metadata')
        print(f"  ({wl_count} from wirelists, {md_count} from metadata fallback)\n")
        for b in boards:
            src = f"[{b.wirelist}.wl]" if b.wirelist else "[metadata]"
            print(f"  {b.board_id:30} {len(b.pages):>3}p  {src:15} {b.name}")
        return
        
    if not (args.all or args.board):
        parser.print_help()
        print("\nError: Must specify --all, --board SLUG, or --list")
        sys.exit(1)
        
    if args.board:
        boards = [b for b in boards if b.board_id == args.board]
        if not boards:
            print(f"Error: Board not found: {args.board}")
            sys.exit(1)
            
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"Loading body definitions from {args.dir}...")
    t0 = time.time()
    all_defs = load_all_body_defs(args.dir)
    print(f"Loaded {len(all_defs)} body definitions in {time.time() - t0:.1f}s")
    
    # Track stats for summary
    board_results = []
    total_pages_rendered = 0
    total_bodies_rendered = 0
    
    for board in boards:
        print(f"\nProcessing board: {board.name} ({board.board_id}) - {len(board.pages)} pages")
        board_dir = os.path.join(args.output_dir, board.board_id)
        os.makedirs(board_dir, exist_ok=True)
        
        wl_data = None
        if board.wirelist:
            wl_path = os.path.join(args.wl_dir, f"{board.wirelist}.wl")
            if os.path.exists(wl_path):
                try:
                    wl_data = parse_wl_netlist(wl_path)
                except Exception as e:
                    print(f"Warning: failed to parse wirelist {wl_path}: {e}")
        
        pages_stats = []
        svg_files_for_pdf = []
        
        for i, page in enumerate(board.pages, 1):
            print(f"  [{i}/{len(board.pages)}] {page.name}...", end=" ", flush=True)
            
            try:
                drw = parse_drw_file(page.filepath, debug=False)
                
                # Combine defs
                combined_defs = dict(all_defs)
                for bd in drw.body_defs:
                    combined_defs[bd.name] = bd
                    
                designators = {}
                if wl_data:
                    wl_comps = wl_data.components_on_page(page.name)
                    designators = build_designator_map(drw, wl_comps)
                    
                svg_out = render_svg(drw, combined_defs, designators=designators)
                svg_filename = f"{page.name}.svg"
                svg_path = os.path.join(board_dir, svg_filename)
                
                with open(svg_path, 'w') as f:
                    f.write(svg_out)
                    
                svg_files_for_pdf.append(svg_path)
                
                png_filename = None
                if args.png:
                    png_filename = f"{page.name}.png"
                    png_path = os.path.join(board_dir, png_filename)
                    subprocess.run(
                        ['rsvg-convert', '-w', str(args.png_width), svg_path, '-o', png_path],
                        check=True, capture_output=True
                    )
                
                title = ''
                if drw.trailer:
                    title = drw.trailer.title_line_1 or ''
                
                stats = {
                    'page_name': page.name,
                    'svg_file': svg_filename,
                    'png_file': png_filename,
                    'title': title.strip(),
                    'bodies': len(drw.body_placements),
                    'points': len(drw.points)
                }
                pages_stats.append(stats)
                
                total_pages_rendered += 1
                total_bodies_rendered += stats['bodies']
                print("OK")
                
            except Exception as e:
                print(f"FAILED: {e}")
                
        pdf_generated = False
        if args.pdf and svg_files_for_pdf:
            if args.versions:
                # Version-aware PDF: one per revision
                _render_versioned_pdfs(board, board_dir, all_defs, args)
                pdf_generated = True
            else:
                print(f"  Generating PDF for {board.board_id}...")
                pdf_path = os.path.join(board_dir, f"{board.board_id}.pdf")
                try:
                    subprocess.run(
                        ['rsvg-convert', '-f', 'pdf', '-o', pdf_path] + svg_files_for_pdf,
                        check=True, capture_output=True
                    )
                    pdf_generated = True
                except Exception as e:
                    print(f"  WARNING: PDF generation failed: {e}")
                
        board_results.append({
            'board': board,
            'pages_stats': pages_stats,
            'pdf_generated': pdf_generated,
            'total_bodies': sum(p['bodies'] for p in pages_stats),
            'status': '✅ OK' if len(pages_stats) == len(board.pages) else '❌ Errors'
        })
        
    # Generate HTML Index
    if args.index:
        print("\nGenerating HTML index...")
        index_html = _generate_index_html(board_results, total_pages_rendered, total_bodies_rendered)
        index_path = os.path.join(args.output_dir, "index.html")
        with open(index_path, 'w') as f:
            f.write(index_html)
        print(f"  Index written to {index_path}")
            
    # Print Summary Table
    print(f"\n  {'Board':<35} {'Pages':>7} {'Bodies':>8}  {'Status'}")
    print(f"  {'─'*35} {'─'*7} {'─'*8}  {'─'*8}")
    for b_res in board_results:
        b_name = b_res['board'].name[:35]
        print(f"  {b_name:<35} {len(b_res['pages_stats']):>7} {b_res['total_bodies']:>8}  {b_res['status']}")

def _render_versioned_pdfs(board, board_dir, all_defs, args):
    """Render separate PDFs for each design revision of a board.
    
    Uses the coherence algorithm to identify revisions based on board
    designator matching, then prints a diagnostic table and renders
    each revision as a separate PDF.
    """
    # Determine prefix from board_id
    prefix = board.board_id.rstrip('_0123456789')
    if not prefix:
        prefix = board.board_id
    
    # Get WL page count
    wl_count = None
    if board.wirelist:
        wl_path = os.path.join(args.wl_dir, f"{board.wirelist}.wl")
        if os.path.exists(wl_path):
            try:
                wl = parse_wl_netlist(wl_path)
                wl_count = len(set(c.page for c in wl.components))
            except Exception:
                pass
    
    # Run the analysis
    versions = analyze_board_versions(
        prefix, args.dir, wl_page_count=wl_count
    )
    
    if not versions:
        print(f"  No revisions found for prefix '{prefix}'")
        return
    
    # Print diagnostic table BEFORE rendering
    all_pages = _extract_page_versions(args.dir, prefix)
    print_diagnostic_table(prefix, all_pages, versions)
    
    # Render PDFs
    for vi, vs in enumerate(versions, 1):
        best_tag = " ★ BEST" if vs.is_best else ""
        print(f"  Rendering v{vi}: \"{vs.board_designator}\" of_{vs.of_total} "
              f"({len(vs.pages)}/{vs.of_total}p, score={vs.score:.2f}){best_tag}")
        
        # Render SVGs for this version's pages
        version_svgs = []
        for pv in vs.pages:
            svg_path = os.path.join(board_dir, f"{pv.name}.svg")
            if os.path.exists(svg_path):
                version_svgs.append(svg_path)
            else:
                try:
                    drw = parse_drw_file(pv.filepath, debug=False)
                    combined_defs = dict(all_defs)
                    for bd in drw.body_defs:
                        combined_defs[bd.name] = bd
                    svg_out = render_svg(drw, combined_defs)
                    with open(svg_path, 'w') as f:
                        f.write(svg_out)
                    version_svgs.append(svg_path)
                except Exception as e:
                    print(f"      Failed to render {pv.name}: {e}")
        
        if not version_svgs:
            continue
        
        # Generate PDF with version info in filename
        best_suffix = "_BEST" if vs.is_best else ""
        # Sanitize designator for filename
        desig_slug = re.sub(r'[^a-zA-Z0-9]+', '_', vs.board_designator).strip('_').lower()
        pdf_name = (f"{board.board_id}_v{vi}_{desig_slug}_of{vs.of_total}"
                    f"_s{vs.score:.0%}{best_suffix}.pdf")
        pdf_path = os.path.join(board_dir, pdf_name)
        
        try:
            subprocess.run(
                ['rsvg-convert', '-f', 'pdf', '-o', pdf_path] + version_svgs,
                check=True, capture_output=True
            )
            print(f"      → {pdf_name}")
        except subprocess.CalledProcessError:
            # Retry with reduced zoom for oversized SVGs
            rendered = False
            for zoom in ['0.5', '0.25']:
                try:
                    subprocess.run(
                        ['rsvg-convert', '-f', 'pdf', '-z', zoom, '-o', pdf_path] + version_svgs,
                        check=True, capture_output=True
                    )
                    print(f"      → {pdf_name} (zoom={zoom})")
                    rendered = True
                    break
                except subprocess.CalledProcessError:
                    continue
            if not rendered:
                print(f"      PDF failed for {pdf_name}")
        except Exception as e:
            print(f"      PDF failed: {e}")


if __name__ == "__main__":
    main()

