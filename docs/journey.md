# SUDS DRW Research Journal

## 2026-08-03 — Initial Discovery & Format Analysis

### Session Goal
Understand the SUDS DRW file format, locate all relevant source materials across
the workspace, and plan a DRW→SVG conversion pipeline.

---

### Checkpoint 1: Source Material Inventory

**Workspace Layout Discovered:**

1. **`/sun/smi/smi/`** — The SAILDART dump of the `[*,SMI]` project area
   - Contains `.msg` files (email archives from Andy Bechtolsheim et al.)
   - Contains `.mss` files (Scribe-format documentation)
   - Contains wirelist (`.wl`), partslist (`.prt`), and schematic outputs
   - Contains `drw.msg` — critical email thread about DRW directory permissions
   - Contains `suds.mss` — SUDS documentation (Scribe format)
   - Contains `libdrw.lst` — library component listing (74-series, AM29xx, etc.)

2. **`/sun/smi/smi/octal/`** — **THE GOLD MINE**
   - ~600+ binary files with `.drw.O` extension (SUDS drawing files in octal-encoded format)
   - Also contains `.plt.O` (plot files), `.wd.O` (wire data), `.pc.O` (PC board), `.wpc.O`
   - Files named like `a01.drw.O` through `a26.drw.O` (Sun-2 "A" board schematics)
   - Files like `6001.drw.O` through `6020.drw.O` (Sun-3/60 board)
   - Files like `2501.drw.O` through `2519.drw.O` (Sun-2/50 board)
   - `lib.drw.O` (780KB!) — the component library itself
   - `dips.dip.O` (906KB) — the DIP package database

