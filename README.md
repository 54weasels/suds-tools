# SUDS DRW → SVG Conversion Tools

**Stanford University Drawing System (SUDS) — Modern Format Recovery Project**

This project decodes and renders archival SUDS `.DRW` schematic drawing files
from the Stanford AI Lab (SAIL) / Sun Microsystems era into modern SVG vector graphics.

## What is SUDS?

SUDS was a pioneering CAD system developed at Stanford in the 1970s, running on PDP-10
mainframes under the WAITS operating system. It was used to design:

- The **Super Foonly** (F-1 processor)
- The **S-1 Supercomputer** (SCALD/SUDS at LLNL)
- The original **Sun-1** and **Sun-2** workstations (by Andy Bechtolsheim)
- Various Stanford AI Lab hardware

The DRW files in this archive contain the actual schematics for these historically
significant machines, drawn by Andy Bechtolsheim and others.

## Data Sources

| Source | Location | Description |
|--------|----------|-------------|
| SMI Archive | `../smi/` | SAILDART dump of `[*,SMI]` — Sun Microsystems Inc files |
| SMI Octal | `../smi/octal/` | 685 binary `.drw.O` files (36-bit words in octal format) |
| SUDS Repo | `../../saildart/SUDS/` | PDP-10/SUDS GitHub repo with tools & docs |
| PDP-10 Source | `../../saildart/SUDS/bits/saildart/` | Authoritative DRAW program assembly source |

## Project Structure

```
suds-tools/
├── README.md                   # This file
├── docs/
│   ├── journey.md              # Research journal & findings
│   ├── drw_format.md           # DRW file format specification
│   ├── file_inventory.md       # Index of all DRW files found
│   └── continuation_prompt.md  # Context prompt to continue this work
├── src/
│   ├── word36.py               # 36-bit PDP-10 word primitives
│   ├── unpack.py               # Binary format decoder (octal/ITS)
│   ├── drw_model.py            # Data model (13 dataclasses)
│   ├── drw_parser.py           # DRW binary parser (all 13 sections)
│   ├── svg_renderer.py         # SVG rendering engine
│   ├── library.py              # Library file loader with auto-discovery
│   ├── dip_generator.py        # Synthetic DIP fallback body generator
│   └── cli.py                  # CLI entry point
├── scripts/
│   └── render_q_series.py      # Batch render script for Q-series boards
├── best_drw/                   # Curated best-version DRW files for rendering
├── output/
│   └── q_series/               # Rendered SVG + PNG output (28 pages)
└── test/
    ├── test_unpack.py           # Unpack verification tests
    └── foo.drw.*                # Test DRW files
```

## Usage

### Render a single schematic

```bash
python3 -m src.cli best_drw/qx1.drw.O --auto-lib best_drw --output qx1.svg
```

### Batch render Q-series (Sun-2 68010 CPU board)

```bash
python3 scripts/render_q_series.py --dir best_drw --output-dir output/q_series
```

This renders all Q-series pages to SVG and converts to PNG via `rsvg-convert`.

### Render all DRW files

```bash
python3 scripts/render_q_series.py --dir best_drw --output-dir output/all --all
```

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1. Binary Decoder | 36-bit word unpacking (`word36.py`, `unpack.py`) | ✅ Complete |
| 2. DRW Parser | Full file parser (`drw_parser.py`, `drw_model.py`) | ✅ 675/685 clean (98.5%) |
| 3. SVG Renderer | Schematic → SVG rendering | ✅ Complete |
| 4. KiCad Export | Netlist extraction → KiCad format | 🔲 Planned |
| 5. Batch Tools | Multi-page PDF, index, bulk conversion | 🔲 Planned |

### Corpus Statistics (685 files)

| Metric | Count |
|--------|-------|
| Body definitions | 1,433 |
| Body placements | 33,339 |
| Connection points | 461,931 |
| Properties | 19,662 |
| Files with trailers | 685/685 |
| Library body defs (auto-discovered) | 669 |
| Synthetic DIP fallbacks | ~90 |
| Files rendered | 685/685 (100%) |

10 files produce parse warnings — all are truncated archive files hitting exact EOF boundaries.

### SVG Renderer Details

The renderer produces monochrome SVG output calibrated against original SUDS pen plotter
output (`.plt` files rendered via `harscn`). Key parameters:

| Setting | Value | Notes |
|---------|-------|-------|
| `TEXT_SCALE` | 4.0 | SUDS text_size × 4.0 = SVG font-size in drawing units |
| `PIN_NUM_FONT_SIZE` | 3.0 | Pin numbers slightly smaller than body text |
| Coordinate system | 1 unit = 12.5 mils | Standard SUDS grid |
| Y-axis | Flipped via `scale(1,-1)` | SUDS Y-up → SVG Y-down |
| Body resolution | Auto-discover 12 library files | Library defs override synthetic DIPs |
