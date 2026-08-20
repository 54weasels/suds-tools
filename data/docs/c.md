---


---


# The McSun Workstation


# Engineering Manual


Company Confidential

Sun Microsystems Inc.

[date]


>
The McSun is a low-cost, yet high-performance workstation.
A member of the Sun-2 family of workstations,
it provides the memory management and all the architectural features
of the larger Sun-2 workstations.

The main differences of the McSun versus other Sun-2 workstations is
the display. First, it is refreshed out of main memory, second,
it is smaller resolution than the larger Sun-2s.
The other difference is that there is no expansion capability in
a McSun except memory expansion. The basic machine comes with
1 megabyte main memory that is expandable up to four megabytes.


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.

Sun, McSun, and the combination of Sun with a numeric suffix
are trademarks of Sun Microsystems Inc.


---


---

# Data Sheet


## Features


### Processor


- 32-bit VLSI CPU, 10 Mhz

- 1 MByte of main memory

- expandable up to 4 MBytes total

- multiprocess, demand paging virtual memory management

- 16 Mbytes virtual address space per process


### Display


- programmable resolution

- refreshed out of main memory


### I/O


- integral Ethernet interface transfers directly into memory

- two programmable serial I/O ports

- two serial interfaces for keyboard and mouse


### Other Features


- system timers

- 64K bytes EPROM

- self-diagnostic capabilities

- single +5V power supply, 10 Amps max.


---

## Architecture Overview


The McSun workstation implements the Sun-2 Architecture Specification.
This specification defines how the hardware capabilities
of the machine are visible to the software.
The complete specification of the architecture is contained
in the Sun-2 architecture manual.
The following is a brief overview of the architecture and its
implementation in the McSun Workstation.


### CPU, MMU, and Device Layers


The Sun-2 architecture is divided into three layers:
the CPU layer, MMU layer, and Device Layer.

The CPU layer consists of the Motorola 68010 instruction-set-processor,
extended with a number of external registers, which are
the bus error register, the system enable register,
the diagnostic register, and the ID-PROM.

The MMU layer defines how virtual addresses are translated into
physical address and the implementation of multiple address spaces,
protection, and sharing.

The Device layer of the Sun-2 architecture defines what devices
exist in the architecture and how they are accessed.
These devices include main memory and I/O devices.

All CPU accesses to the device layaer pass through the MMU
and thus are translated and protected in an identical fashion.
In addition, direct memory accesses by I/O devices
also pass through the memory memory management and thus
operate in a fully protected environment.


---

### McSun Architecture


