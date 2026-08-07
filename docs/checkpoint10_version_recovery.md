# SUDS Board Grouping: Version Recovery & Coherence Algorithm

## Checkpoint 9: Version Recovery Complete

### Problem Discovered
The `data/drw/` directory contained **wrong file versions** for 189 out of 685 DRW files. The earlier board selection script had picked stale versions from version history instead of the latest versions from `smi/octal/`.

### Critical Example: X Board (SUN-3/F)
| File | data/drw (WRONG) | smi/octal (CORRECT) |
|------|------------------|---------------------|
| x2.drw.O | "(C) 1982 SMI SUN 68000 MEMORY BOARD" 2/4 | "SUN-3/F" 2/15 |
| x3.drw.O | "(C) 1982 SMI SUN 68000 MEMORY BOARD" 3/4 | "SUN-3/F" 3/15 |
| x4.drw.O | "(C) 1982 SMI SUN 68000 MEMORY BOARD" 4/4 | "SUN-3/F UARTS" 4/10 |
| x7.drw.O | "SUN-3 MEMORY" 7/10 | "SUN-3/F PARITY" 7/15 |
| x8.drw.O | "SUN-3 VIDEO MEMORY" 8/10 | "SUN-3/F RAS/CAS" 8/15 |

### Recovery Results
- **189 files** replaced with correct versions from `smi/octal/`
- Recovery report saved to `data/version_recovery.json`
- X board SUN-3/F went from **10/15 pages (score 0.80)** → **14/15 pages (score 0.96)**

---

## Algorithm: Designator-First Coherence Scoring

### Priority Hierarchy
```
1. WL header         ★★★★★  Per-page board name + sheet info (highest authority)
2. DRW board desig.  ★★★★☆  Extracted from title_line_1 (maximum weight in scoring)
3. "Page X of Y"     ★★★☆☆  Self-declared total page count
4. BOM/WD data       ★★☆☆☆  Cross-reference (confirmation)
```

### Scoring Formula
$$\text{Score}(S, Y) = 0.35 \cdot C_{\text{desig}} + 0.20 \cdot C_{\text{of}} + 0.20 \cdot C_{\text{coverage}} + 0.15 \cdot C_{\text{wl}} + 0.10 \cdot C_{\text{size}}$$

### Board Designator Extraction
```
"(C) 1982 SMI, SUN 68010, CPU"    → "SUN 68010" → normalized to "SUN-2"
"PROPRIETARY SMI, SUN-2, CLOCKS"  → "SUN-2"
"SUN-3/F"                          → "SUN-3/F"
"SUN MICROSYSTEMS INC" + "501-1007-08" → "501-1007-08" (fallback to title2)
```

### Normalization Rules
- SUN 68010, SUN-2 CPU, SUN-2/50 → "SUN-2"
- SUN-3 and SUN-3/F merge only when same "of" total

---

## Data Sources

### WL Authority Map (`data/wl_authority.json`)
- 66 wirelists → 564 page entries
- Each entry: `{board, function, board_type, sheet_x, sheet_of, date}`
- Example: `x.wl → X2: {board: "SUN-3/F", function: "", sheet: 2/15}`

### Version Recovery Report (`data/version_recovery.json`)
- 189 file replacements documented
- Each entry: `{filename, data_drw_meta, octal_meta, action, reason}`

---

## Output
- All boards rendered as SVG with designator overlays
- Version-aware PDFs: `{board}_v{n}_{designator}_of{total}_s{score}_{BEST}.pdf`
- HTML index with provenance information
