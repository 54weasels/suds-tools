# Version Selection & Coherence Algorithm

This document describes the version recovery process and the designator-first
coherence algorithm used to group SUDS DRW schematic pages into coherent board
revisions.

## The Problem

The SAILDART SMI archive contains 685 DRW schematic files. A single board prefix
(e.g., `x` for the Sun-3 CPU board) may contain pages from **multiple design
revisions** spanning years of development. The filename `x2.drw.O` might have
started as a "SUN 68000 MEMORY BOARD" schematic (1982), evolved into a "SUN-3"
page (1985), and finally became a "SUN-3/F" page (1986).

The challenge is to:
1. Select the correct file version for each page
2. Group pages into coherent board revisions
3. Identify the "best" (most complete) revision

## Version History

### SAILDART Archive Structure

```
smi/octal/{name}.drw.O        # Latest/final version
smi/prev/{name}.drw.{N}.O     # Version N (1 = oldest, higher = newer)
```

The `smi/prev/` directory contains **5,197 version history files**. Each file
represents a snapshot at one point in time. The file in `smi/octal/` is the
final version that was on disk when the SAILDART archive was captured.

### Version Recovery

The `data/drw/` working directory was initially populated by a curation script
that selected from version history. This script made incorrect choices for
**189 files** — picking older versions instead of the latest.

**Recovery process:**
1. MD5 comparison of all 685 files between `data/drw/` and `smi/octal/`
2. Parse both versions to extract metadata (title, page number, "of" total)
3. Replace all mismatched files with the canonical `smi/octal/` version
4. Save audit trail to `data/version_recovery.json`

**Example — x2.drw.O version history:**

| Version | Date | Board Designator | Page/Of |
|---------|------|------------------|---------|
| x2.drw.1.O | 1982-04-06 | SUN 68000 MEMORY BOARD | 2/4 |
| x2.drw.2.O | 1984-05-03 | LONG-DISTANCE-KIT | 2/2 |
| x2.drw.3.O | 1985-11-30 | SUN-3 | 2/10 |
| x2.drw.4.O | 1986-04-05 | SUN-3/E | 2/15 |
| x2.drw.5.O | 1986-06-01 | SUN-3/F | 2/15 |
| x2.drw.6.O | 1986-06-29 | SUN-3/F | 2/15 |
| **x2.drw.O** | **1986-07-08** | **SUN-3/F** | **2/15** |

This single filename held content for **four different boards** over its lifetime.

## Data Authority Hierarchy

When determining which board a page belongs to, these sources are consulted
in priority order:

| Priority | Source | Description |
|----------|--------|-------------|
| 1 (highest) | **WL header** | Per-page board name from wirelist generation |
| 2 | **DRW trailer** | Board designator extracted from title block |
| 3 | **DRW "of" field** | Self-declared "Page X of Y" total |
| 4 | **BOM** | Bill-of-materials cross-reference |
| 5 (lowest) | **WD/PLT** | Wire data / plotter correlation |

### WL Authority Map

The WL (Wirelist) file header contains the **definitive** per-page board
identity from the time the wirelist was generated. This is stored in
`data/wl_authority.json` (66 wirelists, 564 page entries).

WL format (per page):
```
X2	1,SMI		08-JUL-86  0750
	SUN-3/F						DECPC
						SHEET 2 OF 15
```

Each page entry records: board name, page function, board type, sheet number,
and date. The WL is more authoritative than DRW metadata because DRW files
can be overwritten with unrelated content while the WL preserves the mapping
from when the wirelist was last generated.

## Coherence Algorithm

### Board Designator Extraction

The board designator is extracted from the DRW trailer `title_line_1` by
stripping copyright/company prefixes:

```python
"(C) 1982 SMI, SUN 68010, CPU"        → "SUN 68010"
"PROPRIETARY SMI, SUN-2, CLOCKS"       → "SUN-2"
"SUN-3/F"                              → "SUN-3/F"
"FERRARI"                              → "FERRARI"
"(C) 1982 SMI SUN 68000 MEMORY BOARD"  → "SUN 68000 MEMORY BOARD"
"SUN MICROSYSTEMS INC" + "501-1007-08" → "501-1007-08"  (fallback to title2)
```

When the stripped title is empty (company name only), the algorithm falls
back to `title_line_2` which often contains a Sun part number.

### Normalization

Related board names are normalized to a common root:
- `SUN 68010`, `SUN-2 CPU`, `SUN-2/50` → `SUN-2`
- `SUN-3` and `SUN-3/F` merge only when sharing the same "of" total

### Grouping

Pages are clustered by `(normalized_designator, of_total)`:
1. Build initial clusters from all pages
2. Merge clusters sharing the same designator root and "of" value
3. For each cluster, select the best page for each position

### Scoring

Each version set receives a weighted score:

$$\text{Score} = 0.35 \times C_{\text{desig}} + 0.20 \times C_{\text{of}} + 0.20 \times C_{\text{coverage}} + 0.15 \times C_{\text{wl}} + 0.10 \times C_{\text{size}}$$

| Component | Weight | Description |
|-----------|--------|-------------|
| C_desig | 0.35 | Fraction of pages with matching board designator |
| C_of | 0.20 | Fraction of pages agreeing on "of Y" total |
| C_coverage | 0.20 | Pages present / total declared (completeness) |
| C_wl | 0.15 | 1.0 if target matches WL page count, 0.5 if off by 1 |
| C_size | 0.10 | Prefer later/larger revisions |

The board designator has the **highest individual weight** — this is the board
identity printed in the lower-left title block and is the most reliable single
signal for determining which board a page belongs to.

### Output

Version-aware PDFs are named:
```
{board_id}_v{N}_{designator_slug}_of{total}_s{score%}[_BEST].pdf
```

Example for the X prefix:
```
x_v1_sun_3_f_of15_s96%_BEST.pdf       # 14/15 SUN-3/F pages ★
x_v2_ferrari_of20_s66%.pdf              # 1/20 Ferrari pages
x_v3_sun_3_of12_s63%.pdf                # 1/12 SUN-3 earlier revision
```

## Implementation

- **Algorithm**: `src/version_coherence.py`
- **Batch renderer**: `scripts/batch_render.py` (with `--versions` flag)
- **Index generator**: `scripts/generate_index.py`
- **Recovery data**: `data/version_recovery.json`
- **WL authority**: `data/wl_authority.json`
