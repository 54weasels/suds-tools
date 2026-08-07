#!/usr/bin/env python3
"""Build a comprehensive version index of ALL DRW files across octal/ and prev/.

Scans every .drw.O and .drw.N.O file, extracts metadata (board designator,
page number, of total, date, size, body count), and produces a complete
version catalog for use by the coherence algorithm.

Output: data/drw_version_index.json
"""
import glob
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.drw_parser import parse_drw_file
from src.version_coherence import extract_board_designator


def scan_all_drw_files(octal_dir, prev_dir):
    """Scan all DRW files and extract metadata."""

    entries = []  # List of {basename, version, filepath, metadata...}
    errors = []

    # 1. Scan octal/ (latest versions)
    octal_files = sorted(glob.glob(os.path.join(octal_dir, '*.drw.O')))
    print(f"Scanning {len(octal_files)} files in octal/...")

    for i, fpath in enumerate(octal_files):
        if (i + 1) % 100 == 0:
            print(f"  [{i+1}/{len(octal_files)}]...")
        fname = os.path.basename(fpath)
        basename = fname.replace('.drw.O', '')

        entry = _extract_metadata(fpath, basename, version='latest')
        if entry:
            entries.append(entry)
        else:
            errors.append(fname)

    # 2. Scan prev/ (older versions)
    prev_files = sorted(glob.glob(os.path.join(prev_dir, '*.drw.*.O')))
    print(f"Scanning {len(prev_files)} files in prev/...")

    for i, fpath in enumerate(prev_files):
        if (i + 1) % 200 == 0:
            print(f"  [{i+1}/{len(prev_files)}]...")
        fname = os.path.basename(fpath)

        # Parse: basename.drw.N.O
        m = re.match(r'^(.+)\.drw\.(\d+)\.O$', fname)
        if not m:
            continue
        basename = m.group(1)
        version = int(m.group(2))

        entry = _extract_metadata(fpath, basename, version=version)
        if entry:
            entries.append(entry)
        else:
            errors.append(fname)

    return entries, errors


def _extract_metadata(fpath, basename, version):
    """Extract metadata from a single DRW file."""
    try:
        stat = os.stat(fpath)
        file_date = time.strftime('%Y-%m-%d', time.localtime(stat.st_mtime))
        file_size = stat.st_size

        drw = parse_drw_file(fpath, debug=False)
        t = drw.trailer

        if not t:
            return None

        title1 = (getattr(t, 'title_line_1', '') or '').strip()
        title2 = (getattr(t, 'title_line_2', '') or '').strip()
        page = str(getattr(t, 'page', '') or '').strip()
        of_str = str(getattr(t, 'of_string', '') or '').strip()

        # Parse integers
        try:
            page_int = int(re.match(r'(\d+)', page).group(1)) if page else 0
        except (AttributeError, ValueError):
            page_int = 0

        try:
            of_int = int(re.match(r'(\d+)', of_str).group(1)) if of_str else 0
        except (AttributeError, ValueError):
            of_int = 0

        desig = extract_board_designator(title1, title2)
        n_bodies = len(getattr(drw, 'body_placements', []))
        n_points = len(getattr(drw, 'points', []))

        # Extract page prefix (letters before digits)
        prefix_m = re.match(r'^([a-zA-Z]+)', basename)
        prefix = prefix_m.group(1).lower() if prefix_m else basename.lower()

        return {
            'basename': basename,
            'version': version,
            'filepath': fpath,
            'prefix': prefix,
            'file_date': file_date,
            'file_size': file_size,
            'page_num': page_int,
            'of_total': of_int,
            'title_line_1': title1,
            'title_line_2': title2,
            'board_designator': desig,
            'bodies': n_bodies,
            'points': n_points,
        }
    except Exception:
        return None


def build_version_catalog(entries):
    """Organize entries into a catalog by basename, showing all versions."""

    catalog = {}  # basename -> [versions sorted newest first]

    for e in entries:
        bn = e['basename']
        if bn not in catalog:
            catalog[bn] = []
        catalog[bn].append(e)

    # Sort each basename's versions: 'latest' first, then by version number desc
    for bn in catalog:
        def sort_key(e):
            if e['version'] == 'latest':
                return (1, 9999)
            return (0, e['version'])
        catalog[bn].sort(key=sort_key, reverse=True)

    return catalog


