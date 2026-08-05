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

### Corpus Status
- **675/685 files** parse cleanly (98.5%)
- **10 files** have warnings (all are truncated files hitting EOF at exact file boundary)
- **0 failures**

### What Has Been Completed
- Phase 1: Binary format decoder (`word36.py`, `unpack.py`) — bit-perfect
- Phase 2: DRW parser (`drw_parser.py`, `drw_model.py`) — 98.5% clean
  - Header, type names, library filespecs
  - Body definitions with correct RSTRZ + PROPIN (and BTEXT for old versions)
  - Macros, body placements, points (halfword-level, working)
  - Set centers, trailer, extra parts, signals, DIP/wire-rule filespecs

### What Needs To Be Done Next
1. **SVG Renderer** — Map body def lines to SVG paths, handle orientation transforms, render text
2. **KiCad Netlist Export** — Traverse point connectivity graph, output KiCad format
3. **Component Library Parsing** — Load `lib.drw.O` symbol database for cross-referenced drawings
4. **Batch Processing** — CLI tools to batch-convert directories

### Key Reference Files
- Journey: `suds-tools/docs/journey.md`
- Format spec: `suds-tools/docs/drw_format.md`
- PDP-10 source: `saildart/SUDS/bits/saildart/IN.FAI[NEW,DRW]` (THE authority)
- Parser: `suds-tools/src/drw_parser.py`
- Model: `suds-tools/src/drw_model.py`
- Binary decoder: `suds-tools/src/word36.py`, `suds-tools/src/unpack.py`

### Architecture
- **Python** for the toolchain
- **Pipeline**: `unpack(bytes) → parse_drw(words) → render_svg(drawing)`
- **Body defs use word-level RSTRZ**, placements/points use halfword-level grab_7bit_ascii
