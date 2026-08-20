---


---


# ROPC: A RasterOp Chip


Design Reference Document

Version 0.5

SUN MICROSYSTEMS INC.

January 11, 1982


>
This document provides a preliminary functional specification
of the RasterOp Chip (ROPC). This specification is intended as
a preliminary design reference document and as such is subject
to change.

Direct all comments pertaining to this draft to:


```

Andreas Bechtolsheim
Sun Microsystems Inc
2550 Garcia Av
Mountain View, CA 94043
415-960-1300

```


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.


---


---

# Features


## FUNCTION


RasterOp interfaces between microprocessor and bitmap memory

ROPC assists character painting, multi-window systems, and vector drawing

ROPC handles all bitshifting and bitmasking to manipulate bitmap

implements 256 functions between destination, source, and pattern register

speedup up to 10:1 over software


## GENERAL PURPOSE


16-bit data paths for processor data and memory

can be used with virtually all microprocessors

supports black&white and color displays

independent of display resolutions

supports RasterOps on main memory


## LOW-COST


28-pin package

replaces about 80 TTL packages

5V-only operation

standard TTL interface levels


---

# Architecture


## Overview


The RasterOp Chip supports raster graphics or bit-map graphics applications,
as they are present in bit-map graphics displays and raster hardcopy devices.

Raster graphics can display arbitrary characters and graphics,
including variable width fonts, foreign alphabets, mathematical symbols,
vectors, curves, shaded regions, and even photographs.
The capability of displaying composite images, that is displays that combine
both text and graphics, makes raster scan graphics a good foundation for
virtually all graphics applications, including office automation, CAD/CAM,
typesetting, and others.

