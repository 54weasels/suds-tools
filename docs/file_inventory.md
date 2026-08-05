# DRW File Inventory

## SMI Octal Files (`/sun/smi/smi/octal/`)

These are the primary target files — the actual Sun workstation schematics.

### Sun-2 "A" Board (CPU Board)
| File | Size | Description |
|------|------|-------------|
| `a01.drw.O` - `a26.drw.O` | 1.6K - 633K | 26 schematic pages |
| `a.pc.O` | 1.4MB | PC board layout |
| `a.wpc.O` | 579K | Wire-to-PC mapping |
| `a.vrn.O` | 1.8MB | Verification data |

### Sun-2 "B" Board
| File | Size | Description |
|------|------|-------------|
| `b01.drw.O` - `b19.drw.O` | 25K - 253K | 19 schematic pages |
| `b.pc.O` | 1.3MB | PC board layout |

### Sun-2/50 Board (25xx series)
| File | Size | Description |
|------|------|-------------|
| `2501.drw.O` - `2519.drw.O` | 15K - 246K | 19 schematic pages |
| `25.pc.O` | 976K | PC board layout |

### Sun-3/60 Board (60xx series)
| File | Size | Description |
|------|------|-------------|
| `6001.drw.O` - `6020.drw.O` | 15K - 250K | 20 schematic pages |
| `60.pc.O` | 1.2MB | PC board layout |

### Sun-2/100 Board (20xx series)
| File | Size | Description |
|------|------|-------------|
| `2001.drw.O` - `2008.drw.O` | 35K - 68K | 8 schematic pages |

### Color Graphics Board
| File | Size | Description |
|------|------|-------------|
| `cg1.drw.O` - `cg7.drw.O` | 55K - 226K | 7 schematic pages |
| `cg.pc.O` | 508K | PC board layout |

### Ethernet Board
| File | Size | Description |
|------|------|-------------|
| `eth1.drw.O` - `eth9.drw.O` | 17K - 129K | 9 schematic pages |
| `ethp1.drw.O` - `ethp8.drw.O` | 17K - 129K | 8 pages (variant) |

### Sun-2 "D" Board
| File | Size | Description |
|------|------|-------------|
| `d01.drw.O` - `d11.drw.O` | 34K - 267K | 11 schematic pages |
| `d.pc.O` | 460K | PC board layout |

### Float Point Processor
| File | Size | Description |
|------|------|-------------|
| `f00.drw.O` - `f20.drw.O` | 14K - 266K | 21 schematic pages |
| `f.pc.O` | 1.1MB | PC board layout |

### Memory Board (M series)
| File | Size | Description |
|------|------|-------------|
| `m1.drw.O` - `m20.drw.O` | 8K - 176K | 20 schematic pages |
| `m16.pc.O` | 342K | PC board layout |

### Libraries & Databases
| File | Size | Description |
|------|------|-------------|
| `lib.drw.O` | 780K | **Master component library** |
| `dips.dip.O` | 906K | **DIP package database (~900 components)** |
| `ecllib.drw.O` | 86K | ECL library |
| `libold.drw.O` | 431K | Older library version |
| `libs.drw.O` | 94K | Supplementary library |

### Other Notable Files
| File | Size | Description |
|------|------|-------------|
| `micro.drw.O` | 693K | Microcode-related schematic |
| `el2003.drw.O` | 910K | Large ECL schematic |
| `5380.drw.O` | 995K | Largest individual DRW file |
| `mouse.drw.O` | 50K | Mouse interface |
| `foo.drw.O` | 2.2K | Test/example file (good first target!) |

---

## SAILDART Archive (`/sun/saildart/SUDS/bits/saildart/`)

Hundreds of files from the WAITS-era SAIL system, organized by PDP-10 directory:
- `[N,DRW]` — New/current drawings
- `[D,DRW]` — SUDS "D" program (DRAW) code & data
- `[WL,DRW]` — Wirelister code & data
- `[LIB,DRW]` — Library files
- `[DAT,DRW]` — Data files (cards, DIPS database)
- `[PLT,DRW]` — Plot program code & data
- `[NEW,DRW]` — Newer versions
- `[DEC,DRW]` — DEC-related files

Notable files:
- `D.MSS[N,DRW]` (234K) — SUDS "D" program documentation
- `D.DMP[D,DRW]` (246K) — D program memory dump
- `DRAW.FAI[D,DRW]` — DRAW program source (FAIL assembly)
- `DIPS.DIP[LIB,DRW]` (424K) — Largest DIPS database version
- Various `L*.DRW[N,DRW]` files — LISP machine schematics

---

## ITS-1990 Files (`/sun/saildart/SUDS/bits/its-1990/`)

Organized by SUDS program:
- `draw/` — Drawing program files
- `pc/` — PC board layout files  
- `wl/` — Wirelister files

These use ITS "evacuated" encoding (handled by `unpack.c`).

---

## File Count Summary

| Location | DRW Files | Total Files | Format |
|----------|-----------|-------------|--------|
| `smi/octal/` | ~350+ | ~600+ | Octal-encoded |
| `SUDS/bits/saildart/` | ~200+ | ~800+ | SAILDART ANSI |
| `SUDS/bits/its-1990/` | unknown | 3 dirs | ITS evacuated |
| **Total** | **~550+** | **~1400+** | |
