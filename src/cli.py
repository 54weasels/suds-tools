import argparse
import os
from src.drw_parser import parse_drw_file
from src.library import load_libraries
from src.svg_renderer import render_svg

def main():
    parser = argparse.ArgumentParser(description="Convert SUDS DRW to SVG")
    parser.add_argument("input", help="Input DRW file")
    parser.add_argument("--library", action="append", help="Library DRW files")
    parser.add_argument("--output", help="Output SVG file")
    args = parser.parse_args()
    
    if not args.output:
        base = os.path.basename(args.input)
        name, _ = os.path.splitext(base)
        if name.endswith('.drw'):
            name = name[:-4]
        args.output = f"{name}.svg"
        
    print(f"Parsing {args.input}...")
    drw = parse_drw_file(args.input)
    
    library_defs = {}
    if args.library:
        print(f"Loading libraries: {args.library}")
        library_defs = load_libraries(*args.library)
        
    print("Rendering SVG...")
    svg_out = render_svg(drw, library_defs)
    
    with open(args.output, 'w') as f:
        f.write(svg_out)
        
    print(f"Done. Wrote to {args.output}")

if __name__ == "__main__":
    main()
