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
├── wd/             # WD wire data files (binary) — intermediate netlists
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

## Component Designators

- Designators are from WL files, not DRW
- Convention: [Prefix][Page*100+Seq]
- Batch renderer automatically overlays designators on SVG output

## Board Grouping & Version Selection

### Designator-First Coherence Algorithm

Each board prefix (e.g., `x`, `q`, `a`) may contain DRW pages from multiple
design revisions. The coherence algorithm identifies and separates these into
distinct version sets:

1. **Board designator extraction** — strips copyright prefixes from `title_line_1`
   to extract the board identity (e.g., "SUN-3/F", "SUN 68010")
2. **Clustering** — groups pages by `(designator, of_total)` pairs
3. **Merging** — joins related designators (e.g., SUN-3 + SUN-3/F when same "of")
4. **Scoring** — weighted formula: `0.35×desig + 0.20×of + 0.20×coverage + 0.15×wl + 0.10×size`
5. **Ranking** — highest-scoring version set is marked `_BEST`

### Data Authority Hierarchy

```
WL header (per-page board name)     ★★★★★  Highest — preserves original mapping
DRW trailer (board designator)      ★★★★☆  May be stale if file overwritten
DRW "Page X of Y" consistency      ★★★☆☆  Self-declared page total
BOM/WD cross-reference             ★★☆☆☆  Confirmation signal
```

### Version Recovery

The `data/drw/` files are sourced from `smi/octal/` (latest SAILDART version).
An initial curation step had incorrectly selected older versions for 189 files.
These were recovered by comparing all 685 files against the canonical archive and
replacing mismatched versions. The recovery audit trail is in `data/version_recovery.json`.

**Example:** For the X board (SUN-3/F), files `x2.drw.O` through `x4.drw.O` had
been populated with a 1982 "SUN 68000 MEMORY BOARD" instead of the 1986 SUN-3/F
schematics. After recovery, the SUN-3/F board went from 10/15 to 14/15 pages.

### WL Authority Map

The `data/wl_authority.json` file contains per-page board identity extracted from
66 wirelist file headers. Each entry records the board name, page function, sheet
number, and date from when the wirelist was generated. This is the highest-authority
source for page-to-board assignment.

## Project Structure

```
suds-tools/
├── README.md                       # This file
├── docs/
│   ├── journey.md                  # Research journal & findings (10 checkpoints)
│   ├── drw_format.md               # DRW file format specification
│   ├── suds_format_reference.md    # Complete SUDS technical reference
│   ├── file_inventory.md           # Index of all DRW files found
│   └── version_selection.md        # Version recovery & coherence algorithm docs
├── src/
│   ├── word36.py                   # 36-bit PDP-10 word primitives
│   ├── unpack.py                   # Binary format decoder (octal/ITS)
│   ├── drw_model.py                # Data model (13 dataclasses)
│   ├── drw_parser.py               # DRW binary parser (all 13 sections)
│   ├── svg_renderer.py             # SVG rendering engine
│   ├── library.py                  # Library file loader with auto-discovery
│   ├── dip_generator.py            # Synthetic DIP fallback body generator
│   ├── board_registry.py           # Board discovery (WL + metadata)
│   ├── wl_parser.py                # Wirelist netlist parser
│   ├── wd_parser.py                # Wire Data intermediate format parser
│   ├── version_coherence.py        # Designator-first coherence scoring
│   └── cli.py                      # CLI entry point
├── scripts/
│   ├── batch_render.py             # Batch SVG/PDF renderer with --versions
│   └── generate_index.py           # Provenance-rich HTML index generator
├── data/
│   ├── drw/                        # 685 DRW files (canonical from smi/octal)
│   ├── wirelists/                  # 68 WL wirelist files
│   ├── wd/                         # WD wire data files
│   ├── parts/                      # 100 PRT parts list files
│   ├── bom/                        # 54 BOM files
│   ├── wirelist_errors/            # 90 WLS error files
│   ├── commands/                   # COM/TXT batch scripts
│   ├── wl_authority.json           # WL per-page board authority map
│   ├── version_recovery.json       # Recovery audit trail (189 replacements)
│   ├── board_registry.json         # Cross-referenced board registry
│   └── pdf_groupings.json          # OCR-extracted PDF page assignments
├── output/
│   └── boards/                     # Rendered SVG + PDF output per board
│       ├── index.html              # Provenance-rich HTML index
│       ├── x/                      # SUN-3/F board (14/15 pages)
│       ├── q/                      # SUN-2 CPU board (multiple revisions)
│       └── ...                     # 163 board directories total
└── test/
    ├── test_unpack.py              # Unpack verification tests
    └── foo.drw.*                   # Test DRW files
```

## Usage

```bash
# List all discovered boards
python3 scripts/batch_render.py --list

# Render all boards with version-aware PDFs and HTML index
python3 scripts/batch_render.py --all --pdf --versions --index

# Render a single board
python3 scripts/batch_render.py --board x --pdf --versions

# Generate provenance-rich index (after batch render)
python3 scripts/generate_index.py
```

### Version-Aware PDF Output

With `--versions`, each board generates separate PDFs per design revision:
```
x_v1_sun_3_f_of15_s96%_BEST.pdf       # 14/15 SUN-3/F pages, score 96%, best
x_v2_ferrari_of20_s66%.pdf              # 1/20 Ferrari pages (partial)
x_v3_sun_3_of12_s63%.pdf                # 1/12 SUN-3 (earlier revision)
```

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1. Binary Decoder | 36-bit word unpacking | ✅ Complete |
| 2. DRW Parser | Full file parser (13 sections) | ✅ 675/685 clean (98.5%) |
| 3. SVG Renderer | Schematic → SVG rendering | ✅ Complete |
| 4. Batch Tools | Multi-page PDF, index, bulk conversion | ✅ Complete |
| 5. Version Recovery | Correct file version selection | ✅ 189 files recovered |
| 6. Coherence Algorithm | Designator-first board grouping | ✅ Complete |
| 7. Provenance Index | HTML index with full provenance | ✅ Complete |
| 8. KiCad Export | Netlist extraction → KiCad format | 🔲 Planned |

### Corpus Statistics

| Metric | Count |
|--------|-------|
| DRW files (canonical versions) | 685 |
| Body definitions discovered | 1,433 |
| Body placements | 33,339 |
| Connection points | 461,931 |
| Library body defs (auto-discovered) | 669 |
| Synthetic DIP fallbacks | ~90 |
| Files rendered | 685/685 (100%) |
| Board directories | 163 |
| Version-aware PDFs | 279 |
| Files recovered from version history | 189 |
| Wirelists parsed for authority data | 66 |

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

