---


---


# Sun-2 Video Board


# Engineering Manual


SUN MICROSYSTEMS INC.

[date]


>
**Trade Secret Notice**

This document contains unpublished, proprietary information
and describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied
or duplicated in any form without the prior written consent of
SUN MICROSYSTEMS INC.


---


---

# Principles of Operation


## Introduction


This chapter describes the theory of operation of the Sun-2 Video Board.
The discussion assumes that the reader is familiar with the architecture,
the installation, and the programming of the Sun-2 Video Board.
In addition, the discussion assumes that the reader has a working knowledge
of digital electronics and has access to descriptions of the components
used on the board.

The following sections illustrate the conventions
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
For example, all P1.Bus signals start with the prefix "P1.".

Connector signals are distinguished by a suffix of "[]" with an
optional string enclosed inside the square brackets identifying
the connector name.

Clock signals are labelled either according to their function or according
to their timing.
Clock signals with a suffix of the form (#1.#2-#3) are periodic clocks that
have a clock period of #1 nanoseconds with an active clock phase from
#2 to #3.

---

## Schematic Conventions: Components


Components in the schematics are identified by Component Name
(also referred to as Body Name in the wirelist).
Components are named according to "generic" or industry standard names.
Logic components are typically drawn according to their function instead
of normal form.
Those components that are used in the logical inverse of their normal form,
such as inverted-input gates, are identified by a name followed
by a backslash (e.g. 74LS00\).

Each component carries a label or designator.
Lables consist of one letter followed by one to four digits.
The letter indicates the type of component and is one of:


```

Letter	Component Type
--------------------------------
C	Standard Capacitor
K	Electrolytic Capacitor
X	Decoupling Capacitor
J       Jumper or Connector
R       Resistor
S       single-in-line component
U       dual-in-line component

```


Component names (Body Names) are translated into Diptypes that specify
the physical component associated with the component name.
There is only one diptype for components that are sections
of the same physical package (e.g. gates of a 74LS00 diptype).

Location labels are cross-indexed in the wirelist
into diptype and component names and locations on the schematics.
Diptypes are translated by the parts list
into manufacturer codes and part names.
In this document, section numbers are identified by a dash-number
following the location label with dash-numbers enumerated
starting at 0.


## Schematic Conventions: Programmable Logic


Programmable logic components, such as PALs and PROMs, are described
in a high-level functional language from which they are translated
automatically into the bitpatterns for programming.

Programmable logic elements are identified by name.
The source code for the programmable logic elements is included
in chapter 5 of this manual.

---

## Power


The Sun-2 video board uses a single 5 Volt power supply. The maximum current
requirement is 4 Amp.


## Initialization


The 796-Bus Init signal `P1.INIT\` resets the video control register
`74LS273:U224, 74LS273:U234` to all 0's.
This disables the video enable `V.VEN`, interrupt enable `V.INTEN`,
and copy enable `V.COPY`.
The negated interrupt enable signal `V.INTEN` also clears any pending
video interrupts `V.VINT` in the interrupt flipflop `74LS74:U223`.


## Clock Generation


All on-board clocks related to the video are derived from the
100 MHz crystal oscillator `K1114A:U418`. Clocks related to the
synchronous communication controller are derived from 19.6608 MHz
cyrstal oscillator `K1114A:U417` in conjunction with counter/divider
`74LS393:U416-1`.

The 10 nsec clock `V.C(10.5-0)` is buffered by AND-Gate `74F08:U406-1`.
The buffered clock directly drives the video shift register `74F194:U409`
and the divider `74F74:U407` which generates the
20 nsec clock `V.C(20.0-10)` and the 40 nsec clock `V.C(40.0-20)`.

Clocks `V.C(40.20-0)` and `V.C(20.10-0)` are ANDed in gate `74F08:U406-0`
and are delayed by gate `74F08:U406-3` to generate signal `V.SLOAD`
which controls loading of the video shift register `74F194:U409`.
The timing diagram below shows the timing relation of these signals,
including typical signal skew.


```

------------------------------------------------------------------------

V.C(10.0-5)	____----____----____----____----____----____----____----

V.C(20.0-10)	________--------________--------________--------________

V.C(40.0-20)	____________----------------________________------------

V.SLOAD		____________________________________--------____________


```


---

## Memory Controller


The memory controller state machine generates the timing for the memory
and other basic timing strobes for the video board.
It consists of PROMs `74S288:U400, 74S288:U402, 74S288:U404`
and latches `74F374:U401, 74F374:U403, and 74F374:U405`.
The state machine is clocked with `V.C(40.0-20)`.

The memory controller has a total of 16 states, enumerated 0 through 15,
that are continuously executed in sequence. Each state has a duration of 40 nsec,
thus a full 16 state cycle repeats every 640 nsec.

The memory controller alternates between processor cycles and video refresh cycles.
The first nine states, state 0 through 8,
execute a processor cycle if signal `XREQ=1`
and they execute an idle cycle if signal `XREQ=0`.
States 9 through 15 always execute a video refresh cycle.

A processor cycle is executed if the synchronous request signal `V.XREQ`
is active (the generation of `V.XREQ` is described below under request logic).
During a processor cycle, signals `V.PRA` and `V.PCA` enable the
processor row and column address from the processor address latches
`74F374:U330` and `74F374:U332`, respectively,
in time for `V.RAS` and `V.CAS`, the row and column address strobe.
The RAM Write Enable signal `V.W\` is asserted starting at state 2
for early write-cycle timing. However, RAMs are only written into if
enabled by decoders `74LS138:U106` and `74LS138:U107`.
These decoders generate a write strobe during `V.W\`
if the respective external write strobe `V.XWEL` or `V.XWEU` is present
and for the device(s) selected by address `V.XA01, V.XA02, and V.XA19`.

If no external write strobes are pending, then a read cycle is executed.
On a read cycle, the word addressed by `V.XA01` and `V.XA02`
is enabled via decoder `74LS138:U106` to pass through one pair of
data bus buffrs `AM2949:U200-U207`
and is latched into the data output register `74F374:U221, U231`
at the rising edge of signal `V.WEBUF\` at the end of state 8.
At the same time, the parity generator `82S62:U222, U232`
generates byte parity for the data word read.
The parity generated is latched into the parity latch `74F374:U223`.

During a video refresh cycle, signals `V.PRA` and `V.PCA` enable the
video row and column address contained in counters `74LS461:U331`
and `74LS461:U333`.
The data at the video address is read out 64-bits in parallel and
is latched at the end of state 15 in the video data register (74LS374:U300-U307).

During all 16 states, the memory controller output enables consecutive
bytes from the video data register onto video output bus `V.O0-V.O7`
via control lines `V.OE0\-V.OE7\`.
Starting with `V.OE0\` in state 0, one byte from
the video data register is enabled every two states.
The video output bus feeds multiplexor `74F258:U408`
which is controlled by signal `V.STATE0` to select one nibble at a time
for loading into shift register `74F194:U409`.


---

## Memory Controller Timing Diagram


```


XREQ=0
------------------------------------------------------------------------
State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
------------------------------------------------------------------------
VOE	0       1       2       3	4       5       6       7

Clock	--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__

RAS\	--------------------------------------------____________________

CAS\	----------------------------------------------------____________

OEVRA\	--------------------------------________________----------------

OEVCA\	------------------------------------------------________________

OEPRA\	----------------------------------------------------------------

OEPCA\	----------------------------------------------------------------

G\	----------------------------------------------------____________

W\	----------------------------------------------------------------

HCLK\	----____--------------------------------------------------------

ENREQ	--------____________________________________________________----

XREQ=1
------------------------------------------------------------------------
State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
------------------------------------------------------------------------
VOE	0       1       2       3	4       5       6       7

Clock	--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__

RAS\	------------____________________------------____________________

CAS\	--------------------________________----------------____________

OEVRA\	--------------------------------________________----------------

OEVCA\	------------------------------------------------________________

OEPRA\	________________------------------------------------------------

OEPCA\	----------------________________--------------------------------

G\	--------------------________________----------------____________

W\	--------____________________________----------------------------

WEBUF\	--------------------------------____----------------------------

ACK\	------------------------____________----------------------------

HCLK\	----____--------------------------------------------------------

ENREQ	------------------------------------_______________________----

;

```


---

## Video Controller


The video controller generates the timing for the video monitor.
The following description applies to the "standard Sun-2 video monitor".
This video monitor has the following attributes:


```

    Visible Display	1152 pixels by 900 lines
    Video Clock:	10 nsec		100 MHz
    Horizontal Cycle:	15.36 usec    	65.10 kHz
    Vertical Cycle:	14376 usec	69.56 Hz
    Horizontal Retrace:	3.84 usec
    Vertical Retrace:	552 usec

```


Video controller latch `74F374:U413` latches the outputs of
horizontal and vertical decoding PROM on the rising edge of `V.HCLK`.


## Horizontal State Machine


Horizontal counter `74LS393:U411` is advanced every 640 nsec with the
falling edge of clock `V.HCLK`.
Horizontal counter is reset with `V.HRESET` generated by video controller latch.

Horizontal decode PROM inputs are horizontal counter states V.H0 through V.H6,
plus VSYNC\ and VBLANK from the vertical state machine.
Horizontal decode PROM outputs are V.HRESET, V.HSYNC, V.DISPEN, and V.VCLK.
The horizontal decode PROM function is defined in PROM V0.


## Vertical State Machine


Vertical counter `74LS393:U414 and 74LS393:U416` is advanced on falling
edge of clock `V.VCLK`.
Vertical counter is reset with `V.VRESET` from video controller latch.

Vertical decode PROM `3622:U415` decodes vertical counter states
`V.VSTATE0 through 7` plus the AND of `V.VSTATE8 and V.VSTATE9`.
Vertical decode PROM outputs are V.VSYNC, V.RESET\, V.VBLANK, and V.RESET\.
The vertical decode PROM function is defined in PROM V1.

---

## Horizontal State Machine


```

Signal	State

STATE+1	0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 2 2 2 2
	0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3

HCLK 	-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

DISPEN	------------------------------------____________

HSYNC	____________________________________--------____

HRESET	--______________________________________________

VCLOCK	________________________________________--______


```


## Vertical State Machine


```

Signal	State

STATE+1	0 0 0 0 0 0 0 0 ... 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 ... 9 9 9 9
	0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 ... 3 3 3 3
	0 1 2 3 4 5 6 7 ... 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 ... 1 2 3 4

VCLK	-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

VBLANK	____________________--------------------------------------------

VSYNC	________________________--------------------____________________

VRESET	______________________________________________________________--


```


---

## Address Paths


The video memory on the board, chips `4416:U311-U318, U321-U328`,
is dual ported for processor access and video refresh.
The processor address is stored in register `74LS374:U320`
for the video memory row-address and in register `74LS374:U322`
for the column address.
The video refresh address is stored in counters `74LS491:U331`
and `74LS491:U333` for row and column address, respectively.
Notice that the organization of the 4416 RAM chips require
an 8-bit row address and a 6-bit column address.
Address lines `V.A7` and `V.A0` are not used during the column access.

The video refresh counters are incremented during every 640 nsec
cycle with the rising edge of `V.STATE3` except during states
without display enable. They are reset to 0 when `V.DISPEN`
is inactive and `V.RESET\` is active during a rising clock edge.


## P2-Bus Interface Logic


Major components of the P2-Bus Interface Logic are
Address Decoding, Request Generation, and Interrupt Logic.


### P2-Bus Address Interface


The Sun P2-Bus features multiplexed address lines for the
low-order address bits. Latches `74F374:U100` and `74F374:U101`
latch the multiplexed row and column address, respectively,
to make the demultiplexed address available on the board.

The three most significant address bits, `P2.A20, P2.A21, and P2.A22`
are decoded with chip `74F138:U104` and switch `DIPSW:U106`
to produce the signal `BOARDSEL\`. The decoding is on 1 Megabyte
boudaries as follows:


```

BASE	SWITCH
--------------
0M	1
1M	2
2M	3
3M	4
4M	5
5M	6
6M	7
7M	8
--------------

```


Only one of the eight address switches must be closed at any one time.

A separate path for selecting the video board exists by means
of the address comparator `LS2521:U109` and the video base
register `74LS273:U224,U234`.
When the value of address bits `P2.A17` through `P2.A22`
matches the value of `V.BASE1` through `V.BASE6` while
`P2.CAS\` and `P2.RAS\` are asserted
then the output of the comparator generates
signal `V.CSEL\` .


### P2-Bus Read/Write Cycles


The video board implements buffered write cycles and unbuffered reads.
Reads follow the traditional conventions of memory systems.
When the processor reads from the video board,
the video board performs the desired access and returns the data read
to the processor. Since the memory on the video board is dual-ported
and asynchronous to the processor, the processor will have to wait
until the read data is available. This is implemented by the video
board asserting the `P2.WAIT` signal until the read data is available.

Write cycles, on the other hand, are buffered.
The video board provides a set of registers that store all information
related to a write cycle, effectively implementing a 1-deep FIFO.
On a write cycle, the processor thus needs not to wait until the
dual-ported video memory is available. Rather, the write cycle
is automatically completed with the data stored in the registers.
However, a second write cycle can only be initiated when the
current write cycle has been completed.
This is done by the video board asserting
the `P2.WAIT` signal if a write cycle to the video board is attempted
while a previous request is still in progress.

An interesting case occurs if a write cycle is immediately
followed by a read cycle. In this case, the write cycle is
still in progress while the new read cycle is pending.
The design of the request logic assures that the read cycle
is only begun after the write cycle has been completed.


### P2-Bus Request Interface


The P2-Bus request logic consists of flipflops `74F74:U110`
and synchronizer `74F74:U111`.
Write requests, identified by signal `V.WE` asserted,
are latched at the trailing edge of `V.SEL\`.
Read requests, identified by signal `P2.R/W\` active,
are latched at the trailing edge of `XRAS` in anticipation
of a potential read cycle.
The read request signal `V.RREQ` is then and-ed with `BOARDSEL`
in gate `74F00:U119-0` to indicate a valid read request.
Valid read request is or-ed with write request signal `V.WREQ`
in gate `74F00:U119-1` to produce read/write request.
Purpose of AND gate `74F08:U410-3` is to inhibit the request
signal `V.REQ` when a previous request is acknowledged via
signal `V.ACK\`. This generates a new edge on `V.REQ`
if a write request and a read-request overlap as can happen
if a write is immediately followed by a read.

`V.REQ` latches the demultiplexed processor address
into the processor address register `74F374:U330, U332`.
It also latches the low-order address bits `A01,A02`,
the register select address bits `A11,A12`,
the IO/Memory select bit `IO/M\`,
and the write enable bits `V.WE, V.WEL, V.WEU`
into register `74F374:U113`.

`V.REQ` is sampled at the rising edge of `V.ENREQ` with flipflop
`74F74:U111-0`. The sampled signal is reclocked on the next clock edge
in flipflop `74F74:U111-1` and turns into signal `V.XREQ`
that controls the memory state machine.

`V.WREQ` and `V.RREQ` are ored together with gate `74F32:U114-1`
to generate `V.WAIT` which drives `P2.WAIT` via tri-state driver
`74F240:U102`. WAIT is asserted while the video board is selected
via signal `V.SEL\` and read request or write request are pending.


### P2-Bus Interrupt Logic


Interrupt flipflop (74LS74:U233) is set at the leading edge
of `V.VBLANK` as long as interupt enable `V.INTEN` is enabled.
`V.INT` is driven to the P1-Bus via open collector driver
`7407:U115-0` and jumper select `J.16:U116`.

---

# PROMs


## Introduction


This chapter contains the source files and object files for the
programmable read-only memories on the board.
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

The PROM source code is followed by the generated
hexadecimal object code which also includes a 16-bit checksum.

---

## PROM V0, Sourcecode


```

begin "v0"

comment	This information proprietary to Sun Microsystems Inc

1 state = 64 pixel, 1 pixel = 10 nsec

	    Range	Length	Length	Time
	    [State]	[State]	[Pixel]	[usec]
------------------------------------------------------------
cycle	    00..23	24	1536	15.36
visible	    00..17	18	1152	11.52
invisble    18..23	6	384	3.84
frontporch  18..18	0	0	0
hsync	    18..21	4	256	2.56
backporch   22..23	2	128	1.28
------------------------------------------------------------

;
require "prom.sai" source!file;
$512;

define

h0	=[a0],
h1	=[a1],
h2	=[a2],
h3	=[a3],
h4	=[a4],
h5	=[a5],
h6	=[a6],
h7	=[a7],
vblank	=[a8],

state	=[(h0*d0 + h1*d1 + h2*d2 + h3*d3 + h4*d4 + h5*d5 + h6*d6 + h7*d7)],
nstate	=[((state + 1) MOD 24)],

dispen	=[(¬vblank ∧ (0≤nstate≤17))],
hsync	=[(18≤nstate≤21)],
hreset	=[(nstate = 0)],
vclock	=[(nstate = 20)];

prombegin

prom(0,d0,	hsync);
prom(0,d1,	dispen);
prom(0,d2,	vclock);
prom(0,d3,	hreset);

promend;
writeprom("v0",0);
end "v0";

```


---

## PROM V0, Objectcode


```

:1000000002020202020202020202020202020202D0
:10001000020101050100000A0202020202020202BC
:100020000202020202020202020101050100000AAC
:1000300002020202020202020202020202020202A0
:10004000020101050100000A02020202020202028C
:100050000202020202020202020101050100000A7C
:100060000202020202020202020202020202020270
:10007000020101050100000A02020202020202025C
:100080000202020202020202020101050100000A4C
:100090000202020202020202020202020202020240
:1000A000020101050100000A02020202020202022C
:1000B0000202020202020202020101050100000A1C
:1000C0000202020202020202020202020202020210
:1000D000020101050100000A0202020202020202FC
:1000E0000202020202020202020101050100000AEC
:1000F00002020202020202020202020202020202E0
:1001000000000000000000000000000000000000EF
:1001100000010105010000080000000000000000CF
:1001200000000000000000000001010501000008BF
:1001300000000000000000000000000000000000BF
:10014000000101050100000800000000000000009F
:10015000000000000000000000010105010000088F
:10016000000000000000000000000000000000008F
:10017000000101050100000800000000000000006F
:10018000000000000000000000010105010000085F
:10019000000000000000000000000000000000005F
:1001A000000101050100000800000000000000003F
:1001B000000000000000000000010105010000082F
:1001C000000000000000000000000000000000002F
:1001D000000101050100000800000000000000000F
:1001E00000000000000000000001010501000008FF
:1001F00000000000000000000000000000000000FF
:0000000000
PROM 	v0	Checksum 	02C8


```


---

## PROM V1, Sourcecode


```

begin "v1"

comment	This information proprietary to Sun Microsystems Inc.

1 states = 1 line = 15.36 usec		65.10 kHz

	    Range	Length	Time
	    [Lines]	[Lines]	[usec]
------------------------------------------------------------
cycle	    000..935	936	14376	69.56 Hz
visible	    000..899	900	13824
invisble    900..935	36	552
frontporch  900..900	0	0
vsync	    900..909	10	154
backporch   910..935	23	384
------------------------------------------------------------
;
require "prom.sai" source!file;
$512;

define

v0	=[a0],
v1	=[a1],
v2	=[a2],
v3	=[a3],
v4	=[a4],
v5	=[a5],
v6	=[a6],
v7	=[a7],
v89	=[a8],

line	=[(v0*d0 + v1*d1 + v2*d2 + v3*d3 + v4*d4
	 + v5*d5 + v6*d6 + v7*d7 + v89*d8 + v89*d9)],

vsync	=[(900≤line≤909)],
reset	=[(line = 935)],
vblank	=[(line ≥ 900)],
vreset	=[(line = 935)];

prombegin

prom(0,d0,	vsync);
prom(0,d1,	¬reset);
prom(0,d2,	vblank);
prom(0,d3,	vreset);

promend;
writeprom("v1",0);
end "v1";

```


---

## PROM V1, Objectcode


```

:1000000002020202020202020202020202020202D0
:1000100002020202020202020202020202020202C0
:1000200002020202020202020202020202020202B0
:1000300002020202020202020202020202020202A0
:100040000202020202020202020202020202020290
:100050000202020202020202020202020202020280
:100060000202020202020202020202020202020270
:100070000202020202020202020202020202020260
:100080000202020202020202020202020202020250
:100090000202020202020202020202020202020240
:1000A0000202020202020202020202020202020230
:1000B0000202020202020202020202020202020220
:1000C0000202020202020202020202020202020210
:1000D0000202020202020202020202020202020200
:1000E00002020202020202020202020202020202F0
:1000F00002020202020202020202020202020202E0
:1001000002020202020202020202020202020202CF
:1001100002020202020202020202020202020202BF
:1001200002020202020202020202020202020202AF
:10013000020202020202020202020202020202029F
:10014000020202020202020202020202020202028F
:10015000020202020202020202020202020202027F
:10016000020202020202020202020202020202026F
:10017000020202020202020202020202020202025F
:100180000202020207070707070707070707060615
:1001900006060606060606060606060606060606FF
:1001A000060606060606060C0606060606060606E9
:1001B00006060606060606060606060606060606DF
:1001C00006060606060606060606060606060606CF
:1001D00006060606060606060606060606060606BF
:1001E00006060606060606060606060606060606AF
:1001F000060606060606060606060606060606069F
:0000000000
PROM 	v1	Checksum 	0600


```


---

## PROM V2, Sourcecode


```

begin "v2"

require "prom.sai" source!file;
$32;

define

state0	=[a0], state1	=[a1], state2	=[a2], state3	=[a3],
xreq	=[a4],

state	=[(state0*d0 + state1*d1 + state2*d2 + state3*d3)],
nstate	=[((state + 1) MOD 16)],
pra	=[(xreq ∧ (0≤nstate≤3))],
pca	=[(xreq ∧ (4≤nstate≤7))],
vra	=[(8≤nstate≤11)],
vca	=[(12≤nstate≤15)],
voe(n)	=[((nstate DIV 2 )=n)],
ras	=[(xreq ∧ (3≤nstate≤7) ∨ (11≤nstate≤15))],
cas	=[(xreq ∧ (5≤nstate≤8) ∨ (13≤nstate≤15))],
g	=[(xreq ∧ (5≤nstate≤8) ∨ (13≤nstate≤15))],
webuf	=[(xreq ∧ (nstate=8))],
w	=[(xreq ∧ (2≤nstate≤8))],
hclk	=[(nstate=1)],
enreq	=[(nstate=15 ∨ (0≤nstate≤1) ∨ xreq ∧ (2≤nstate≤8))],
ack	=[(xreq ∧ (6≤nstate≤8))];

prombegin

prom(0,d0,	nstate LAND d0);
prom(0,d1,	nstate LAND d1);
prom(0,d2,	nstate LAND d2);
prom(0,d3,	nstate LAND d3);
prom(0,d4,	¬pra);
prom(0,d5,	¬pca);
prom(0,d6,	¬vra);
prom(0,d7,	¬vca);

prom(1,d0,	¬voe(6));
prom(1,d1,	¬voe(7));
prom(1,d2,	¬voe(4));
prom(1,d3,	¬voe(5));
prom(1,d4,	¬voe(2));
prom(1,d5,	¬voe(3));
prom(1,d6,	¬voe(0));
prom(1,d7,	¬voe(1));

prom(2,d0,	¬ras);
prom(2,d1,	¬cas);
prom(2,d2,	¬g);
prom(2,d3,	¬w);
prom(2,d4,	hclk);
prom(2,d5,	¬webuf);
prom(2,d6,	enreq);
prom(2,d7,	¬ack);

promend;

writeprom("v20",0); writeprom("v21",1); writeprom("v22",2);

end "v2"

```


---

## PROM V2, Objectcode


```


:10000000F1F2F3F4F5F6F7B8B9BABB7C7D7E7FF078
:10001000E1E2E3D4D5D6D7B8B9BABB7C7D7E7FE028
:0000000000
PROM 	v20	Checksum 	1830

:10000000BF7F7FEFEFDFDFFBFBF7F7FEFEFDFDBFFE
:10001000BF7F7FEFEFDFDFFBFBF7F7FEFEFDFDBFEE
:0000000000
PROM 	v21	Checksum 	1BE4

:10000000FFAFAFAFAFAFAFAFAFAFAEAEA8A8E8EF47
:10001000FFE7E6E6E0606041AFAFAEAEA8A8E8EF6C
:0000000000
PROM 	v22	Checksum 	171D


```


---

# Signal Summary


The signal summary describes the meaning of the signal present in the schematics.
Signal names are shown active high, and signal vectors are combined into
a single name.


--------------------------------------------------------------------------------
Mnemonic	Description
--------------------------------------------------------------------------------

A01..16		On-board Word Address
AREADY		Audio Chip Ready
BOARDSEL	Board Select
C50		Clock 19.6608 MHz
D00..15		On-board Data Bus
P1.INIT		796-Bus INIT
P1.INT0..7	796-Bus Interrupt Levels
P2.A00..22	P2-Bus Addresses
P2.CAS		P2-Bus Column-Address Strove
P2.DI00..15	P2-Bu Data In
P2.DIL		P2-Bus Parity In Lower
P2.DIU		P2-Bus Parity In Upper
P2.DO00..15	P2-Bus Data Out
P2.DOL		P2-Bus Parity Out Lower
P2.DOU		P2-Bus Parity Out Uper
P2.R/W		P2-Bus Read/Write\
P2.RAS		P2-Bus Row-Address Strobe
P2.WAIT		P2-Bus Wait
P2.WEL		P2-Bus Write Enable Lower
P2.WEU		P2-Bus Write Enable Upper
R/W\		Read/Write\
RXD0		Receive Data 0
RXD1		Receive Data 1
TXD0		Transmit Data 0
TXD1		Transmit Data 1
V.A0..7		Video Memory Address
V.ACK		Request Acknowledge
V.AUDIO		Audio Output
V.BASE0..11	Base Value
V.C(10.5-0)	Video Clock (100 MHz)
V.CAS		Video Memory Column Address Strobe
V.COPY		Video Memory Copy Bit
V.CSEL		Video Copy Select
V.D00..63	Video Data Bus (64 Bits)
V.DISPEN	Video Display Enable
V.DOL		Video Parity Out Lower
V.DOU		Video Parity Out Upper
V.ENREQ		Video Enable Request
V.G		Video Memory G Enable
V.H		Video Pullup
V.H0..3		Video Horizontal PROM outputs
V.HCLK		Video Horizontal Clock
V.HRESET	Video Horizontal Reset
V.HSTATE0..7	Video Horizontal State
V.HSYNC		Video Horizontal Sync
V.INTEN		Video Interrupt Enable
V.IO/M\		Video Input-Output/Memory
V.O0..7		Video Output Data
V.OX0..3	Video Output Multiplexed
V.OE0..3	Video Output Enable
V.PCA		Video Processor Column Address
V.PRA		Video Processor Row Address
V.RAS		Video Row Address Strobe
V.RD.CTRL	Video Read Control Register
V.RD.SCC	Video Read Serial Communic. Controller
V.REQ		Video Request
V.RESET		Video Reset Counter
V.RREQ		Video Read Request
V.SEL		Video Select
V.SINT		Video Serial Interrupt
V.SRLOAD	Video Shift Register Load
V.STATE0..3	Video State
V.V0..3		Video Vertical PROM outputs
V.VBLANK	Video Vertical Blanking
V.VCA		Video Video Column Address
V.VCLK		Vertical Clock
V.VEN		Video Enable
V.VIDEO		Video Signal
V.VINT		Video Interrupt
V.VOE0..7	Video Output Enable
V.VRA		Video Row Address
V.VRESET	Vertical Reset
V.VSTATE0..7	Vertical State
V.VSYNC		Vertical Sync
V.WE		Write Enable
V.WEBUF		Write Enable Buffer
V.WEL		Write Enable Lower
V.WEU		Write Enable Upper
V.WL.CTRL	Write Lower Control Register
V.WL0..3	Write Lower Bytes
V.WREQ		Write Request
V.WU.AUDIO	Write Upper Audio
V.WU.CTRL	Write Upper Control Register
V.WU.SCC	Write Upper Serial Comm. Control
V.WU0..3	Write Upper Bytes
V.W		Write Strobe
V.XREQ		Synchronized Request
V.XWEL		Synchronized Write Enable Lower
V.XWEU		Synchronized Write Enable Upper
V.XA01..4	Synchronized Address
V.XA19		Synchronized Address
XCAS		External Column Address Strobe
XRAS		External Row Address Strobe


---

# Schematics


The schematics is contained in the file with extension ".PRE".

Whenever possible, standard drawing conventions are employed.
Signal flow is shown from left to right, and top to bottom.
Connected Sections of the design are logically grouped together,
as much as the available space allowed.

Component identifiers are chosen to reflect the location on the
schematics in the first digit.
For example, component U100 is most likely positioned on page 1.

Schematics file names are chosen to reflect the drawing page number.


# Silkscreen and Printed Circuit Board Layout


This chapter shows copies of the printed circuit layout and
silkscreen data.

---

# Parts List


The partslist is contained in the file with extension ".PRT".
This list is organized under the following heading:


```


PART NUMBER	DIPTYPE		COUNT	DESCRIPTION				LOCATIONS


```


*Partnumber* is not used.

*Diptype* is the generic component name.

*Count* is the number of times the component is used on the board.

*Description* are properties attached to the component to fully specify it.

*Locations* are the labels where the component is used.

---

# Wirelist


The wirelist is contained in the file with extension ".WL".
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


---

# Wirelist Summary


The wirelist is contained in the file with extension ".WLS".
The wirelist is comprised of the following sections which are
distinguished by the header lines on each page.


#### Component Summary


The Component Summary lists the DIPTYPE, the BODY NAME,
the number of sections, DIPS, and spare sections with and without location,
and the estimated power consumption.


```

DIPTYPE	BODY NAME	# SECTION	TOTAL DIPS	#SPARE SECTIONS	  MA  V

```


This listing ends with the total chip count and the total current of the design.


#### Runs With No Output


This section contains those signals that are not connected to an output pin.
These signals include connector signals, unused inputs, signals connected
to jumpers (that are not being driven), and signals connected to special
components that do not have standard output/input types.


#### Runs Which Are Overloaded


These signals, as the name implies, are not driven sufficiently
for the total input current connected.


#### Runs With No Inputs


These signals do not have inputs connected to them.
They are typically unused outputs or connector outputs.


#### Unused Extra Outputs


These signals are outputs that are not tristated and
without any connections. Similar to previous category.


#### Runs With No Inputs Or Outputs


These are signals with neither outputs or inputs
connected to them. They include unused connector pins, comments, etc.


#### Runs With Wire-Or Warning


These signals have multiple outputs connected to them, including
signals terminated with pullups and inactive tri-state outputs.

---

# Silkscreen and Printed Circuit Board Layout


This chapter shows the printed circuit layout and silkscreen layout.