RasterOp finds its application in the manipulation of raster display data.
RasterOp means that rectangular areas of display data ("Raster")
are modified or combined according to a preselected operation ("Op").
The RasterOp function provides complete generality to paint characters,
manipulate windows, scroll screens, and to draw vectors.
An example of RasterOp is shown in Figure [Figure](#RasterOP),
in which source characters are copied to a destination in the frame buffer.

Other graphic functions such as vector drawing, text, cursors,
and multiple windows can be implemented on top of the basic
RasterOp mechanism.


## History


RasterOp grew out of an attempt to unify the treatment of text and
bitmap graphics in the early history of the Xerox Smalltalk language.
It was then implemented on the Xerox Alto computer as a microcoded
instruction called BitBlt, for Bit Boundary Block Transfer.
The Alto BitBlt instruction provides 8 Boolean functions
each combining a source raster with a destination.

A generalized version of RasterOP has been implemented in the Sun Workstation.
The Sun RasterOp allows up to three operands to be combined with any one
of the 256 possible ternary Boolean functions on three operands.

The three operands are the destination, source, and the pattern.
The destination is the operand being changed in the frame buffer,
the source is an operand to be combined with the destination,
and the pattern is a third operand, aligned with the background,
that can be combined with source and destination to generate stipple patterns.
The ROPC RasterOp chip as proposed in this document is a generalized version
of the Sun RasterOp capability that is usable for a wide variety of systems.


## Literature


A. Bechtolsheim, F. Baskett, and Vaughan Pratt,
"The SUN Workstation Architecture", Technical Report No 229,
Computer Systems Laboratory, Stanford University, March 1982.

D. Ingalls, "The Smalltalk Graphics Kernel",
*Byte Magazine*, Volume 6, No. 8, August 1981.

C. P. Thacker, E. M. McCreight, B. W. Lampson, R. F. Sproull, and D. R. Boggs,
"Alto: A personal Computer", in Siewiorek, Bell, and Newell, eds., *Computer
Structures: Readings and Examples*, McGraw Hill, 1979.


---

## Design Goals


The proposed ROPC includes the following design goals:


*General Purpose*. The ROPC will need to work in a variety of display
situations, including black&white and color, frame buffers with different
resolution, different microprocessors, different memory management units,
and different main memory organizations. These issues are further
discussed below.

*Black&White and Color*. The proposed ROPC can be used with single-plane
black and white frame buffers as well as color frame buffer.
In a color system, maximum performance is achieved by stacking
one RasterOp chip per image plane.

*Resolution Independence*. The proposed ROPC is not tied to any particular
frame buffer or display resolution. Displays from 512*512 to 1024*1024
and more can be used. The ROPC will be more effective for larger displays,
though, because in the smallest displays equivalent functions can be
achieved at acceptable speed in software.

*Microprocessor Independence*. The ROPC is not tied to any particular
microprocessor. Since the RasterOp chip only deals with data and is
thus only connected to the data bus, it can be used with virtually any
microprocessor or controller.

*Virtual Memory Capability*. The ROPC must be usable in virtual memory systems
where RasterOps can be interrupted due to page faults. The proposed ROPC
includes features that allow it to save and restore all internal state
with minimal overhead.

*High-Speed Operation*. The ROPC must offer sufficient control lines that
allow a suitable sequencer to do raster operations in one cycle,
without having to reload internal registers.

*Word Memory Model*. The ROPC assumes that everything except the source
is bitaligned with the destination and that the unit of memory accesses
are 16-bit words. This means the ROPC supports raster operations on main
memory and frame buffers that are organized as words.
It also makes the ROPC compatible with error detecting and correcting memories.

*Transparent Memory Access*. The ROPC should allow easy access to memory for
normal read/write operations either by output tristate control or by a
transparent data path inside the chip.

*Simple Interface*.
The RasterOp chip set directly connects to a microprocessor and memory data bus.
The only external components required for a complete graphics system is
a simple timing generator and a videocontroller component.

*Low Cost*. The ROPC minimizes cost in three ways.
One, it is sufficiently general to be usable in many different system. Second,
the chip has a small die that is easy to test, minimizing manufacturing costs.
Third, it integrates maximum functionality and minimizes exteral parts cost.
All these reasons should make the ROPC affordable enough
such that even low-cost bitmap terminals can use it.


---

# Functional Description


This chapter describes the Operation of the ROPC in a functional way.
In particular, the ROPC's registers, combination function, and
operation are detailled.


## Registers and Function Unit


Figure [Figure](#ROPC) shows the major functional components
of the RasterOp Chip.
There are three data registers, *destination*, *source*, and *pattern*,
feeding into the function unit.
There are seven control registers controlling the operation:
*function*, *shift*, *mask0*, *mask1*, *width*, *base*, and *mode*.


![Placeholder: ropc2.press]()


*Figure: **RasterOp Chip Block Diagram***

<a id="ROPC"></a>


## Data Registers


The three data registers: destination, source, and pattern, hold the data
participating in a frame buffer update operation.
Data registers are loaded before writing new output data back to the
memory or frame buffer.


### Destination Register <16>


The destination register holds the previous data of the location
in memory being modified.


### Source Register <32>


The source register holds data to be combined with the destination data
and the pattern data to compose new output data.
There are actually two 16-bit source registers forming a single 32-bit
register from which the shifter extracts a 16-bit field bitaligned
with the desired destination data. The operation of the source register
is further described below.


### Pattern Register <16>


Like the source register, the pattern register holds data to be combined
with the destination data and source data to compose new data for the frame buffer.
However, unlike the source register the pattern data is not bitshifted
and is always aligned with the destination data.
This way, the pattern data can be used for stipple-pattern generation.


## Control Registers


The seven control registers: function, shift, mask0, mask1, width, base, and mode
control the actual raster operation described below.
Typically, the control registers are setup by the host microprocessor
and remain unchanged for the duration of the raster operation.


### Function Register <8>


The function register specifies how the function unit combines destination,
source, and pattern data to form new output data.
The eight-bit value of the function register selects one of the 256
possible RasterOps for three boolean operands (see section ``RasterOps'' below).


### Shift Register <5>


The shift register specifies the shift amount of the shifter.
Positive and negative shift amounts can be specified. The sign of
the shift amount determines which of the source registers is loaded
into the second source register before being loaded with new data
from the data bus.


### Mask0 and Mask1 Register <16>


The Mask0 and Mask1 registers enable which bits in the destination register
are actually modified and which ones are not modified. Masking is controlled
by the bit-wise OR of both register values.

A "0" bit in both Mask registers enables modification. A "1" bit in
either mask register *masks* the raster operation, causing the
affected destination bits to be rewritten with their old value.
Setting both masking registers to all "0s" effectively disables operation
of the mask registers.

The operation of the mask registers are controlled by the width and
the count register described below.


### Width Register <8>


The width register normally stores the width of the raster operation in memory words.
It is used in conjunction with the two mask registers and the count register
described below to deal with the left and right boundary conditions
in raster operations.


### Count Register <8>


The purpose of the count register is to maintain a position count
of the execution of rasterOp along a raster scan line and to deal
with the boundary conditione at the start and the end of a raster line.
The Count register achieves this by selectively enabling
the mask0 or mask1 registers on the boundary conditions.

The count register is actually a counter that can be read and written
via the microprocessor interface. The value of Count is initialized to the
0 whenever the width register is loaded.
Count is incremented by "1" every time the function output is enabled,
indicating a write to raster memory. When the value of count reaches
the value of the width register, then on the next cycle the count register
is automatically reset to 0.

The count register controls the mask registers as follows:
Whenever count is equal to 0, then the mask0 register is enabled.
Whenever count is equal to width, then the mask1 register is enabled.
In all other cases neither mask register is enabled.

Notice that by setting the width register to "0", both the mask1 and
the mask0 register are enabled continuously. Thus, setting width to "0"
effectively disables the operation of the counter.


### Mode Register


The mode register is a single bit that drives an output pin of the ROPC
to indicate external logic the execution of rasterOp cycles.
The mode register can be loaded and saved the same way
as any other register. It is thus part of the rasterop state.

---

## Combination Function


The ROPC supports a three operand RasterOp in hardware.
During a RasterOp, the ROPC generates output data
according to the function specified by the function register and as a result
of data present in the data registers: destination, source, and pattern
(see the description of these registers for details).

There are 256 possible functions mapping three boolean operands into a
boolean result.  The ROPC's eight-bit FUNCTION register selects
one of these at a time by acting as a three-bits-in, one-bit-out
lookup table for corresponding bits of the Destination, Source,
and Pattern register.

For example, suppose we want to set Output data equal to
(Destination OR Source register),
ignoring the value of the Pattern register.
Consider the application of this function to a single pixel.
The function may be expressed in tabular form as follows:


```


Pattern Source	Dest.	Output = Source OR Destination
-------------------------------
0	0	0	0
0	0	1	1
0	1	0	1
0	1	1	1
1	0	0	0
1	0	1	1
1	1	0	1
1	1	1	1
-------------------------------

```


The Pattern, Source, and Destination columns in the table form an index running
from zero (000) through seven (111).  The eight bits of the output column
uniquely specify the desired boolean function, and these are precisely
the eight bits which are to be loaded into the frame buffer's FUNCTION
register.  By convention, the least significant bit of the function
appears at the top of the table, hence this function
(Source OR Destination) is represented by the eight-bit value 11101110 (0xEE).

The ROPC allows all 256 possible RasterOp functions,
although only a few are used in practice.
For example, to clear a window, the constant function 0
(clear output) or 0xFF(set output) is applied to the desired area.
To flash (invert) a window, the function `NOT Dst` is performed on that window.
To write a character, the `Src`
function is used, while `NOT Src` writes the character inverted (black on
white). `Dst OR Src` overstrikes (paints) the character,
and `Src OR Msk` writes the character with a background pattern.


---

## Operation


In a typical operation, the control registers
(Function, Shift, Mask0, Mask1, Width, and Count)
are setup in advance and remain unchanged for the duration of the raster operation.

A 16-bit Raster Operation is performed by loading source data from the
microprocessor into the source register, reading the destination in memory
and loading its old value into the destination register, and then writing
the new output value of the RasterOp chip into the destination in memory.

The ROPC assumes that everything except the source is bit-aligned with
the destination in memory. The source data is first bit-shifted in order
to be aligned with the destination before it takes part in the raster operation.

This is achieved by implementing the source register as two 16-bit registers
that are combined to form a single 32-bit register.
Whenever the source register is loaded with new data,
its low-order 16-bits are copied into the high-order 16-bits
and the low-order 16-bits are filled with the new data.
This way, the source register contains a 32-bit value from which
any 16-bit field can be extracted by means of the barrel shifter.


## Formal Description


The barrel shifter extracts 16 bits out of the 32 bit source register
as determined by shift amount to produce aligned source SRC'.


```

	SRC' ← (SRC_NEW & SRC_OLD) ↑ SHIFT

```


SRC' is then combined bitwise with PAT and DST according to
function FUN to form SRC'':


```

	SRC'' ← FUN ( SRC', PAT, DST )

```


In parallel, the mask0 and mask1 registers are ored together to form a composite bitmask.
A "1" bit in the composite bit mask means that the corresponding destination bit is
rewritten (i.e. not changed). A "0" bit means that the corresponding bit is changed.
Mask0 and Mask1 are enabled on the left and right boundary conditions as
determined by the value of WIDTH and COUNT for first word and last word masking.


```

	MSK ← (IF (COUNT = WIDTH) THEN MASK1 ELSE 0)
	       OR (IF (COUNT = 0) THEN MASK0 ELSE 0)

```


The final output is then the bitwise combination of:


```

	OUT ← (DST AND MSK) OR (SRC''' AND NOT MSK)

```


---

# Implementation


This chapter describes a proposed pinout and interface to the ROPC chip.


## Overview


The proposed pinout is a *single-bus* or *multiplexed-bus* interface
that fits the ROPC into a single 28-pin package.
Multiplexing all functions of the ROPC over a single bus works well
for both frame buffer in memory and separate frame buffer systems.
The multiplexed bus structure offers maximum flexibility
how the part can be used while minimizing board space requirements.
In brief, the 28-pin package appears to have no deficiencies over
higher pinout packages that had been considered as long as the
multiplexed bus can be turned around with minimal delay.


## Proposed 28-Pin Pinout


```


Microprocessor and Memory Interface (22)

	D (0..15)  I/O	Data Bus.

	A (3)	   I	Address Select

	RD\	   I	Read. Reads register selected by A on Data Bus D.

	WR\	   I	Write. Writes value on data bus into register selected by A.

	CS\	   I	Chip Select Input


Sequencer Interface (4)

	MODE\	   O	Mode Output.

	LD.SRC\    I	Load Source0 and Source1

	LD.DST\	   I	Load Destination Register from Data Bus

	OE.FUN\	   I	Output Enable Function Output


Power and Ground (2)

	VCC	   VCC	+5V Power

	GND	   GND	Ground


```


---

# Microprocessor and Memory Interface


This chapter describes the interface signals that serve
both the microprocessor and the memory interface.


## Data Bus


The bidirectional data bus connects via buffers to both the
microprocessor data bus and the memory data bus.
The data bus serves four purposes:

1) to read and write on-chip registers from the microprocessor
for setting up raster operations and for saving and restoring state,

2) to load source data into the chip from the microprocessor
under sequencer control during rasterOp cycles,

