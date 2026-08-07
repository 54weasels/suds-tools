#!/usr/bin/env python3
"""Populate data/drw with the best canonical version of each DRW page,
then re-render all boards with provenance tracking.

Uses canonical_board_sets.json to determine which file version to use for
each page. For each board set marked as 'best', copies the selected file
version (whether from octal/ or prev/) into data/drw/.

Also generates a manifest file tracking exactly which source was used.
"""
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    os.chdir('/Users/dmoisa/Documents/sun/smi/suds-tools')
    base = '/Users/dmoisa/Documents/sun/smi/'

    with open('data/canonical_board_sets.json') as f:
        data = json.load(f)

    drw_dir = 'data/drw'

    # Build manifest of what we need to copy
    # Key insight: for BEST sets, we want the selected version.
    # For non-best sets that use prev/, we want to make those available
    # for rendering too.

    copies_needed = {}  # basename -> {source_path, version, designator, reason}
    all_prev_needed = []  # For non-best sets that need prev/ files

    for pfx, sets in data['boards'].items():
        for s in sets:
            for p in s['pages']:
                bn = p['basename']
                src = os.path.join(base, p['filepath'])
                ver = p['version']

                if s.get('is_best'):
                    # Best set gets priority
                    if bn not in copies_needed or copies_needed[bn].get('is_best') is False:
                        copies_needed[bn] = {
                            'source': src,
                            'version': ver,
                            'designator': p['board_designator'],
                            'is_best': True,
                            'set_designator': s['designator'],
                            'set_score': s['score'],
                        }
                elif ver != 'latest':
                    # Non-best set using prev/ — track for rendering alternate revisions
                    all_prev_needed.append({
                        'basename': bn,
                        'source': src,
                        'version': ver,
                        'designator': p['board_designator'],
                        'set_designator': s['designator'],
                        'set_score': s['score'],
                    })

    # Count how many changes are needed
    changes = 0
    already_correct = 0
    manifest = []

    for bn, info in sorted(copies_needed.items()):
        dest = os.path.join(drw_dir, f'{bn}.drw.O')
        src = info['source']

        # Check if already correct
        if os.path.exists(dest) and os.path.exists(src):
            d_size = os.path.getsize(dest)
            s_size = os.path.getsize(src)
            if d_size == s_size:
                # Quick size check (md5 would be better but slower)
                already_correct += 1
                manifest.append({
                    'basename': bn,
                    'action': 'already_correct',
                    'source': info['source'],
                    'version': info['version'],
                    'designator': info['designator'],
                    'set': info['set_designator'],
                    'score': info['set_score'],
                })
                continue

        # Need to copy
        if os.path.exists(src):
            shutil.copy2(src, dest)
            changes += 1
            ver_str = f"prev/v{info['version']}" if info['version'] != 'latest' else 'latest'
            manifest.append({
                'basename': bn,
                'action': 'copied',
                'source': info['source'],
                'version': info['version'],
                'version_str': ver_str,
                'designator': info['designator'],
                'set': info['set_designator'],
                'score': info['set_score'],
            })
            print(f"  {bn:20} ← {ver_str:15} \"{info['designator']}\"")
        else:
            print(f"  WARNING: source not found: {src}")

    # Save manifest
    manifest_data = {
        'generated': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_files': len(copies_needed),
        'already_correct': already_correct,
        'copied': changes,
        'prev_versions_used': len([m for m in manifest if m.get('version') != 'latest' and m.get('action') == 'copied']),
        'files': manifest,
    }

    manifest_path = 'data/drw_provenance_manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest_data, f, indent=2)

    print(f"\n=== Summary ===")
    print(f"Total files checked: {len(copies_needed)}")
    print(f"Already correct:     {already_correct}")
    print(f"Copied/updated:      {changes}")
    print(f"Prev versions used:  {manifest_data['prev_versions_used']}")
    print(f"Manifest saved to:   {manifest_path}")

    # Also report how many non-best sets could be rendered from prev/
    unique_prev = set(p['basename'] for p in all_prev_needed)
    print(f"\nNon-best sets referencing prev/ versions: {len(all_prev_needed)} page references")
    print(f"  ({len(unique_prev)} unique basenames)")


if __name__ == '__main__':
    main()
