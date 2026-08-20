#!/usr/bin/env python3
"""Convert all .mss Scribe files to Markdown and generate a categorized index."""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.mss_converter import convert_mss


# ── Board names that have matching .pc.O files ─────────────────────────────
BOARD_NAMES = {
    'a', 'b', 'f', 'g', 'p', 'q', 'x', 'y', 'd',
    'cg', 'em', 'ep', 'ev', 'fm', 'm1', 'mm1',
    'ti', 've', 'sio', 'back', 'vmem', 'vmep', 'vmes',
}

# ── Categorization rules ──────────────────────────────────────────────────
def categorize(stem: str) -> str:
    """Assign an .mss file to a document category."""
    s = stem.lower()

    # Board manuals (match known boards or board-like patterns)
    if s in BOARD_NAMES:
        return 'Board Engineering Manuals'
    # Board manual variants (a1, aem, b1, g1, g4, p1, p3, q1, etc.)
    if len(s) <= 4 and s[0] in 'abcdefgmpqstvxy' and any(
            c.isdigit() for c in s[1:]):
        return 'Board Engineering Manuals'
    if s in ('aem', 'aem1', 'aold', 'ax', 'ay', 'qem', 'qold',
             'd1', 'e', 'e1', 'e3', 'em', 'lc', 'lcws',
             'm16', 'm50', 'vmep', 'vmem', 'vem', 'vme',
             'sx1', 'sio', 'sio1', 'y1', 'y2', 'y4',
             'ti1', 'ti4', 'v', 'v1', 'v4'):
        return 'Board Engineering Manuals'

    # Architecture & system
    if s in ('arch', 's', 's2', 'sun', 'sun1', 'sun2', 'sun3',
             'overvi', '68000', '68000i', 'bus', 'p2bus',
             'proc', 'mcsun1', 'all', 'cover'):
        return 'Architecture & System'

    # Graphics & display
    if s in ('cg4', 'sc1', 'sc4', 'sc4old', 'scolor', 'graph',
             'grap', 'ga', 'gr', 'ropc'):
        return 'Graphics & Display'

    # Product specs & marketing
    if s in ('160', '50', '50pd', 'pd', 'market', 'perf', 'plan',
             'works', 'apple', 'hard', 'disk', 'smi', 'smi2',
             'smi3', 'smi4', 'sun2lc', 'projec'):
        return 'Product Specs & Planning'

    # Networking
    if 'eth' in s:
        return 'Networking'

    # Keyboard & peripherals
    if s in ('keybd', 'km', 'mouse'):
        return 'Peripherals'

    # PROM / PAL / tools
    if s in ('suds', 'pal', 'prom', 'chips', 'electr', 'timing'):
        return 'Tools & Components'

    return 'Memos & Notes'


def main():
    smi_dir = PROJECT_ROOT.parent / 'smi'
    out_dir = PROJECT_ROOT / 'data' / 'docs'
    out_dir.mkdir(parents=True, exist_ok=True)

    mss_files = sorted(smi_dir.glob('*.mss'))
    if not mss_files:
        print(f'No .mss files found in {smi_dir}')
        sys.exit(1)

    categories: dict[str, list[tuple[str, str, int, str]]] = {}
    total_lines = 0
    errors = 0

    for f in mss_files:
        try:
            content = f.read_text(errors='replace')
            md = convert_mss(content, f.name, smi_dir)
            out_file = out_dir / (f.stem + '.md')
            out_file.write_text(md)

            lines = md.splitlines()
            total_lines += len(lines)

            # Extract title from first heading
            title = f.stem
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break

            cat = categorize(f.stem)
            categories.setdefault(cat, []).append(
                (f.name, title, len(lines), out_file.name))

        except Exception as e:
            print(f'  ✗ {f.name}: {e}')
            errors += 1

    # ── Generate index.md ─────────────────────────────────────────────
    # Category display order
    cat_order = [
        'Board Engineering Manuals',
        'Architecture & System',
        'Graphics & Display',
        'Product Specs & Planning',
        'Networking',
        'Peripherals',
        'Tools & Components',
        'Memos & Notes',
    ]

    idx = ['# Sun Microsystems Engineering Documents\n']
    idx.append(f'Converted from CMU Scribe (.mss) format. '
               f'{len(mss_files)} documents, {total_lines:,} lines.\n')

    for cat in cat_order:
        items = categories.get(cat, [])
        if not items:
            continue
        idx.append(f'\n## {cat}\n')
        idx.append('| Document | Source | Lines |')
        idx.append('|----------|--------|------:|')
        for fname, title, lcount, outname in sorted(items):
            idx.append(f'| [{title}]({outname}) | `{fname}` | {lcount} |')

    (out_dir / 'index.md').write_text('\n'.join(idx) + '\n')

    print(f'\nConverted {len(mss_files)} files to {out_dir}/')
    print(f'Total output: {total_lines:,} lines')
    if errors:
        print(f'Errors: {errors}')
    print(f'Index: {out_dir}/index.md')


if __name__ == '__main__':
    main()