3) to load destination data into the chip from the memory
under sequencer control during rasterOp cycles,

4) to write destination data to memory
under sequencer control during rasterOp cycles.

Purpose 1) is accomplished using the remaining microprocessor
interface lines (read, write, chip select, and address 0..2).
Function 2)-4) is performed by the sequencer logic using
the explicit control lines of the sequencer interface.


## Read, Write, Chip Select


These interface lines have the standard characteristics of
the Intel-type interface lines. It must be possible to assert
Chip Select continuously.


## Decoding of Address Lines A0..A2


All internal registers can be read and written via the
microprocessor interface. The three address lines A0..A2
are used to select among eight register locations in the chip.
Note that some registers are packed into a single location.
This reduces both the number of address lines required
as well as the overhead to save and restore state to the chip.


```


	-----------------------------------------
	|	Address	Register		|
	-----------------------------------------
	|	0	Destination		|
	|	1	Source0			|
	|	2	Source1			|
	|	3	Pattern			|
	|	4	Mask0			|
	|	5	Mask1			|
	|	6	Width/Count		|
	|	7	Mode/Shift/Function 	|
	-----------------------------------------


```


## Layout of Packed Registers


```


Width/Count:

	15		8		0
	---------------------------------
	| Width(8)	| Count(8)	|
	---------------------------------

Mode/Shift/Function:

	15		8		0
	---------------------------------
	| X(3)| Shift(5)| Function(8)	|
	---------------------------------
	X: Mode (1), Reserved (2)


```


