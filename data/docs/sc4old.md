---


---


# Sun-2 Color Video Board


# Engineering Manual


Sun Microsystems Inc.

July 1983

Rev A


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


This chapter describes the operation of the Sun-2 color video board
from a hardware perspective. This manual is intended for those people
who must debug the hardware and it steps through the functional areas
of the board in the same order that a technician might.

This manual assumes the reader is loosely familiar with the architecture
and programming of the Sun-2 color board; if not, the reader should first
peruse the Sun-2 Color Graphics Board User Manual. This manual further
assumes that data sheets of all relevant components are available for
reference.

The Sun-2 color board combines both transistor-transistor-logic (TTL)
and emitter-coupled-logic (ECL). As many hardware types are unfamiliar
with ECL logic, these people should first obtain an ECL data book to
familiarize themselves with ECL logic levels and the ECL components
used on this board. All ECL nets on the board are given a common prefix
or a common form to help delineate the borders between the TTL and ECL
circuitry. These schematic conventions are discussed in the next section
to help familiarize the reader with the Sun-2 color schematics before
the dissection of these diagrams begins.

This chapter (Chapter 4) is intended to aid step by step debugging of
faulty hardware. The first section of Chapter 4 provides some
information on schematic conventions and the succeeding sections
Chapters 5 through 7 are primarily for reference.
Chapter 5 documents the programmable logic; chapter 6 includes the
complete set of electrical schematics; and chapter 7 consists of a
complete wirelist of the board (power and ground nets not included).


## Schematic Conventions


### Signal Names


When possible, the schematics were drawn to standard drafting conventions
with input signal entering from the left and output signals exiting to the right.

