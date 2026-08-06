# Continuation Prompt

> Use this prompt to continue work on the SUDS DRW → SVG conversion project
> in a new AI session. It captures all the critical context discovered so far.

---

## Prompt

You are continuing work on a project to build tools that read vintage Stanford SUDS (Stanford University Drawing System) `.DRW` schematic files and render them as modern SVG vector graphics.

### Project Location
- **Tools/docs**: `/Users/dmoisa/Documents/sun/smi/suds-tools/`
- **SMI archive** (text files, emails, docs): `/Users/dmoisa/Documents/sun/smi/smi/`
- **Binary DRW files** (octal-encoded): `/Users/dmoisa/Documents/sun/smi/smi/octal/` — 685 `.drw.O` files
- **Best-version DRW files** (curated): `/Users/dmoisa/Documents/sun/smi/suds-tools/best_drw/`
- **SUDS tools & source**: `/Users/dmoisa/Documents/sun/saildart/SUDS/`
  - `tools/suds.txt` — DRW format specification
  - `tools/soap.c` — existing DRW parser (netlist only, no graphics) by brad@heeltoe.com
  - `tools/unpack.c` — 36-bit word unpacker for ITS evacuated format
  - `tools/nl.c` — netlist processor
  - `doc/The_Stanford_University_Design_System_Overview.pdf` — SUDS overview
  - `bits/saildart/` — SAILDART archive DRW files (WAITS encoding)
  - `bits/its-1990/` — ITS-era DRW files (evacuated encoding)
- **Authoritative PDP-10 source** (CRITICAL — primary reference, NOT soap.c):
  - `bits/saildart/IN.FAI[NEW,DRW]` — File reading code (RSTRZ, RDTYPX, RDBOD, RDPNT)
  - `bits/saildart/OUT.FAI[NEW,DRW]` — File writing code
  - `bits/saildart/FIRST.FAI[NEW,DRW]` — Initialization
  - `bits/saildart/WLFST.FAI[NEW,DRW]` — Bit definitions and constants
  - `bits/saildart/LOWCOR.FAN[N,DRW]` — IOVER definition (line 189: `MD,<IOVER__25>`)

### What is SUDS?
SUDS was a CAD system on PDP-10 mainframes (1970s-80s) used by Andy Bechtolsheim at Stanford to design the original Sun workstations. Files use 36-bit word binary format with:
- ASCIZ strings via RSTRZ: reads full 36-bit words, terminates when LOW 8 BITS of a word = 0
- 18-bit signed coordinates
- Sentinel value `0o400000` (0x20000) marking section boundaries
- Hierarchical structure: Header → Type Names → Libraries → Body Defs → Macros → Placements → Points → Set Centers → Trailer → Extra Parts → Signals

### Critical Technical Discoveries

**1. Version = 21 decimal = 0o25 octal for ALL SMI files.**
   - IOVER defined as 25 (octal) in LOWCOR.FAN for Drawing mode (MD).
   - Assembly comparison constants (CAIL, CAILE, CAIGE) use OCTAL literals.

**2. Version Gate Corrections (ALL constants are OCTAL):**

| Feature | Assembly Gate | V21 (0o25) |
|---------|--------------|------------|
| DIP type string | 0o10 ≤ ver < 0o23 | NOT read |
| BITS word | ver ≥ 0o13 | Read |
| DEFOFF word | ver ≥ 0o12 | Read |
| DEFOF1 word | ver > 0o23 | Read |
| Pin format v2 | ver ≥ 0o17 | 3 words/pin |
| BTEXT format | ver < 0o23 | NOT used for v21 |
| PROPIN format | ver ≥ 0o23 | Used for v21 |

**3. RSTRZ is word-level, not byte-level:**
   - Reads full 36-bit words, NOT individual characters
   - Zero word → failure return (empty string)
   - Non-zero word → decode chars, check low 8 bits for NUL
   - This is different from soap.c's `grab_7bit_ascii` which stops at first NUL byte

**4. Body def PROPIN format (v21):**
   Each entry: RSTRZ(value) + RSTRZ(name) + 3 WORDIN (text_size, text_loc, const_offset)
   Terminated by RSTRZ failure (zero word).

**5. soap.c is NOT authoritative:**
   It gets several things wrong (byte-level strings, property format for v21 files, point bits as enum not bitfield). Use the PDP-10 IN.FAI source as the primary reference.

### What Has Been Completed

**Phase 1: Binary Format Decoder** ✅
- `word36.py`, `unpack.py` — bit-perfect decoding verified against `cat36`

**Phase 2: DRW Parser** ✅
- `drw_parser.py`, `drw_model.py` — 675/685 clean (98.5%)
- All 13 file sections parsed

**Phase 3: SVG Renderer** ✅
- `svg_renderer.py` — Full rendering engine (body symbols, wiring, text, title block)
- `library.py` — Auto-discovers 12 library files (669 unique body defs)
- `dip_generator.py` — Synthetic DIP fallback for bodies not in libraries
- `render_q_series.py` — Batch rendering script
- 685/685 files render successfully (100%)
- 28 Q-series pages (Sun-2 68010 CPU) rendered with 100% body resolution
- Monochrome plotter-style output calibrated against original `.plt` output
- Text scale: `TEXT_SCALE=4.0`, `PIN_NUM_FONT_SIZE=3.0`
- Library defs always override synthetic DIPs (fixed priority bug with 68010)
- Pin numbers offset above wire lines to avoid collision
- IC designators centered above body; passives preserve SUDS editor offsets

### What Needs To Be Done Next
1. **KiCad Netlist Export** — Traverse point connectivity graph, output KiCad format
2. **Batch Processing** — Multi-page PDF output, board-level aggregation, index pages
3. **Further visual refinements** — Any remaining text alignment or body rendering issues

### Key Reference Files
- Journey: `suds-tools/docs/journey.md`
- Format spec: `suds-tools/docs/drw_format.md`
- PDP-10 source: `saildart/SUDS/bits/saildart/IN.FAI[NEW,DRW]` (THE authority)
- Renderer: `suds-tools/src/svg_renderer.py`
- Parser: `suds-tools/src/drw_parser.py`
- Model: `suds-tools/src/drw_model.py`
- Binary decoder: `suds-tools/src/word36.py`, `suds-tools/src/unpack.py`
- Library loader: `suds-tools/src/library.py`
- Batch script: `suds-tools/scripts/render_q_series.py`

### Architecture
- **Python** for the toolchain
- **Pipeline**: `unpack(bytes) → parse_drw(words) → render_svg(drawing)`
- **Body defs use word-level RSTRZ**, placements/points use halfword-level grab_7bit_ascii
- **Library priority**: Inline defs > Library defs > Synthetic DIPs
- **SVG coordinate system**: Y-flipped via `scale(1,-1)`, viewBox from bounding box + 20u padding
- **Transform order**: `translate(x,y) scale(-1,1) rotate(angle)` (SVG right-to-left)
