"""CLI entry point for SUDS DRW → SVG conversion.

Usage:
    python3 -m src.cli <input.drw.O> [--library lib.drw.O ...] [--output output.svg]
    python3 -m src.cli <input.drw.O> --auto-lib <octal_dir> [--output output.svg]
"""
import argparse
import os
import sys
from src.drw_parser import parse_drw_file
from src.library import load_libraries, auto_discover_libraries
from src.svg_renderer import render_svg


def main():
    parser = argparse.ArgumentParser(
        description="Convert SUDS DRW schematic files to SVG")
    parser.add_argument("input", help="Input DRW file (.drw.O)")
    parser.add_argument("--library", action="append", default=[],
                        help="Library DRW file(s) for body definitions (repeatable)")
    parser.add_argument("--auto-lib", metavar="DIR",
                        help="Auto-discover all library files in directory")
    parser.add_argument("--output", "-o", help="Output SVG file (default: <name>.svg)")
    args = parser.parse_args()

    # Default output name
    if not args.output:
        base = os.path.basename(args.input)
        name = base
        for ext in ['.drw.O', '.O']:
            if name.endswith(ext):
                name = name[:-len(ext)]
                break
        args.output = f"{name}.svg"

    # Parse input
    print(f"Parsing {args.input}...")
    drw = parse_drw_file(args.input)
    if drw.parse_warnings:
        for w in drw.parse_warnings:
            print(f"  WARNING: {w}", file=sys.stderr)

    # Load libraries
    lib_paths = list(args.library)
    if args.auto_lib:
        discovered = auto_discover_libraries(args.auto_lib)
        # Don't add the input file itself as a library
        input_abs = os.path.abspath(args.input)
        discovered = [p for p in discovered if os.path.abspath(p) != input_abs]
        lib_paths.extend(discovered)

    library_defs = {}
    if lib_paths:
        print(f"Loading {len(lib_paths)} libraries...")
        library_defs = load_libraries(*lib_paths)
        print(f"  {len(library_defs)} body definitions loaded")

    # Render
    print("Rendering SVG...")
    svg_out = render_svg(drw, library_defs)

    with open(args.output, 'w') as f:
        f.write(svg_out)

    sz = os.path.getsize(args.output)
    print(f"Done. Wrote {sz:,} bytes to {args.output}")


if __name__ == "__main__":
    main()
