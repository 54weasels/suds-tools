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

### Data Directory Layout
```text
data/
├── drw/            # 685 DRW schematic page files (binary, octal-encoded)
├── wirelists/      # 68 WL wirelist files (text) — canonical board→page mappings
├── parts/          # 100 PRT parts list files (text)
├── wirelist_errors/ # 90 WLS error summary files (text)
├── bom/            # 54 BOM bill-of-materials files (text)
└── commands/       # COM/TXT batch command scripts for WL tool
```

### File Extension Reference
| Extension | Type | Purpose |
|-----------|------|---------|
| `.drw.O` | Binary (octal) | Schematic drawing page |
| `.wl` | Text | Wirelist — canonical board→page mapping + netlist |
| `.prt` | Text | Parts list / BOM |
| `.plt.O` | Binary (octal) | Pen plotter output |
| `.pc.O` | Binary (octal) | PCB layout |
| `.wpc.O` | Binary (octal) | Wire-to-PC mapping |
| `.wd.O` | Binary (octal) | Wire data (intermediate) |
| `.wls` | Text | Wirelist error/warning summary |
| `.bom` | Text | Bill of materials |
| `.con` | Text | Connectivity table |
| `.vrn.O` | Binary (octal) | DRC verification data |
| `.net` | Text | Raw pin-to-pin netlist |
| `.dip.O` | Binary (octal) | IC package database |
| `.lsd` | Text | Human-readable DIP dump |
| `.mss` | Text | Scribe document sources |
| `.msg` | Text | Email/notes archive |

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

```bash
# List all boards (wirelist-based grouping)
python3 scripts/batch_render.py --list

# Render all boards with PDFs and HTML index
python3 scripts/batch_render.py --all --pdf --index

# Render a single board
python3 scripts/batch_render.py --board q
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