def find_all_board_sets(catalog, wl_authority):
    """For each board prefix, find ALL possible revisions across all versions.

    This considers every version of every page, not just the latest.
    """

    # Group by prefix
    by_prefix = {}
    for bn, versions in catalog.items():
        for v in versions:
            pfx = v['prefix']
            if pfx not in by_prefix:
                by_prefix[pfx] = []
            by_prefix[pfx].append(v)

    # For each prefix, find unique (designator, of_total) pairs
    board_sets = {}
    for pfx, all_versions in sorted(by_prefix.items()):
        combos = {}  # (desig, of) -> [page entries]
        for v in all_versions:
            if v['of_total'] <= 0:
                continue
            desig = v['board_designator'].upper().strip() or '(unknown)'
            key = (desig, v['of_total'])
            if key not in combos:
                combos[key] = []
            combos[key].append(v)

        if combos:
            board_sets[pfx] = combos

    return board_sets


def main():
    octal_dir = '/Users/dmoisa/Documents/sun/smi/smi/octal'
    prev_dir = '/Users/dmoisa/Documents/sun/smi/smi/prev'
    output_path = '/Users/dmoisa/Documents/sun/smi/suds-tools/data/drw_version_index.json'
    wl_path = '/Users/dmoisa/Documents/sun/smi/suds-tools/data/wl_authority.json'

    t0 = time.time()
    entries, errors = scan_all_drw_files(octal_dir, prev_dir)
    elapsed = time.time() - t0

    print(f"\nScanned {len(entries)} files in {elapsed:.1f}s ({len(errors)} errors)")

    # Build catalog
    catalog = build_version_catalog(entries)
    print(f"Catalog: {len(catalog)} unique base names")

    # Load WL authority
    wl_auth = {}
    if os.path.exists(wl_path):
        with open(wl_path) as f:
            wl_auth = json.load(f)

    # Find all board sets
    board_sets = find_all_board_sets(catalog, wl_auth)

    # Summary statistics
    total_revisions = sum(len(combos) for combos in board_sets.values())
    print(f"Board prefixes: {len(board_sets)}")
    print(f"Total (designator, of) combinations: {total_revisions}")

    # Show top-level summary
    print(f"\n{'Prefix':8} {'Revisions':>10}  Board Designators")
    print("-" * 90)
    for pfx, combos in sorted(board_sets.items()):
        desigs = sorted(set(k[0] for k in combos.keys()))
        desigs_str = ', '.join(d[:25] for d in desigs[:5])
        if len(desigs) > 5:
            desigs_str += f', ... +{len(desigs)-5} more'
        print(f"{pfx:8} {len(combos):>10}  {desigs_str}")

    # Save the full index (without filepath to keep size manageable)
    index_data = {
        'metadata': {
            'scan_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'octal_files': len([e for e in entries if e['version'] == 'latest']),
            'prev_files': len([e for e in entries if e['version'] != 'latest']),
            'total_entries': len(entries),
            'unique_basenames': len(catalog),
            'board_prefixes': len(board_sets),
            'total_revisions': total_revisions,
            'errors': len(errors),
        },
        'catalog': {},
    }

    # Save catalog with filepath made relative
    base_dir = '/Users/dmoisa/Documents/sun/smi/'
    for bn, versions in sorted(catalog.items()):
        index_data['catalog'][bn] = []
        for v in versions:
            entry = dict(v)
            # Make filepath relative
            if entry['filepath'].startswith(base_dir):
                entry['filepath'] = entry['filepath'][len(base_dir):]
            index_data['catalog'][bn].append(entry)

    with open(output_path, 'w') as f:
        json.dump(index_data, f, indent=2, default=str)

    print(f"\nIndex saved to {output_path}")
    fsize = os.path.getsize(output_path)
    print(f"Index size: {fsize / 1024:.0f} KB")


if __name__ == '__main__':
    main()