---

# Sequencer Interface


The sequencer interface consists of four explicit control lines
that allow external timing logic to execute RasterOp cycles.
These four control lines, further described below, allow to explicitely
control all the ROPC registers that participate in single cycle RasterOps.
Specifically, the explict control lines allow to laad the source
and the destination registers and to control the function output.

The explicit control lines have the same effect as executing
the equivalent function via the microprocessor interface,
being wired-or to the internally decoded register controls.
The advantage of the explicit lines is that the sequencer logic
can be kept completely separate from the microprocessor interface.


## Mode Output


The mode output reflects the state of the internal mode register bit.
If set, the mode output might indicate that the microprocessor now
wants to enable the sequencer to execute rasterOp cycles
until the mode output bit is reset.

Since the mode register does not affect any on-chip functions
the interpretation of the mode output is up to the embedding system.
Typically, the mode output needs to be gated externally to be only active
when rasterOp cycles are actually being executed. For example, the signal
might need to be gated to be active only during write cycles to memory and
inactive during all other cycles.


## Load Source


In a RasterOp cycle, the load source input is the first sequencer signal
asserted. Load source is a common strobe for both source registers.
It latches the bus data either into the left or the right source register
(dependent on the setting of the left/right control bit),
while at the same time moving the previous data from the affected register
into the other register which is not being loaded.
This effectively rotates the content of source register in the direction
specified by the left/right bit.
The trailing edge of Load Source holds the data in the flow-thru
source registers. Notice that temporary storage is required between
the two halves of the source register.


