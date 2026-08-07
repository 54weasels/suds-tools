# Auxiliary Data Sources for Board Grouping

## Summary of Findings

The **WL (Wirelist) file** is by far the most powerful signal. It contains the **authoritative page list and per-page board designator** from the time the wirelist was generated, which in many cases is **more correct than the current DRW file contents** (because DRW files were overwritten/repurposed in the archive).

## Data Source Comparison

| Source | Signal Strength | What It Contains | Example |
|--------|---------------|------------------|---------|
| **WL header** | ★★★★★ | Per-page: board name, page function, "Sheet X of Y", page list, dates | X2→SUN-3/F (DRW says "SUN 68000 MEMORY BOARD") |
| **BOM** | ★★★☆☆ | Part-file name, complete component BOM with quantities | `Part-File: A` → links to board A |
| **DRW trailer** | ★★★☆☆ | Board designator, page function, "Page X of Y" | Can be wrong if file was overwritten |
| **WD (Wire Data)** | ★★☆☆☆ | Bodies + signals per page (binary) | Confirms component count |
| **PLT (Plotter)** | ★★☆☆☆ | Trailer text + component designators | Confirms which DRW revision was plotted |

## Key Discovery: WL Overrides DRW

For the X board, the WL file (`x.wl`, dated 13-AUG-86) lists all 15 pages as **SUN-3/F**:

```
X1   SUN-3/F                 SHEET 1 OF 15
X2   SUN-3/F                 SHEET 2 OF 15    ← DRW says "SUN 68000 MEMORY BOARD"!
X3   SUN-3/F                 SHEET 3 OF 15    ← DRW says "SUN 68000 MEMORY BOARD"!
X4   SUN-3/F   UARTS         SHEET 4 OF 10    ← DRW says "SUN 68000 MEMORY BOARD"!
X5   SUN-3/F   ETHERNET      SHEET 5 OF 15
X6   SUN-3/F   SCSI          SHEET 6 OF 15
X7   SUN-3/F   PARITY        SHEET 7 OF 15    ← DRW says "SUN-3" (no /F)
X8   SUN-3/F   RAS/CAS       SHEET 8 OF 15    ← DRW says "SUN-3" (no /F)
X9   SUN-3/F   MEMORY        SHEET 9 OF 15
X10  SUN-3/F   VIDEO CONTROL SHEET 10 OF 15
X11  SUN-3/F   VIDEO MUX     SHEET 11 OF 15
X12  SUN-3/F   COLOR VIDEO RAM  SHEET 12 OF 15
X13  SUN-3/F   COLOR VIDEO   SHEET 13 OF 15
X14  SUN-3/F   MONOCHROME VIDEO SHEET 14 OF 15
X15  SUN-3/F   CAPS AND PULLUPS SHEET 15 OF 15
```

> [!IMPORTANT]
> The DRW files x2, x3, x4 were **overwritten** in the SAILDART archive with unrelated "SUN 68000 MEMORY BOARD" drawings. The WL file preserves the original correct mapping. This means the DRW content at x2/x3/x4 is wrong for the SUN-3/F board, but the WL still knows they belong to it.

## Other WL Variants for X

Multiple WL files exist for the X prefix, each representing a different board configuration:

| WL File | Pages | Description |
|---------|-------|-------------|
| `x.wl` | X1-X15 (15p) | Full SUN-3/F board |
| `xm.wl` | X1,X10M,X14M,X15,X2-X5,X8,X9 (10p) | Monochrome variant (uses `*M` pages) |
| `xc.wl` | X1-X5,X8,X9,X12,X13,XC10,XC11,XC15 (12p) | Color variant (uses `XC*` pages) |
| `x10.wl` | X10-X14 (5p) | Video subsystem only |

## BOM Files

54 BOM files exist. Each contains:
- `Part-File: X` header linking to the board prefix
- Complete component list with quantities, costs, manufacturers
- Can verify which components belong to which board

## Proposed Algorithm Enhancement

```
Priority hierarchy for page-to-board assignment:
1. WL header (highest authority — preserves original mapping)
2. DRW trailer board designator (may be stale if file was overwritten)
3. "Page X of Y" consistency
4. BOM cross-reference (component counts)
5. WD/PLT correlation (confirmation)
```

### Specific improvements:
- Parse WL headers for ALL wirelists to get per-page `(board_designator, page_function, sheet_x_of_y)`
- When WL says a page belongs to a board but DRW metadata disagrees → **trust the WL**
- Use WL page function names (PARITY, RAS/CAS, MEMORY) to fill in missing `title_line_2` from DRW
- Mark pages where DRW content was overwritten (WL says board X, DRW content is board Y)

> [!WARNING]
> For X2/X3/X4: the WL knows they should be SUN-3/F pages, but the actual DRW **drawing content** is wrong (shows memory board schematics). These pages should be included in the page list with a warning that the schematic content doesn't match.
