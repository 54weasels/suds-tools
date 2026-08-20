---


---


# Sun-1 Color Video Board


# Engineering Manual


Sun Microsystems Inc.

May 1983

Rev D


>
**Trade Secret Notice**

This document contains unpublished, proprietary information
and describes subject matter proprietary to Sun Microsystems Inc.
This document may not be disclosed to third parties or copied
or duplicated in any form without the prior written consent of
Sun Microsystems Inc.


>
Multibus is a trademark of Intel Corporation.


---


---

# Principles of Operation


## Introduction


This chapter describes the operation of the Sun color video board.
The discussion assumes that the reader is familiar with the architecture,
the installation, and the programming of the Sun color video board.
In addition, the discussion assumes that the reader has a working knowledge
of digital electronics and has access to descriptions of the components
used on the board.

A set of schematic diagrams for the Sun color video board are included
in chapter 6 of this manual and a complete wirelist is included
in chapter 7. The following two sections illustrate the conventions
employed in the schematics and the wirelist.


## Schematic Conventions: Signals


When possible, the schematics were drawn to standard drafting conventions
with input signal entering from the left and output signals exiting to the right.

Both active-high and active-low signals are used.
A signal name that is followed by a backslash ("\") indicates
that the signal is asserted active low (<0.4V), e.g. OE\.
Conversely, a signal without a backslash denotes a
signal that is asserted active high (>2.4V).

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
For example, all Multibus signals start with the prefix "BUS.".

---

## Schematic Conventions: Components


Components in the schematics are identified by component name
(also referred to as body name in the wirelist).
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
	L	Used as Kludge for sub-miniature coax connectors
	J       Jumper or Connector
	R       Resistor
	U       dual-in-line component
	M	64K RAM
	V	24-pin Slim DIP


The three digits give the approximate component position on the board,
with the first digit indicating the row position and the last two digits
the position along the row.

Component names (body names) are translated into diptypes that specify
a particular physical component associated with the component name.
A diptype specifies a particular physical component
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


The Sun color video board requires 5.5 amps at 5 Volts and 630 milli-amp at
-5.2 Volts.


## Initialization


When the BUS.INIT signal is received from the Multibus,
the control register (U1028) is cleared to all 0's,
thereby disabling video (DISP_ON), interrupts (INTEN), and
paint-mode (PAINT). The negated interrupt enable (INTEN)
also clears any interrupts pending in interrupt flipflop (U2200), and the
color map set used for both video and for updating is set to zero.


## Timing


Control of five signals on the color video board completely determines
the state of that card. These signals are SYSCP1, the system clock before it
is feed into a line driver; STATE11, which resets a state machine with
ten states (830 nsec) generating the control lines for the frame buffer;
HRESET, which resets the horizontal line state machine; VRESET, which resets
the vertical line state machine; and VODD, which determines if we are painting
the odd or the even set of lines on the CRT. These five signals can be driven
by the on-board versions of these signals (the signal name prefixed with a `N.",
or they can be driven from the
P2-connector which allows upto three color boards to be driven in parallel
for a 24-bit deep frame buffer. Inserting all five jumpers at location J2010
causes these signals to be driven by the on-board sources for these connectors.
These signals are additionally output onto the P2-bus, so any set of color
boards should always be inserted into a set of slots in a cardcage which does
not share a P2 connector with any other slots.

Assume for all further discussion that the color board`s synchronization
signals are all generated on-board.

The basic clock on the board is generated by the 23.485 MHz crystal oscillator
at location U1902. The oscillator's output, CLK, is feed into a flipflop
frequency divider at location U1801. The signal N.SYSCP1 then drives both
a pin on the P2 connector and the input to the 74S240 line driver at
U2300(6). The output of this line driver is SYSCP, the system clock. This
clock is both the pixel clock and controls the frame buffer control state
machine, the horizontal line state machine, and the vertical line state
machine.

---

## Memory Control State Machine


The memory control state machine generates the memory timing
and other basic timing strobes for the video board.
It consists of the 32x8 PROMs GC0 (U1512), GC2 (U1904), GC3 (U1604);
74S374 output registers U1514, U1806, U1506; the 74S163 4-bit counter at
U1804; and indirectly the 1024x8 PROMs GC5 (U1524) and GC6 (U1522).
The 74S374 output registers and the 4-bit counter are clocked by SYSCP.

PROM GC2 generates the RAS, CAS, and WE strobes for the fRAMe buffer; these
signals are further modified before they actually drive the 64K RAM.
PROM GC2 also generates the signals YLINOE and XLINOE which multiplex the
RAS and CAS address lines during page-mode video cycles on the frame buffer,
and YREGOE and XREGOE which multiplex the RAS and CAS address lines during
the read-modify-write cycles that update the frame buffer. The input
X.RMW160 to PROM GC2 flags when a read-modify-write cycle should be performed
on the frame buffer.

The frame buffer
memory consists of forty 64K RAM organized as five pixels of eight bits
each. Thus, we must actually generate five write-enable pulses which will drive
eight 64K RAM apiece.
PROM GC0 is selected by the WE strobe generate by PROM GC2 and generates these
five write-enable strobes WE0 through WE4. PROM GC5 takes the horizontal
X-address MODULO 5 (for example, 21 MOD 5 equals 1, 614 MOD 5 equals 4) and
outputs this value as signals BANK0..BANK2 which drive the inputs to PROM GC0.
Another input to PROM GC0 is PAINT which is a flag from the status register
to activate all five write-enable strobes at once to write five adjacent pixels
with the same pixel value. The last input to PROM GC0 is a latched version of
the write strobe from the Multibus; it is active on write cycles and is
necessary because the signal WE from PROM GC2 is actually generated on both
read and write accesses to the frame buffer.

The other five outputs of PROM GC5 (XE0..XE4) function to multiplex the
forty-bit wide output of the frame buffer into the eight-bit 'Destination
Register' input to the function unit. As a quick elucidation of the
relationship between the signals BANK0..BANK2 and XE0..XE4, if the binary
encoded value of BANK0..2 is 3, then, simultaneously, signal XE3 would
be active while XE0..XE2 and XE4 would be deasserted.

PROM GC6 takes the value of the horizontal X-address register and divides
it by five. This new value is then combined with the output of the
vertical Y-address register to supply the RAS and CAS addresses for the
frame buffer during read-modify-write cycles.

PROM GC3 generates several signals. It generates HINCR once every ten clock
periods to increment the value of the horizontal line state machine. It generates
N.STATE11 which reloads the memory control state every tenth clock period.
It generates CP2 which loads the second level of video pixel buffers from the
first level of video pixel buffers every fifth clock period. (The first level
of the video pixel buffers is loaded on the rising edge of CAS). Lastly,
PROM GC3 generates signals OE1 through OE5 which effectively
multiplex 5:1 the pixel buffer output to the color map input.

The memory control state machine has ten states, and executes one of
two cycle types. In the first cycle type, no request to update the frame
buffer is present (X.RMW160 deasserted), and the state machine just extracts
the next ten pixels to display from frame buffer. In the second cycle type,
a request to update the frame buffer is present (X.RMW160 asserted). The
state machine extracts the next ten pixels to display, and additionally,
performs a read-modify-write cycle on the frame buffer memory.

---

## Memory Controller Timing Diagram


In the timing diagram below, the ten memory control states are labelled
2 through 11, corresponding to the outputs SH0..SH3 of the memory control
counter. Furthermore, for illustrative purposes, let us assume that BANK0-
BANK2, PAINT, and Z.MWRITE\ are at 0 volts.


```


		Video Cycle		Video and RMW Cycle
State (Hex)	2 3 4 5 6 7 8 9 A B 	2 3 4 5 6 7 8 9 A B
Signal:

RAS1		--------__________--    --------__------__--

RAS1A		---------__________-	---------__------__-

RAS.0\		_________-----------	_________---_____---

CAS1		----__----__________	----__----__------__

CAS2		--------____________	--------____----____

CAS.0\		-___--___-----------	-___--___----____---

WE\		--------------------	--------------__----

WE0\		--------------------	----------------__--

YLINOE\		------------------__	------------------__

XLINOE\		________------------	________------------

YREGOE\		--------____--------	--------____--------

XREGOE\		--------------------	------------____----

N.STATE11\	----------------__--	----------------__--

CP2		________--________--	________--________--

HINCR		____--____--________	____--____--________

OE1\		--------__--------__	--------__--------__

OE2\		__--------__--------	__--------__--------

OE3\		--__--------__------	--__--------__------

OE4\		----__--------__----	----__--------__----

OE5\		------__--------__--	------__--------__--


```


---

## Video Controller


The video controller generates the timing for the video monitor.
The timing described herein applies to a monitor with the following attributes:


	474 by 640 pixel active display area
	15.75 KHz horizontal frequency
	60 Hz vertical frequency
	2 to 1 vertical interlace


The video controller consists of the following components:
horizontal counter 74S163 (U2112 and U2114),
horizontal half-line toggle 74S74 (U1300),
vertical counter 74S163 (U1612 and U1712),
interlace toggle 74S74 (U1300),
horizontal decode PROM GC1 (U1800),
vertical decode PROM GC4 (U1508), and
video controller latch 74S374 (U1508).

The horizontal counter is advanced after every memory cycle (830 nsec) by
signal HINCR generated by the memory control state machine. The horizontal
counter is preset by signal RESET_H which is indirectly generated by
the horizontal state machine.

The vertical counter is clocked at the same time the horizontal counter is
preset. The vertical counter is cleared by signal RESET_V which is also
used to toggle the even/odd flag N.VODD. An extremely important aspect
of the timing of the state machine is that the vertical counter is clocked
(and/or cleared) on the same clock cycle as both the horizontal counter
and the even/odd flag N.VODD. If this is not the case, then erroneous data
would be generated by the video controller.

The even/odd flag VODD toggles on every vertical frame and is used both
for frame buffer addressing and RS-170 sync generation.

Horizontal state PROM GC1 inputs are the horizontal counter states H0 through
H7, plus a two bit code from the vertical state machine.
The two bit code VCODE0 and VCODE1 is zero during horizontal lines which we
will display; it is one during lines for which we generate vertical sync
equalization pulses (before actual sync); it is two during lines for which
the vertical sync should be generated; and, it is three during horizontal
lines for which normal horizontal sync should be generated but where no video is
output.
The horizontal PROM GC1 outputs are N.HRESET, SYNCH, DISPEN1, and HALFWAY.
The first three signals are self-explanatory. The last signal is used to clock
a flip-flop which toggles in the middle of the horizontal line period. This
signal is needed by the vertical state machine which must occasionally
generate the vcodes for sync on half-line boundaries.

Vertical state PROM GC4 inputs are the vertical counter states V1 through V8,
plus the horizontal half-line indicator HALF and the even/odd frame flag VODD.
The vertical state machine outputs are VCODE0 and VCODE1, which feed back into
the horizontal state machine, and N.VRESET and VBLANK. VBLANK is true during
the vertical blanking interval and is anded with the display enable signal
to generate TVBLANK which enables processor accesses to the color map.
As you remember from section 4.7, signal N.VRESET is jumpered to signal VRESET
in a single color board configuration, but the jumper can be removed to allow
multiple color boards to be operated on in parallel.

Video controller latch 74LS374 (U4) latches the outputs of
the horizontal and vertical state machines on the leading edge of the
system clock.

---

## Horizontal State Machine


Signal State (Vcode1 = 0; Vcode0 = 0; Normal Display Lines)

H0..H7 222222222222200000000000000000000000000000000000000000000000000111111111111111
       333334444455500000111112222233333444445555566666777778888899999000001111122222
       024680246802402468024680246802468024680246802468024680246802468024680246802468

HRESET _____________________________________________________________________________-

SYNCH\ --______---------------------------------------------------------------------

DISPEN ______________----------------------------------------------------------------

HALFWA ________________________________________--------------------------------------


Signal State (Vcode1 = 0; Vcode0 = 1; Sync Equalization Period)

H0..H7 222222222222200000000000000000000000000000000000000000000000000111111111111111
       333334444455500000111112222233333444445555566666777778888899999000001111122222
       024680246802402468024680246802468024680246802468024680246802468024680246802468

HRESET _____________________________________________________________________________-

SYNCH\ --___------------------------------------___----------------------------------

DISPEN ______________________________________________________________________________

HALFWA ________________________________________--------------------------------------


Signal State (Vcode1 = 1; Vcode0 = 0; Vertical Sync Generation)

H0..H7 222222222222200000000000000000000000000000000000000000000000000111111111111111
       333334444455500000111112222233333444445555566666777778888899999000001111122222
       024680246802402468024680246802468024680246802468024680246802468024680246802468

HRESET _____________________________________________________________________________-

SYNCH\ --__________________________________-----__________________________________---

DISPEN ______________________________________________________________________________

HALFWA ________________________________________--------------------------------------


Signal State (Vcode1 = 1; Vcode0 = 1; Period After Vsync and Equalization)

H0..H7 222222222222200000000000000000000000000000000000000000000000000111111111111111
       333334444455500000111112222233333444445555566666777778888899999000001111122222
       024680246802402468024680246802468024680246802468024680246802468024680246802468

HRESET _____________________________________________________________________________-

SYNCH\ --______----------------------------------------------------------------------

DISPEN ______________________________________________________________________________

HALFWA ________________________________________--------------------------------------


---

## Vertical State Machine


Signal	State

V1..V7	0 0 0 0 0 0 0 0 ... 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
	0 0 0 0 0 0 0 0 ... 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 4 5 5 5 5 5 5
	0 1 2 3 4 5 6 7 ... 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5

HALF  	_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

VRESET	______________________________________________________________--
  (EVEN)
VRESET	____________________________________________________________----
  (ODD)
VBLANK\	----------------------------____________________________________
  (EVEN)
VBLANK\	--------------------------______________________________________
  (ODD)
VCODE0	____________________________------______------------------------
  (EVEN)
VCODE0	__________________________-------______-------------------------
  (ODD)
VCODE1	__________________________________------______------------------
  (EVEN)
VCODE1	__________________________-______------______-------------------
  (ODD)


Note that the vertical syncs (i.e. vcode = 2) on even and odd frames
must be equi-distant from each other. The even sync occurs at state 241
and the remaining time until the odd interval is 14 lines. The odd
sync occurs at state 240.5 and the time until the even interval is 13.5.
Now, (14 + 240.5 = 13.5 + 241) so the sync pulses are equi-distant.

Note that the vertical sync time lasts 3 line times on both even and odd
frames and that the sync equalization time also lasts 3 horizontal periods
before and after the vertical sync.

Note also that both VCODE0 and VCODE1 are asserted during the first
half of state 237 on odd frames only.
This keeps the DISPEN1 signal from the horizontal state machine disabled,
but it also forces a normal sync signal during the very beginning of
stae 237. During the second half of state 237 on odd frames, VCODE1 is
dropped, and a half-width sync pulse will be generated during the middle
of line 237. It is the difference in sync timings for the odd and even
frames that allows to monitor to determine which frame is actually odd
and which is even.

---

## RS-170A Sync Timing


The Horizontal and Vertical State Machines implement the RS-170A monitor
standard. Unfortunately,  RS-170A standard is not quite compatible with
the NTSC Brodcast Standard.  The NTSC standard is a subset of the RS-170A
standard that specifies 525 total vertical lines with 480 visible lines.
The Sun-1 color board generates 511 total vertical lines with 474 visible.

Another problem with the RS-170A standard is that very few monitor
manufacturers really conform to the standard.  Most "RS-170" monitors
require a vertical sync signal that drops active low just once at the
end of a vertical scan; the RS-170A standard requires that the vertical
sync signal toggles on half-line boundaries to generate what is termed
"equalization pulses".

Of the few monitor manufacturers that do conform to the RS-170A standard
(Hitachi, Barco, Aydin, et al), there exists the further caveat that each
requires a different peak-to-peak voltage range on the sync signal. The
RS-170A standard calls for a 1.0 Vpp sync signal; most monitors want
a 4.0 Vpp signal. The Sun-1 color graphics card is strapped at shipping
to generate a 4.0 Vpp sync signal.  To adjust this sync level, remove
the card from your system.  Possesion of this document presupposes that
*you* are an OEM customer qualified to remove cards from your system.
If you have problems with this, please contact the support personnel at
Sun Microsystems. Viewing the color graphics card from the component side,
there are four sub-miniature coax connectors; the sub-miniature coax
connector on the far left is the sync connector. On the solder side of
the card, there is a jumper about 0.5 inches below the sync connector.
This jumper connects the sync signal to the sync connector. Replacing
this jumper with a 280 ohm (+- 25%) resistor will divide the sync level
from 4.0 Vpp to approximately 1.0 Vpp.

The diagrams on the following pages are reproduced from the RS-170A standard.

---

### RS-170A Timing Diagram - Page 1 of 2


---

### RS-170A Timing Diagram - Page 2 of 2


---

## Data Paths


### Main Data Bus


The on-board data bus B.D0..B.D7 is buffered from the Multibus data bus and
connects the following elements of the board:


```

	Multibus Data Input and Output (AM8303: U2125),
	Red Color Map Data Input and Output (AM2949: U1204),
	Green Color Map Data Input and Output (AM2949: U1212),
	Blue Color Map Data Input and Output (AM2949: U1226),
	Function Register Input and Output (AM2952: V1034),
	Mask (color) Register Input and Output (AM2952: V1032),
	Source (data) Register Input and Output (AM2952: V1030),
	Status Register Input (74LS273: U1028),
	Status Register Output (74LS244: U1026),
	X and Y-Register Read-back Muxs (74S257: U2124,U2322,U2116),
	Frame Buffer Read Latch (74LS374: U2334).

```


The outputs and inputs are enabled with the corresponding output enable
and write enable strobes generated by the address decoding logic on the board.


### Video Data Path


Video data (display data) is read from the frame buffer memory
using page-mode cycles on 150 nsec RAM and is clocked into a 40-bit wide, 2-bit
deep pixel buffer. The pixel buffer is implemented using ten 74LS374 registers
(U1334,U1434,U1534,U1634,U1734,U1834,U1934,U2034,U2134,U2234).

The output enables on the second-level of the pixel buffer are then used to
multiplex the pixel data five-to-one onto the eight-bit bus XDO0..XDO7.
Every 80 nano-seconds, the bus XDO0..XDO7 is clocked into a register
(74S534 at U1228) which then feeds the address inputs to the red, green, and
blue color maps (2148 1K by 4 RAM at U1206, U1208, U1214, U1216, U1220, U1222).

The data outputs of the color map RAM are then latched 80 nanoseconds later
into the 74S534 registers at U1202, U1210, U1218. The data bus at this point
is 24-bits wide (eight bits each for red, green, and blue), and flows through
the TTL to ECL converters at U1002, U1004, U1010, U1012, U1018, U1020 to drive
the video DACs at locations U1006, U1014, and U1022. The outputs of the
three video DACs are now connected via coaxial cable to a color monitor
and respectively drive the red, green, and blue color guns of that monitor.

During horizontal and vertical retrace periods, the output of register
U1228 is disabled and the address inputs to the color map are buffered
versions of the
Multibus address lines to allow read or write accesses to the color map.
Also during horizontal and vertical retrace, the outputs
of the 10124Q TTL to ECL converters are disabled (forced high) to
generate the video blanking level for the monitor's RGB electron guns.

---

### RasterOp Data Path


The RasterOp unit is composed of the following chips:


```

	Function Unit (74S251: U1036,U1038,U1040,U1042,U1044,U1046,U1048,U1050),
	Function Register (AM2952: V1034),
	Mask (Color) Register (AM2952: V1032),
   	Source Register (74LS374: U1030),
	Destination Multiplexors (74S240: U1035,U1335,U1635,U1835,U2135),

```


The Function, Source, and Mask Registers are loaded from the Data Bus.

On a read-modify-write RasterOp cycle, the following events happen:
Data is read from the frame buffer and the desired eight bits are allowed
to flow through one of the 74S240 buffers to the destination inputs of
the function unit.
The destination data, the source data, and the mask register data
enter the function unit and generate a new destination data
according to the function selected by the function register.
The new destination data is then rewritten into the frame buffer.


## Address Paths


This section describes the addressing of the frame buffer.
The addressing is somewhat different for the two major kind of
memory cycles: video refresh and read/write.

During *video refresh* cycles the memory address comes from the
video controller state machine and drives memory
via the RAS and CAS address registers (74LS374) at locations U1812 and U1814
and the address line driver (74S244) at location U1828.

During *read/write* cycles the memory address comes from the
X and Y-address registers and drives memory
via the RAS and CAS address registers (74LS374) at locations U1824 and U1826
and the same address line driver at location U1828.

The frame buffer memory is organized as forty 64K RAM corresponding to
five consecutive pixels of eight bits. PROM GC5 generates the necessary
bank selects (BANK0..BANK2) and bank buffer enables (XE0..XE4) by computing
the value of the X-address register MODULO 5.

Addresses for the 64K RAM
are formed by dividing the X-address by 5 using PROM GC6. This value and the
Y-address are then concatenated to form the 16-bit address for the 64K RAM.
The exact mapping of X and Y addresses into RAS and CAS addresses is shown
in the table below:


```


	    Video Cycle Signals	    Update Cycle Signals
RAM Addr	RAS 	CAS		RAS	CAS
--------	---	---		---	---
R.A0		 H1	 H0		XH1	XH0
R.A1		 H2	 V3		XH2	BV3
R.A2		 H3	 V4		XH3	BV4
R.A3		 H4	 V5		XH4	BV5
R.A4		 H5	 V6		XH5	BV6
R.A5		 H6	 V7		XH6	BV7
R.A6		 V1	 V8		BV1	BV8
R.A7		 V2      VODD		BV2	BVODD


```


---

## Multibus Interface Logic


Major components of the Multibus interface logic are
Multibus address decoding, request generation, and interrupt logic.


### Base Address Decoding and Other Jumpers


For more information on jumpering, see the Sun Color Board User's Manual.

The color video board occupies 16K bytes in the Multibus memory address space.
The board can be addressed on any one of the 64 16K byte boundaries
of the 1M byte Multibus address space by means of the jumper posts at location
J2110 (J1).
The address select jumper posts are identifiable as there should be six of them
side by side. If you still can't find them,
see the parts location diagram in this manual.
The most significant address bit is on the far right;
the least significant address bit is on the far left.
A one in the address is selected by inserted a jumper at that pole position.
For example, the jumper positions shown below select the following addresses
(an inserted jumper is shown as a "1", a missing jumper is shown as a "0"):


```

	JUMPER		BASE ADDRESS
	------		------------
	000000		0x100000
 	111111		0x1FC000
	110111		0x1EC000     /* Standard base for single color board */
	010111		0x1E8000     /* Base for second board in 3 board system */
	100111		0x1E4000     /* Base for third board in 3 board system */

```


The address select jumpers feed one set of inputs to the eight bit comparator
(AM25LS2521) at location U2210. The other set of inputs to the address
comparator come from Multibus address bits BUS.A14\ through BUS.A19. If
your board won't respond at all, check the output of this comparator first
(MEMSEL).

The second set of jumpers decide wether or not any other
color boards should be synchronized with this board. These jumpers are at location
J2010 (J2). There are only five of these jumpers, and they are located just above
the address select jumpers. Either *all* of these jumpers should be in, or
none of them should be in. If this is a single color-board configuration,
or if this board is the master board in a multi-board color system, then all
jumpers should be in. If this board is a slave-board in a multi-board color
system, then *all* these jumpers should be removed; there can be only *one*
master board in a multi-board color system. Note that when these jumpers are
in, five signals generated on the board will each drive a net on the
board *and a pin on the P2 connector*. Because of this:

**WARNING: NEVER INSERT A COLOR BOARD INTO A CARD SLOT WITH A P2 CONNECTOR**

If this happens, the signal runs on the color board that are connected
to the P2 bus may have their drivers burned out by a signal on another Multibus
card that is also driving that P2 bus line; similarly the other cards on the
P2 bus may be damaged.
However, in a multi-board color system, the color boards must be plugged into
a common P2 connector. *Make sure that only one of the color cards
has jumpers installed at location J2010*.

To reiterate the connection of jumpers at location J2010 (J2):

```

	JUMPERS		FUNCTION
	-------		--------
	 11111		Single color board or master color board
	 00000		Slave color board in a multi-board color system
	 ?????		Any other combination will not work

```


---

The third set of jumpers on the card define the interrupt level for the card.
Interrupts do not have to be enabled and can be permanently disabled by
installing no jumper at location J2304 (J3). There are eight pairs of jumper poles
for the interrupt level select; the jumper location can be determined from
this unique feature or from the part location diagram. Interrupt level 0
is selected by inserting a jumper on the far right. Interrupt level 7 is
selected by inserting a jumper on the far left. Note that on Sun-1 processor
boards, only interrupt levels 1,2, and 3 are usable by Multibus devices. As
a quick example (A "1" shows the existence of a jumper):


```


	JUMPERS		INTERRUPT LEVEL SELECTED
	--------	------------------------
	00000010	Interrupt Level 1
	00000100	Interrupt Level 2
	00001000	Interrupt Level 3
	01000000	Interrupt Level 6 	(Won`t work with Sun-1 Processor)
	00000000	Interrupts Disabled	(Ignore Diagnostic error message)


```


The fourth set of jumper poles on  the board selects byte orders between
MC68000 and Intel-based microprocessors. Given a 16-bit word, Motorola defines
the high-byte as byte zero and the low-byte as byte one. Intel defines the
high-byte as byte one and the low-byte as byte zero. The four pole jumper
at location J2324 (J4) inverts address bit A0 on the Multibus as needed. If you
jumper the board wrong, every other pixel on your screen will be swapped. If
do not install any jumper at all at this location, you will not be able to
access every other pixel on the screen. Looking at the board from the component
side and with the Multibus connector towards you, jumper J2324 (J4) as follows
(In this example, connect the poles marked with a "+"):


```


	JUMPER		FUNCTION
	------		--------

	  0+		Select MC68000 byte-order
	  0+

	  00		Select 8086 byte-order
	  ++

	  00		Don't do this.
	  00


```


The last jumper on the board was described earlier an adjusts the peak-to-peak
voltage level of the sync signal.  To adjust this sync level, remove
the card from your system.  Viewing the color graphics card from the
component side,
there are four sub-miniature coax connectors; the sub-miniature coax
connector on the far left is the sync connector. On the solder side of
the card, there is a jumper about 0.5 inches below the sync connector.
This jumper connects the sync signal to the sync connector. Replacing
this jumper with a 280 ohm (+- 25%) resistor will divide the sync level
from 4.0 Vpp to approximately 1.0 Vpp.

---

### Multibus Address Decoding


The Sun color video board has a fully buffered Multibus interface (see next
section in manual as well). When the color
board is ready to receive a new command from the Multibus, the Multibus
address latch (74S533: U2316; 74LS533: U2310)
is opened. After the command is received, the addresses from the Multibus
and the Multibus read and write strobes (BUS.MRDC and BUS.MWTC) are
latched and decoded as follows (See User's Manual for more information):


```

	Address Bits
A13 A12 A11 A10  A9  A8  A7  A6   	Function Selected
-------------------------------	   ---------------------------
 0   0   1   n   X   X   X   X     On read or write, update x-address register
				   (set n where n=0 or 1) with A9 through A0.
 0   0   0   n   X   X   X   X     On read or write, update y-address register
				   (set n where n=0 or 1) with A8 through A0.
 1   0   1   n   X   X   X   X     Update x-address register set n and Data
				   Register. Do pixel read or write.
 1   0   0   n   X   X   X   X     Update y-address register set n and Data
				   Register. Do pixel read or write.

 X   1   0   X   0   0   X   X     Access red color lookup map. Read/Write
				   only performed during blanking interval.
 X   1   0   X   0   1   X   X     Access green color lookup map. Read/Write
				   only performed during blanking interval.
 X   1   0   X   1   0   X   X     Access blue color lookup map. Read/Write
				   only performed during blanking interval.

 X   1   1   X   0   0   0   X     Read/Write Status Register.
 X   1   1   X   0   1   0   X     Read/Write Mask (Color) Register.
 X   1   1   X   1   0   0   X     Read/Write Function Register.

 X   1   1   n   1   1   0   0     Read returns x-address register (set n)
				   bits A7-A0.
 X   1   1   n   1   1   1   0     Read returns x-address register (set n)
				   bits A9-A8. Bits 2 through 7 in returned
				   byte are invalid.
 X   1   1   n   1   1   0   1     Read returns y-address register (set n)
				   bits A7-A0.
 X   1   1   n   1   1   1   1     Read returns y-address register (set n)
				   bits A9-A8. Bits 2 through 7 in returned
				   byte are invalid.

```


---

### Multibus Request Logic


The video board uses a buffered interface to the Multibus.
When the Multibus master issues a read or write request (BUS.MRDC or
BUS.MWTC),
and the video board is addressed appropriately as described above
and the video board is idle (no previous request pending)
then an onboard request (REQ) is generated that latches
the Multibus address lines and the read or write strobe.
Immediately after the address lines are latched,
a Multibus transfer acknowledge (BUS.XACK) is issued allowing the
master to continue with other operations.
However, when the video board is busy, that is,
when a previous request is in progress (REQ asserted), the board will not
respond to Multibus requests until the previous request is completed.
Overlapped requests are prevented by tying REQ to the active low enable
on the base address comparator (25LS2521 at U2210). This keeps NEWREQ
from being asserted until the current request is processed.

BUS.MRDC and BUS.MWTC are buffered with receiver 74S240 (U2300) to
form signals READ and WRITE. READ or WRITE is gated with MEMSEL
(74S32: U2100) to form NEWREQ. NEWREQ is delayed 40 nsec and then
enables driver 74S240 (U2300) which asserts BUS.XACK as soon as T.ACK
is asserted. T.ACK is asserted well before NEWREQ40 in all cases except
accesses to the color map. On color map accesses, T.ACK will go active
between 100 and 180 nsec after NEWREQ. The delay caused by T.ACK is
required to access the color map RAM.

Note that read requests from the frame buffer are acknowledged immediately.
This happens because reads from the frame buffer are buffered by the
74LS374 register at U2334. Data returned on a frame buffer read
is actually the pixel datum requested on the previous read. All software
written to access the frame buffer must handle this feature.

When the Multibus read/write strobes are deasserted, NEWREQ is also
deasserted. This in turn asserts SETREQ which presets REQ (74S74: U2200).
SETREQ is only active for 20 nsec; after this time, if the board access
is not an update to the frame buffer (RMW asserted) then RMW will clear
the REQ flip-flop (74S74: U2200) and another request can be immediately
processed by the color board.

If the access to the board specifies an update to the frame buffer, then
REQ will remain asserted after SETREQ is deasserted. The events leading
to the deassertion of REQ are now described.
REQ is synchronized
once with the system clock to generate REQ80 (74LS174: U1700).
Now, on frame buffer update
accesses, signal RMW will be asserted. RMW is also synchronized once with the
system clock to generate RMW80 (74LS174: U1700). REQ80 is gated with RMW80
(74S08: U1800) and this value (X.RMW160) is clocked into a flip-flop (74S74: U1600)
by signal YREQOE
just before the start of the Read-Modify-Write cycle time of the frame buffer.
If X.RMW160 is asserted at the start of the RMW cycle time, then the access
to the frame buffer continues, and the REQ flip-flop is cleared by the
memory control state machine output WE. Pardon the naming problem, but WE
is generated both when reading/writting the frame buffer.

Once REQ is deasserted, the device select comparator is reenabled, the address
and read/write latches are openned, and the board is ready to process another
command.

---

### Interrupt Logic


All updates to the color maps can only occur during a vertical retrace
period. Likewise, switching between color maps can cause un-aesthetic
jitters if the switch is not made during the vertical retrace period.

The user has two options when waiting for the vertical retrace period.
He/she can do a busy-wait while waiting for bit 7 in the status register
(TVBLANK) to go true, or the user can take an interrupt at the start
of the vertical retrace.

To enable interrupts, bit D4 (INTEN) in the status register 74LS273 (U1028)
needs to be set and the desired interrupt level be selected via jumpers
at location J2304 (See preceding pages).
When INTEN is asserted, the leading edge of VBLANK sets VINT
(74S74: U2200). VINT is then passed through an open-collector inverter
and is output onto the Multibus after passing through the jumper box
at J2304.
A pending interrupt is cleared by deasserting INTEN which clears the
flip-flop generating VINT.

---

# Programmable Logic


## Introduction


This chapter contains the source files and object files for
programmable logic elements such as PALs and PROMs.
The content of these elements is defined in the high-level
language C and is automatically translated
into bitpatterns for programming.

Without attempting to give a full definition of the macros used,
the following explanation should provide sufficient information
to understand the programs.

*prom1024x4* (or a statement in the same format) sets the number of
addressable locations in the prom (in this case 1024).The width of
each entry in the prom is irrelevant.

*prombegin* tells the program to evaluate the following statements
until *promend* for each location value of the location counter.

*prom(#1, #2,	expression)* means to put the value of *expression*
into PROM *#1* bit position *#2*. A single program can define
the contents of multiple PROMs by using multiple PROM numbers *#1*.

*promend* terminates the evaluation of statements.

*writeprom("file",#)* writes the object code of PROM *#* into file *file*.
Each separate PROM needs to be written into a separate file.

In the following listings, the PROM source code is followed by the generated
hexadecimal object code which also includes a 16-bit checksum.

---

## PROM GC0


```

/* ======================================================================
   Author:
   Date :  March 17, 1983
   Purpose: This file contains the source code for prom CG0 on the Sun-1
	color board. This prom controls the generation of WE\ lines to
	the frame buffer memory.
   Timing:
   Speed: 50 nsec
   Rev: Revision D.
   Bugs:
   ====================================================================== */

#include "/usr/pwc/pl/prom.c"

/* Define Inputs to 32K x 8 Prom. */
#define bank0    (a0)
#define bank1    (a1)
#define bank2    (a2)
#define paint    (a3)
#define mread    (a4)

#define mwrite   (! mread)

#define bank bankk()
bankk()
{ short i;
  i = (cvb(bank0)*d0 + cvb(bank1)*d1 + cvb(bank2)*d2);
  return(i);
}

/* Define Outputs from Prom */
#define we0  (mwrite && (paint || (bank == 0)))
#define we1  (mwrite && (paint || (bank == 1)))
#define we2  (mwrite && (paint || (bank == 2)))
#define we3  (mwrite && (paint || (bank == 3)))
#define we4  (mwrite && (paint || (bank == 4)))

main()
{
prom32x8;

prombegin
prom(0,d0,!we0)
prom(0,d1,!we1)
prom(0,d2,!we2)
prom(0,d3,!we3)
prom(0,d4,!we4)
prom(0,d5, 1)
prom(0,d5, 1)
prom(0,d5, 1)
promend;

writeprom("cg0",0);
}


====================================================================

PROM:	cg0	Checksum:	1EC9
ADDR  DATA

   0  FE  FD  FB  F7  EF  FF  FF  FF  E0  E0  E0  E0  E0  E0  E0  E0
  16  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF  FF

```


---

## PROM GC1


/* ======================================================================
   Author:
   Date :  March 17, 1983
   Purpose: This file contains the source code for prom CG1 on the Sun-1
	color board. This prom controls the horizontal timing of an RS-170A
   	60 Hz interlaced monitor with a displayable area of 474 by 640 pixels.
   Timing:
   Speed: 50 nsec
   Rev: Revision D.
   Bugs:
   ====================================================================== */

#include "/usr/pwc/pl/prom.c"
#define range(low,x,high) ((low<=x)&&(x<=high))

/* Define Inputs to 1K x 4 Prom. */
#define vcode0   (a0)
#define vcode1   (a1)
#define h0       (a2)
#define h1       (a3)
#define h2       (a4)
#define h3       (a5)
#define h4       (a6)
#define h5       (a7)
#define h6       (a8)
#define h7       (a9)


#define pixel5 pix()
pix()
{ short i;
  i = (cvb(h0)*d0 + cvb(h1)*d1 + cvb(h2)*d2 + cvb(h3)*d3 +
       cvb(h4)*d4 + cvb(h5)*d5 + cvb(h6)*d6 + cvb(h7)*d7 );
  return(i);
}

#define vcode  	  (cvb(vcode0)*d0 + cvb(vcode1)*d1)
#define vscan	  (vcode == 0)
#define veq  	  (vcode == 0)
#define vsynch	  (vcode == 0)
#define aft_vsync (vcode == 0)


/* Define Outputs from Prom */

#define hreset range(129,pixel5,229)
#define dispen (vscan && range(2,pixel5,229))
#define halfway range(55,pixel5,229)

#define sync synch()
synch()
{ short i;
  if (vscan || aft_vsync) {
     i = range(234,pixel5,245);
  } else if (veq) {
     i = (range(234,pixel5,239) || range(56,pixel5,61));
  } else if (vsynch) {
     i = (range(234,pixel5,255) || range(0,pixel5,44) || range(56,pixel5,122));
  }
  return(i);
}


main()
{
prom1024x4;

prombegin
prom(0,d0, hreset)
prom(0,d1,!sync)
prom(0,d2, dispen)
prom(0,d3, halfway)
promend;

writeprom("cg1",0);
}


====================================================================

PROM:	cg1	Checksum:	21B0
ADDR  DATA

   0  02  02  00  02  02  02  00  02  06  02  00  02  06  02  00  02
  16  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
  32  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
  48  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
  64  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
  80  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
  96  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
 112  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
 128  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
 144  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
 160  06  02  00  02  06  02  00  02  06  02  00  02  06  02  00  02
 176  06  02  00  02  06  02  02  02  06  02  02  02  06  02  02  02
 192  06  02  02  02  06  02  02  02  06  02  02  02  06  02  02  02
 208  06  02  02  02  06  02  02  02  06  02  02  02  0E  0A  0A  0A
 224  0E  08  08  0A  0E  08  08  0A  0E  08  08  0A  0E  08  08  0A
 240  0E  08  08  0A  0E  08  08  0A  0E  0A  08  0A  0E  0A  08  0A
 256  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 272  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 288  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 304  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 320  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 336  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 352  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 368  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 384  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 400  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 416  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 432  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 448  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 464  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A
 480  0E  0A  08  0A  0E  0A  08  0A  0E  0A  08  0A  0E  0A  0A  0A
 496  0E  0A  0A  0A  0E  0A  0A  0A  0E  0A  0A  0A  0E  0A  0A  0A
 512  0E  0A  0A  0A  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 528  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 544  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 560  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 576  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 592  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 608  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 624  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 640  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 656  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 672  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 688  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 704  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 720  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 736  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 752  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 768  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 784  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 800  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 816  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 832  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 848  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 864  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 880  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 896  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B  0F  0B  0B  0B
 912  0F  0B  0B  0B  0F  0B  0B  0B  02  02  02  02  02  02  02  02
 928  02  02  02  02  02  02  02  02  00  00  00  00  00  00  00  00
 944  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00  00
 960  00  02  00  00  00  02  00  00  00  02  00  00  00  02  00  00
 976  00  02  00  00  00  02  00  00  02  02  00  02  02  02  00  02
 992  02  02  00  02  02  02  00  02  02  02  00  02  02  02  00  02
1008  02  02  00  02  02  02  00  02  02  02  00  02  02  02  00  02


---

## PROM GC2


```

/* ======================================================================
   Author:
   Date :  March 17, 1983
   Purpose: This file contains the source code for prom CG2 on the Sun-1
	color board. This prom controls the Ras, Cas, We\ and address
	multiplexors for the frame buffer memory.
   Timing:
   Speed: 50 nsec
   Rev: Revision D.
   Bugs:
   ====================================================================== */
#include "/usr/pwc/pl/prom.c"
#define range(low,x,high) ((low<=x)&&(x<=high))

/* Define Inputs to 32K x 8 Prom. */
#define sh0    (a0)
#define sh1    (a1)
#define sh2    (a2)
#define sh3    (a3)
#define do←rmw (a4)

#define st state()
state()
{ short i;
  i = (cvb(sh0)*d0 + cvb(sh1)*d1 + cvb(sh2)*d2 + cvb(sh3)*d3 );
  return(i); }

/* Define Outputs from Prom */
#define ras1 (range(2,st,5) || (st==11) || (do←rmw&⦥(7,st,9)))
#define cas1 (range(2,st,3) || range(5,st,6) || (do←rmw&⦥(8,st,10)))
#define cas2 (range(2,st,5) || (do←rmw&⦥(8,st,9)))
#define weh  (do←rmw && (st==9))
#define ylinoe (st==11)
#define xlinoe range(2,st,5)
#define yregoe range(6,st,7)
#define xregoe (do←rmw && range(8,st,9))

main()
{
prom32x8;

prombegin
prom(0,d0, ras1)
prom(0,d1, cas1)
prom(0,d2, cas2)
prom(0,d3,!weh)
prom(0,d4,!ylinoe)
prom(0,d5,!xlinoe)
prom(0,d6,!yregoe)
prom(0,d7,!xregoe)
promend;

writeprom("cg2",0);
}

====================================================================

PROM:	cg2	Checksum:	1C23
ADDR  DATA

   0  F8  F8  DF  DF  DD  DF  BA  B8  F8  F8  F8  E9  F8  F8  F8  F8
  16  F8  F8  DF  DF  DD  DF  BA  B9  7F  77  FA  E9  F8  F8  F8  F8

```


---

## PROM GC3


```

/* ======================================================================
   Author:
   Date :  March 17, 1983
   Purpose: This file contains the source code for prom CG3 on the Sun-1
	color board. This prom controls reseting the memory control state
	machine, incrementing the horizontal state machine, and clocking
	and multiplexing the frame buffer video buffer.
   Timing:
   Speed: 50 nsec
   Rev: Revision D.
   Bugs:
   ====================================================================== */
#include "/usr/pwc/pl/prom.c"
#define range(low,x,high) ((low<=x)&&(x<=high))

/* Define Inputs to 32K x 8 Prom. */
#define sh0    (a0)
#define sh1    (a1)
#define sh2    (a2)
#define sh3    (a3)
#define pu     (a4)

#define st state()
state()
{ short i;
  i = (cvb(sh0)*d0 + cvb(sh1)*d1 + cvb(sh2)*d2 + cvb(sh3)*d3 );
  return(i); }

/* Define Outputs from Prom */
#define state11 (st==10)
#define hincr	((st== 3) || (st== 6))
#define cp2	((st== 6) || (st==11))
#define oe1	((st== 6) || (st==11))
#define oe2	((st== 7) || (st== 2))
#define oe3	((st== 8) || (st== 3))
#define oe4	((st== 9) || (st== 4))
#define oe5	((st==10) || (st== 5))

main()
{
prom32x8;

prombegin
prom(0,d0,!state11)
prom(0,d1, cp2)
prom(0,d2,!oe1)
prom(0,d3,!oe2)
prom(0,d4,!oe3)
prom(0,d5,!oe4)
prom(0,d6,!oe5)
prom(0,d7, hincr)
promend;

writeprom("cg3",0);
}

====================================================================

PROM:	cg3	Checksum:	0FB6
ADDR  DATA

   0  7D  7D  75  ED  5D  3D  FB  75  6D  5D  3C  7B  7D  7D  7D  7D
  16  7D  7D  75  ED  5D  3D  FB  75  6D  5D  3C  7B  7D  7D  7D  7D

```


---

## PROM GC4


/* ======================================================================
   Author:
   Date :  March 17, 1983
   Purpose: This file contains the source code for prom CG4 on the Sun-1
	color board. This prom controls the vertical timing of an RS-170A
	60 Hz interlaced monitor with a displayable area of 474 by 640 pixels.
   Timing:
   Speed: 50 nsec
   Rev: Revision D.
   Bugs:
   ====================================================================== */

#include "/usr/pwc/pl/prom.c"
#define range(low,x,high) ((low<=x)&&(x<=high))

/* Define Inputs to 1K x 4 Prom. */
#define vodd     (a0)
#define v1       (a1)
#define v2       (a2)
#define v3       (a3)
#define v4       (a4)
#define v5       (a5)
#define v6       (a6)
#define v7       (a7)
#define v8       (a8)
#define halfway  (a9)

#define V vv()
vv()
{ short i;
  i = (cvb(v1)*d0 + cvb(v2)*d1 + cvb(v3)*d2 + cvb(v4)*d3 +
       cvb(v5)*d4 + cvb(v6)*d5 + cvb(v7)*d6 + cvb(v8)*d7 );
  return(i);
}

/* Define Outputs from Prom */

#define vscan	  0
#define veq  	  1
#define vsynch	  2
#define aft_vsync 3

#define vcode vvcode()
vvcode()
{ short code;
  if (!vodd) {
     if range(0,V,237) {
        code = vscan;
     } else if range(238,V,240) {
	code = veq;
     } else if range(241,V,243) {
	code = vsync;
     } else if range(247,V,255) {
	code = aft_vsync;
     }


---


  } else if (vodd) {
     if range(0,V,236) {
	code = vscan;
     } else if ((V==237)&&(!halfway)) {
	code = aft_vsync;
     } else if ((V==237)&&( halfway)) {
	code = veq;
     } else if range(238,V,239) {
	code = veq;
     } elwe if ((V==240)&&(!halfway)) {
	code = veq;
     } elwe if ((V==240)&&( halfway)) {
	code = vsync;
     } else if range(241,V,242) {
	code = vsync;
     } else if ((V==243)&&(!halfway)) {
	code = vsync;
     } else if ((V==243)&&( halfway)) {
	code = veq;
     } else if range(244,V,245) {
	code = veq;
     } else if ((V==246)&&(!halfway)) {
	code = veq;
     } else if ((V==246)&&( halfway)) {
	code = aft_vsync;
     } else if range(247,V,255) {
	code = aft_vsync;
     }
  }
  return(code);
}

#define vreset ((vodd && (V==254)) || ((!vodd) && (V==255)))
#define vblank (vcode > 0)


main()
{
prom1024x4;

prombegin
prom(0,d0, vcode&d0)
prom(0,d1, vcode&d1)
prom(0,d2, vreset)
prom(0,d3,!vblank);
promend;

writeprom("cg4",0);
}


====================================================================

PROM:	cg41	Checksum:	1E62
ADDR  DATA

   0  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  16  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  32  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  48  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  64  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  80  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
  96  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 112  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 128  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 144  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 160  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 176  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 192  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 208  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 224  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 240  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 256  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 272  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 288  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 304  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 320  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 336  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 352  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 368  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 384  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 400  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 416  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 432  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 448  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 464  08  08  08  08  08  08  08  08  08  08  08  03  01  01  01  01
 480  01  01  02  02  02  02  02  02  01  01  01  01  01  01  03  03
 496  03  03  03  03  03  03  03  03  03  03  03  03  03  07  07  03
 512  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 528  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 544  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 560  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 576  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 592  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 608  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 624  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 640  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 656  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 672  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 688  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 704  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 720  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 736  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 752  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 768  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 784  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 800  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 816  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 832  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 848  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 864  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 880  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 896  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 912  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 928  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 944  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 960  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08  08
 976  08  08  08  08  08  08  08  08  08  08  08  01  01  01  01  01
 992  01  02  02  02  02  02  02  01  01  01  01  01  01  03  03  03
1008  03  03  03  03  03  03  03  03  03  03  03  03  03  07  07  03


---

## PROM GC5 and GC6


/* ======================================================================
   Author:
   Date :  March 17, 1983
   Purpose: This file contains the source code for proms CG5 and CG6 on
	the Sun-1 color board. Prom CG6 divides the horizontal pixel
	address by 5 (Horizontally, the frame buffer is organized as 128 sets
	of 5 pixels). Prom CG5 computes the horizontal pixel address MOD 5.
	Prom CG5 selects the pixel (0..4) from the 5-wide set that is
	being addressed.
   Timing:
   Speed: 50 nsec
   Rev: Revision D.
   Bugs:
   ====================================================================== */

#include "/usr/pwc/pl/prom.c"
#define DIV /
#define MOD %

/* Define Inputs to 1K x 8 Prom. */
#define h0    (a0)
#define h1    (a1)
#define h2    (a2)
#define h3    (a3)
#define h4    (a4)
#define h5    (a5)
#define h6    (a6)
#define h7    (a7)
#define h8    (a8)
#define h9    (a9)


#define H hh()
hh()
{ short i;
  i = (cvb(h0)*d0 + cvb(h1)*d1 + cvb(h2)*d2 + cvb(h3)*d3 + cvb(h4)*d4 +
       cvb(h5)*d5 + cvb(h6)*d6 + cvb(h7)*d7 + cvb(h8)*d8 + cvb(h9)*d9);
  return(i);
}

#define set    (H DIV 5)
#define entry  (H MOD 5)

#define entry0 (entry==0)
#define entry1 (entry==1)
#define entry2 (entry==2)
#define entry3 (entry==3)
#define entry4 (entry==4)


---


main()
{
prom1024x8;

prombegin
prom(0,d0, entry&d0)
prom(0,d1, entry&d1)
prom(0,d2, entry&d2)
prom(0,d3, entry0)
prom(0,d4, entry1)
prom(0,d5, entry2)
prom(0,d6, entry3)
prom(0,d7, entry4)

prom(1,d0, set&d0)
prom(1,d1, set&d1)
prom(1,d2, set&d2)
prom(1,d3, set&d3)
prom(1,d4, set&d4
prom(1,d5, set&d5
prom(1,d6, set&d6)
prom(1,d7, 1)

promend;

writeprom("cg5",0);
writeprom("cg6",1);
}


====================================================================

PROM:	cg5	Checksum:	21E6
ADDR  DATA

   0  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
  16  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
  32  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
  48  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
  64  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
  80  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
  96  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 112  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 128  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 144  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 160  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 176  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 192  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 208  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 224  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 240  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 256  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 272  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 288  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 304  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 320  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 336  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 352  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 368  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 384  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 400  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 416  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 432  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 448  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 464  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 480  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 496  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 512  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 528  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 544  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 560  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 576  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 592  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 608  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 624  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 640  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 656  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 672  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 688  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 704  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 720  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 736  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 752  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 768  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 784  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 800  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 816  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 832  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 848  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 864  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 880  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 896  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 912  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
 928  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB
 944  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C
 960  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0
 976  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9
 992  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA
1008  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB  7C  F0  E9  DA  BB


====================================================================

PROM:	cg6	Checksum:	D79A
ADDR  DATA

   0  80  80  80  80  80  81  81  81  81  81  82  82  82  82  82  83
  16  83  83  83  83  84  84  84  84  84  85  85  85  85  85  86  86
  32  86  86  86  87  87  87  87  87  88  88  88  88  88  89  89  89
  48  89  89  8A  8A  8A  8A  8A  8B  8B  8B  8B  8B  8C  8C  8C  8C
  64  8C  8D  8D  8D  8D  8D  8E  8E  8E  8E  8E  8F  8F  8F  8F  8F
  80  90  90  90  90  90  91  91  91  91  91  92  92  92  92  92  93
  96  93  93  93  93  94  94  94  94  94  95  95  95  95  95  96  96
 112  96  96  96  97  97  97  97  97  98  98  98  98  98  99  99  99
 128  99  99  9A  9A  9A  9A  9A  9B  9B  9B  9B  9B  9C  9C  9C  9C
 144  9C  9D  9D  9D  9D  9D  9E  9E  9E  9E  9E  9F  9F  9F  9F  9F
 160  A0  A0  A0  A0  A0  A1  A1  A1  A1  A1  A2  A2  A2  A2  A2  A3
 176  A3  A3  A3  A3  A4  A4  A4  A4  A4  A5  A5  A5  A5  A5  A6  A6
 192  A6  A6  A6  A7  A7  A7  A7  A7  A8  A8  A8  A8  A8  A9  A9  A9
 208  A9  A9  AA  AA  AA  AA  AA  AB  AB  AB  AB  AB  AC  AC  AC  AC
 224  AC  AD  AD  AD  AD  AD  AE  AE  AE  AE  AE  AF  AF  AF  AF  AF
 240  B0  B0  B0  B0  B0  B1  B1  B1  B1  B1  B2  B2  B2  B2  B2  B3
 256  B3  B3  B3  B3  B4  B4  B4  B4  B4  B5  B5  B5  B5  B5  B6  B6
 272  B6  B6  B6  B7  B7  B7  B7  B7  B8  B8  B8  B8  B8  B9  B9  B9
 288  B9  B9  BA  BA  BA  BA  BA  BB  BB  BB  BB  BB  BC  BC  BC  BC
 304  BC  BD  BD  BD  BD  BD  BE  BE  BE  BE  BE  BF  BF  BF  BF  BF
 320  C0  C0  C0  C0  C0  C1  C1  C1  C1  C1  C2  C2  C2  C2  C2  C3
 336  C3  C3  C3  C3  C4  C4  C4  C4  C4  C5  C5  C5  C5  C5  C6  C6
 352  C6  C6  C6  C7  C7  C7  C7  C7  C8  C8  C8  C8  C8  C9  C9  C9
 368  C9  C9  CA  CA  CA  CA  CA  CB  CB  CB  CB  CB  CC  CC  CC  CC
 384  CC  CD  CD  CD  CD  CD  CE  CE  CE  CE  CE  CF  CF  CF  CF  CF
 400  D0  D0  D0  D0  D0  D1  D1  D1  D1  D1  D2  D2  D2  D2  D2  D3
 416  D3  D3  D3  D3  D4  D4  D4  D4  D4  D5  D5  D5  D5  D5  D6  D6
 432  D6  D6  D6  D7  D7  D7  D7  D7  D8  D8  D8  D8  D8  D9  D9  D9
 448  D9  D9  DA  DA  DA  DA  DA  DB  DB  DB  DB  DB  DC  DC  DC  DC
 464  DC  DD  DD  DD  DD  DD  DE  DE  DE  DE  DE  DF  DF  DF  DF  DF
 480  E0  E0  E0  E0  E0  E1  E1  E1  E1  E1  E2  E2  E2  E2  E2  E3
 496  E3  E3  E3  E3  E4  E4  E4  E4  E4  E5  E5  E5  E5  E5  E6  E6
 512  E6  E6  E6  E7  E7  E7  E7  E7  E8  E8  E8  E8  E8  E9  E9  E9
 528  E9  E9  EA  EA  EA  EA  EA  EB  EB  EB  EB  EB  EC  EC  EC  EC
 544  EC  ED  ED  ED  ED  ED  EE  EE  EE  EE  EE  EF  EF  EF  EF  EF
 560  F0  F0  F0  F0  F0  F1  F1  F1  F1  F1  F2  F2  F2  F2  F2  F3
 576  F3  F3  F3  F3  F4  F4  F4  F4  F4  F5  F5  F5  F5  F5  F6  F6
 592  F6  F6  F6  F7  F7  F7  F7  F7  F8  F8  F8  F8  F8  F9  F9  F9
 608  F9  F9  FA  FA  FA  FA  FA  FB  FB  FB  FB  FB  FC  FC  FC  FC
 624  FC  FD  FD  FD  FD  FD  FE  FE  FE  FE  FE  FF  FF  FF  FF  FF
 640  80  80  80  80  80  81  81  81  81  81  82  82  82  82  82  83
 656  83  83  83  83  84  84  84  84  84  85  85  85  85  85  86  86
 672  86  86  86  87  87  87  87  87  88  88  88  88  88  89  89  89
 688  89  89  8A  8A  8A  8A  8A  8B  8B  8B  8B  8B  8C  8C  8C  8C
 704  8C  8D  8D  8D  8D  8D  8E  8E  8E  8E  8E  8F  8F  8F  8F  8F
 720  90  90  90  90  90  91  91  91  91  91  92  92  92  92  92  93
 736  93  93  93  93  94  94  94  94  94  95  95  95  95  95  96  96
 752  96  96  96  97  97  97  97  97  98  98  98  98  98  99  99  99
 768  99  99  9A  9A  9A  9A  9A  9B  9B  9B  9B  9B  9C  9C  9C  9C
 784  9C  9D  9D  9D  9D  9D  9E  9E  9E  9E  9E  9F  9F  9F  9F  9F
 800  A0  A0  A0  A0  A0  A1  A1  A1  A1  A1  A2  A2  A2  A2  A2  A3
 816  A3  A3  A3  A3  A4  A4  A4  A4  A4  A5  A5  A5  A5  A5  A6  A6
 832  A6  A6  A6  A7  A7  A7  A7  A7  A8  A8  A8  A8  A8  A9  A9  A9
 848  A9  A9  AA  AA  AA  AA  AA  AB  AB  AB  AB  AB  AC  AC  AC  AC
 864  AC  AD  AD  AD  AD  AD  AE  AE  AE  AE  AE  AF  AF  AF  AF  AF
 880  B0  B0  B0  B0  B0  B1  B1  B1  B1  B1  B2  B2  B2  B2  B2  B3
 896  B3  B3  B3  B3  B4  B4  B4  B4  B4  B5  B5  B5  B5  B5  B6  B6
 912  B6  B6  B6  B7  B7  B7  B7  B7  B8  B8  B8  B8  B8  B9  B9  B9
 928  B9  B9  BA  BA  BA  BA  BA  BB  BB  BB  BB  BB  BC  BC  BC  BC
 944  BC  BD  BD  BD  BD  BD  BE  BE  BE  BE  BE  BF  BF  BF  BF  BF
 960  C0  C0  C0  C0  C0  C1  C1  C1  C1  C1  C2  C2  C2  C2  C2  C3
 976  C3  C3  C3  C3  C4  C4  C4  C4  C4  C5  C5  C5  C5  C5  C6  C6
 992  C6  C6  C6  C7  C7  C7  C7  C7  C8  C8  C8  C8  C8  C9  C9  C9
1008  C9  C9  CA  CA  CA  CA  CA  CB  CB  CB  CB  CB  CC  CC  CC  CC


---

# Schematics


This chapter contains the signal summary, the parts list,
the parts location diagram, and the schematics of the Sun color video board.


## Signal Summary


--------------------------------------------------------------------------------
Mnemonic	Description
--------------------------------------------------------------------------------

B.A0..B.A13	Latched version of Multibus address lines
B.D0..B.D7	Buffered version of Multibus data lines
BANK0..BANK2	Selects RAM bank zero through four
BBUS.A0		Multibus address bit 0. Can be inverted to select MC68000 byte order
BH0..BH9	Output of X-address registers
BL.D0..D7	Data lines to blue color lookup map
BLU_ALOG	Blue video output
BUS.A0..A19	Multibus address lines
BUS.AACK	UNUSED, Multibus advanced acknowledge
BUS.BCLK	UNUSED, Multibus bus clock
BUS.BHEN	UNUSED, Multibus byte high enable
BUS.BPRN	UNUSED, Multibus priority in
BUS.BPRO	UNUSED, Multibus priority out
BUS.BREQ	UNUSED, Multibus bus request
BUS.BUSY	UNUSED, Multibus busy
BUS.CBRQ	UNUSED, Multibus common bus request
BUS.CCLK	UNUSED, Multibus constant clock
BUS.D0..D15	Multibus data lines
BUS.INH1..2	UNUSED, Multibus inhibit lines
BUS.INIT	Multibus init
BUS.INT0..INT7	Multibus interrupt request
BUS.INTA	UNUSED Multibus interrupt acknowledge
BUS.IORC	UNUSED Multibus I/O read control
BUS.IOWC	UNUSED Multibus I/O write control
BUS.MRDC	Multibus memory read control
BUS.MWTC	Multibus memory write control
BUS.XACK	Multibus transfer acknowledge
BV1..BV8	Output of Y-address registers
BVODD		LSB from Y-address registers. Even or odd video frame
C.A0..C.A7	Address inputs to color map
CAS.0..CAS.4	Column Address Strobe to frame buffer memory
CAS1		Output from state machine used to generate CAS.0..CAS.4
CAS2		Output from state machine used to generate CAS.0..CAS.4
CAS2A		CAS2 delayed 42 nano-seconds
CLK		24MHZ output from crystal oscillator
CLK_HODD	Resets 74S74 at U13000 which toggles at half the horizontal line freq
CLK_VODD	Sets flip-flop which toggles after every vertical frame
CMAP		Request to access color map.
CMAP80 		Request to access color map. Delayed 80  nsec
CMAP160		Request to access color map. Delayed 160 nsec
CMSEL 		Request to access color map, but only active during video retrace.
COLORPL0..1	Output of status register. Selects one of four sets of color maps.
CP2		Clocks second level of buffers on frame buffer memory data output
CR_LOAD		Clock to load mask (color) register
CR_OE		Enables read-back of mask register
CREG0..CREG7	Mask register output
DAC_ON		When active, enables video signal generation
DI0..DI7	Data inputs to frame buffer memory
DISP_ON		Status register bit that can disable video output
DISPEN		Display enable. Signal aligned with start and end of valid pixels
DISPEN1		Used to generate DISPEN.
DISPEN2		Used to generate DISPEN.
DO0..DO39	Data Output of frame buffer memory.
DR_LOAD		Clock to load data register.
DREG0..DREG7	1030(2)   TOT	24.00	-2.60	1Q	74LS374	74LS374	CG4	B8
E.BL0..E.BL7	ECL data input to blue DAC.
E.DISP		ECL level that generates composite blanking video levels.
E.GR0..E.GR7	ECL data input to green DAC.
E.PU		ECL high value (approx. -1V)
E.RD0..E.RD7	ECL data input to red DAC.
E.SYSCP		ECL version of system clock.
FR_LOAD		Clock to load function register.
FR_OE 		Enables read-back of function register
FREG0..FREG7	Output of function register
GR.D0..GR.D7	Data lines to green color lookup map
GRN_ALOG	Green video output
H_TC		Terminal count from horizonal state machine
H0-H7		Horizontal state. 232-255 on video retrace, 0-127 on display.
HALF		True during the second half of each horizontal line
HALFWAY		Clock to set HALF
HINCR		Clock to increment horizontal state machine
HOLD_DS		Latch control for Multibus address lines
HRESET		Reset for horizontal state machine
HRESET25	HRESET delayed two gate times
INTEN		Interrupt enable
J0..J7		Temporary local signal name
K0..K7		Temporary local signal name
L0..L7		Temporary local signal name
M0..M5		Temporary local signal name
MEMSEL		Memory select
MREAD		Memory read
MWRITE		Memory write
N.HRESET	Connected to HRESET  except in multiple board color systems
N.STATE11	Connected to STATE11 except in multiple board color systems
N.SYSCP1	Connected to SYSCP1  except in multiple board color systems
N.VODD		Connected to VODD    except in multiple board color systems
N.VRESET	Connected to VRESET  except in multiple board color systems
N0..N4		Temporary local signal name
NEWREQ		New request from Multibus
NEWREQ20	NEWREQ delayed 20 nanoseconds
NEWREQ40	NEWREQ delayed 40 nanoseconds
OE1..OE5	Output enable multiplexors on pixel buffers
PAINT		Status bit enables writing five adjacent pixels with same data
PU		Pull-Up
PU1		Pull-Up
PU2		Pull-Up
PU3		Pull-Up
PU4		Pull-Up
PU5		Pull-Up
PU6		Pull-Up
R.A0..R.A7	Frame buffer memory address lines
RAM0..RAM7	Buffered frame buffer output, input to function unit
RAS.0..RAS.4	Row Address Strobe to frame buffer memory
RAS1		Used to generate RAS.0 .. RAS.4
RAS1A		RAS1 delayed 40 nanoseconds
RAS2		RAS1 delayed 60 nanoseconds
RC.A0..RC.A7	Inputs to line drivers for 64K RAM address lines
RD_BLU		Read from blue color map
RD_GRN		Read from green color map
RD_OE		Enable Read-back of buffered datum from frame buffer
RD_RAM		Clocks next datum to be read from frame buffer
RD_RED		Enable read of data from red color lookup map
RD.D0..RD.D7	Data lines to red color lookup map
RDCMAP		Enables color map read control signals only during video retrace
RED_ALOG	Red video output
REGSEL		Decoded address selects one of the registers
REGS		Decoded address selects one of registers. Enabled with NEWREQ20
REQ		Request pending
REQ80		Request delayed 80 nsec
RESET_H		Reset horizontal state machine
RESET_V		Reset vertical state machine
RMW		Selected address requires Read-Modify-Write cycle on frame buffer
RMW80		RMW delayed 80 nanoseconds
RWCMAP0-1	Selects which of four sets in color map to update
RWCMSEL		Read/Write color map select
SETREQ 		Sets REQ when Multibus read/write strobe goes inactive
SH0..SH3	Horizontal micro..state
SR_LOAD		Load status register
SR_OE		Enable read-back of status register
STATE11		Resets horizontal micro-state machine
SYNCH		RS-170A external sync signal
SYSCP		System clock. 82 nanosecond period
SYSCP1		Used to generate system clock
SYSCP2		Used to generate system clock
T.ACK		Temporary bus acknowledge signal
TVBLANK		Temporary video blanking signal
V1..V8		Vertical state
VBLANK		Video blanking signal
VCMAP0..VCMAP1	Selects which of four sets in color map to display
VCODE0..VCODE1	Vertical code. Zero implies vertical scan. One through three
		are used for sync signal generation.
VEE		-5.2 Volts
VINT		Vertical retrace interrupt
VODD		Even or Odd set of vertical lines
VODD1		Used to generate VODD
VRESET		Vertical state machine reset
VSYNCH		External Video Sync
WE		Frame buffer write enable
WE0..WE4	Write Enables for the five banks of 64K RAM in frame buffer
WE80		Frame buffer write enable delayed 80 nanoseconds
WE160		Frame buffer write enable delayed 160 nanoseconds
WR_BLU		Write enable for blue color lookup map
WR_GRN		Write enable for green color lookup map
WR_RED		Write enable for red color lookup map
X.RMW160	RMW request clocked just prior to period for frame buffer RMW
XDO0..XDO7	Output of frame buffer pixel buffer
XE0..XE4	Mux selects for bank of RAM operated on in RasterOp cycle
XH0..XH6	X-address value divided by 5
XLINOE		Selects CAS address during video memory cycles
XREGOE		Selects CAS address during RMW memory cycles
XREG		X-address register write select
XYH_OE		X and Y-address register high-byte read select
XYL_OE		X and Y-address register low-byte read select
Y.CAS		CAS signal before memory drivers
Y.RAS		RAS signal before memory drivers
YLINOE		Selects RAS address during video memory cycles
YREGOE		Selects RAS address during RMW memory cycles
YREG		Y-address register write select
Z.MREAD		Latched version of Multibus read strobe
Z.MWRITE	Latched version of Multibus write strobe


---

## Parts List


As an aid in specifying and ordering components, this parts list
translates diptypes into manufacturer names and manufacturer codes.
Only one manufacturer code is given, alternative sources
may be substituted. A manufacturer code of "ANY" is used
for generic parts with a large number of second sources.
Note that all fast parts in this list may be substituted with shottky parts.


```


--------------------------------------------------------------------------------
GENERIC	PINS SMIPART	QTY	MFC	MFPART		DESCRIPTION
--------------------------------------------------------------------------------

10124Q	16  100-1000      7	FAIR	10124Q		TTL TO ECL CONVERTER
2148	18  100-0002      6	INTEL	D2148H-3	1K-BY-4 STATIC RAM 45 NSEC
2952	24  100-0601      2	AMD	AM2952DC	EIGHT-BIT NON INVERTING I/O PORT
3625	18  100-1114      2	INTEL	3625		1K-BY-4 PROM, 55 NSEC
3628	24  100-1052      2	INTEL	3628		1K-BY-8 PROM, 70 NSEC
4164	16  510-0105     40	ANY	4164		64K-BY-1 DYN RAM 150 NSEC
7406	14  100-0009      1	TI	SN7406N		HEX BUFFER OPEN COLLECTOR
74F00	14  100-1008      3	FAST	74F00N		QUAD 2-INPUT NAND GATES
74F02	14  100-1009      1	FAST	74F02N		QUAD 2-INPUT NOR GATES
74F04	14  100-1010      1	FAST	74F04N		HEX INVERTERS
74F08	14  100-1011      1	FAST	74F08N		QUAD 2-INPUT AND GATES
74F112	14  100-1016      1	FAST	74F112N		DUAL DGE D-TYPE FLIPFLOP
74F138	16  100-1049      1	FAST	74F138N		1-TO-8 LINE DECODER
74F139	16  100-1012      2	FAST	74F139N		1-TO-8 LINE DECODER
74F163	16  100-1038      5	FAST	74F163N		BINARY 4-BIT COUNTER
74F240	20  100-1017      6	FAST	74F240N		OCTAL INVERTING BUFFER
74F244	20  100-1018      3	FAST	74F244N		OCTAL NONINVERTED BUFFERS
74F251	16  100-1019      8	FAST	74F251N		1-OF-8 DATA SELECTOR
74F257	16  100-1037      4	FAST	74F257N		QUAD DATA SELECTOR
74F32	14  100-1020      2	FAST	74F32N		QUAD 2-INPUT OR GATES
74F374	20  100-1021      4	FAST	74F374N		OCTAL REGISTER
74F533	20  100-1039      2	FAST	74F533N		OCTAL LATCH INVERTING
74F534	20  100-1036      1	FAST	74F534N		OCTAL REGISTER INVERTING
74F74	14  100-1022      4	FAST	74F74N		DUAL D-TYPE FLIPFLOP
74LS04	14  100-0010      1	TI	SN74LS04N	HEX INVERTER
74LS174	16  100-1048      1	TI	SN74LS174N	HEX D FLIPFLOP
74LS244	20  100-0015      2	TI	SN74LS244N	OCTAL NONINVERTED BUFFERS
74LS273	20  100-0064      1	TI	SN74LS273N	OCTAL D-TYPE FLIPFLOP
74LS374	20  100-0018     16	TI	SN74LS374N	OCTAL REGISTER
74LS670	16  100-0066      6	TI	SN74LS670N	4-BY4 REGISTER FILES
74S288	16  100-0029      3	TI	TBP18S030N	32-BY-8 BIPOLAR PROM
8303B	20  100-0036      1	AMD/NAT	DP8303N		OCTAL INVERTING TRANSCEIVER
AM2949	20  100-1033      3	AMD	AM2949PC	OCTAL BUFFER
DAC-805	18  100-1092      3	INTECH  VDAC-0805	8-BIT DAC, 100 MHZ, LATCHED.
K1114A	4   150-0042      1	MOTOROL	K1114A		XTAL OSCILLATOR. 23.485 MHZ
LS2521	20  100-0096      1	AMD	AM25LS2521	EIGHT-BIT EQUAL TO COMPARATOR
MTTLDL	14  150-1015      1	ECC	MTTLDL-50	DELAY LINE. 50 NSEC
R9.SIP	10  120-0078      5	BURNS	4310R-101-XXX	RESISTOR SIP, 1K OHM
J.4	4   130-0273      2	BERG	STICK, 4 PINS
J.10	10  130-0273      5	BERG	STICK, 10 PINS
J.12	12  130-0273      6	BERG	STICK, 16 PINS
C	2   110-0047    128	ANY	CAPACITOR	0.1 UFD CAP
K	2   110-0047     14	AVX	CAPACITOR	CAP 10 UF
X	2   110-0040      3	AVX			TANTALUM CAP 100 UFD

```


---

## Schematic GC1 (page 1 of 7)


---

## Schematic GC2 (page 2 of 7)


---

## Schematic GC3 (page 3 of 7)


---

## Schematic GC4 (page 4 of 7)


---

## Schematic GC5 (page 5 of 7)


---

## Schematic GC6 (page 6 of 7)


---

## Schematic GC7 (page 7 of 7)


---

## Parts Location Diagram


---

## Parts Location Listing


This section contains a cross listing of SUDS part locations, Koloa PC
Layout part locations, and actual board locations. All (x,y) board
locations are measured in tenths of inches from the component
side tooling hole in the
lower right corner (just above the multibus connector) to pin 1 of
the component in question.


UNUMBER	KOLOA LOC	XLOC	YLOC
------- ----- ---       ----    ----
    C1	I6E8		 86	 48
    C2	J0E8		 90	 48
    C3	J4E8		 94	 48
    C4	J8E8		 98	 48
    C5	K2E8		102	 48
    C6	K6E8		106	 48
    C7	L0E8		110	 48
    C8	L4E8		114	 48
    C9	I6D9		 86	 39
    K1	A4A4		  4	  4
    K2	A7A4		  7	  4
    K3	B0A4		 10	  4
    K4	G4A3		 64	  3
    K5	G7A3		 67	  3
    K6	F5C6		 55	 26
    K7	F3C6		 53	 26
    K8	C2B7		 22	 17
    K9	C4B7		 24	 17
    X1	C7F8		 27	 58
    X2	E3F8		 43	 58
    X3	F9F8		 59	 58
   C10	J0D9		 90	 39
   C11	J4D9		 94	 39
   C12	J8D9		 98	 39
   C13	K2D9		102	 39
   C14	K6D9		106	 39
   C15	L0D9		110	 39
   C16	L4D9		114	 39
   C17	I6D0		 86	 30
   C18	J0D0		 90	 30
   C19	J4D0		 94	 30
   C20	J8D0		 98	 30
   C21	K2D0		102	 30
   C22	K6D0		106	 30
   C23	L0D0		110	 30
   C24	L4D0		114	 30
   C25	I6C1		 86	 21
   C26	J0C1		 90	 21
   C27	J4C1		 94	 21
   C28	J8C1		 98	 21
   C29	K2C1		102	 21
   C30	K6C1		106	 21
   C31	L0C1		110	 21
   C32	L4C1		114	 21
   C33	I6B2		 86	 12
   C34	J0B2		 90	 12
   C35	J4B2		 94	 12
   C36	J8B2		 98	 12
   C37	K2B2		102	 12
   C38	K6B2		106	 12
   C39	L0B2		110	 12
   C40	L4B2		114	 12
   C41	I6A3		 86	  3
   C42	J0A3		 90	  3
   C43	J4A3		 94	  3
   C44	J8A3		 98	  3
   C45	K2A3		102	  3
   C46	K6A3		106	  3
   C47	L0A3		110	  3
   C48	L4A3		114	  3
   C49	I6F0		 86	 50
   C50	J0F0		 90	 50
   C51	J4F0		 94	 50
   C52	J8F0		 98	 50
   C53	K2F0		102	 50
   C54	K6F0		106	 50
   C55	L0F0		110	 50
   C56	L4F0		114	 50
   C57	I1E6		 81	 46
   C58	I1E2		 81	 42
   C59	I1D8		 81	 38
   C60	I1D4		 81	 34
   C61	I1D0		 81	 30
   C62	I1C6		 81	 26
   C63	I1C2		 81	 22
   C64	I1B8		 81	 18
   C65	I1B4		 81	 14
   C66	I1B0		 81	 10
   C67	I1A6		 81	  6
   C68	I2F7		 82	 57
   C69	H7G1		 77	 61
   C70	H3G1		 73	 61
   C71	G9G1		 69	 61
   C72	A9F5		  9	 55
   C73	A9F1		  9	 51
   C74	A9E6		  9	 46
   C75	A9E2		  9	 42
   C76	C0D3		 20	 33
   C77	C0C7		 20	 27
   C78	A9D3		  9	 33
   C79	A9C8		  9	 28
   C80	A9C4		  9	 24
   C81	A9C0		  9	 20
   C82	A9B6		  9	 16
   C83	B0B2		 10	 12
   C86	C1F0		 21	 50
   C87	C5F0		 25	 50
   C90	D7F0		 37	 50
   C91	E1F0		 41	 50
   C94	E9F0		 49	 50
   C95	F3F0		 53	 50
   C96	G5F0		 65	 50
   C97	G5D8		 65	 38
   C98	G5C6		 65	 26
   C99	G5B4		 65	 14
   K10	J3G1		 93	 61
   K11	J8G1		 98	 61
   K12	K4G1		104	 61
   K13	L0G1		110	 61
   K14	G1A3		 61	  3
  C100	G1B4		 61	 14
  C101	G1C6		 61	 26
  C102	F7C6		 57	 26
  C103	F6A7		 56	  7
  C104	E6A7		 46	  7
  C105	D4A7		 34	  7
  C106	D7E0		 37	 40
  C107	D7D6		 37	 36
  C108	D7D2		 37	 32
  C109	E2C9		 42	 29
  C110	C5D9		 25	 39
  C111	C0D9		 20	 39
  C112	B2D5		 12	 35
  C113	E4C4		 44	 24
  C114	E5C4		 45	 24
  C115	E9C4		 49	 24
  C201	B6G0		 16	 60
  C202	B3F0		 13	 50
  C203	B3E1		 13	 41
  C204	C5G2		 25	 62
  C205	C5F8		 25	 58
  C206	C5F4		 25	 54
  C207	C9G0		 29	 60
  C208	C9F0		 29	 50
  C209	C9E1		 29	 41
  C210	E1G2		 41	 62
  C211	E1F8		 41	 58
  C212	E1F4		 41	 54
  C213	E5E1		 45	 41
  C214	E5F0		 45	 50
  C215	E5G0		 45	 60
  C216	F7G2		 57	 62
  C217	F7F8		 57	 58
  C218	F7F4		 57	 54
  C219	I2G2		 82	 62
  U935	J0G2		 90	 62
 J2010	D0B7		 30	 17
 J2110	D0B4		 30	 14
 J2304	C2A5		 22	  5
 J2324	F9A5		 59	  5
 M1336	I6E7		 86	 47
 M1338	J0E7		 90	 47
 M1340	J4E7		 94	 47
 M1342	J8E7		 98	 47
 M1344	K2E7		102	 47
 M1346	K6E7		106	 47
 M1348	L0E7		110	 47
 M1350	L4E7		114	 47
 M1536	I6D8		 86	 38
 M1538	J0D8		 90	 38
 M1540	J4D8		 94	 38
 M1542	J8D8		 98	 38
 M1544	K2D8		102	 38
 M1546	K6D8		106	 38
 M1548	L0D8		110	 38
 M1550	L4D8		114	 38
 M1736	I6C9		 86	 29
 M1738	J0C9		 90	 29
 M1740	J4C9		 94	 29
 M1742	J8C9		 98	 29
 M1744	K2C9		102	 29
 M1746	K6C9		106	 29
 M1748	L0C9		110	 29
 M1750	L4C9		114	 29
 M1936	I6C0		 86	 20
 M1938	J0C0		 90	 20
 M1940	J4C0		 94	 20
 M1942	J8C0		 98	 20
 M1944	K2C0		102	 20
 M1946	K6C0		106	 20
 M1948	L0C0		110	 20
 M1950	L4C0		114	 20
 M2136	I6B1		 86	 11
 M2138	J0B1		 90	 11
 M2140	J4B1		 94	 11
 M2142	J8B1		 98	 11
 M2144	K2B1		102	 11
 M2146	K6B1		106	 11
 M2148	L0B1		110	 11
 M2150	L4B1		114	 11
 R1004	B7G1		 17	 61
 R1007	B5G2		 15	 62
 R1012	D3G1		 33	 61
 R1015	D1G2		 31	 62
 R1020	E9G1		 49	 61
 R1023	E7G2		 47	 62
 R1101	B1F4		 11	 54
 R1513	D8D9		 38	 39
 R2210	D1B2		 31	 12
 U1002	B3F9		 13	 59
 U1005	B8G3		 18	 63
 U1010	C9F9		 29	 59
 U1013	D4G3		 34	 63
 U1018	E5F9		 45	 59
 U1021	F0G3		 50	 63
 U1026	G1G1		 61	 61
 U1028	G5G1		 65	 61
 U1030	G9G0		 69	 60
 U1035	I2F6		 82	 56
 U1036	I6F8		 86	 58
 U1038	J0F8		 90	 58
 U1040	J4F8		 94	 58
 U1042	J8F8		 98	 58
 U1044	K2F8		102	 58
 U1046	K6F8		106	 58
 U1048	L0F8		110	 58
 U1050	L4F8		114	 58
 U1100	A8F9		  8	 59
 U1200	A8F5		  8	 55
 U1202	B3E9		 13	 49
 U1204	B7F0		 17	 50
 U1206	C1E9		 21	 49
 U1208	C5E9		 25	 49
 U1210	C9E9		 29	 49
 U1212	D3F0		 33	 50
 U1214	D7E9		 37	 49
 U1216	E1E9		 41	 49
 U1218	E5E9		 45	 49
 U1220	E9E9		 49	 49
 U1222	F3E9		 53	 49
 U1224	F7F0		 57	 50
 U1226	G1F0		 61	 50
 U1228	G5E9		 65	 49
 U1300	A8F1		  8	 51
 U1334	H9E6		 79	 46
 U1335	I2E5		 82	 45
 U1400	A8E6		  8	 46
 U1434	H9E2		 79	 42
 U1504	B8D9		 18	 39
 U1506	C1D9		 21	 39
 U1508	C5D8		 25	 38
 U1512	D6E0		 36	 40
 U1514	D9D9		 39	 39
 U1520	F0E0		 50	 40
 U1522	F1D9		 51	 39
 U1524	F8D9		 58	 39
 U1528	G5D7		 65	 37
 U1534	H9D8		 79	 38
 U1600	A8E2		  8	 42
 U1602	B2D4		 12	 34
 U1604	B6D5		 16	 35
 U1612	D6D6		 36	 36
 U1620	F0D6		 50	 36
 U1634	H9D4		 79	 34
 U1635	I2D4		 82	 34
 U1700	A9D7		  9	 37
 U1712	D6D2		 36	 32
 U1720	F0D2		 50	 32
 U1734	H9D0		 79	 30
 U1800	A8D3		  8	 33
 U1801	A8C8		  8	 28
 U1804	B9C7		 19	 27
 U1806	C1C8		 21	 28
 U1808	C5C8		 25	 28
 U1810	C9C7		 29	 27
 U1812	D3C7		 33	 27
 U1814	D7C7		 37	 27
 U1820	F0C8		 50	 28
 U1824	F7C5		 57	 25
 U1826	G1C5		 61	 25
 U1828	G5C5		 65	 25
 U1834	H9C6		 79	 26
 U1835	I2C3		 82	 23
 U1900	A8C4		  8	 24
 U1902	B2C1		 12	 21
 U1904	B7C2		 17	 22
 U1916	E1C3		 41	 23
 U1918	E5C3		 45	 23
 U1920	E9C3		 49	 23
 U1922	F3C3		 53	 23
 U1934	H9C2		 79	 22
 U2000	A8C0		  8	 20
 U2034	H9B8		 79	 18
 U2100	A8B6		  8	 16
 U2112	D3B6		 33	 16
 U2114	D7B6		 37	 16
 U2116	E1B5		 41	 15
 U2118	E5B5		 45	 15
 U2120	E9B5		 49	 15
 U2122	F3B5		 53	 15
 U2124	F7B4		 57	 14
 U2126	G1B3		 61	 13
 U2128	G5B3		 65	 13
 U2134	H9B4		 79	 14
 U2135	I2B2		 82	 12
 U2200	A9B2		  9	 12
 U2202	B3B3		 13	 13
 U2204	B7B3		 17	 13
 U2210	D1B1		 31	 11
 U2234	H9B0		 79	 10
 U2300	B1A8		 11	  8
 U2310	D3A7		 33	  7
 U2316	E5A7		 45	  7
 U2322	F5A7		 55	  7
 U2334	H9A6		 79	  6
 V1032	H3G0		 73	 60
 V1034	H7G0		 77	 60


---

## PC Padmaster/Soldermask


---

## PC Layout Layer 1 (Page 1 of 6)


---

## PC Layout Layer 2 (Page 2 of 6)


---

## PC Layout Layer 3 (Page 3 of 6)


---

## PC Layout Layer 4 (Page 4 of 6)


---

## PC Layout Layer 5 (Page 5 of 6)


---

## PC Layout Layer 6 (Page 6 of 6)


---

# Wirelist


This chapter contains the wirelist for the Rev A Sun color video board.
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