## Load Destination


Load destination is the second signal asserted in a single-cycle RasterOp.
It loads the data read back from memory into the destination register.
The trailing edge of Load Destination holds the data in the flow-thru
destination register.


## Output Enable Function


Output enable Function is the final signal asserted in a single-cycle RasterOp.
It turnes around the RasterOp chip and drives the output of the function unit
back to the data bus to be written into memory.


## Timing Diagram of One-Cycle RasterOp


The following example shows how a sequencer asserts the
control lines to achieve single cycle RasterOp operation with
a read-modify-write memory cycle (All control lines are shown active low).
To minimize the length of the rmw-memory cycle it is important
to minimize the flow-through time of destination data into the chip
until valid function data output.


```

		     1)
LD.SRC\	----__________--------------------------------------------
				    2)
LD.DST\	--------------_______________-----------------------------
						    3)
OE.FUN\	-----------------------------________________-------------

Notes:

    1)	Source data from microprocessor loaded into ROPC
    2)	Destination data from memory loaded into ROPC
    3)	Output from function unit written back into memory

```


---

# Technical Summary


#### Data Registers


```

    Destination	16-bit	Data read from memory
    Source	32-bit	Source data
    Pattern	16-bit	Pattern data

```


#### Control Registers


```

    Mask0	16-bit	Mask register 0
    Mask1	16-bit	Mask register 1
    Width	8-bit	Width of raster in memory words
    Count	8-bit	Position of rasterOp along scanline
    Function	8-bit	Combination Function
    Shift	4-bit	Shift amount
    Left/Right	1-bit	Left/Right Select Bit
    Mode	1-bit	Mode Register


```


## Function Blocks


The ROPC consists out of the following major function blocks:


```

    8	16-bit registers
    1	8-bit registers
    1	4-bit registers
    1	32-bit to 16-bit shifter/extractor
    16	8-to-1 multiplexors/function generators
    16	(A AND M) OR (A AND NOT M) circuits

```