The figure [Figure](#b11) is a block diagram of a McSUn Workstation.


![b11.press](../svg/b11.drw.O.svg)


*Figure: **McSun Architecture***

<a id="b11"></a>


The CPU and the Ethernet interface arbitrate for the virtual address bus
and the data bus. The virtual address of the active master
is translated by the MMU into a physical address.
The physical address contends with the video refresh address
for access to main memory.
The ID PROM, System Enable Register, EPROM, Timer, and UARTs
are accessible on the data bus.

Main memory is dual-ported between processor (and Ethernet
accesses and video refresh. A memory controller arbitrates
between processor and video requests and generates all the
required memory timing signals.
Video requests are higher priority than processor requests.
If a video request is pending, a video cycle is executed as soon as possible.
Depending on the kind of RAM chips used, a video cycle consists
of either a nibble-mode RAS cycle or a back-to-back RAS cycle.
If no video request is pending, the memory controller serves
processor requests such that a processor cycle runs without wait states.

---

### MMU Overview


The Sun-2 Memory Management Unit provides address translation, protection,
sharing, and memory allocation for multiple processes executing on the CPU.

The memory management consists of a context register, a segment map,
and a page map.
Virtual addresses from the processor are translated into intermediate
addresses by the segment map and then into physical addresses by the page map.

The most important numbers for the memory management are a page size of
2048 bytes and a segment size of 32K bytes (giving 16 pages per segment).
Up to 8 contexts can be mapped concurrently.
The maximum virtual address space for each context is 16M bytes.

The figure [Figure](#b12) shows how virtual addresses are translated into
physical ones.


![b12.press](../svg/b12.drw.O.svg)


*Figure: **Sun-2 Memory Management***

<a id="b12"></a>


---

## Specification Summary


### CPU





- M68010 CPU, 10 MHz




### Memory





- 1 MByte of main memory

- 3 MByte of expansion memory

- hardware memory refresh




### Memory Management Unit





- Sun-2 memory management unit

- two-level, multiprocess virtual memory management

- full support for demand paging

- 16 Mbytes virtual address space per process

- separate address spaces for supervisor and user

- valid, accessed, and modified tags to assist paging algorithms

- separate read, write, and execute tags for user and supervisor accesses




### Display





- refreshed from main memory

- 896 by 700 display format

- 50 MHz video clock

- 60 Hz non-interlaced video refresh




### Ethernet Interface





- VLSI Ethernet controller (AMD 7990)

- packets transferred directly in and out of main memory

- extensive diagnostic capabilities




### Serial I/O Ports





- two programmable serial i/o ports

- based on synchronous communication controller (Zilog 8530)

- software programmable baud rates (75 Baud to 19.2 Kbaud)

- asynchronous, synchronous, and bit-stuffing protocols

- two serial ports for keyboard and mouse




### Other Features





- 64K bytes EPROM (27128)

- five programmable 16-bit timers (AMD 9513)

- software interrupt capability

- software readable identification PROM




### Environmental Characteristics


- Operating Temperature:	10 - 55 C

- Humidity:		0 - 90 %, non-condensing


### Power Characteristics


- 10 Amp max at +5 Volt +- 5%

- 0.5 Amp max at +12 Volt +- 5%


### Physical Characteristics


- Height:	xxx mm (xx.xx")

- Width:	xxx mm (xx.xx")

- Depth:	xxx mm (xx.xx")

- Weight: xxx g (xx oz)


---

# User Guide


## Programming


The McSun is a member of the Sun-2 family of workstations.
It thus implements the full Sun-2 architecture which
is specified in the Sun-2 Architecture Manual.
No attempt is made to repeat this information here.
However, this section does describe the McSun implementation
specific features of the Sun-2 architecture.


### MMU Implementation


The MMU of the McSun implements a page number field of 12 bits.
It thus supports a physical address of 23 bits, capable of addressing 8 MBytes.
The other physical address bits in the page map are not implemented.
On a read cycle, the not implemented bits read back as 0.


### Physical Address Assignments


```


Type	Address		Device				Wait States
------------------------------------------------------------------------------
0	23-bit		Memory Bus

	[0x000000]	Physical Memory	1..4 MBytes	0
------------------------------------------------------------------------------
1	23-bit		I/O Bus

	[0x000000]	EPROM				2
	[0x000800]	Ethernet Interface		2
	[0x001000]	Reserved			2
	[0x001800]	Keyboard/Mouse Interface	2
	[0x002000]	Serial Port			2
	[0x002800]	Timer				2
	[0x003000]	Reserved			2
	[0x003800]	Reserved			2
------------------------------------------------------------------------------

```


### Video Memory


Video is refreshed out of main memory starting at physical address 0.
Video Enable is the DTR Output of the Mouse UART.
Video Interrupt is the DCD Input of the Mouse UART.


### Interrupt Assignments


The following table summarizes the interrupt level assignments
for the devices that have been described in this manual.
All these interrupts are autovectored.


```

-----------------------------------------------------
    7	TIMER1, Ethernet
    6	Serial Ports, Video
    5	TIMER2..5
    4	Spare
    3	System enable register EN.INT3
    2 	System enable register EN.INT2
    1 	System enable register EN.INT1
------------------------------------------------------

```


### CPU Timing


CPU Timing is as follows:


```


CPU clock cycle:	100 nanoseconds (10 MHz)
CPU basic cycle:	400 nanoseconds


```


---

# Theory of Operations


## Power Estimate


```


Board without RAM:		5 Amp

Average current per RAM:	40 mA active, 4 mA standby

Average numbers of RAMs active:	20/32

Average RAM current per 1 MB:	20*40+8*4 = 0.832 Amp

Average RAM current per 4 MB:	80*40+32*4 = 3.3 Amp

Total current with 4 MB RAM:	8.3 Amp


```


---

## Memory


*Reference:* Schematics Page 4, 5


### Introduction


The memory subsystem consists of the following functions:


memory array

processor address multiplexor

video address counter

RAS decoder

CAS decoder

data driver and multiplexor


The interconnection of these pieces is shown in the Figure [Figure](#b31).


![Placeholder: b31.press]()


*Figure: **Memory Interface***

<a id="b31"></a>


---

### Memory Organization


Memory is organized as a 32-bit wide bank of 256K RAM chips,
providing one Megabyte of storage.
This memory is accessed in two ways: one for processor cycles
and one for video cycles.

Processor cycles access memory as 16-bit words.
The A01 address bit from the CPU decodes one of two
row-address-strobes [M.RAS0,M.RAS1], enabling access
of even or odd words of memory, respectively.
The untranslated address bits from the CPU form the
memory row-address bits, the column address is formed
from the translated address bits.
For special cycles [SPECIAL=1], such as MMU updates,
CAS is not asserted.
On a read operation, the selected word is read-back via the
32-to-16 bit data multiplexors [ALS257] to the CPU.
On a write operation, the write-data-buffers [ALS244]
drive the write data to all memory chips.
The upper and lower write enable, [M.WEU, M.WEL]
control which bytes are actually written into memory.

Video cycles read two consecutive 32-bit word
from memory in a nibble mode cycle.
The video address counters [74LS590] provide a 16-bit address.
The low-order eight bits of which form the row-address,
the high-order eight bits the column address. The ninth
row/column address bit, [MA8] is kept at 0 during video cycles,
since this bit is used for the nibble-mode cycle internal to the RAM chips.
Both [RAS0, RAS1] are asserted enabling all 32 RAM chips present.
After reading the first 32-bit word into the video data register 0,
a second 32-bit word is read by pulsing the column address strobe quickly
and this word is stored into video data register 1.


### Address Mapping


The table below illustrates how the processor and video addresses
are mapped to the multiplexed RAM addresses.
Multiplexed address bit 8 is the nibble-mode bit.
During the video nibble-mode cycle, the even (MA8=0) row address
is accessed with the first nibble,
followed by the odd (MA8=1) row address with the second nibble.


```


MA  = MEMORY ADDRESS
PRA = PROCESSOR ROW ADDRESS
PCA = PROCESSOR COLUMN ADDRESS
VRA = VIDEO ROW ADDRESS
VCA = VIDEO COLUMN ADDRESS
--------------------------------------
MA	PRA	PCA	VRA	VCA
--------------------------------------
MA8	A02	MA19	0/1	0
MA0	A03	MA11	A03	A11
MA1	A04	MA12	A04	A12
MA2	A05	MA13	A05	A13
MA3	A06	MA14	A06	A14
MA4	A07	MA15	A07	A15
MA5	A08	MA16	A08	A16
MA6	A09	MA17	A09	A17
MA7	A10	MA18	A10	A18
---------------------------------------

```


---

## Memory Controller State Machine


The memory controller controls the timing of processor and video memory cycles.
States are enumerated S0 through S9 for the processor,
corresponding to the respective 68010 states, and S16 through S31 for the video.
States are executed in sequence except as follows:


```


IF S0 AND VREQ THEN S16
IF S2 AND VREQ THEN S16
IF S8 AND VREQ THEN S16
IF S3 AND ¬PREQ THEN S2
IF S24 THEN S1 (NIBBLE MODE RAM)
IF S28 THEN S1 (STANDARD RAM)


```


### Processor Cycle


```


	S0  S1  S2  S3  S4  S5  S6  S7  S8  S9

C-100	----____----____----____----____----____

RAS\	--------____________________------------

PCA\	----------------________________--------

CAS\	----------------________________--------

DAS\	--------------------____________--------

DTACK	----------------________________--------


```


### Video Cycle, Nibble-RAM


```


	S16 S17 S18 S19 S20 S21 S22 S23 S24 S1

C-100	----____----____----____----____----__

RAS\	--------________________________------

CAS\	----------------________----________--

LD1/VRA\----________----------------________--

LD0/VCA\------------____________--------------


```


### Video Memory Cycle, Regular RAM


```


	S16 S17 S18 S19 S20 S21 S22 S23 S24 S25 S26 S27 S28 S1

C-100	----____----____----____----____----____----____----____

RAS\	--------________________--------________________--------

CAS\	----------------____________------------____________----

LD1/VRA\----________----------------________--------------------

LD0/VCA\------------____________------------____________--------


```


---

### Memory Controller PAL: B430


```


P16R6

% INPUTS:

AS\	Processor Address Strobe
UDS\	Processor Upper Data Strobe
LDS\	Processor Lower Data Strobe
READ	Processor Read (Write\)
DSEN\	Processor Data Strobe Enable
VREQ	Video Request

% CLOCKED OUTPUTS

X0
X1
X2
X3
X4
CASEN\	Processor CAS Enable

% UNCLOCKED OUTPUTS:

WEU\	Memory WEU
WEL\	Memory WEL

% FUNCTIONS:

/X0	= X0

/X1	= /X0 * X1
	+ S1 * /VREQ
	+ S5 * /VREQ
	+ S9
	+ S17
	+ S21

/X2	= /X0 * X2
	+ S3 * /VREQ
	+ S3 * AS
	+ S5 * /VREQ
	+ S19 * /S4
	+ S21 * /VREQ

/X3	= /X0 * X3
	+ S7
	+ S9
	+ S23

/X4	= /X0 * X4
	+ S0 * VREQ
	+ S2 * VREQ
	+ S3 * /AS
	+ S8 * VREQ

CASEN\	= AS * S3
	+ CASEN * AS

WEU\	= /S4 * /READ * UDS * DSEN

WEU\	= /S4 * /READ * LDS * DSEN


```


---

### Memory Controller PROM: B432


```

begin "b432"

require "prom.sai" source!file;
$32$8;

adrs(0,0,	state0);
adrs(1,0,	state1);
adrs(2,0,	state2);
adrs(3,0,	state3);
adrs(4,0,	state4);

define

state	=[(state0*d0 + state1*d1 + state2*d2 + state3*d3 + state4*d4)],
nstate	=[(state + 1)],
pca	=[(4≤nstate≤7)],
das	=[(5≤nstate≤8)],
vra	=[((17≤nstate≤18) ∨ (23≤nstate≤24))],
vca	=[(19≤nstate≤21)],
ras	=[((2≤nstate≤7) ∨ (18≤nstate≤23))],
cas	=[((4≤nstate≤8) ∨ (20≤nstate≤21) ∨ (23≤nstate≤24))],
dtack	=[(4≤nstate≤8)];

prombegin

bit(0,0,	¬ras);
bit(0,1,	¬cas);
bit(0,2,	¬das);
bit(0,3,	¬dtack);
bit(0,4,	0);
bit(0,5,	¬pca);
bit(0,6,	¬vra);
bit(0,7,	¬vca);

promend;

writeprom("b432",0);

end "b432";

```


---

## Video Clock and Shifter


The video clock oscillator [K1114A:U620]
generates video clock [C-20] that clocks the shift registers
[74F194:U631,U6132].
The schematics documents the video clock as 50 MHz, although
slower and faster clock frequencies can be used.
The maximum clock frequency of the design is 64 MHz.

Shift-register [74F194:U632] generates the four timing strobes
[V.Q0..3] as illustrate`α⊂in the figure below.
When the shift-register reaches state "1111", output [V.Q3]
loads the constant data "0001" on its data input.


```


C-20	--__--__--__--__--__

V.Q0	--------------------

V.Q1	____------------____

V.Q2	________--------____

V.Q3	____________----____

STATE	Q3Q2Q1Q0
----------------
S1	0 0 0 1
S2	0 0 1 1
S3	0 1 1 1
S4	1 1 1 1


```


During initialization, the first "1" on [V.Q3] will initialize the cycle.
If the shift register powers up in a state of all "0",
then a "1" appears on [V.Q3] after four clock transitions
because the right shift input is connected to [VCC].

Timing strobe [V.Q1] clocks flipflop [74F74:U621] generating
clock [V.HCLK].
This signal clocks horizontal counter [74LS590:U624],
video state register [74F374:U628],
video output register [74F534:U629].
In addition, [V.HCLK] controls multiplexor [ALS257],
selecting the nibble of the video output register to be loaded into
the video shift register. The first nibble selected
after a low-to-high transition on [V.HCLK] is bits [4..7],
since the bits are shifted out with the most significant bit first.


---

### Horizontal State Machine


The horizontal counter [74LS590:U624] is advanced every 8 pixel times
with the rising edge of [V.HCLK].
Horizontal counter is reset with [V.HRESET\] generated by video state register.

The low-order three bits of the horizontal counter are decoded
in dr [74LS138:U620] and generate the output enables
for the 64-bit video holding register, one byte at a time.
All outputs of the horizontal counters, plus vertical blank signal [V.VBLANK]
from the vertical state machine, are decoded by
horizontal decode PROM [P9X4:U626]. The outputs of this
horizontal decode PROM are [V.HRESET, V.HSYNC, V.VCLK] and [V.DISPEN].


### Horizontal Decode PROM: B626


```


begin "b626"

comment	This information proprietary to Sun Microsystems Inc

1 state = 8 pixel, 1 pixel = 20 nsec

	    Range	Length	Length	Time
	    [State]	[State]	[Pixel]	[usec]
------------------------------------------------------------
cycle	    00..138	139	1112	22.22	45 KHz
visible	    00..111	112	896	17.92
invisble    112..138	26	208	4.16
frontporch  112..112	0	0	0
hsync	    112..119	8	64	1.28
backporch   120..138	18	144	2.88
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
nstate	=[((state + 1) MOD 138)],

dispen	=[(¬vblank ∧ (0≤nstate≤111))],
hsync	=[(112≤nstate≤119)],
hreset	=[(nstate = 0)],
vclock	=[(nstate = 112)];

prombegin

prom(0,d0,	¬dispen);
prom(0,d1,	vclock);
prom(0,d2,	hsync);
prom(0,d3,	¬hreset);

promend;
writeprom("b626",0);
end "b626";


```


---

### Vertical State Machine


The vertical counter [74LS590:U626] is advanced every fourth
transition of clock [V.VCLK].
Vertical counter is reset with [V.VRESET] from video state register.

Vertical decode PROM [P9X4:U1815] decodes vertical counter states
[V.VSTATE0..7] and outputs [V.VSYNC, V.RESET] and [V.VBLANK].


---

### Vertical Decode PROM: B627


```


begin "b627"

comment	This information proprietary to Sun Microsystems Inc.

1 line = 22.22 usec = 45.00 KHz
1 state = 2 lines = 44.44 usec

	    Range	Length	Time
	    [Lines]	[Lines]	[usec]
------------------------------------------------------------
cycle	    000..749	750	16666	60 Hz
visible	    000..699	700	15555
invisble    700..749	50	1111
frontporch  700..700	0	0
vsync	    700..710	10	222
backporch   710..749	40	999
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
v8	=[a8],

line	=[2*(v0*d0+v1*d1+v2*d2+v3*d3+v4*d4+a5*d5+v6*d6+v7*d7+v8*d8)],

vsync	=[(700≤line<710)],
reset	=[(line = 748)],
vblank	=[(line ≥ 700)];

prombegin

prom(0,d0,	vsync);
prom(0,d1,	¬reset);
prom(0,d2,	vblank);
prom(0,d3,	0);

promend;
writeprom("b627",0);
end "b627";


```