Both active-high and active-low signals are used.
A signal name that is followed by a backslash ("\") indicates
that the signal is asserted active low.
Conversely, a signal without a backslash denotes a
signal that is asserted active high.

Signals with multiple meanings or synonyms,
the synonyms are listed separated by a slash "/".
For example, the signal name for a read-write signal
that is active low for write is "RD/WR\".

Clock nets are all of the form "C(xx.yy-zz)". The digits "xx" specify the
period of the clock in nanoseconds. The digits "yy" specify the leading edge
of the clock signal and the digits "zz" specify the trailing edge of the
clock signal.

Signals that are part of busses are indicated by a common prefix
followed by a number. For example, a 16 bit data bus might be labelled
"D0", "D1", "D2", and so on until "D15".

A group of signals that are part of a signal vector are denoted by
a common prefix separated by the suffix with ".".
For example, all P2-bus signals start with the prefix "P2.".

Lastly, all ECL nets on the Sun-2 color board are prefixed
with "E." or are clock nets labelled in the form "C(Exx.yy-zz)".
All nets without the preceeding forms are TTL signals.

---

### Component Conventions


Components in the schematics are identified by component type
(also referred to as body name).
Components are named according to "generic" or industry standard names
such as "74LS00".
Components drawn in the morgan equivalent of their normal form are denoted
with a backslash; for instance, a low-power shottky "OR" gate with inverting
inputs is a "74LS00\".

Each component carries a location label.
Sections of a logical function that carry the same location label are
physically packaged into the same part. All location codes consist of
a letter from the alphabet followed by a number. The hundreds digit
of a location label specifies the page in the schematics where the
part can be found.
The letter prefix on the location label identifies the component type
and is one of:


	Letter	Component Type
	--------------------------------
	C,K     Capacitor
	U       Standard IC DIP
	M	64K RAM
	R       Resistor
	Y	PC-to-BNC Connector
	V	Voltage Regulator


Location labels are cross-indexed in the wirelist into component types,
and component types are translated into Sun Microsystem and manufacturer
part numbers by the parts list found in Chapter 6.


### Programmable Logic


Programmable logic elements such as PALs and PROMs are described
in a high-level functional language from which they are translated
automatically into the bitpatterns for programming.

Programmable logic elements are identified by name (SC1 through SC18).
The source code for the programmable logic is included in chapter 5 of this manual.
Tables and timing diagrams explaining programmable logic elements
are included in the description of the particular
functional block whenever appropriate.

---

## Power


The Sun-2 color video board requires a worst-case 25 Amp at 5.0 Volt and
4.0 Amp at -5.2 Volt. All power supply voltages should be within ten percent
of the specified voltage. At these current levels, the Sun-2 color board
consumes 146 watts. Typical current levels are XX Amp at 5.0 Volt and
YY Amp at -5.2 Volt.

After checking the Sun-2 color card for power-ground shorts, the card should
be inserted into a system with the Sun-2 single board and power should be
applied. The power supply may now have to be adjusted.


## Initialization


During system reset, the signal P2.INIT\ clears the control
register U207. With the control register reset, video is disabled (EN.VIDEO),
interrupts are inhibited (INTEN), and the TTL shadow color map is made
available for access by the host software (UPCMAP).

After system reset, if any video pattern appears on the monitor,
then the status register is not being properly reset and the signal P2.INIT\
should be investigated.


## Clock Timing


Most of the ECL circuitry on the color board is used for generating clocks
that vary with the value of zoom. The clock circuitry on the board is
independent of all other functional areas on the board and is probably the
biggest cause of bus timeouts for boards in initial testing.

For the purpose of the following discussion, let us assume that our video
clock is exactly 100 MHz. The 100 MHz crystal oscillator outputs a TTL
signal that is feed into a MC10124 TTL-to-ECL converter. This
100 MHz clock is then buffered by a MC10H102 ECL NOR gate
which sharpens the rise and fall times on this clock line. As a note of
interest for ECL designers, the MC10H116 inverters do not work well at all
in this capacity. The 100 MHz ECL clock, C(E10.0-5), now clocks three
MC10H136 hexadecimal counters.

The ECL counter at U1606 counts down to
divide C(E10.0-5) by a factor of four to produce the clock C(E40.0-20).
The TTL version of C(E40.0-20) drives the Prom and Pal state machines
on the board. The period of these state machines is roughly 40 nanoseconds.
A failure of this clock line would generate continuous timeouts when
accessing the frame buffer memory.

The other two ECL counters also count down to produce a clock that
varies with the zoom and which we use on the 74F194 video shift registers.
The counter at U1604 is loaded with the value of zoom, counts down
to zero, and is reloaded to repeat the cycle. The outputs of counter
U1604 are connected together in a Wire-Or; only when all binary outputs
of U1604 are zero will the signal E.ZERO\ be active. With zoom equal to
zero, E.ZERO\ will be a constant logic low, but with zoom greater than zero,


```

	Period of control signal E.ZERO\ = 10nsec * (zoom + 1)

```


When E.ZERO\ is asserted (and E.ZSYNC\ deasserted) then the ECL counter
at location U1605 will be allowed to increment. The two low-order outputs
of the counter U1605 are WIRE-ORed together such that the zoom clock
C(EZ40.0-30) will be asserted three states out of four and will be
unasserted on the fourth state. Like the control signal E.ZERO\,


```

	Period of zoom clock C(EZ40.0-30) = 40nsec * (zoom + 1)

```


The precursor to the system clock, C(E40.0-20), and the zoom clock, C(EZ40.0-30),
are syncronized during every horizontal retrace. The system clock gates
the zoom syncronization signal ZSYNC40\ which is converted to an ECL
signal which is re-clocked by C(E40.30-40) to generate E.ZSYNC\. When asserted,
the signal E.ZSYNC\ forces C(EZ40.0-30) low. Now, the trailing edge of
E.ZSYNC\ is always 30 nsec after the leading edge of the system clock,
so on the next low-to-high transition of C(E10.0-5), both C(E40.0-20)
and C(EZ40.0-30) will be asserted simultaneously.

The signal E.ZERO\ is also used to generated the signals SFT.S0 and SFT.S1
which control the parallel loading and serial shifting of the 74F194 shift
registers in the video output path. The buffered signal E.ZERO1\ is used
to improve the clock to select hold time on the hex counters U1604 and U1605.

The useful ECL clock and control signals are converted to TTL by MC10125
level converters and are then fed into 74F244 drivers which can sink a more
reasonable amount of current. Not all the control signals need to be routed
through 74F244 drivers, but routing every MC10125 output through the 74F244
drivers keeps the signal skews roughly equivalent.

The signal C(E10.0-5) is buffered and delayed by one gate and then drives
an MC10125 and a 74F244 that are just for it. Using these
unused sections would induce coupling which affects the signal C(10.0-5).
Flakey bits in the video output have a high probability of being caused by
an IC that just can't quite handle the 100 MHz clock rate. For instance,
Both the MC10125 and the 74F244 are beginning to degrade exponentially at
100 MHz and a 74F240 will not even operate at 100 MHz. The 74F04 seems
to operate at a frequency range beyond the 74F244, but unfortunately, a
74F04 does not drive C(10.0-5) to quite as high a voltage
as the 74F244. On the same clock line, a 74F244 does not drive low
quite as well as a 74F04, but then again, the 74F244 has a faster rise
time and the propagation delays between two separate 74F244s are probably
closer than between a 74F244 and a 74F04 (The other clocks are buffered
by a 74F244). In summary, the 100 MHz clock signals are the most
sensitive signals on the board and are probably the problem with a
board generating an unstable video image.

The following diagrams illustrate the clock waveforms at the trailing edge
of the zoom syncronization signal ZSYNC40\:


```


Clock Timing Diagrams
---------------------

C(E10.0-5)    _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

C(E20.0-10)   _--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--_

C(E40.0-20)   _----____----____----____----____----____----____----____----___

C(E40.30-40)  -______--______--______--______--______--______--______--______-

ZSYNC40\      __________xx----------------------------------------------------

E.ZSYNC\      _______________-------------------------------------------------

At Zoom = 0,
-----------
E.ZERO\       ________________________________________________________________

C(EZ40.0-30)  _________________------__------__------__------__------__------_

SFT.S0        ----------------------------------------------------------------

SFT.S1        -----------------______--______--______--______--______--______-

At Zoom = 1,
-----------
E.ZERO\       _________________--__--__--__--__--__--__--__--__--__--__--__--_

C(EZ40.0-30)  _________________------------____------------____----------____-

SFT.S0        -----------------__--__--__--__--__--__--__--__--__--__--__--__-

SFT.S1        -----------------______________--______________--____________--_

At Zoom = 2,
-----------
E.ZERO\       _________________----__----__----__----__----__----__----__----_

C(EZ40.0-30)  _________________------------------______------------------_____

SFT.S0        -----------------____--____--____--____--____--____-¬____--____-

SFT.S1        -----------------______________________--______________________-

At Zoom = 3,
-----------
E.ZERO\       _________________------__------__------__------__------__------_

C(EZ40.0-30)  _________________------------------------________---------------

SFT.S0        -----------------______--______--______--______--______--______-

SFT.S1        -----------------______________________________--_______________


```


---

## P2-Bus Interface


After the initialization and clock circuitry, the bus interface circuitry
is the next functional block to verify. The bus interface operates
asyncronously with the state machines and handles the functions of
latching the P2-Bus data and address, setting the control or frame
buffer request flip-flop, and issuing the P2-Bus data transfer acknowledge.
The P2-Bus interface is designed to operate with a 68010 running at upto
12.5 MHz. The following discussion assumes the bus is operating at 12.5 MHz.

The assertion of the P2-Bus strobe P2.S4\ begins a bus cycle. When asserted,
address bits P2.A1 through P2.A10 have been valid for 110 nsec, address
bits P2.A11 through P2.A26 have been valid for 10 nsec, data bits P2.D0
through P2.D15 have been valid for 25 nsec (on write), P2.R/W\ has been
valid for 65 nsec, and P2.LDS\ and P2.UDS\ may not be valid for another
10 nsec. Assuming that no previous request is still in progress, P2.S4\
causes the Pal SC1 to assert A_LATCH\ which disables the flow-through
on the data and address latches. The signal A_LATCH\ is then inverted
and clocks the control register request flip-flop, the frame buffer request
flip-flop, and bit P2.UDS\ which overflowed from the 74F373 address latches.
If the control registers on the board are addressed, C.SEL\ will be asserted
and A_LATCH will set the control request signal C.REQ\. If the frame buffer
memory is addressed, FB.SEL\ will be asserted and A_LATCH will set the
frame buffer request signal FB.REQ\.

With a 12.5 MHz P2-Bus, there may not be enough set-up time on P2.UDS\ and
P2.LDS\ before the assertion of A_LATCH\. The delay path from P2.S4\ to
A_LATCH\ consists of a 74F240 and a high-speed 16L8 Pal. With a 10 MHz P2-Bus,
this set-up time improves by 10 nsec and is not a concern.

Control registers are read and written asyncronously as the request is
made. Frame buffer writes, however, are buffered one deep and a new bus
cycle may begin while the previous request is still being processed. In
this case, the signal END_RMW\ which clears the frame buffer request
flip-flop is also used to force the deassertion of A_LATCH\ so that
the pending request can be accepted simultaneously with the completion
of the current frame buffer write cycle.

The signal A_LATCH is delayed in 50 nsec increments by a delay line hybrid
to produce A_LATCH50, A_LATCH100, and A_LATCH150. If a request flip-flop
has been set, A_LATCH100 is used to generate any appropriate write strobes,
and signal A_LATCH150 is used to generate any appropriate buffer enable.
A delay line is used so that the write strobes to the
RasterOp chips are asserted for a minimum of 60 nsec and that the data to the
ROPC is held for at least 20 nsec. Using the delay line, we can also
generate the transfer acknowledge (P2.ACK\) as quickly as possible after
an access to a control register.

There are four fundamental types of accesses to the Sun-2 color board:
control read cycles, control write cycles, frame buffer read cycles, and
frame buffer write cycles. The timing for these access types follows:


```

Control Read Cycle (2 Wait States)
----------------------------------

68010 10 MHz Clk  -S4-_S5_-S6-_S7_-S8-_S9_-SA-_SB_-S0-_S1_-S2-_S3_-S4-_S5_

P2.D7..P2.D0	  XXXXXXXXXXXXXXXXXXXXX---VALID---XXXXXXXXXXXXXXXXXXXXXXXX

P2.A26..P2.A0     XXXX-----------VALID------------XXXXXXXXXXXXXXXXXXXX----

P2.S4\		  ----____________________________--------------------____

A_LATCH 	  _____----------------------------____________________---

A_LATCH150        _________________----------------------------___________

C.REQ\            -----___________________________---------------------___

C.ACK\		  ------____________------------------------------------__

P2.ACK\		  ------------------__________________--------------------


Control Write Cycle (1 Wait State)
----------------------------------

68010 10 MHz Clk  -S4-_S5_-S6-_S7_-S8-_S9_-S0-_S1_-S2-_S3_-S4-_S5_-S6-_S7_

P2.D7..P2.D0	  XX---------VALID--------XXXXXXXXXXXXXXXXXX-------VALID--

P2.A26..P2.A0     XXXX-------VALID--------XXXXXXXXXXXXXXXXXXXX-----VALID--

P2.S4\		  ----____________________--------------------____________

A_LATCH 	  _____--------------------____________________-----------

A_LATCH150        _________________--------------------___________________

C.REQ\            -----___________________---------------------___________

WRITE_STROBES\	  -----____________----------------------------___________

C.ACK\		  -----_---------------------------------------_----------

P2.ACK\		  ------_________________-----------------------__________


```


```


Frame Buffer Read Cycle (3 to 10 Wait State)
--------------------------------------------

68010 10 MHz Clk  -S4-_S5_-S6-_S7_...................._SX_-SY-_SZ_-S0-_S1_

P2.D7..P2.D0	  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX---VALID----XXXXXXXX

P2.A26..P2.A0     XXXX-------------------VALID--------------------XXXXXXXX

P2.S4\		  ----____________________________________________--------

A_LATCH 	  _____--------------------------------------------_______

FB.REQ\           -----___________________________________________-------

END_RMW\          ------------------------------------------------_-------

RDAT(0-120)\      -----------------------_________------------------------

C.ACK\            ------------------------_________-----------------------

P2.ACK\		  ---------------------------------_______________--------


Frame Buffer Write Cycle (1 Wait State)
---------------------------------------

68010 10 MHz Clk  -S4-_S5_-S6-_S7_-S8-_S9_-S0-_S1_-S2-_S3_-S4-_S5_-S6-_S7_

P2.D7..P2.D0	  XX---------VALID--------XXXXXXXXXXXXXXXXXX-------VALID--

P2.A26..P2.A0     XXXX-------VALID--------XXXXXXXXXXXXXXXXXXXX-----VALID--

P2.S4\		  ----____________________--------------------____________

A_LATCH 	  _____-------------------------------------------___-----

FB.REQ\           -----__________________________________________----_____

END_RMW\ 	  -----------------------------------------------___------

RDAT(0-120)\	  ----------------------------------------__________------

C.ACK\		  -----_---------------------------------------------_----

P2.ACK\		  ------_________________-----------------------------____


```


---

## Memory Timing


The memory control state machines generates the memory timing for
the color video board. This section describes all the circuitry necessary
for the frame buffer memory to operate correctly. While the memory timings
do depend on the zoom syncronization (Prom SC10), a failure in that logic
will not generate frame buffer memory errors. This section does not
attempt to explain the interaction of the rasterop chips with the memory;
it assumes that all memory operations treat the frame buffer as pixel-mode
memory or word-mode memory.

The memory control circuitry resides predominately on pages 3 through 5
of the schematics. The
heart of the memory control is prom SC11. This prom operates on
40 nsec boundaries and generates the next state for the memory timing.
There are sixteen possible memory control states
(ST3..ST0). The first eleven states of the memory control cycle generate
a nibble mode read cyle that buffers the next block of data for video output.
The last five states of the memory controller are reserved for read/write updates
to the frame buffer memory; if no request is pending, a Cas-Before-Ras
refresh cycle is run.

At zoom zero, one memory cycle consists of one nibble-mode video read cycle
followed by one read/write cycle. At larger zooms, however, a memory cycle
consists of one nibble-mode video read cycle followed by multiple read/write
cycles. For example, at zoom one, the 64 pixels buffered during a video read
cycle will be output over 32 states instead of 16 states. At zoom one, we
perform one video read cycle followed by 3 read/write cycles and we repeat
state1 as many times as necessary to pad the total period of the memory
control cycle to 32 states. At zoom two, we perform one video read cycle,
7 read/write cycles, and repeat state1 3 extra times.


```


   States per memory control cycle = 16 * (zoom + 1)

   Nibble-mode video read cycles per memory control cycle = 1

   Read/write cycles per memory control cycle = (16 * (zoom + 1) - 11) DIV 5

   Times State1 repeated per memory control cycle = (16 * (zoom + 1) - 11) MOD 5


```


Besides running a variable number of read/write cycles after each nibble-mode
video read cycle, prom SC11 will syncronize the memory cycles with the zoomed
clock C(Z40.0-30) at the start of each scan line.
When signal ZSYNC\ is asserted, SC11 advances ST3..ST0 one
state at a time until state10. Prom SC11 then holds at state10 until ZSYNC\
is deasserted. When SC11 resumes, the low-to-high transition of RAS.7\
to RAS.0\ marking the end of the nibble-mode video read cycle will
coincide with the rising edge of C(Z40.0-30). At low zoom, however, a malfunction
of signal ZSYNC\ can not cause frame buffer memory errors; a failure of ZSYNC\
can only disrupt video output and hence is discussed in the section on zoom.

Frame buffer read/write cycles are performed only if RMW is asserted during
memory control states 11 through 15. At states 9 and 14, prom SC11 generates
RMW_INC. This signal clocks 74F74 U117 section #0; if
a frame buffer request (FB.REQ) is pending, RMW.REQ is asserted. RMW.REQ
is clocked 40 nsec later to generate RMW.

The selection/update of individual 64K rams is accomplished via the separate
encoding of the ras, cas and write-enable lines. Prom
SC11 generates RASX\ which is delayed 40 nsec to produce RAS.7\..RAS.0\.
RASX\ does not vary with the type of frame buffer access and depends only
on the values of ST3..ST0. Note that the 40 nsec delay of RASX\ was
introduced because prom SC11 could not drive the 8 TTL
loads of RASX\ quickly enough.

CAS is decoded by pals SC12 and SC13. During nibble-mode video read cycles,
the values of CAS15\..CAS0\ are identical and determined by ST3..ST0. During
the optional read/write memory cycles, if RMW is deasserted, CAS15\..CAS0\
remain low so that the ram outputs remain driven to valid TTL logic levels
(The voltage margins on the AM29520 video data buffers degrade when their
inputs are left floating). While CAS15\..CAS0\ remain asserted, RAS\ will
make a high-to-low transition to effect a Cas-Before-Ras Hidden Refresh
Cycle. At low values of zoom, the assignment of address bits to the frame
buffer memory will assure the dynamic rams' refresh as the nibble-mode
read cycles are run. However, at large values of zoom, refresh is not
guaranteed by the nibble-mode video read cycles. At a 64 KHz horizontal
line rate, one Cas-Before-Ras cycle per scan line would refresh 256 rows
in exactly 4 msec. To ensure that at least one Cas-Before-Ras refresh cycle
is run every scan line, RMW.REQ is reset by CLR_RMW\ at state10 during ZSYNC\.
Forcing the deassertion of RMW during the first read/write memory cycle
after ZSYNC\ ensures that the frame buffer memory never loses refresh.

If RMW is asserted during a memory read/write cycle, some cas lines
will be deasserted at states 11 and 12 to select those memory array columns.
If signal ONE_PIX\ is asserted, pal SC4 has decoded a pixel-mode memory
cycle and only the cas line selected by A3..A0 will be toggled. If ONE_PIX\
is deasserted and A20 is asserted, the access uses rasterops in pixel-mode
and all cas lines will be active. If A20 is deasserted, the access uses
word-mode; if A0 is a logic low, CAS7\..CAS0\ will be active; if UDS
is active, CAS15\..CAS8\ will be active. Bits UDS and A3, A20 and A2 are
mutually exclusive and are multiplexed by U502 to the inputs of SC12 and SC13;

Word-mode access to specific bit planes and pixel-mode
protection of arbitrary bit-planes is controlled by the write-enable lines
WE.A\ to WE.H\ on the frame buffer memory. The write-enable lines are
controlled by the per-plane mask register and pals SC14 and SC15.
The write-enable lines are organized as a separate control signal for
each bit plane in the memory. For word-mode frame buffer accesses,
bits A19..A17 select the accessed plane and bit-plane protection is
expected to come from the CPU page maps. For pixel-mode accesses, a zero
bit in the per-plane mask register will protect the corresponding
bit plane from update. All write-enable lines are only asserted when
signal RDAT(0-120)\ is valid. Note that pals SC14 and SC15 do not
distinquish read from write by using the signal RD/WR\ ; instead, these
pals using the signal FB_RD\ generated by pal SC4.

The timing of a normal memory cycle at zoom zero follows:

C(40.0-20)
RAS
CAS
RDAT(0-120)\
RMW_INC


---

	- On previous section, discuss proms that do RMW_TC and SPARE_TC.


---

## Memory Addressing

   - Stuff on page 3


---

## Zoom and Pan

	- ZSYNC and video ouput buffer and 74F194.

	- Discuss modification of RMW states and spares for first cycle
	  on scan line at high zoom.


---

## ROPC timings


	-LD.SRC
	- LD.DST
	-HR.TOG
	- One diagram for each addressing mode. ZOOM 0.
	- One diagram at large zoom for one addressing mode.


---

## COLOR MAP


---

## H and V sync

	- discuss with enough detail that someone else can redo proms for
	  new monitor.

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
