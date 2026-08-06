#!/usr/bin/env python3
"""Batch render Q-series SUDS DRW files to SVG and PNG.

Loads ALL body definitions from the entire best_drw/ directory
(every DRW file contributes its inline body defs as a shared library),
then renders each Q-series schematic page.

Usage:
    python3 scripts/render_q_series.py [--dir best_drw] [--output-dir output/q_series]
"""
import argparse
import glob
import os
import subprocess
import sys
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.drw_parser import parse_drw_file
from src.drw_model import BodyDefinition
from src.svg_renderer import render_svg


def load_all_body_defs(drw_dir: str) -> dict:
    """Load ALL body definitions from every DRW file in a directory.
    
    This gives us maximum body resolution — every inline body def
    from any schematic page is available as a shared library.
    
    Priority: DRW library defs always override synthetic DIP defs,
    because library defs have correct geometry while synthetics only
    approximate pin layout.
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


def render_file(drw_path: str, all_defs: dict, output_dir: str,
                make_png: bool = True, png_width: int = 3000) -> dict:
    """Render a single DRW file to SVG (and optionally PNG).
    
    Returns dict with stats about the rendering.
    """
    basename = os.path.basename(drw_path)
    name = basename.replace('.drw.O', '')
    
    svg_path = os.path.join(output_dir, f'{name}.svg')
    png_path = os.path.join(output_dir, f'{name}.png')
    
    # Parse
    drw = parse_drw_file(drw_path, debug=False)
    
    # Count resolved/unresolved bodies
    used_names = {bp.body_name for bp in drw.body_placements}
    # Inline defs from this file take priority
    combined = dict(all_defs)
    for bd in drw.body_defs:
        combined[bd.name] = bd
    
    resolved = sum(1 for n in used_names if n in combined)
    unresolved = [n for n in used_names if n not in combined and n.strip()]
    
    # Render SVG
    svg_out = render_svg(drw, all_defs)
    with open(svg_path, 'w') as f:
        f.write(svg_out)
    
    # Convert to PNG
    if make_png:
        try:
            subprocess.run(
                ['rsvg-convert', '-w', str(png_width), svg_path, '-o', png_path],
                check=True, capture_output=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"    WARNING: PNG conversion failed: {e}")
            png_path = None
    else:
        png_path = None
    
    title = ''
    page = ''
    if drw.trailer:
        title = drw.trailer.title_line_1 or ''
        page = drw.trailer.page or ''
    
    return {
        'name': name,
        'svg_path': svg_path,
        'png_path': png_path,
        'bodies': len(drw.body_placements),
        'points': len(drw.points),
        'resolved': resolved,
        'unresolved': unresolved,
        'title': title.strip(),
        'page': page,
    }


def main():
    parser = argparse.ArgumentParser(
        description='Batch render Q-series SUDS DRW files')
    parser.add_argument('--dir', default='best_drw',
                        help='Directory with best DRW files (default: best_drw)')
    parser.add_argument('--output-dir', default='output/q_series',
                        help='Output directory (default: output/q_series)')
    parser.add_argument('--no-png', action='store_true',
                        help='Skip PNG conversion')
    parser.add_argument('--all', action='store_true',
                        help='Render ALL files, not just Q-series')
    parser.add_argument('--png-width', type=int, default=3000,
                        help='PNG width in pixels (default: 3000)')
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load all body definitions from all files
    print(f"Loading all body definitions from {args.dir}/...")
    t0 = time.time()
    all_defs = load_all_body_defs(args.dir)
    t_load = time.time() - t0
    print(f"  {len(all_defs)} unique body definitions loaded in {t_load:.1f}s")
    
    # Find Q-series files
    if args.all:
        pattern = os.path.join(args.dir, '*.drw.O')
    else:
        # Q-series: q1-q9, q1b-q9b, qx1-qx9
        pattern = os.path.join(args.dir, 'q*.drw.O')
    
    files = sorted(glob.glob(pattern))
    if not files:
        print(f"No matching files found in {args.dir}/")
        return
    
    print(f"\nRendering {len(files)} files...\n")
    
    # Render each file
    results = []
    for i, fpath in enumerate(files, 1):
        name = os.path.basename(fpath).replace('.drw.O', '')
        print(f"  [{i}/{len(files)}] {name}...", end=' ', flush=True)
        t0 = time.time()
        
        try:
            result = render_file(fpath, all_defs, args.output_dir,
                                make_png=not args.no_png,
                                png_width=args.png_width)
            elapsed = time.time() - t0
            
            status = f"{result['bodies']} bodies, {result['points']} pts"
            if result['unresolved']:
                status += f", {len(result['unresolved'])} unresolved"
            print(f"OK ({elapsed:.1f}s) — {status}")
            results.append(result)
        except Exception as e:
            print(f"FAILED: {e}")
    
    # Summary
    print(f"\n{'='*70}")
    print(f"Rendered {len(results)}/{len(files)} files to {args.output_dir}/")
    print(f"{'='*70}")
    
    # Show any unresolved bodies
    all_unresolved = set()
    for r in results:
        all_unresolved.update(r['unresolved'])
    
    if all_unresolved:
        print(f"\nUnresolved body definitions ({len(all_unresolved)}):")
        for name in sorted(all_unresolved):
            files_needing = [r['name'] for r in results if name in r['unresolved']]
            print(f"  {name:20} needed by: {', '.join(files_needing)}")
    
    print(f"\nSummary:")
    print(f"  {'File':<10} {'Bodies':>7} {'Points':>7} {'Resolved':>9} {'Title'}")
    print(f"  {'─'*10} {'─'*7} {'─'*7} {'─'*9} {'─'*40}")
    for r in results:
        res_str = f"{r['resolved']}/{r['resolved']+len(r['unresolved'])}"
        title_short = r['title'][:40] if r['title'] else ''
        print(f"  {r['name']:<10} {r['bodies']:>7} {r['points']:>7} {res_str:>9} {title_short}")


if __name__ == '__main__':
    main()
