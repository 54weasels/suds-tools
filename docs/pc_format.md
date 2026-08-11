# PC File Format Specification

**Source**: `dscr.txt` lines 498-562, 563-664, 770-802, 806-822  
**Preserved in**: `/Users/dmoisa/Documents/sun/saildart/SUDS/bits/tots/draw/dscr.txt`  
**SUDS Version**: 21 decimal (0o25 octal) — written by IOVER in `LOWCOR.FAN[N,DRW]:189`

> **Note**: Empirical data verified against actual `.pc.O` files (like `mouse.pc.O` and `x.pc.O`).

---

## Notation Convention

```
--------
!   A
!   B
!   C
--------
D
```

Means: the sequence of words A, B, C is **repeated** until the value of A equals D.

All values are **36-bit PDP-10 words** unless otherwise noted.  
Each word is stored as two 18-bit halves: `LEFT_HALF,,RIGHT_HALF`  
Sentinel value for section boundaries: `0,,400000` (octal) = `0x20000` = `131072` decimal (Note: as a full word, this is `0o400000`).

**ASCIZ strings (RSTRZ)**: Read full 36-bit words; terminate when `word & 0o377 == 0` (low 8 bits zero). Packed 5 7-bit characters per word.

**Coordinates**: All coordinates are in mils (18-bit signed integers).

---

## File Structure

### 1. Header

| Field | Type | Description |
|-------|------|-------------|
| VERSION # | word | File format version (IOVER). SMI files observed value: 0o21 (17 decimal). |
| Nomenclature type | ASCIZ | Board/nomenclature type ("DECPC" for all observed files) |

### 2. Macros

```
--------
!   ASCIZ /MACRO NAME/
!   BYTE(9) MACRO BODY ENDING WITH 0 BYTE
--------
0
```

*Note: This section is typically empty in all observed test files.*

### 3. Body Placements

```
--------
!   LOC OF BODY (X,Y)
!   ASCIZ STRING NAME OF DIP TYPE (Usually empty word 0)
!   BYTE (6)L(12)N(18)ORIENTATION
!   XWD BODY BITS, BODY ID
!   XWD SPACING, NUM_PINS
--------
0,,400000
```

*Notes*:
- In version 0o21, the ASCIZ DIP type name is always EMPTY (a single zero word).
- The DIP type is identified by the `L` field in the orientation word, which is an index into the DIP library (`DIPS.DIP`).
- `L` is DIP library index, `N` is a sequence number.
- `SPACING` is multiplied by 5 mils for 2-pin DIPs. For larger components, spacing is 0.

### 4. Side 1 Points (Component Side)

```
--------
!   LOC OF POINT (X,Y)
!   POINT ID
!   --------
!   !   ID OF A NEIGHBOR
!   --------
!   0
!   XWD BITS, PAD_NUMBER
!   SIZE OF TEXT (0 IF NONE)
!       X,Y CONSTANT OFFSET FROM POINT LOC
!       ASCIZ TEXT (IF ANY)
!   ID OF FEED THROUGH (0 IF NONE)
--------
0,,400000
```

*Notes*:
- **Point IDs** are either generated sequential numbers or `XWD PIN_ID, BODY_ID` for DIP pins.
- **Bits**: `0o440000` = DIP pin with pad, `0o400000` = trace point. Inner planes are NOT stored as separate layers — they're represented by plane attachment bits on feed-through/pin points (bits 0-3 for planes 0-3).
- **Pad Numbers**: 0 = none, 1 = standard DIP, 2 = clearance, 3 = pin-1 square.
- **Feed-through IDs** link to the corresponding point on Side 2.

### 5. Side 2 Points (Solder Side)

```
--------
!   LOC OF POINT (X,Y)
!   ... (Same format as Side 1 Points) ...
--------
0,,400000
```

### 6. Set Centers

```
--------
!   LOC OF SET CENTER (X,Y)
!   --------
!   !   BODY ID
!   --------
!   0
!   --------
!   !   POINT ID
!   --------
!   0
--------
0,,400001
```

*Note*: This section terminates with `0,,400001` instead of `0,,400000`!

### 7. Trailer

| Order | Field | Description |
|-------|-------|-------------|
| 1 | ASCIZ | Board type |
| 2 | word | Card location word: `BYTE(4)N(5)L(3)X(6)N(18)0` |
| 3 | word | Card filename (FILNAM) |
| 4 | word | Extension: `EXT,,0` (or 0 if none) |
| 5 | word | PPN (Project-Programmer Number) |
| 6 | word | `0` (end of file) |

---

## CRD CARD.TAB Format

**Source**: `dscr.txt` lines 770-802

FMARK = `400000,,0`
CMARK = `0,,400000`

```
--------
!   --------
!   !   X,Y OF CARD OUTLINE
!   --------
!   FMARK
!   --------
!   !   X,Y START FINGER (CONNECTION END)
!   !   X,Y END FINGER
!   !   BYTE(6) 0,0,0,L,L,N
!   --------
!   FMARK
!   --------
!   !   X,Y START FINGER (BACK)
!   !   X,Y END FINGER (BACK)
!   !   BYTE(6) 0,0,0,L,L,N
!   --------
!   FMARK
!   --------
!   !   X,Y START OF SHORTING BAR (FRONT)
!   !   X,Y END
!   --------
!   FMARK
!   --------
!   !   X,Y START OF SHORTING BAR (BACK)
!   !   X,Y END
!   --------
!   CMARK
--------
CMARK
```

---

## PCP/PLT Format

**Source**: `dscr.txt` lines 563-664

Low order bit OFF always starts a new command.

### Lines
```
--------
!   XWD X*2, Y*2       (Low order bit of left half OFF means bunch of points joined by vectors)
!   XWD X*2, Y*2+1     (Ends with start of new command)
!   ...
--------
```

### Text
```
--------
!   XWD X*2+1, Y*2           (1 in left half means text)
!   XWD 0, ROTATION+SIZE*2+1 (0 in LH means text)
!   ASCII /5 CHARS OF TEXT/ + 1
--------
```
Rotation: `0` = normal upright, `400000` = rotated 90 degrees CCW.

### Small Diamond (PLT) / Drill Hole (PCP)
```
--------
!   XWD X*2+1, Y*2
!   XWD 2, 1                 (2 in left half means diamond/drill hole)
--------
```

### Pads (MPC)
```
--------
!   XWD X*2+1, Y*2
!   XWD 4, <PAD TYPE>*2+1
--------
```

These formats may be mixed until a word with `LEFT HALF = 400001` is seen. File ends with:

```
400001,,0 (+400000 if front side, +200000 if inner plane)
BITS (Bit 35 = flipped plot)
CRDNAM
CRDEXT,,0
CRDPPN
```

---

## DIPS.DIP Format

**Source**: `dscr.txt` lines 806-822

```
--------
!   # OF PINS
!   ASCIZ /DIPNAME/
!   ASCIZ /PART NUMBER STRING/
!   --------
!   !   XWD BITS, PS #
!   !   XWD HI, LOW LOADING (Signed halfwords, in .01 mA units)
!   !       (For power pins: HI is voltage in .01 V, LOW is supply current in .01 mA)
!   !   SIXBIT /USE/
!   !   SECT BITS,, 1ST SECT PIN #
!   --------
--------
0
```