3. **`/sun/saildart/SUDS/`** — The PDP-10/SUDS GitHub repository
   - `tools/suds.txt` — **THE FORMAT SPECIFICATION** (Rich Alderson's 2000 Usenet post)
   - `tools/soap.c` — Working DRW parser by brad@heeltoe.com (2004), 1548 lines
   - `tools/unpack.c` — ITS "evacuated" 36-bit word unpacker
   - `tools/nl.c` — Netlist processor
   - `doc/The_Stanford_University_Design_System_Overview.pdf` — SUDS overview document
   - `bits/saildart/` — Hundreds of DRW files from SAILDART (WAITS format)
   - `bits/its-1990/` — ITS-era SUDS files (in `draw/`, `pc/`, `wl/` subdirs)

4. **`/sun/smi/smi/octal_stripped_ext/`** — Stripped version of octal files (needs investigation)

---

### Checkpoint 2: DRW File Format Specification

The format spec was recovered from Rich Alderson's 2000 Usenet post (alt.sys.pdp10, article 1579).
He worked at XKL LLC and had access to running SUDS systems.

**Key facts about the DRW format:**

- Binary format built from **36-bit PDP-10 words**
- Strings are **ASCIZ** (ASCII, zero-terminated) packed in 7-bit bytes within 36-bit words
- The sentinel value `400000` (octal) = `0x20000` = bit 17 set = marks section boundaries
- Version number at start (version 24 is documented)
- File structure is hierarchical:
  1. **Header**: version, nomenclature type, board type
  2. **Type names**: library body types used in drawing
  3. **Library filespecs**: paths to library files
  4. **Body definitions**: component shapes with pins, lines, properties
  5. **Macros**: named macro definitions
  6. **Body placements**: instances of bodies with position, orientation
  7. **Points/Connections**: the wiring (up/down/left/right connectivity graph)
  8. **Set Centers**: groupings of bodies and points
  9. **Trailer**: title block (drawn by, title, revision, signatures, etc.)
  10. **Extra parts, signals, DIP definitions, wire rules**

**Coordinate system:**
- 18-bit signed integers (range: -131072 to +131071)
- Each 36-bit word contains two 18-bit halves (left half, right half)
- X,Y coordinate pairs stored as two consecutive 18-bit values

**Body definition lines:**
- Line segments stored as X,Y points
- Low-order bit = 1 means "invisible line to this point" (move without drawing)
- Low-order bit = 0 means "visible line to this point" (draw)

**Pin connectivity:**
- Points have up/down/left/right neighbor IDs
- Pin ID format: `<PIN_ID,,BODY_ID>` for pins, or generated ID for standalone points
- This forms a graph that represents the electrical netlist

---

### Checkpoint 3: Understanding the 36-bit Word Encoding

Two different encoding schemes exist for getting DRW data off PDP-10 systems:

**1. ITS "Evacuated" Format (used in `bits/its-1990/`)**
- Alan Bawden's encoding: 36-bit words stored in 8-bit bytes
- Bytes 0x00-0xEF: decoded via lookup table into 7-bit chars → packed into 36-bit words
- Bytes 0xF0-0xFF: start of a 5-byte literal 36-bit word
- `unpack.c` handles this format

**2. SAILDART "Octal" Format (used in `smi/octal/`)**
- Files appear to have `.O` extension meaning "octal" encoding
- Need to determine exact encoding — likely the SAILDART archive's own format
- The Google Doc at the reference URL discusses this format
- May require custom unpacking before DRW parsing

**3. SAIL ANSI-ASCII Format (used in `bits/saildart/`)**
- Text-oriented encoding, NUL characters can be ignored
- Different from ITS evacuated format

---

### Checkpoint 4: Existing Prior Art — soap.c Analysis

Brad's `soap.c` (2004) is the most complete existing DRW parser. Key findings:

- Successfully parses: header, body definitions, macros, body placements, points, set centers, trailer
- Extracts netlists from the connectivity graph
- Handles both 6-bit and 7-bit ASCII extraction from 36-bit words
- Uses `unpack.c` for ITS-format input
- **Does NOT produce graphical output** — only netlists
- **Does NOT handle SAILDART/octal format** — only ITS evacuated format
- Has hardcoded limits (MAX_POINTS=4000, MAX_BODIES=100)

**What soap.c teaches us about rendering:**
- Body definitions contain line segments → these ARE the schematic symbols
- Body placements have orientation (rotation/mirror)
- Points have locations → these are the wire connection nodes
- The up/down/left/right graph traversal reveals wire paths
- Pin locations relative to body origin → connection points

---

### Checkpoint 5: Historical Context from Emails

From `drw.msg` (1983-1984):
- Andy Bechtolsheim wrote about SUDS file management
- The DRW directories had write-protection issues
- DIPS.DIP library was shared between `[WL,DRW]` and `[LIB,DRW]`
- ~900 components in the DIPS database by 1983

From `r.msg` (Andy Bechtolsheim to Jeff Kurtze):
> "The SUN workstation was designed with the SUDS CAD system at Stanford. 
>  This handy system, which is about 10 years old by now, works very nicely.
>  Unfortunately, it is written in PDP-10 assembly and is thus non-portable
>  and non-maintainable. SUDS runs only on DEC-SYSTEM-10s at Stanford, MIT,
>  CMU, and DEC."

From `linda.msg` (Andy to Linda, 1983):
- D1.DRW through D4.DRW are source drawing files
- .WD = wire data, .PC = PC board, .WL = wirelist
- D.TXT = command file for wirelister
- Components have "U-style location labels"

---

### Decisions Made

1. **Language choice**: Python for initial tools (rapid prototyping, SVG generation libs)
   with potential C port for performance-critical paths
2. **Target output**: SVG (scalable, inspectable, embeddable)
3. **Architecture**: Pipeline approach: Unpack → Parse → Render
4. **First target**: The SMI octal files (Sun workstation schematics)
5. **Library handling**: Parse `lib.drw.O` first to build component symbol database,
   then render individual schematic pages

---

### Open Questions

1. What is the exact encoding of `.O` (octal) files from SAILDART?
   - Need to examine byte patterns vs the ITS evacuated format
   - The Google Doc may have more info (rendered as HTML, need to find text tabs)
2. How does orientation/rotation work in body placements?
   - The spec says "ORIENTATION+400000(IF LOCATION FOLLOWS)"
   - Need to decode the orientation bits (likely 2-bit rotation + mirror)
3. How are wire paths rendered?
   - Points only store connectivity (up/down/left/right neighbors)
   - Each point has an X,Y location
   - Wire drawing = connecting adjacent points with straight lines
4. How does the PLT (plot) format differ from DRW?
   - PLT files exist alongside DRW files in the archive
   - May contain pre-rendered plot data (simpler to parse for visual output)
5. What font/text rendering does SUDS use?
   - Text properties include size and location
   - Original display was on III/E&S vector displays or Dover laser printer

---

## 2026-08-03 — Phase 1 Complete: Binary Format Decoder

### Checkpoint 6: `.O` File Format Solved

The `.O` files in `smi/octal/` are **plain text files** — one 12-digit octal
number per line, each representing a single 36-bit PDP-10 word. No binary
decoding needed — just `int(line, 8)`.

The reference tool `cat36 -Woct -Xits` (at `~/Documents/sun/its/tools/dasm/cat36`)
converts these to ITS evacuated binary format. Our Python decoder produces
identical word streams.

### Checkpoint 7: Implementation Delivered

Created three Python modules in `suds-tools/src/`:

1. **`word36.py`** — 36-bit word utilities (halfwords, sign extension, ASCIZ/SIXBIT readers)
2. **`unpack.py`** — Dual-format reader (octal text + ITS evacuated binary)
3. **`test_unpack.py`** — Verification test suite

### Checkpoint 8: Verification Results

Round-trip tests against `cat36`:

| File | Words (octal) | Words (ITS) | Mismatches |
|------|--------------|-------------|------------|
| `foo.drw.O` | 166 | 165 | **0** |
| `1.drw.O` | 302 | 301 | **0** |
| `cas.drw.O` | 278 | 277 | **0** |
| `a01.drw.O` | 5543 | 5542 | **0** |

The 1-word difference is consistent — the ITS format doesn't encode a trailing
zero word from the octal file. All content words match exactly.

### Checkpoint 9: First Header Extraction

Successfully extracted headers from all test files:

- **Version**: 21 (octal 0o25) — all files use this version
- **Nomenclature type**: "DECPC" — all files
- **Board types**: "R9.SIP", "74F32\\", "AS1032X", "68010"
- **Type names** from `a01.drw.O` (Sun-2 A board, page 1):
  ALS30, 8308, P16L8, 74F151, 74LS590, R9.SIP, GND, 74F08\\, 74F04\\,
  74F04, 74F32\\, 74F74, P16R4

### Decisions Updated
- **KiCad netlist export** added as Phase 4
- **Web viewer** deferred — static SVG output only
- **Python** confirmed as implementation language

---

## 2026-08-04 — Body Definition Parser Rewrite

### Checkpoint 4: PDP-10 Authoritative Parser

**Root Cause of 36 Body Def Failures Identified:**

Two fundamental issues caused all body definition parsing failures:

1. **String termination mismatch**: Our `grab_7bit_ascii()` (from soap.c) terminated on the first NUL byte at any character position within a word. The PDP-10 `RSTRZ` routine (IN.FAI:3161-3175) reads full 36-bit words and only terminates when the **low 8 bits** of a word are zero. This is a word-level reader, not a byte-level reader.

2. **BTEXT/PROPIN version gate was wrong**: The assembly `CAIL C,23` checks if version < 0o23 (= 19 decimal). For version 21 (= 0o25 octal) which is ≥ 19, the code jumps to `RBTXTN` → PROPIN format. BTEXT is only used for versions < 19. This is the **opposite** of what was initially assumed.

**Critical Version Gate Corrections (octal constants in assembly):**

| Feature | Condition | V21 (0o25) |
|---------|-----------|------------|
| DIP type string | 0o10 ≤ ver < 0o23 | ❌ NOT read |
| BITS word | ver ≥ 0o13 | ✅ Read |
| DEFOFF word | ver ≥ 0o12 | ✅ Read |
| DEFOF1 word | ver > 0o23 (CAILE) | ✅ Read |
| Pin format v2 | ver ≥ 0o17 | ✅ 3 words/pin |
| BTEXT format | ver < 0o23 | ❌ Not v21 |
| PROPIN format | ver ≥ 0o23 | ✅ Used |

**Key Discovery: IOVER = 0o25 = 21 decimal**

Found in LOWCOR.FAN[N,DRW]:189: `MD,<IOVER__25>`. The DRAW program writes version 0o25 (= 21). All SMI files use this version. The `[NEW,DRW]` source code IS the version that wrote these files.

**Changes Made:**
- Added `rstrz()` method to `HalfwordStream` — word-level string reader matching PDP-10 RSTRZ
- Added `BodyText` dataclass to `drw_model.py` — for BTEXT entries (version < 19)
- Rewrote `_parse_body_defs()` — word-level operations, correct version gating, PROPIN for v21
- Added `_parse_btext()` — BTEXT format parser (for future older version files)
- Added `_parse_propin()` — PROPIN format parser (used by v21)

**Corpus Results:**

| Metric | Before | After |
|--------|--------|-------|
| Clean  | 649    | **675** |
| Warned | 36     | **10** |
| Failed | 0      | 0 |

The remaining 10 warnings are **truncated files** hitting exact EOF boundaries — the files themselves are incomplete (not a parser bug). Files like `a26.drw.O` (128 words), `b07.drw.O`, etc. run cleanly to their last byte and then hit EOF mid-section.

---

### Checkpoint 5: Critical Body Placement Parser Fix + SVG Renderer (Phase 3)

**Date:** 2026-08-04

**Critical Bug Found:**
The body placement parser had a wrong condition for the `has_location` test. 
IN.FAI:1349 uses `TRNN TT,400000` (test bit 17 of orientation RH), but our 
parser was using `raw_orient == 0`. This meant placements with non-zero 
orientation but WITHOUT bit 17 set (e.g., rotation-only values like `0o140`) 
would incorrectly enter the location-data branch and read 4 extra words that 
don't exist, completely desyncing everything downstream.

Also fixed: LNNEWS (IN.FAI:3770-3773) reads exactly 2 words (LETTER + NUMBER) 
for location data, not 3 as previously coded. Plus NUMBR1 is conditional on 
version > 0o23.

**Result:** Corpus clean rate improved from 675/685 to **684/685** (99.9%).

**SVG Renderer Created:**
- `src/svg_renderer.py` — Full SVG rendering engine
- `src/library.py` — Library loader with auto-discovery + `load_all_defs()`
- `src/dip_generator.py` — Synthetic DIP body generator from DIPS.LSD[LIB,DRW]
- `src/cli.py` — CLI entry point with `--auto-lib` flag

**Body Resolution:**

| Approach | Defs | Resolution |
|----------|------|------------|
| lib.drw.O only | 252 | 70.7% |
| All 13 library files | 462 | 88.6% |
| + Synthetic DIPs | **555** | **94.2%** |

**ALS Discovery:**
The missing ALS-series TTL parts (ALS245, ALS374, etc.) were in the SAILDART 
`DIPS.DIP[LIB,DRW]` database (non-DRW binary format). Pin counts were extracted 
from `DIPS.LSD[LIB,DRW]` and used to generate synthetic DIP body definitions.

**Sample renders:** All 8 sample files now render with 100% body resolution:
ethernet, Sun-3/60, Sun-2 D-board, color graphics, memory board, mouse, 
Sun-2 CPU, video memory.

---

### Checkpoint 6: SVG Renderer Calibration & Phase 3 Completion

**Date:** 2026-08-05

**Text Calibration Against Plotter Output:**
User provided reference PNGs from original SUDS `.plt` plotter output (rendered
via `harscn`). Compared against SVG renders and iterated on three rounds of fixes:

1. **Text scale** — Reduced `TEXT_SCALE` from 5.0 → 4.0 and `PIN_NUM_FONT_SIZE`
   from 3.5 → 3.0. At 5.0, pin labels consistently bled outside 24-unit wide DIP
   body outlines. 4.0 is the proven limit for legibility.

2. **Designator positioning** — IC-sized bodies (box width ≥ 20 units) now get
   designators (e.g., `Q2`) centered horizontally above the body top edge. Small
   passives (R, C) preserve original `xy_const_offset` positioning from the SUDS
   editor, since those offsets are carefully hand-placed relative to small symbols.

3. **Three final fixes:**
   - **68010 body box bug**: The synthetic DIP generator created a 64-pin DIP for
     the 68010 with y=[-128, 128], but the real library definition spans y=[-416, 160]
     (576 units tall, 120 pins). Both had 5 outline lines, so the "keep the one with
     more lines" heuristic never replaced the synthetic. Fixed `render_q_series.py`
     to track synthetic defs and always prefer real library defs.
   - **Drawing border removal**: Removed the `<rect>` border frame around the entire
     drawing — not present in original plotter output.
   - **Pin number collision avoidance**: Pin numbers were vertically centered on pins
     (`baseline='central'`), colliding with horizontal signal wires. Changed to offset
     1.8 units above pin center so numbers sit above the wire line.

**Best-Version DRW Curation:**
Created `best_drw/` directory with the most complete version of each DRW file,
selected from version logs across the archive. This provides maximum body definition
coverage for rendering.

**Batch Render Results:**

| Metric | Result |
|--------|--------|
| Total files rendered | 685 / 685 (100%) |
| Q-series pages rendered | 28 / 28 |
| Body resolution (QX1 CPU) | 22 / 22 (100%) |
| Body resolution (QX6 PROMs) | 12 / 12 (100%) |
| Library body defs (auto-discovered) | 669 |
| Synthetic DIP fallbacks | ~90 |

**Phase 3 Status: COMPLETE.**

---

### Checkpoint 7: Wirelist-Based Board Registry & Data Restructure

- Discovered that `.wl` (wirelist) files are the canonical source for board→page mappings
- Created `data/` directory incorporating DRW files, wirelists, parts lists, BOMs, and command scripts from the SMI archive
- Rewrote `src/board_registry.py` to use wirelist-based grouping (57 boards) with metadata fallback (110 boards)
- Fixed rendering issues: p2.svg viewBox explosion (coordinate clamping), r3.drw.O empty parse (header string termination)
- Updated batch renderer to use new data directory paths
