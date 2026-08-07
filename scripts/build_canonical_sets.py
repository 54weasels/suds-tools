#!/usr/bin/env python3
"""Build canonical best-version board sets from the complete version index.

For each board prefix, considers ALL available versions (latest + prev/)
and selects the combination of page versions that produces the most coherent
board set. This means an older version of a page may be chosen if it produces
a more complete board grouping.

Input:  data/drw_version_index.json, data/wl_authority.json
Output: data/canonical_board_sets.json
        data/drw/ (updated with best versions for each board set)
"""
import json
import os
import re
import shutil
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.version_coherence import _normalize_designator


def load_index(path='data/drw_version_index.json'):
    with open(path) as f:
        return json.load(f)


def load_wl_authority(path='data/wl_authority.json'):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def extract_prefix(basename):
    """Extract the alphabetic prefix from a basename."""
    m = re.match(r'^([a-zA-Z]+)', basename)
    return m.group(1).lower() if m else basename.lower()


def build_canonical_sets(index, wl_auth):
    """Build canonical board sets by considering ALL versions of every page."""

    catalog = index['catalog']
    base_path = '/Users/dmoisa/Documents/sun/smi/'

    # Step 1: Group all page versions by prefix
    by_prefix = defaultdict(lambda: defaultdict(list))
    for basename, versions in catalog.items():
        pfx = extract_prefix(basename)
        for v in versions:
            page_num = v['page_num']
            if page_num <= 0:
                continue
            by_prefix[pfx][page_num].append(v)

    # Step 2: For each prefix, identify all distinct board designators
    results = {}
    total_sets = 0

    for pfx in sorted(by_prefix.keys()):
        positions = by_prefix[pfx]

        # Collect all (designator, of_total) seen across all versions
        desig_of_combos = defaultdict(set)  # (norm_desig, of) -> set of page_nums
        all_entries = []

        for page_num, versions in positions.items():
            for v in versions:
                desig = v.get('board_designator', '').strip()
                if not desig:
                    continue
                norm = _normalize_designator(desig)
                of_val = v.get('of_total', 0)
                if of_val > 0:
                    desig_of_combos[(norm, of_val)].add(page_num)
                    all_entries.append(v)

        if not desig_of_combos:
            continue

        # Step 3: For each (desig, of), build the best possible page set
        board_sets = []
        for (norm_desig, target_of), page_nums in sorted(
            desig_of_combos.items(),
            key=lambda x: len(x[1]),
            reverse=True
        ):
            if target_of <= 0:
                continue

            # Find the best version of each page that matches this designator+of
            selected_pages = {}
            for page_num in range(1, target_of + 1):
                candidates = positions.get(page_num, [])
                matching = []
                for v in candidates:
                    v_desig = _normalize_designator(v.get('board_designator', ''))
                    v_of = v.get('of_total', 0)
                    if v_desig == norm_desig and v_of == target_of:
                        matching.append(v)
                    elif v_desig == norm_desig:
                        # Same designator, different of — weaker match
                        matching.append(v)

                if matching:
                    # Prefer: exact of match > latest version > most bodies
                    def score(v):
                        s = 0
                        if v.get('of_total') == target_of:
                            s += 1000
                        if v.get('version') == 'latest':
                            s += 100
                        elif isinstance(v.get('version'), int):
                            s += v['version']
                        s += (v.get('bodies', 0) + v.get('points', 0)) * 0.001
                        return s

                    best = max(matching, key=score)
                    selected_pages[page_num] = best

            if not selected_pages:
                continue

            n = len(selected_pages)
            coverage = n / target_of

            # Score this set
            exact_of_match = sum(1 for v in selected_pages.values()
                                 if v.get('of_total') == target_of) / n if n else 0
            exact_desig_match = sum(1 for v in selected_pages.values()
                                   if _normalize_designator(v.get('board_designator', '')) == norm_desig) / n if n else 0

            # Get WL page count
            wl_match = 0.0
            wl_data = wl_auth.get(pfx, {})
            wl_count = wl_data.get('page_count', 0)
            if wl_count > 0:
                if target_of == wl_count:
                    wl_match = 1.0
                elif abs(target_of - wl_count) == 1:
                    wl_match = 0.5

            max_of = max((k[1] for k in desig_of_combos.keys() if k[1] > 0), default=1)
            size_score = target_of / max_of if max_of > 0 else 0

            total_score = (
                0.35 * exact_desig_match +
                0.20 * exact_of_match +
                0.20 * coverage +
                0.15 * wl_match +
                0.10 * size_score
            )

            # Determine provenance for each selected page
            pages_info = []
            for page_num in sorted(selected_pages.keys()):
                v = selected_pages[page_num]
                source = 'latest' if v['version'] == 'latest' else f"prev/v{v['version']}"
                pages_info.append({
                    'page_num': page_num,
                    'basename': v['basename'],
                    'version': v['version'],
                    'source': source,
                    'filepath': v['filepath'],
                    'board_designator': v['board_designator'],
                    'of_total': v['of_total'],
                    'file_date': v['file_date'],
                    'bodies': v['bodies'],
                })

            # Identify raw designator (not normalized)
            raw_desigs = [p['board_designator'] for p in pages_info if p['board_designator']]
            # Pick the most specific (longest) raw designator
            raw_desig = max(raw_desigs, key=len) if raw_desigs else norm_desig

            board_sets.append({
                'designator': raw_desig,
                'designator_normalized': norm_desig,
                'of_total': target_of,
                'pages_found': n,
                'coverage': round(coverage, 3),
                'score': round(total_score, 3),
                'score_breakdown': {
                    'c_desig': round(exact_desig_match, 3),
                    'c_of': round(exact_of_match, 3),
                    'c_coverage': round(coverage, 3),
                    'c_wl': round(wl_match, 3),
                    'c_size': round(size_score, 3),
                },
                'pages': pages_info,
                'missing_pages': [i for i in range(1, target_of + 1) if i not in selected_pages],
                'uses_prev_versions': any(p['version'] != 'latest' for p in pages_info),
            })

        if board_sets:
            # Sort by score
            board_sets.sort(key=lambda s: s['score'], reverse=True)
            board_sets[0]['is_best'] = True
            for s in board_sets[1:]:
                s['is_best'] = False

            results[pfx] = board_sets
            total_sets += len(board_sets)

    return results, total_sets


