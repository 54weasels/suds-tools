#!/usr/bin/env python3
"""Batch render all SUDS PC board files to HTML.

Renders every .pc.O file in the SMI octal directory to an interactive
HTML/SVG file in data/pc_boards/.  Automatically discovers matching
PRT (parts list), STF (stuffing), and CRD (card outline) files.

CRD auto-detection: each board's component extents are measured and
the smallest CRD card outline that fits is selected.  Non-card PCBs
(mouse boards, silk overlays, etc.) are explicitly excluded.

Usage:
    python3 scripts/render_pc_boards.py [--board NAME] [--list]
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.unpack import read_file
from src.pc_parser import PCParser
from src.crd_parser import parse_crd_file
from src.dip_library import parse_dip_library
from src.dip_type_map import build_dip_type_map
from src.pc_svg_renderer import render_pc_html


# Known silk-screen overlay files (separate PC file with board outline text)
# In SUDS, silk screens are generated from the main board PC file + STF;
# these are pre-rendered silk artwork stored as separate PC files.
SILK_OVERLAYS = {
    'd': 'mupac.pc.O',       # Mupac wire-wrap board outline for d board
    'mouse': 'msilk.pc.O',   # Silk screen for mouse board
    'mouse2': 'm2silk.pc.O', # Silk screen for mouse2 board
}

# Known PRT file mappings (board prefix → PRT filename)
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

# Known STF file mappings
STF_MAP = {
    'a': 'a.stf', 'cg': 'cg.stf',
    'foo': 'foo.stf', 'g': 'g.stf',
    'mouse': 'mouse.stf', 'p': 'p.stf', 'q': 'q.stf',
    'sio': 'sio.stf',
    'vme3x2': 'vme3x2.stf', 'vmxpig': 'vmxpig.stf',
    'x': 'x.stf', 'y': 'y.stf',
}

# Boards that should NEVER get a card outline — they are not
# standard card form factors (small PCBs, silk overlays, etc.)
NO_CRD_BOARDS = {
    'mouse', 'mousef',          # Mouse PCB (small standalone board)
    'mupac', 'msilk', 'm2silk', # Silk-screen overlay files
    'm2sola',                   # Solder-side artwork
    'ether',                    # Small Ethernet transceiver board
    'ratsht',                   # Rat's nest / test pattern
    'a20', 'ax',                # Small test/adapter boards
    'back',                     # Backplane (custom shape)
    'vmemb',                    # Corrupt data: S2 X-shifted ~200 mils, 16% non-45° traces
}

# Explicit CRD overrides (board → CRD file or None).
# Used when auto-detection picks wrong CRD or for boards where
# the correct CRD is known from physical reference.
CRD_OVERRIDES: dict[str, str | None] = {
    # mouse2 has DECPC type in WLD but is physically a small board
    'mouse2': None,
    # p has corrupt body coordinates that confuse auto-detection;
    # valid components fit within Multibus outline
    'p': 'multi0.crd.O',
}


def auto_detect_crd(pc, crd_list):
    """Find the smallest CRD card outline that fits the board's components.

    Args:
        pc: Parsed PCFile
        crd_list: List of (filename, CRDFile, area_sq_mils) sorted by area

    Returns:
        (crd_filename, CRDFile) or (None, None) if no CRD fits
    """
    bx = [b.loc[0] for b in pc.bodies if abs(b.loc[0]) < 50000]
    by = [b.loc[1] for b in pc.bodies if abs(b.loc[1]) < 50000]

    if not bx or len(pc.bodies) < 3:
        return None, None

    for crd_name, crd, area in crd_list:
        ox = [p[0] for p in crd.outline]
        oy = [p[1] for p in crd.outline]
        orig = crd.pc_origin
        # Check if all components fit within the CRD outline (50 mil tolerance)
        comp_max_x = max(bx) + orig[0]
        comp_max_y = max(by) + orig[1]
        if comp_max_x <= max(ox) + 50 and comp_max_y <= max(oy) + 50:
            return crd_name, crd

    return None, None


def main():
    parser = argparse.ArgumentParser(description='Render SUDS PC board files to HTML')
    parser.add_argument('--board', '-b', help='Render only this board (e.g. "g", "qx")')
    parser.add_argument('--list', '-l', action='store_true', help='List available boards')
    args = parser.parse_args()

    smi_dir = PROJECT_ROOT / '..' / 'smi'
    octal_dir = smi_dir / 'octal'
    output_dir = PROJECT_ROOT / 'data' / 'pc_boards'

    if not octal_dir.exists():
        print(f'Error: octal directory not found: {octal_dir}')
        sys.exit(1)

    # Discover all PC files
    pc_files = sorted(f.name for f in octal_dir.iterdir() if f.name.endswith('.pc.O'))
    boards = [f.replace('.pc.O', '') for f in pc_files]

    # Load all CRD files, sorted by area (smallest first for tightest fit)
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

    if args.list:
        print(f'{len(boards)} PC board files:')
        # Need to parse each to detect CRD for listing
        for b in boards:
            prt = PRT_MAP.get(b, '')
            stf = STF_MAP.get(b, '')
            silk = SILK_OVERLAYS.get(b, '')
            extras = []
            if prt: extras.append(f'PRT={prt}')
            if stf: extras.append(f'STF={stf}')
            if silk: extras.append(f'silk={silk}')
            print(f'  {b:12s}  {" ".join(extras)}')
        return

    if args.board:
        boards = [b for b in boards if b == args.board]
        if not boards:
            print(f'Board "{args.board}" not found')
            sys.exit(1)

    # Load shared resources
    dip_lib_path = octal_dir / 'dips.dip.O'
    dip_lib = parse_dip_library(str(dip_lib_path)) if dip_lib_path.exists() else None

    output_dir.mkdir(parents=True, exist_ok=True)

    # Render each board
    ok_count = 0
    fail_count = 0
    t_start = time.time()

    for board in boards:
        pc_path = octal_dir / f'{board}.pc.O'
        out_path = output_dir / f'{board}_board.html'

        try:
            pc = PCParser(read_file(str(pc_path)), source_path=pc_path.name).parse()
            n_pts = len(pc.side1_points) + len(pc.side2_points)

            # Determine CRD for this board
            crd = None
            crd_name = None

            if board in CRD_OVERRIDES:
                # Explicit override
                override = CRD_OVERRIDES[board]
                if override:
                    for cn, cc, ca in crd_list:
                        if cn == override:
                            crd_name, crd = cn, cc
                            break
            elif board not in NO_CRD_BOARDS:
                # Auto-detect from component extents
                crd_name, crd = auto_detect_crd(pc, crd_list)

            # Build DIP type map from available sources
            stf_path = smi_dir / STF_MAP[board] if board in STF_MAP else None
            prt_path = smi_dir / PRT_MAP[board] if board in PRT_MAP else None
            if stf_path and not stf_path.exists():
                stf_path = None
            if prt_path and not prt_path.exists():
                prt_path = None

            dip_types = build_dip_type_map(
                board, str(octal_dir),
                stf_path=str(stf_path) if stf_path else None,
                prt_path=str(prt_path) if prt_path else None,
            )

            # Load silk overlay if available
            silk_pc = None
            if board in SILK_OVERLAYS:
                silk_path = octal_dir / SILK_OVERLAYS[board]
                if silk_path.exists():
                    silk_pc = PCParser(
                        read_file(str(silk_path)),
                        source_path=silk_path.name
                    ).parse()

            render_pc_html(
                pc, str(out_path),
                crd=crd, dip_lib=dip_lib, silk_pc=silk_pc, dip_types=dip_types,
            )
            ok_count += 1
            src_info = []
            if crd_name:
                src_info.append(f'CRD={crd_name}')
            if dip_types.prt_count > 0:
                src_info.append(f'PRT={dip_types.prt_count}')
            if dip_types.wd_count > 0:
                src_info.append(f'WD={dip_types.wd_count}')
            if dip_types.stf_count > 0:
                src_info.append(f'STF={dip_types.stf_count}')
            src = ' '.join(src_info) if src_info else 'no CRD, DIP lib only'
            print(f'  ✓ {board:12s}  bodies={len(pc.bodies):4d}  pts={n_pts:5d}  {src}')

        except Exception as e:
            fail_count += 1
            print(f'  ✗ {board:12s}  ERROR: {e}')

    elapsed = time.time() - t_start
    print(f'\nDone: {ok_count} rendered, {fail_count} failed, in {elapsed:.1f}s')
    print(f'Output: {output_dir}/')


if __name__ == '__main__':
    main()
