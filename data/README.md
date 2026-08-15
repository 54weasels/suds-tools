# SUDS Tools — Data Directory

This directory contains archival SUDS data files organized by type, and rendered
output from the various parsers and renderers.

## Directory Layout

```text
data/
├── drw/                            # 685 DRW files (best canonical version per page)
├── wirelists/                      # 68 WL wirelist files — canonical board→page mappings
├── wd/                             # WD wire data files (binary) — intermediate netlists
├── parts/                          # 100 PRT parts list files (text)
├── bom/                            # 54 BOM bill-of-materials files (text)
├── wirelist_errors/                # 90 WLS error summary files (text)
├── commands/                       # COM/TXT batch command scripts for WL tool
├── pc_boards/                      # 64 rendered PC board HTML files (interactive SVG)
│   └── index.html                  # Searchable board index grouped by form factor
├── board_pdfs/                     # Best-version PDFs for each board (checked in)
│   └── index.html                  # Provenance-rich HTML index
├── drw_version_index.json          # Complete index of all 2,215 DRW file versions
├── canonical_board_sets.json       # 352 board sets with scoring and page selection
├── drw_provenance_manifest.json    # Which version was selected per page and why
├── wl_authority.json               # WL per-page board authority map (66 WLs, 564 pages)
├── version_recovery.json           # Recovery audit trail
├── board_registry.json             # Cross-referenced board registry
└── pdf_groupings.json              # OCR-extracted PDF page assignments
```

## File Extension Reference

| Extension | Type | Purpose |
|-----------|------|---------|
| `.drw.O` | Binary (octal) | Schematic drawing page |
| `.wl` | Text | Wirelist — canonical board→page mapping + netlist |
| `.prt` | Text | Parts list / BOM |
| `.plt.O` | Binary (octal) | Pen plotter output |
| `.pc.O` | Binary (octal) | PCB layout |
| `.wpc.O` | Binary (octal) | Wire-to-PC mapping |
| `.wd.O` | Binary (octal) | Wire data (intermediate) |
| `.stf` | Text | Stuffing file — grid-coordinate component placement |
| `.wls` | Text | Wirelist error/warning summary |
| `.bom` | Text | Bill of materials |
| `.con` | Text | Connectivity table |
| `.vrn.O` | Binary (octal) | DRC verification data |
| `.net` | Text | Raw pin-to-pin netlist |
| `.dip.O` | Binary (octal) | IC package database |
| `.crd.O` | Binary (octal) | Board outline / card definition |
| `.lsd` | Text | Human-readable DIP dump |
| `.mss` | Text | Scribe document sources |
| `.msg` | Text | Email/notes archive |

## PC Board Renders (`pc_boards/`)

64 interactive HTML/SVG renderings of all `.pc.O` files in the SMI archive.
Each HTML file contains:

- **Multi-layer SVG** with toggleable layers (traces, pads, vias, bodies)
- **Component designators** (U704, C109) centered on each DIP body
- **Chip type labels** (74LS374, AM2949) above bodies, sourced from PRT/WD/STF files
- **Board outline** from CRD card definition file
- **Silkscreen overlay** (for boards with separate silk PC files, e.g. `d`)

### DIP Type Data Sources

Component type labels are resolved from the highest-priority available source:

| Priority | Source | Format | Coverage |
|----------|--------|--------|----------|
| 1 | PRT (parts list) | Text, `DIPTYPE → LOCATIONS` | Uses PC board designators |
| 2 | WD (wire data) | Binary, per-sheet body records | Uses schematic designators |
| 3 | STF (stuffing file) | Text, grid-coordinate mapping | Board-specific format |
| 4 | DIP library | Binary, package type codes | Internal codes only |

### Regenerating

```bash
python3 scripts/render_pc_boards.py          # Render all 64 boards
python3 scripts/generate_pc_index.py         # Generate searchable index
python3 scripts/render_pc_boards.py -b g     # Render single board
python3 scripts/render_pc_boards.py --list   # List available boards
```

## Schematic PDFs (`board_pdfs/`)

Best-version PDFs for each board, rendered from DRW schematic files.
See `board_pdfs/index.html` for a browsable provenance-rich index.

### Regenerating

```bash
python3 scripts/batch_render.py --all --pdf --versions
python3 scripts/generate_index.py
```