def main():
    os.chdir('/Users/dmoisa/Documents/sun/smi/suds-tools')

    print("Loading version index...")
    index = load_index()
    wl_auth = load_wl_authority()

    meta = index['metadata']
    print(f"  {meta['total_entries']} total DRW files "
          f"({meta['octal_files']} latest + {meta['prev_files']} prev)")
    print(f"  {meta['unique_basenames']} unique base names")

    print("\nBuilding canonical board sets...")
    t0 = time.time()
    results, total_sets = build_canonical_sets(index, wl_auth)
    elapsed = time.time() - t0
    print(f"  {len(results)} prefixes, {total_sets} board sets in {elapsed:.1f}s")

    # Count sets that use prev versions
    uses_prev = sum(1 for pfx_sets in results.values()
                    for s in pfx_sets if s.get('uses_prev_versions'))

    # Save
    output = {
        'metadata': {
            'generated': time.strftime('%Y-%m-%d %H:%M:%S'),
            'source_files': meta['total_entries'],
            'board_prefixes': len(results),
            'total_board_sets': total_sets,
            'sets_using_prev_versions': uses_prev,
        },
        'boards': results,
    }

    output_path = 'data/canonical_board_sets.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    fsize = os.path.getsize(output_path)
    print(f"\nSaved to {output_path} ({fsize / 1024:.0f} KB)")

    # Print summary
    print(f"\n{'Prefix':8} {'Sets':>4}  Best Set")
    print("-" * 90)
    for pfx, sets in sorted(results.items()):
        best = sets[0]
        prev_marker = " ← uses prev/" if best.get('uses_prev_versions') else ""
        print(f"{pfx:8} {len(sets):>4}  \"{best['designator']}\" "
              f"{best['pages_found']}/{best['of_total']}p "
              f"score={best['score']:.2f}{prev_marker}")

    # Show sets that pull from version history
    print(f"\n=== Board sets using prev/ versions ({uses_prev}) ===")
    for pfx, sets in sorted(results.items()):
        for s in sets:
            if s.get('uses_prev_versions'):
                prev_pages = [p for p in s['pages'] if p['version'] != 'latest']
                prev_str = ', '.join(f"{p['basename']} (v{p['version']})" for p in prev_pages[:5])
                if len(prev_pages) > 5:
                    prev_str += f' +{len(prev_pages)-5} more'
                print(f"  {pfx:8} \"{s['designator']}\" {s['pages_found']}/{s['of_total']}p "
                      f"score={s['score']:.2f}: {prev_str}")


if __name__ == '__main__':
    main()
