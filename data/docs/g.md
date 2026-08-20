---


---


# SUN 1024 Video Board


# Theory of Operations


SUN MICROSYSTEMS INC.

September 1982


>
**Trade Secret Notice**

This document contains unpublished, proprietary information
and describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied
or duplicated in any form without the prior written consent of
SUN MICROSYSTEMS INC.


>
Multibus is a trademark of Intel Corporation.


---


---

# Principles of Operation


## Introduction


This chapter provides a description of the SUN 1024 Video Board circuit operation.
The discussion assumes that the reader is familiar with the architecture,
the installation, and the programming of the SUN 1024 Video Board.
In addition, the discussion assumes that the reader has a working knowledge
of digital electronics and has access to descriptions of the components
used on the board.

A set of schematic diagrams for the SUN 1024 Video Board are included
in Chapter 6 of this manual and a complete wirelist is included
in Chapter 7. The following two sections illustrate the conventions
employed in the schematics and the wirelist.


## Schematic Conventions: Signals


When possible, the schematics were drawn to standard drafting conventions
with input signal entering from the left and output signals exiting to the right.

Both active-high and active-low signals are used.
A signal name that is followed by a backslash ("\") indicates
that the signal is asserted active low (<0.4V), e.g. OE\.
Conversely, a signal without a backslash denotes a
signal that is asserted active high (>2.0V).

For signals with multiple meanings or synonyms,
the synonyms are listed separated by a slash "/".
For example, the signal name for a read-write signal
that is active low for write is "READ/WRITE\".
For signals with multiple functions that are exclusive of each other,
the names are listed separated by a vertical bar or "|".

Signals that are part of busses are indicated by a common prefix
followed by a number. For example, a 16 bit data bus might be labelled
"D0", "D1", "D2", and so on until "D15".
A group of signals that are part of a signal vector are denoted by
a common prefix separated by the suffix with ".".
For example, all Multibus signals start with the prefix "B.".

Clock signals that are labelled C#1.#2-#3 are periodic clocks that are
described by their signal name.
The first number after the "C" indicates the clock period in nanoseconds,
the second number the beginning of the active clock phase,
and the third number the end of the active clock phase.
Other clocks are labelled according to their function.

---

## Schematic Conventions: Components


Components in the schematics are identified by Component Name
(also referred to as Body Name in the wirelist).
Components are named according to "generic" or industry standard names.
The way components are drawn reflects their circuit function rather than
the manufacturer's definition.
Components that are used in the logical inverse of their normal form,
such as inverted-input gates, are identified by a name followed
by a backslash (e.g. 74LS00\).

Each component carries a location label identifying its component type
and approximate location on the board.
Location labels consist of one letter followed by three digits.
The letter indicates the type of component and is one of:


	Letter	Component Type
	--------------------------------
	C,K,X   Capacitor
	J       Jumper of Connector
	R       discrete Resistor
	S       single-in-line component
	U       dual-in-line component


The three digits give the approximate component position on the board,
with the first digit indicating the row position and the last two digits
the position along the row.

Component names (Body Names) are translated into Diptypes that specify
a particular physical component associated with the component name.
A Diptype specifies a particular physical component
associated with one or several component names.
There is only one diptype for components that are sections
of the same physical package (e.g. gates of a 74LS00 diptype).

Location labels are cross-indexed in the wirelist
into diptype and component names and locations on the schematics.
Diptypes are translated by the parts list
into manufacturer codes and part names.


## Schematic Conventions: Programmable Logic


Programmable logic elements such as PALs and PROMs are described
in a high-level functional language from which they are translated
automatically into the bitpatterns for programming.

Programmable logic elements are identified by name.
The source code for the programmable logic is included in chapter 5 of this manual.
Tables and timing diagrams explaining programmable logic elements
are included in the description of the particular
functional block whenever appropriate.

---

## Power


The SUN 1024 video board is designed for 5V-only operation.


## Initialization


When the B.INIT\ signal is received from the Multibus,
the control register (U506) is cleared to all 0's,
thereby disabling video (EN.VIDEO), interrupts (EN.INT),
and setting the interrupt level to 0. The negated interrupt enable (EN.INT)
also clears any interrupts pending in interrupt flipflop (U402)
via NAND gates (U202-2, U202-1).


## Timing


On board timing is generated by the K1114 crystal oscillator (U301)
in conjunction with a flipflop divider (U402).
The frequency of the crystal oscillator is the video clock.
For the standard landscape video monitor (see below), this frequency is 40.00 MHz.

The output of the crystal oscillator, C25.0-12, is
routed to the video shift register (U707, U708) and to
the flipflop divider (U402).
The half-frequency clock signal, C50.0-25, clocks the memory controller state machine
and other synchronous functions on the board.


## Memory Controller


The memory control state machine generates the memory timing
and other basic timing strobes for the graphics board.
It consists of PROMs 74S288 (U107,U307) and latches 74S374 (U106,U306).
The state machine is clocked with the basic system clock C50.0-25.

The state machine has a total of 32 states and executes
at any time one of four major cycle types of 8 states duration.
The four major cycles correspond to the four basic operations of the memory:
read-cycle, write-cycle, refresh-cycle, or idle-cycle.
Each cycle is 400 nsec long, consisting of 8 states of 50 nsec each.
In the timing diagram below, the eight states are labelled 0 through 7,
showing the timing of the state machine outputs.


---

## Memory Controller Timing Diagram


```

	Cycle	Type

	0	Refresh Cycle
	1	Write Cycle
	2	Read Cycle
	3	Idle Cycle

Signal	Refresh Cycle	Write Cycle	Read Cycle	Idle Cycle

	0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7

C50	-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

RAS\	--____________----____________----__________--------------------

CAS0\	----____--______----____________----________--------------------

CAS1\	----____--______------__________------______--------------------

WE\	----------------------------__----------------------------------

LD.BUF	________--______--______________________________________________

OE.PRT\	------------------____------------____--------------------------

LD.REG\	------------------__----------------------__--------------------

OE.SRX\	----------------------------------------------__----------------

LD.PRT\	______________________________________________--________________

C.S0	--______________--______________--______________--______________

C.S3	______--______________--______________--______________--________

C.S7	______________--______________--______________--______________--

STATE0	__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--

STATE1	____----____----____----____----____----____----____----____----

STATE2	________--------________--------________--------________--------

ACK	------------------__--------------------------__----------------


```


---

## Video Controller


The video controller generates the timing for the video monitor.
The timing described herein applies to a "standard landscape monitor"
that has the following attributes:


	800 by 1024 pixel active display area
	30.5 kHz horizontal frequency
	77 Hz vertical frequency.


The video controller consists of the following components:
horizontal counter 74LS393 (U205),
vertical counter 74LS393 (U203,U204),
interlace toggle 74LS393 (U203),
horizontal decode PROM 3622 (U105),
vertical decode PROM 3622 (U104), and
video controller latch 74LS374 (U4).

Horizontal counter is advanced every 400 nsec with the
falling edge of C.S3. Second section of horizontal counter
is clocked with H3 output of first section.
Horizontal counter is reset with HRESET generated by video controller latch.

Vertical counter is clocked with VCLOCK1\, a delayed version of VCLOCK.
Purpose of flipflop 74LS74 (U303) is to delay vertical counter clock
from time C.S0 to time C.S4 (STATE2).
Other sections of vertical counter are clocked with V3 and V7.
Vertical counter is reset with VRESET from video controller latch.

Interlace toggle is clocked with VRESET to change on every vertical frame.

Horizontal decode PROM inputs are horizontal counter states H0 through H6,
plus VSYNC\ and VBLANK from the vertical state machine.
Horizontal decode PROM outputs are HRESET, HSYNC\, DISPEN, and VCLOCK.
Horizontal decode PROM function defined in PROM G0.

Vertical decode PROM inputs are vertical counter states V0 through V5,
VEND, VODD, and HRESET.
VEND is selectable via jumper J3 to be either V10 or NAND (V8,V9) (U202).
Selecting VEND to be V10 enables the vertical state machine
to drive 1024-line (page format) monitors.
Vertical decode PROM outpus are VRESET, VSYNC\, VBLANK, and VCLOCK.
Vertical decode PROM function defined in PROM G1.

Video controller latch 74LS374 (U4) latches the outputs of
horizontal and vertical decoding PROM every state C.S0.

---

## Video Controller Timing Diagram for Standard Monitor


### Horizontal State Machine


```

Signal	State

H0..6	0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3
	0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1

C.S0 	-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

C.S3 	_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

DISPEN	__--------------------------------------------------____________

HSYNC	____________________________________________________------______

HRESET	______________________________________________________________--

VCLOCK	________________________--______________________________--______


```


### Vertical State Machine


```

Signal	State

V1..10	0 0 0 0 0 0 0 0 ... 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
	0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
	0 0 0 0 0 0 0 0 ... 2 2 2 2 2 2 3 3 3 3 3 3 3 3 3 3 ... 7 7 7 7
	0 1 2 3 4 5 6 7 ... 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 ... 6 7 8 9

VCLOCK	-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

VBLANK	____________________--------------------------------------------

VSYNC	________________________________--------------__________________
 (ODD)
VSYNC	__________________________________--------------________________
 (EVEN)
VRESET	________________________________________________________--______
 (ODD)
VRESET	____________________________________________________________--__
 (EVEN)
VINT	____________________--__________________________________________


```

The vertical state count corresponds to half lines.
Note that the vsyncs must be equal distant.
The even sync pulse occurs at state 1031 and the remaining time in the
even interval is 47 states. In the odd state, the sync occurs at state
1030 and there are 46 states remaining.
Thus the total time between syncs is 1077.


---

## Data Paths


The on-board data bus D0..D15 connects the following elements of the board:
Outputs: Multibus Data Port In (U909,U907), RAM Data Out (U110..U117,U310..U317).
Inputs: Multibus Data Port Out (U906,U908),
Function Unit Data In (U210..U217,U410..U417),
Source Register Data In (U910..U916),
Mask Register Data In (U510..U516),
Function Register Data In (U509),
Width Register Data In (U507),
Status Register Data In (U506), and
Video Data Buffer (U707,U709).

The outputs and inputs are enabled with the corresponding output enable
and write enable strobes generated by the memory controller state machine.


### Video Data Path


Video data (display data) is read from the frame buffer memory
and latched in video buffer 74LS374 (U706, U709).
From there, video data is transferred into the video shift register
74S299 (U707, U708).  Via gates 74S00 (U202) and 74S02 (U702),
the video shift register is loaded during the second half of C.S7
whenever there is no blanking (HQ2 true).

During every video refresh cycle, two 16-bit words of video data
are read from the frame buffer in form of a page mode cycle.
The first word passes through the video latch and is loaded
directly into the video shift register.
The second word is latched in the video latch and is subsequently
loaded into the video shift register when the video shift register
completed shifting out the first word.


### RasterOp Data Path


The RasterOp unit is comprised of
Function Unit 74LS251 (U210..U217,U410..U417),
Function Register 74LS374 (U509),
Source Register 74LS374 (U910..U916), and
Mask Register 74LS374 (U510..U516).
The Function, Source, and Mask Registers are loaded from the Data Bus.

On a read-modify-write RasterOp cycle, the following events happen:
Data is read from the frame buffer and is received at the Function Unit,
forming the destination data to be modified.
The content of the source register is shifted through barrel shifter
AM25S10 (U710, U712, U714, U716, U810, U812, U814, U816) by a shift
amount determined by shift PROM G4 (U605).
The destination data, the shifted source data, and the mask register data
enter the function unit and generate a new destination data
according to the function selected by the function register.
The new destination data is then rewritten into the frame buffer.


### Shift Amount Computation


The shift amount in the source barrel shifter depends on the type of cycle.
There are three cases of shift computation illustrated in the table below.
PROM G4 (U605) performs the difference computation. Readcycles to the Multibus
are signalled via the CYCLE0 input to PROM G4. Write cycles from the Multibus
a zero x-source address XS in multplexor/latch 25LS09 (U505).


	Case		Description		Shiftamount
	-----------------------------------------------------
	FB <= FB	Memory to Memory	Xsrc - Xdst
	MB <= FB	Read Operation		Xsrc - 0
	FB <= MB	Write Operation		0 - Xdst


---

## Address Paths


This section describes the addressing of the frame buffer.
The addressing is somewhat different for the two major kind of
memory cycles: video refresh and read/write.

During *video refresh* cycles the memory address comes from the
video controller state machine and drives memory
via multiplexor/drivers DS3848 (U304, U305).
Width Multiplexor 25LS09 (U508) selects 0 for output W which causes
CAS Decoder PROM  G20 (U108) and G21 (U308) to enable all 16 CAS strobes
independent of the X input to the CAS decoder PROM.

During *read/write* cycles the memory address comes from the
(x,y) registers drives memory via multiplexor/drivers DS3848 (U404, U405).
Width Multiplexor 25LS09 (U508) selects the WIDTH0..3 for output W.

The SUN 1024 video board achieves its ability of accessing bit strings
across word boundaries by actually accessing two words within one memory cycle.
This is done by loading the same row-address into all RAM chips at the
beginning of the cycle, but loading two different column addresses
into two groups of RAM chips, individually enabled via CAS decoder PROM.

The CAS Decoder PROM receives the bit address within the word X0..X3,
the width of the access W0..W3, and the CAS1 control as input.
With CAS1 inactive, the CAS Decoder PROM generates the first set
of CAS enables for the first CAS address.
With CAS1 active, the CAS Decoder PROM generates the second set
of CAS enables for the second CAS address.

Simultaneously, the CAS address passes through adder/incrementor
74S283 (U603, U604). For the first CAS address, the carry input CAS1
to the adder is inactive and the address passes through unmodified.
For the second CAS address, however, carry input CAS1 is active
and the CAS address is thus incremented by one to address the
next word location in the frame buffer.


---

## Multibus Interface Logic


Major components of the Multibus Interface Logic are
Multibus Address Decoding, Request Generation, and Interrupt Logic.


### Multibus Address Decoding


The graphics board occupies 128K Bytes in the Multibus memory address space.
The board can be addressed on any one of the eight 128k Byte boundaries
of the 1M Byte Multibus address space be means of switch selector U801.
Alternatively to dip-switch U801, the artwork provides for wirewrap post
jumpers J800.


```

	BASE	SWITCH	JUMPER
	----------------------
	0K	8	15..16
	128K	7	13..14
	256K	6	11..12
	384K	5	9..10
	512K	4	7..8
	640K	3	5..6
	768K	2	3..4
	896K	1	1..2

```


Note: Only one of the eight address switches or jumpers
must be selected on at any one time.

The SUN 1024 Video Board has a fully buffered Multibus interface (see below).
When the SUN 1024 Video Board is ready to receive a new command
from the Multibus, the Multibus address latch 74LS533 (U905 and U903)
is opened. After the command is received and the address latch is closed,
the address bits of the address latch are decoded as follows:

*A16: RasterOp.* This bit is synchronized in Flipflop 74S374 (U902)
and determines whether in case of a write cycle the frame buffer memory
is actually written via gate 74S00 (U701). The bit is meaningless for read cycles.

*A14..A15: Register Select*. These two bits determine via decoder
74S139 (U403) which of the registers is to be updated.

*A12..A13: XY-Register Set*. These two bits enable one of the four
(x,y) register sets contained in dual-port register file 74LS670
(U703, U704, U705, U803, U804, U805). The selected register set is
loaded from address bits A1..A10. In addition, these two bits are
latched in flipflop 74S374 (U902) and determine the register set
to be read for the actual frame buffer operation.

*A11: Y/X\ Select*. Determines whether the *x* or the *y* register
is to be loaded. The bit is decoded via 74S139 (U502).

*A1..A10*. These bits enter the *x* or the *y* register selected
by bits A11..A13. In case of a control register operation. the low-order
two bits A1..A2 decode which control register is addressed via decoder
74S139 (U403).


---

### Multibus Request Logic


The graphics board uses a buffered interface to the Multibus.
When the Multibus master issues a read or write request (B.MEMR, B.MEMW),
and the graphics board is addressed appropriately as described above
and the graphics board is idle (no previous request pending)
then an on-board request is generated that latches Multibus address and data.
Immediately after this address and data are latched,
a Multibus transfer acknowledge (B.XACK) is issued allowing the
master to continue with other operations.
However, when the graphics board is busy, that is,
when a previous request is in progress, the board will not
respond to Multibus requests until the previous request is completed.

Request generation in more detail:
The address decoder 74LS138 (U901) is disabled while an on-board
request is in progress (REQ\ asserted).
If no on-board request is in progress (REQ\ not asserted)
and the board is addressed appropriately then
the address decoder will generate BUSSEL\.

B.MEMR and B.MEMW are buffered with receiver 74S240 (U802) to form READ
and WRITE signals. READ or WRITE is gated with BUSSEL\
via gated with 74S02 (U702) to form DS.
DS is gated with REQ\ through 74S00 (U701) to form XACK
enabling driver 74S240 (U802) to drive B.XACK to Multibus.

The leading edge of XACK\ latches state of WRITE into
write-request flipflop 74S74 (U602-1).
The trailing edge of XACK\, differentiated with three inverter delays
74LS04 (U601) generates a pulse on line SETREQ\
to set request flipflop 74S74 (U602-0).
The output of this request flipflop, REQ, inhibits further requests
from the Multibus by disabling address decoder 74LS138 (U901). REQ also:
closes address latch 74LS533 (U903,U905),
closes data latch 74LS533 (U907,U909),
enables X-Y decoder 74S139 (U502-1), and
enables READREQ\-WRITEREQ\ decoder 74S139 (U502-0).

READREQ\-WRITEREQ\ passes on to memory controller state machine.
The register are synchronized by register 74S374 at time C.S7,
and latched in multiplexor register AM25S09 (U302) at time C.S0.
Purpose of multiplexor register (U302,U508) is to toggle between
refresh and other cycles for memory controller state machine.
Memory controller state machine begins new major cycle at time C.S0.
When it responds to a pending READOP\-WRITEOP\, the memory controller
will generate signal ACK during time S1 for write cycles
and S7 for read cycles. After these times, respectively, the graphics board
has completed using the Multibus data ports.
The trailing edge of ACK will clear request flipflop 74S74 (U602-0),
thereby reopening address and data register 74LS533 (U903,U905,U907,U909),
and disabling READREQ\-WRITEREQ\ and X-Y decoder 74S139 (U502).
Further requests from the Multibus may be accepted at this time.


### Interrupt Logic


The SUN graphics board can generate an interrupt on vertical retrace
to allow software to synchronize with the display update.
To enable interrupts, bit D8 (EN.INT) in the status register 74LS374 (U506)
needs to be set and the desired interrupt level be programmed in bits
D13, D14, and D15 of the status register.
When interrupts are enabled, the next VINT from the video controller
state machine will set interrupt flipflop 74S74 (U402),
thereby enabling decoder 74LS145 (U904) driving the selected
interrupt request on the Multibus.
A pending interrupt is cleared by software writing to the
interrupt register location (WE.INT).

---

## Summary of Multibus Interface


```


	D0..D15	New 16-bit data, read or write

	A1..10	New X or Y address

	A11	0 -> X,  1 -> Y

	A12..13	Selects one of the four sets of (x,y) registers

	A14..15	Select data register to be updated
		On *read cycles*, data is supplied from frame buffer
		On *write cycles*, data is supplied from processor

			0 -> No Register
			1 -> Control Registers
			2 -> Source Register
			3 -> Mask Register

		Control register are further decoded with A1..A2 as follows:

			0 -> Function Register
			1 -> Width Register
			2 -> Control Registers
			3 -> Interrupt Acknowledge

	A16	Enable raster operation on frame buffer

			0 -> no update operation
			1 -> execute update operation

	A17..19	Module Select

	MEMR	IEEE-796 Read Strobe

	MEMW	IEEE-796 Write Strobe

	XACK	IEEE-796 Acknowledge

	INT0..7	Interrupt request. Priority level selectable in software.

	INIT	Initialization, clears control register.

```


---

# Programmable Logic


## Introduction


This chapter contains the source files and object files for
programmable logic elements such as PALs and PROMs.
The content of these elements is defined in a high-level
functional language which is automatically translated
into bitpatterns for programming.

Without attempting to give a full definition of the language,
the following explanation should provide sufficient information
to understand the programs.

*begin "name"* begins a program with the name *name*.

*require "prom.sai" source!file* requests inclusion of the prom library.

*$#* defines a PROM program with *#* addressable locations.

*define "name" = [definition]* defines expressions or equations
that describe the function of the PROM.
The following are reserved identifiers: *D#* is the value of
data bit *#*, *A#* is true if address bit *#* is present in the
current value of the location counter (see below).
All standard operators, including logical AND and OR, are allowed
in expressions. Conditional and case expressions are also possible.

*prombegin* tells the program to evaluate the following statements
until *promend* for each location value of the location counter.

*prom(#1, #2,	expression)* means to put the value of *expression*
into PROM *#1* bit position *#2*. A single program can define
the contents of multiple PROMs by using multiple PROM numbers *#1*.

*promend* terminates the evaluation of statements.

*writeprom("file",#)* writes the object code of PROM *#* into file *file*.
Each separate PROM needs to be written into a separate file.

*end* terminates the program.

In the following listings, the PROM source code is followed by the generated
hexadecimal object code which also includes a 16-bit checksum.

---

## PROM G0


```


comment This information proprietary to SUN MICROSYTEMS INC.;
begin "g0"
require "prom.sai" source!file;
$512;

define

h5	=[a0],
h6	=[a1],
h3	=[a2],
h2	=[a3],
h4	=[a4],
h1	=[a5],
h0	=[a6],
vsync	=[a7],
vblank	=[a8],


h	=[(h0*d0 + h1*d1 + h2*d2 + h3*d3 + h4*d4 + h5*d5 + h6*d6)],
hsync	=[(53 ≤ h < 59)],
dispen	=[((1 ≤ h < 51) ∧ ¬vblank)],
hreset	=[(h = 63)],
vclock	=[((h = 24) ∨ (h = 56))];

prombegin

prom(0,d0,	hreset);
prom(0,d1,	¬hsync);
prom(0,d2,	dispen);
prom(0,d3,	¬vclock);

promend;
writeprom("g0",0);
end;


```


```


PROM:	g0	Checksum:	1524

   0  0A  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A
  16  0E  0E  0A  0A  06  00  0A  0A  0E  0A  0A  0A  0E  0A  0A  0A
  32  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A
  48  0E  0E  0A  0A  0E  08  0A  0A  0E  08  0A  0A  0E  0A  0A  0A
  64  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A
  80  0E  0E  0A  0A  0E  08  0A  0A  0E  08  0A  0A  0E  0A  0A  0A
  96  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A
 112  0E  0A  0A  0A  0E  0A  0A  0A  0E  08  0A  0A  0E  0B  0A  0A
 128  0A  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A
 144  0E  0E  0A  0A  06  00  0A  0A  0E  0A  0A  0A  0E  0A  0A  0A
 160  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A
 176  0E  0E  0A  0A  0E  08  0A  0A  0E  08  0A  0A  0E  0A  0A  0A
 192  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A
 208  0E  0E  0A  0A  0E  08  0A  0A  0E  08  0A  0A  0E  0A  0A  0A
 224  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A  0E  0E  0A  0A
 240  0E  0A  0A  0A  0E  0A  0A  0A  0E  08  0A  0A  0E  0B  0A  0A
 256  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 272  0A  0A  0A  0A  02  00  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 288  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 304  0A  0A  0A  0A  0A  08  0A  0A  0A  08  0A  0A  0A  0A  0A  0A
 320  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 336  0A  0A  0A  0A  0A  08  0A  0A  0A  08  0A  0A  0A  0A  0A  0A
 352  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 368  0A  0A  0A  0A  0A  0A  0A  0A  0A  08  0A  0A  0A  0B  0A  0A
 384  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 400  0A  0A  0A  0A  02  00  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 416  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 432  0A  0A  0A  0A  0A  08  0A  0A  0A  08  0A  0A  0A  0A  0A  0A
 448  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 464  0A  0A  0A  0A  0A  08  0A  0A  0A  08  0A  0A  0A  0A  0A  0A
 480  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A  0A
 496  0A  0A  0A  0A  0A  0A  0A  0A  0A  08  0A  0A  0A  0B  0A  0A


```


---

## PROM G1


```


comment This information proprietary to SUN MICROSYSTEMS INC.;
begin "g1"
require "prom.sai" source!file;
$512;

define

v2	=[a0],
v5	=[a1],
v3	=[a2],
v4	=[a3],
v1	=[a4],
v0	=[a5],
v10	=[a6],
vodd	=[a7],
hreset	=[a8],

adrs	=[(v0*d0 + v1*d1 + v2*d2 + v3*d3 + v4*d4 + v5*d5 + v10*d10)],
vsync	=[(vodd ∧ (1030≤adrs<1036) ∨ ¬vodd ∧ (1031≤adrs<1037))],
vblank	=[(adrs ≥ 1024)],
vreset	=[(hreset ∧ v0
	  ∨ vodd ∧ (adrs = 1076)
	  ∨ ¬vodd ∧ (adrs = 1078))],
vint	=[(adrs = 1024)];

prombegin

prom(0,d0,	vreset);
prom(0,d1,	vint);
prom(0,d2,	vblank);
prom(0,d3,	¬vsync);

promend;
writeprom("g1",0);
end;


```


```


PROM:	g1	Checksum:	13CC

   0  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  16  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  32  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  48  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  64  0E  0C  0C  0C  04  04  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C
  80  0C  0C  0C  0C  04  0C  0C  0C  0C  0C  0C  0D  0C  0C  0C  0C
  96  0C  0C  0C  0C  04  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C
 112  0C  04  0C  0C  04  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C
 128  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 144  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 160  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 176  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 192  0E  0C  0C  0C  04  0C  0C  0C  0C  0C  0C  0D  0C  0C  0C  0C
 208  0C  04  0C  0C  04  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C
 224  0C  0C  0C  0C  04  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C
 240  0C  04  0C  0C  04  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C
 256  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 272  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 288  09  09  09  09  09  09  09  09  09  09  09  09  09  09  09  09
 304  09  09  09  09  09  09  09  09  09  09  09  09  09  09  09  09
 320  0E  0C  0C  0C  04  04  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C
 336  0C  0C  0C  0C  04  0C  0C  0C  0C  0C  0C  0D  0C  0C  0C  0C
 352  0D  0D  0D  0D  05  0D  0D  0D  0D  0D  0D  0D  0D  0D  0D  0D
 368  0D  05  0D  0D  05  0D  0D  0D  0D  0D  0D  0D  0D  0D  0D  0D
 384  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 400  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 416  09  09  09  09  09  09  09  09  09  09  09  09  09  09  09  09
 432  09  09  09  09  09  09  09  09  09  09  09  09  09  09  09  09
 448  0E  0C  0C  0C  04  0C  0C  0C  0C  0C  0C  0D  0C  0C  0C  0C
 464  0C  04  0C  0C  04  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C  0C
 480  0D  0D  0D  0D  05  0D  0D  0D  0D  0D  0D  0D  0D  0D  0D  0D
 496  0D  05  0D  0D  05  0D  0D  0D  0D  0D  0D  0D  0D  0D  0D  0D


```


---

## PROM G2


```


comment This information proprietary to SUN MICROSYSTEMS INC.;
begin "g2"
require "prom.sai" source!file;
$512;

define

x0	=[a0],
x1	=[a1],
x2	=[a2],
x3	=[a3],
w0	=[a4],
w1	=[a5],
w2	=[a6],
w3	=[a7],
cas1	=[a8],

x	=[(x0*d0 + x1*d1 + x2*d2 + x3*d3)],
w	=[(w0*d0 + w1*d1 + w2*d2 + w3*d3)],
width	=[(if w then w else 16)],
en(i)	=[(        (x ≤ (15-i) < (x + width))
	  ∨ cas1 ∧ (x ≤ (15-i+16) < (x + width)))];

prombegin

prom(0,d0,	¬en(14));
prom(0,d1,	¬en(10));
prom(0,d2,	¬en(6));
prom(0,d3,	¬en(2));
prom(0,d4,	¬en(0));
prom(0,d5,	¬en(4));
prom(0,d6,	¬en(8));
prom(0,d7,	¬en(12));

prom(1,d0,	¬en(15));
prom(1,d1,	¬en(11));
prom(1,d2,	¬en(7));
prom(1,d3,	¬en(3));
prom(1,d4,	¬en(1));
prom(1,d5,	¬en(5));
prom(1,d6,	¬en(9));
prom(1,d7,	¬en(13));

promend;

writeprom("g20",0);
writeprom("g21",1);
end;


```


```


PROM:	g20	Checksum:	2193

   0  00  00  01  01  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF
  16  FF  FE  FF  7F  FF  FD  FF  BF  FF  FB  FF  DF  FF  F7  FF  EF
  32  FE  FE  7F  7F  FD  FD  BF  BF  FB  FB  DF  DF  F7  F7  EF  EF
  48  FE  7E  7F  7D  FD  BD  BF  BB  FB  DB  DF  D7  F7  E7  EF  EF
  64  7E  7E  7D  7D  BD  BD  BB  BB  DB  DB  D7  D7  E7  E7  EF  EF
  80  7E  7C  7D  3D  BD  B9  BB  9B  DB  D3  D7  C7  E7  E7  EF  EF
  96  7C  7C  3D  3D  B9  B9  9B  9B  D3  D3  C7  C7  E7  E7  EF  EF
 112  7C  3C  3D  39  B9  99  9B  93  D3  C3  C7  C7  E7  E7  EF  EF
 128  3C  3C  39  39  99  99  93  93  C3  C3  C7  C7  E7  E7  EF  EF
 144  3C  38  39  19  99  91  93  83  C3  C3  C7  C7  E7  E7  EF  EF
 160  38  38  19  19  91  91  83  83  C3  C3  C7  C7  E7  E7  EF  EF
 176  38  18  19  11  91  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF
 192  18  18  11  11  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF
 208  18  10  11  01  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF
 224  10  10  01  01  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF
 240  10  00  01  01  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF
 256  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00
 272  FF  FE  FF  7F  FF  FD  FF  BF  FF  FB  FF  DF  FF  F7  FF  EF
 288  FE  FE  7F  7F  FD  FD  BF  BF  FB  FB  DF  DF  F7  F7  EF  EF
 304  FE  7E  7F  7D  FD  BD  BF  BB  FB  DB  DF  D7  F7  E7  EF  EE
 320  7E  7E  7D  7D  BD  BD  BB  BB  DB  DB  D7  D7  E7  E7  EE  EE
 336  7E  7C  7D  3D  BD  B9  BB  9B  DB  D3  D7  C7  E7  E6  EE  6E
 352  7C  7C  3D  3D  B9  B9  9B  9B  D3  D3  C7  C7  E6  E6  6E  6E
 368  7C  3C  3D  39  B9  99  9B  93  D3  C3  C7  C6  E6  66  6E  6C
 384  3C  3C  39  39  99  99  93  93  C3  C3  C6  C6  66  66  6C  6C
 400  3C  38  39  19  99  91  93  83  C3  C2  C6  46  66  64  6C  2C
 416  38  38  19  19  91  91  83  83  C2  C2  46  46  64  64  2C  2C
 432  38  18  19  11  91  81  83  82  C2  42  46  44  64  24  2C  28
 448  18  18  11  11  81  81  82  82  42  42  44  44  24  24  28  28
 464  18  10  11  01  81  80  82  02  42  40  44  04  24  20  28  08
 480  10  10  01  01  80  80  02  02  40  40  04  04  20  20  08  08
 496  10  00  01  00  80  00  02  00  40  00  04  00  20  00  08  00


```


```


PROM:	g21	Checksum:	2B5C


   0  00  01  01  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF  FF
  16  FE  FF  7F  FF  FD  FF  BF  FF  FB  FF  DF  FF  F7  FF  EF  FF
  32  FE  7F  7F  FD  FD  BF  BF  FB  FB  DF  DF  F7  F7  EF  EF  FF
  48  7E  7F  7D  FD  BD  BF  BB  FB  DB  DF  D7  F7  E7  EF  EF  FF
  64  7E  7D  7D  BD  BD  BB  BB  DB  DB  D7  D7  E7  E7  EF  EF  FF
  80  7C  7D  3D  BD  B9  BB  9B  DB  D3  D7  C7  E7  E7  EF  EF  FF
  96  7C  3D  3D  B9  B9  9B  9B  D3  D3  C7  C7  E7  E7  EF  EF  FF
 112  3C  3D  39  B9  99  9B  93  D3  C3  C7  C7  E7  E7  EF  EF  FF
 128  3C  39  39  99  99  93  93  C3  C3  C7  C7  E7  E7  EF  EF  FF
 144  38  39  19  99  91  93  83  C3  C3  C7  C7  E7  E7  EF  EF  FF
 160  38  19  19  91  91  83  83  C3  C3  C7  C7  E7  E7  EF  EF  FF
 176  18  19  11  91  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF  FF
 192  18  11  11  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF  FF
 208  10  11  01  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF  FF
 224  10  01  01  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF  FF
 240  00  01  01  81  81  83  83  C3  C3  C7  C7  E7  E7  EF  EF  FF
 256  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00
 272  FE  FF  7F  FF  FD  FF  BF  FF  FB  FF  DF  FF  F7  FF  EF  FF
 288  FE  7F  7F  FD  FD  BF  BF  FB  FB  DF  DF  F7  F7  EF  EF  FE
 304  7E  7F  7D  FD  BD  BF  BB  FB  DB  DF  D7  F7  E7  EF  EE  FE
 320  7E  7D  7D  BD  BD  BB  BB  DB  DB  D7  D7  E7  E7  EE  EE  7E
 336  7C  7D  3D  BD  B9  BB  9B  DB  D3  D7  C7  E7  E6  EE  6E  7E
 352  7C  3D  3D  B9  B9  9B  9B  D3  D3  C7  C7  E6  E6  6E  6E  7C
 368  3C  3D  39  B9  99  9B  93  D3  C3  C7  C6  E6  66  6E  6C  7C
 384  3C  39  39  99  99  93  93  C3  C3  C6  C6  66  66  6C  6C  3C
 400  38  39  19  99  91  93  83  C3  C2  C6  46  66  64  6C  2C  3C
 416  38  19  19  91  91  83  83  C2  C2  46  46  64  64  2C  2C  38
 432  18  19  11  91  81  83  82  C2  42  46  44  64  24  2C  28  38
 448  18  11  11  81  81  82  82  42  42  44  44  24  24  28  28  18
 464  10  11  01  81  80  82  02  42  40  44  04  24  20  28  08  18
 480  10  01  01  80  80  02  02  40  40  04  04  20  20  08  08  10
 496  00  01  00  80  00  02  00  40  00  04  00  20  00  08  00  10


```


---

## PROM G4


```


comment This information proprietary to SUN MICROSYSTEMS INC.;
begin "g4"
require "prom.sai" source!file;
$512;

define

xs2	=[a0],
x3	=[a1],
x2	=[a2],
xs3	=[a3],
x1	=[a4],
xs1	=[a5],
readop_i=[a6],
xs0	=[a7],
x0	=[a8],

readop	=[(¬readop_i)],
xs	=[(xs0*d0 + xs1*d1 + xs2*d2 + xs3*d3)],
xd	=[(x0*d0 + x1*d1 + x2*d2 + x3*d3)],
shift	=[(if readop then (xs - 0) else (xs - xd))];

prombegin

prom(0,d0,	shift LAND d1);
prom(0,d1,	shift LAND d0);
prom(0,d2,	shift LAND d3);
prom(0,d3,	shift LAND d2);

promend;
writeprom("g4",0);
end;


```


```


PROM:	g4	Checksum:	0F00

   0  00  08  00  08  00  08  00  08  04  0C  04  0C  04  0C  04  0C
  16  00  08  00  08  00  08  00  08  04  0C  04  0C  04  0C  04  0C
  32  01  09  01  09  01  09  01  09  05  0D  05  0D  05  0D  05  0D
  48  01  09  01  09  01  09  01  09  05  0D  05  0D  05  0D  05  0D
  64  00  08  04  0C  0C  00  08  04  04  0C  00  08  08  04  0C  00
  80  0D  01  09  05  05  0D  01  09  09  05  0D  01  01  09  05  0D
  96  01  09  05  0D  0D  01  09  05  05  0D  01  09  09  05  0D  01
 112  00  08  04  0C  0C  00  08  04  04  0C  00  08  08  04  0C  00
 128  02  0A  02  0A  02  0A  02  0A  06  0E  06  0E  06  0E  06  0E
 144  02  0A  02  0A  02  0A  02  0A  06  0E  06  0E  06  0E  06  0E
 160  03  0B  03  0B  03  0B  03  0B  07  0F  07  0F  07  0F  07  0F
 176  03  0B  03  0B  03  0B  03  0B  07  0F  07  0F  07  0F  07  0F
 192  02  0A  06  0E  0E  02  0A  06  06  0E  02  0A  0A  06  0E  02
 208  0F  03  0B  07  07  0F  03  0B  0B  07  0F  03  03  0B  07  0F
 224  03  0B  07  0F  0F  03  0B  07  07  0F  03  0B  0B  07  0F  03
 240  02  0A  06  0E  0E  02  0A  06  06  0E  02  0A  0A  06  0E  02
 256  00  08  00  08  00  08  00  08  04  0C  04  0C  04  0C  04  0C
 272  00  08  00  08  00  08  00  08  04  0C  04  0C  04  0C  04  0C
 288  01  09  01  09  01  09  01  09  05  0D  05  0D  05  0D  05  0D
 304  01  09  01  09  01  09  01  09  05  0D  05  0D  05  0D  05  0D
 320  0F  03  0B  07  07  0F  03  0B  0B  07  0F  03  03  0B  07  0F
 336  0E  02  0A  06  06  0E  02  0A  0A  06  0E  02  02  0A  06  0E
 352  02  0A  06  0E  0E  02  0A  06  06  0E  02  0A  0A  06  0E  02
 368  0F  03  0B  07  07  0F  03  0B  0B  07  0F  03  03  0B  07  0F
 384  02  0A  02  0A  02  0A  02  0A  06  0E  06  0E  06  0E  06  0E
 400  02  0A  02  0A  02  0A  02  0A  06  0E  06  0E  06  0E  06  0E
 416  03  0B  03  0B  03  0B  03  0B  07  0F  07  0F  07  0F  07  0F
 432  03  0B  03  0B  03  0B  03  0B  07  0F  07  0F  07  0F  07  0F
 448  00  08  04  0C  0C  00  08  04  04  0C  00  08  08  04  0C  00
 464  0D  01  09  05  05  0D  01  09  09  05  0D  01  01  09  05  0D
 480  01  09  05  0D  0D  01  09  05  05  0D  01  09  09  05  0D  01
 496  00  08  04  0C  0C  00  08  04  04  0C  00  08  08  04  0C  00


```


---

## PROM G6


```


comment This information proprietary to SUN MICROSYSTEMS INC.;
begin "g6"
require "prom.sai" source!file;
$32;

define

state0	=[a0], state1	=[a1], state2	=[a2], cycle0	=[a3], cycle1	=[a4],

state	=[(state0 + state1 + state2)],	comment	[0..7];
nstate	=[((state + 1) MOD 8)],		comment next state;
xstate	=[((state + 2) MOD 8)],		comment 2ndnext state;

cycle	=[(cycle0*d0 + cycle1*d1)],	refresh	=[(cycle = 0)],
write	=[(cycle = 1)], read	=[(cycle = 2)],	idle	=[(cycle = 3)],

ras	=[(read ∧ 1≤nstate≤5 ∨ write ∧ 1≤nstate≤6 ∨ refresh ∧ 1≤nstate≤6)],
cas0	=[(read ∧ 2≤xstate≤5
	∨ write ∧ 2≤xstate≤7
	∨ refresh ∧ (2≤xstate≤3 ∨ 5≤xstate≤7))],
cas1	=[(read ∧ 3≤xstate≤5
	∨ write ∧ 3≤xstate≤7
	∨ refresh ∧ (2≤xstate≤3 ∨ 5≤xstate≤7))],
we_ram	=[(write ∧ nstate=6)],			comment gated externally;
ld_buf	=[(refresh ∧ ((nstate=4) ∨ (nstate=0)))],
oe_prt	=[((read ∨ write) ∧ 1≤nstate≤2)],
ld_reg	=[(write ∧ nstate=1 ∨ read ∧ nstate=5)],
ld_prt	=[(read ∧ nstate=7)],
oe_srx	=[(read ∧ nstate=7)],
ack	=[((write ∧ nstate=1) ∨ (read ∧ nstate=7))],

c_s0	=[(nstate=0)],	c_s3	=[(nstate=3)],	c_s7	=[(nstate=7)];

prombegin

prom(0,d0,	c_s0);
prom(0,d1,	cas1);
prom(0,d2,	¬cas0);
prom(0,d3,	¬ras);
prom(0,d4,	¬ld_reg);
prom(0,d5,	we_ram);
prom(0,d6,	¬ack);
prom(0,d7,	c_s7);

prom(1,d0,	c_s3);
prom(1,d1,	¬oe_prt);
prom(1,d2,	ld_buf);
prom(1,d3,	nstate LAND d0);
prom(1,d4,	nstate LAND d1);
prom(1,d5,	¬oe_srx);
prom(1,d6,	ld_prt);
prom(1,d7,	nstate LAND d2);

promend;
writeprom("g60",0);
writeprom("g61",1);
end;

```


```


PROM:	g60	Checksum:	0A42

   0  52  52  52  54  52  54  54  52  00  52  52  52  52  52  52  52
  16  50  52  52  52  52  52  52  52  5C  5C  5C  5C  5C  5C  5C  5C


```


```


PROM:	g61	Checksum:	0840

   0  2A  32  32  3B  32  3B  3B  A6  28  30  30  3B  30  3B  3B  A2
  16  28  30  30  3B  30  3B  3B  A2  2A  32  32  3B  32  3B  3B  A2


```


---

# Schematics


This chapter contains the signal summary, the parts list,
the parts location diagram, and the schematics of the SUN 1024 Video Board.


## Signal Summary


--------------------------------------------------------------------------------
Mnemonic	Description
--------------------------------------------------------------------------------

A0..A16		on-board addresses
AA12..AA16	on-board latched addresses
ACK		Acknowledge
B.A0\..A19\	Multibus address lines
B.AACK\		UNUSED, Multibus advanced acknowledge
B.BCLK\		UNUSED, Multibus bus clock
B.BHEN\		UNUSED, Multibus byte high enable
B.BPRN\		UNUSED, Multibus priority in
B.BPRO\		UNUSED, Multibus priority out
B.BREQ\		UNUSED, Multibus bus request
B.BUSY\		UNUSED, Multibus busy
B.CBRQ\		UNUSED, Multibus common bus request
B.CCLK\		UNUSED, Multibus constant clock
B.D0\..D15\	Multibus data lines
B.INH1\..2\	UNUSED, Multibus inhibit lines
B.INIT\		Multibus init
B.INT0\..INT7\	Multibus interrupt request
B.INTA\		UNUSED Multibus interrupt acknowledge
B.IORC\		UNUSED Multibus I/O read control
B.IOWC\		UNUSED Multibus I/O write control
B.MRDC\		Multibus memory read control
B.MWTC\		Multibus memory write control
B.XACK\		Multibus transfer acknowledge
BUSREAD		READ*BUSSEL
BUSSEL		Multibus Select
C.S0		Clock State 0
C.S3		Clock State 3
C.S7		Clock State 7
C25.0-12	Pixel Clock
C50.0-25	System Clock
CAS0		Column-Address-Strobe 0
CAS1		Column-Address-Strobe 1
CYCLE0		Cycle Type 0
CYCLE1		Cycle Type 1
D0..D15		Data Bus
DISPEN		Display Enable
DS		Data Strobe
EN.INT		Enable Interrupts
EN.VIDEO	Enable Video
FUN0..FUN7	Function Register
GND		Ground
GX600..GX617	Memory Controller Internals
H0..H6		Horizontal Counter Outputs
HQ0..HQ3	Horizontal State Machine Internals
HRESET		Horizontal Counter Reset
HSYNC\		Horizontal Sync Pulse
INT0..INT2	Interrupt Level Select
INT\		Interrupt
J1.HSYNC	TTL horizontal sync
J1.VIDEO	TTL video
J1.VSYNC	TTL vertical sync
LD.BUF		Load Buffer Strobe
LD.PRT		Load Data Port Strobe
LD.REG\		Load Register Strobe
LD.XY\		Load X/Y-Register Strobe
LD.X\		Load X-Register Strobe
LD.Y\		Load Y-Register Strobe
M.A0\..A7\	Memory Address Bus
M.CAS0\..CAS15\	Memory Column Address Strobes
M.DI0..M.DI15	Memory Data In Bus
M.RAS\		Memory Row-Address Strobe
M.WE\		Memory Write Enable Strobe
MASK0..MASK15	Mask Register
OE.PRT\		Output Enable Data Port
OE.SRX\		Output Enable Shifter Buffer
PU		Pullup
PU1		Pullup 1
RASADRS		Row Address Select
RASTEROP	Raster Operation Bit
RAS		Row-Address-Strobe
READ		Read Strobe
READOP		Read Operation
READREQ		Read Request
REFRESH		Refresh Operation
REQ		Request
SD0..SD15	Shift Data
SETREQ\		Set Request
SHIFT0..3	Shift Amount
SRC0..15	Source Register
SRS0..15	Source Register Shifter Internal
SRX0..15	Source Register Shifter
STATE0..3	State
V0..10		Vertical Counter Outputs
VEND		Vertical Counter End
VBLANK		Vertical Blank
VCC		+5V
VCLOCK\		Vertical Counter Clock
VCLOCK1\	Vertical Counter Clock delayed
VIDEO		Video Data
VINT		Vertical Interrupt
VODD		Vertical Odd (Interlace Toggle)
VQ0..3		Vertical Decode PROM Internals
VRESET		Vertical Reset
VSYNC		Vertical Sync
W0..3		Width
WE.CTL\		Write Enable Control Register
WE.FUN\		Write Enable Function Register
WE.INT\		Write Enable Interrupt Flag
WE.MSK\		Write Enable Mask Register
WE.RAM\		Write Enable RAM
WE.SRC\		Write Enable Source Register
WE.STATUS\	Write Enable Status Register
WE.WIDTH\	Write Enable Width Register
WE		Write Enable
WIDTH0..3	Width Register
WRITE		Write
WRITEOP		Write Operation
WRITEX		Write Latched
X0..9		X-Address
XACK		Transfer Acknowledge
XCAS0..15	Cas Decoder Internals
XS0..3		X-Address of Source
XX4..9		X-Address after adder
XXX4..9		X-Address after adder latched
Y0..9		Y-Address


---

## Parts List


As an aid in specifying and ordering components, this parts list
translates diptypes into manufacturer names and manufacturer codes.
Only one manufacturer code is given, alternative sources
may be substituted. A manufacturer code of "ANY" is used
for generic parts with a large number of second sources.


```

--------------------------------------------------------------------------------
GENERIC	 QTY BRAND   PART NUMBER   DESCRIPTION
--------------------------------------------------------------------------------

25LS09     2 AMD     AM25LS09PC    FOUR-BIT REGISTER, INPUT MUX
3622       3 SIG     N82S131       512-BY-4 BIPOLAR PROM
4164      16 ANY     4164          64K-BY-1 DYNAMIC RAM 150 NSEC
74LS393    3 TI      SN74LS393N    DUAL 4-BIT BINARY COUNTER
74LS04     1 TI      SN74LS04N     HEX INVERTER
74LS138    1 TI      SN74LS138N    3-TO-8 DECODER
74LS145    1 TI      SN74LS145N    BDC-TO-DECIMAL DECODER
74LS244    4 TI      SN74LS244N    OCTAL NONINVERTED BUFFERS
74LS251   16 TI      SN74LS251N    1-OF-8 DATA SELECTOR
74LS273    1 TI      SN74LS273N    OCTAL D-TYPE FLIPFLOP WITH CLEAR
74LS374   15 TI      SN74LS374N    OCTAL REGISTER
74LS533    6 AMD     SN74LS533N    OCTAL TRANSPARENT LATCH INVERTING
74LS670    6 TI      SN74LS670N    4-BY4 REGISTER FILES
74LS74     1 TI      SN74LS74      DUAL D-TYPE FLIPFLOPS
74S00      2 TI      SN74S00N      QUAD 2-INPUT NAND GATES
74S02      1 TI      SN74S02N      QUAD 2-INPUT NOR GATES
74S139     2 TI      SN74S139N     DUAL 2-TO-4 LINE DECODER
74S240     1 TI      SN74S240N     OCTAL INVERTING BUFFER
74S283     2 TI      SN74S283N     4-BIT ADDER
74S288     1 TI      TBP18S030N    32-BY-8 BIPOLAR PROM
74S288     1 TI      TBP18S030N    32-BY-8 BIPOLAR PROM
74S299     2 TI      SN74S299N     8-BIT UNIVERSAL SHIFT REGISTER
74S37      1 TI      SN74S37N      QUAD 2-INPUT NAND BUFFERS
74S374     4 TI      SN74S374N     OCTAL D-TYPE LATCHES
74S472     2 TI      TBP28S42N     512-BY-8 BIPOLAR PROM
74S74      2 TI      SN74S74N      DUAL D-TYPE FLIPFLOP
AM25S09    1 AMD     AM25S09PC     FOUR-BIT REGISTER, INPUT MUX
AM25S10    8 AMD     AM25S10PC     SCHOTTKY FOUR-BIT SHIFTER,
C         38 AVX     MD015C104MAA  DIPGUARD CAPACITORS 0.1 UF
DIPSW      1 CUTLER  SM-2AV-951-8  DIPSWITCH WITH 8 POSITIONS
DS1648     4 NAT     DS1648        QUAD MEMORY DRIVER
K1114A     1 MOTOROL K1114A        CRYSTAL OSCILLATOR 40 MHZ
R9.SIP     2 BURNS   4310R-101-103 RESISTOR SIP, 9 RESISTORS, 1K
R	   2 ANY     		   RESISTOR 1/8 WATT 33 OHM
L	   1 ANY		   LED, RED, BUILT-IN RESISTOR


```


---

## Parts Location Diagram


---

## Schematic G1 (page 1 of 5)


---

## Schematic G2 (page 2 of 5)


---

## Schematic G3 (page 3 of 5)


---

## Schematic G4 (page 4 of 5)


---

## Schematic P5 (Page 5 of 5)


---

# Wirelist


This chapter contains the wirelist of the SUN 1024 Video Board.
The wirelist is comprised of the following sections which are
distinguished by the header lines on each page.


#### Schematics List


The schematics list summarizes all schematics files with titles and pages.
It starts with the following header:


```


FILNAM	P,PN		DATE	   TIME	MODULE(DWG NUM)	REV	AUTHOR
	TITLE 1				PROJECT		BOARD TYPE


```


#### Location List


The location list translates all location labels
into diptype and component names and locations on the schematics.
The location list start with the following header:


```


LOC	DIPTYPE	BODY	FILE	POS


```


#### Signal List


The signal list describes all signals and synonyms in alphabetical order.
Signals that have no explicit name are automatically assigned a
computer-generated name that consists of the percent symbol ("%")
followed by the alphabetically lowest location and pin name connected to
this particular signal run. The signal list pages carry the following header:


```


SIGNAL NAME
	LOC(PIN#) TYPE	LOW	HI	USE	DIPTYPE	BODY	FILE	POS


```


For each signal, the connected component locations are listed together
with the pin number, type (input, output, tri-state, open-collector),
low and high currents, usage on component, the component diptype and bodyname,
and a crossreference to the schematic file where this location is used.
Each signal is followed by a calculation of static current loading.


#### Unused Pin List


The last section of the wirelist displays all unused pin locations in a format
similar to the signal list. The header for this section is:


```


UNUSED PINS
	LOC(PIN#) TYPE	LOW	HI	USE	DIPTYPE	BODY	FILE	POS


```
