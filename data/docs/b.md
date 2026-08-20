---


---


# The Sun 2060 Single Board Workstation


# and the Sun 2061 Expansion Board


# Engineering Manual


Company Confidential

Sun Microsystems Inc.

Draft of [date]


>
The Sun 2060 Board is a single board Workstation computer.
It provides on a single, triple height Eurocard all components of a
high-performance engineering/scientific workstation:
CPU, floating point processor, memory, virtual memory management,
display subsystem, networking, serial I/O, system bus interface,
and various system utilities.

The processor is based on the 16 MHZ 68020 CPU and the 68881 FPP.
It uses the Sun-2 multiprocess virtual memory management
which supports processes up to 16 Megabytes.
Included on the board are two or four megabytes of main memory.
With an optional memory expansion board carrying another
two or four megabytes of additional main memory,
systems with up to 8 Megabytes of memory can be configured.
All main memory is equipped with byte parity error detection.

The display subsystem features 1152 by 900 pixel resolution and flicker-free
non-interlaced display refresh at 67 Hz. The display is refreshed
out of a separate, dual-ported video memory.

Input/Output includes a high-performance Ethernet interface with
direct-virtual-memory-access (DVMA) to main memory, two high-speed
serial lines with full modem control, and two additional serial lines
for keyboard and mouse input devices.
An interface to the VME-Bus with master, slave and system controller
capabilities is provided.


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.

Sun and the combination of Sun with a numeric suffix are trademarks of
Sun Microsystems Inc.


---


---

# Data Sheet


## Features


### Processor


- 32-bit 68020 CPU

- optional 68881 IEEE floating point processor

- CPU Cycle Time: 62.5 nanoseconds

- Memory Cycle Time: 250 nanoseconds

- 2 MByte or 4 MByte of main memory

- 2 MByte or 4 MByte of expansion memory

- multiprocess, demand paging virtual memory management

- 16 Mbytes virtual address space per process

- optional DES encryption processor


### Display


- dual-ported 128 KBytes video memory

- 1152 by 900 pixel display resolution

- 67 Hz non-interlaced video refresh


### I/O


- integral Ethernet interface transfers directly into memory

- two programmable serial I/O ports with full modem control

- two additional serial interfaces for keyboard and mouse


### Other Features


- VME System Bus Interface

- DVMA (direct virtual memory access) from VME Bus

- five programmable 16-bit timers

- 32K to 128K bytes EPROM

- extensive self-diagnostic capabilities

- triple-height Eurocard form factor


---

## Introduction


The Sun-2060 Board is a high-performance implementation
of the Sun-2 architecture on a single 400mm by 366.67mm Eurocard.
The board includes the CPU, virtual memory management,
optional processor enhancements,
one to four megabytes of main memory with parity error detection,
a high-resolution display subsystem,
integral Ethernet and RS-423 interfaces,
and a dual-ported interface to the VME-Bus.

The processor is based on the Motorola 68020 32-bit VLSI CPU
in conjunction with the Motorola 68881 IEEE Floating Point processor.
The processor has a CPU clock of 16 MHZ and can execute one
memory cycle every 250 nanoseconds.

The 2050 board includes the Sun-2 virtual memory management unit (MMU).
The Sun-2 MMU was specifically optimized to support the requirements
of the the 4.2 BSD version of the Unix (TM) operating system.
It provides demand paging with multiple, simultaneous process contexts.
Each process can be up to 16 megabytes in size. In addition,
the MMU provides separate address spaces for the system and for the user.

The Sun 2060 board contains 2 or 4 MByte of main memory.
With the Sun 2061 memory expansion board, another 2 or 4 MByte
of main memory can be added, for a maximum main memory size of 8 MByte.
Memory is based on 256K RAM components.
Memory is equipped with byte parity error detection.

Integral to the Sun-2060 Board is a high-resolution
bitmap display subsystem featuring a 1152 by 900 pixel display area
and non-interlaced, 67 Hz refresh. The display is refreshed out of
a dedicated, dual-ported 128 KByte video memory, which is logically
part of main memory.

The Sun 2060 Board includes an integral Ethernet interface.
This interface uses a VLSI Ethernet controller that features
high-performance frame handling and extensive diagnostic capabilities.
Ethernet packets are directly transferred in and out of main memory
through the use of direct virtual memory access (DVMA).

For serial I/O, two highly programmable serial communication channels are provided
featuring software programmable baud rates from 75 Baud to 19.2 KBaud
and supporting asynchronous, synchronous, or bit-stuffing protocols.
Two additional ports are provided for keyboard and mouse interfaces.

The Sun 2060 Board includes a bidirectional interface to the VME Bus
with master and slave capabilities.
The board provides 24-bit address and 16-bit data transfer capabilities
in both directions. It also implements system controller functions such as
arbitration, interrupt handling, reset, and power monitoring.

Other features of the board include an optional DES encryption processor,
programmable timers, and an identification PROM providing software
readable serial number and Ethernet address.

The board also includes extensive facilities for software and hardware diagnostics.
Among them are a bus-error register, a diagnostic display for
displaying error messages, a watchdog timer for automatic restart,
and powerup self-tests.


---

## Sun-2 Architecture Overview


The 2060 Board implements the Sun-2 Architecture Specification.
This specification defines how the hardware capabilities
of the machine are visible to the software.
The complete specification of the architecture is contained
in the Sun-2 architecture manual.
The following is a brief overview of the architecture and its
implementation on the 2060 Board.

The Sun-2 architecture is divided into three spaces:
the CPU space, MMU space, and Device space.

The CPU space comprises the central processing unit (the "CPU")
together with coprocessors, such as the floating point coprocessor,
and DVMA masters, such as the Ethernet interface.

The MMU space is the core of the Sun-2 architecture.
It includes the Sun-2 memory management unit (the "MMU")
as well as all other Sun-2 architecture extensions to the CPU,
such as the bus error register, the system enable register,
the diagnostic register, and the ID-PROM.
The ID-PROM contains a unique serial number and indicates
the implementation type of the architecture.

The Device space of the Sun-2 architecture defines what devices
exist in the architecture and how they are accessed.
These devices include main memory, the system bus, and I/O devices.

All CPU accesses to device space pass through the MMU
and thus are translated and protected in an identical fashion.
In addition, direct memory accesses by I/O devices
also pass through the memory memory management and thus
operate in a fully protected environment.

---

## 2060 Board Block Diagram


Figure [Figure](#a11) illustrates how the CPU, MMU, and devices
are interconnected on the 2060 Board.


![a11.press](../svg/a11.drw.O.svg)


*Figure: **Sun 2060 Board Architecture***

<a id="a11"></a>


The CPU sends out a virtual address that is translated by the MMU
into a physical address.
The CPU, Ethernet Interface, and VME Slave Interface
arbitrate for and share the virtual address bus on the left side of the MMU.
The VME Master Interface, Main Memory, Video Memory, and I/O Devices
are addressed with physical addresses on the right side of the MMU.


---

## Sun-2 MMU Overview


The Sun-2 Memory Management Unit provides address translation, protection,
sharing, and memory allocation for multiple processes executing on the CPU.

The memory management consists of a context register, a segment map,
and a page map.
Virtual addresses from the processor are translated into intermediate
addresses by the segment map and then into physical addresses by the page map.

The memory management uses a page size of 2048 bytes and
a segment size of 32K bytes (giving 16 pages per segment).
Up to 8 contexts can be mapped concurrently.
The maximum virtual address space for each context is 16M bytes.

Figure [Figure](#a12) shows how virtual addresses are translated into
physical ones.


![a12.press](../svg/a12.drw.O.svg)


*Figure: **Sun-2 Memory Management***

<a id="a12"></a>


---

## 2060 Board FloorPlan


Figure [Figure](#a12) gives an overview of the connectors on the 2060 Board.


![a13.press](../svg/a13.drw.O.svg)


*Figure: **Sun 2060 Board Floor Plan***

<a id="a13"></a>


The connectors on the backplane of the board are called the P1, P2, and
P3 connectors.
The P1 Connector carries the VME Bus, also referred to as the P1-Bus.
The P2 Connector serves for the memory expansion bus, or the P2-Bus.
The P3 Connector powers the board and carries some of the P2-Bus lines.

The connector on the input/output side of the board are,
in sequence from top to bottom:
[J601] Keyboard Connector,
[J602] Mouse Connector,
[J603] Serial Port A,
[J604] Serial Port B,
[J605] Keyboard/Mouse Connector,
[J700] Ethernet Port,
and the [J1800] Video Connector.

---

## Specification Summary


### CPU





- M68020 CPU

- M68881 IEEE FLoating Point Processor

- 16 MHZ CPU Clock




### Memory





- 2 or 4 MByte of main memory (256K RAMs)

- 2 or 4 MByte of expansion memory (256K RAMs)

- 250 nanosecond cycle

- byte parity error detection




### Memory Management Unit





- Sun-2 memory management unit

- two-level, multiprocess virtual memory management

- full support for demand paging

- 16 Mbytes virtual address space per process

- separate address spaces for supervisor and user

- valid, accessed, and modified tags to assist paging algorithms

- separate read, write, and execute tags for user and supervisor accesses




### Display Subsystem





- dedicated dual-ported video memory

- 1152 by 900 display format

- 100 MHz video clock

- 67 Hz non-interlaced video refresh




### Ethernet Interface





- VLSI Ethernet controller (Intel 82586)

- digital phase decoder

- packets transferred directly in and out of main memory

- extensive diagnostic capabilities




### Serial I/O Ports





- two programmable serial i/o ports

- based on synchronous communication controller (Zilog 8530)

- software programmable baud rates (75 Baud to 19.2 Kbaud)

- asynchronous, synchronous, and bit-stuffing protocols

- two serial ports for keyboard and mouse




### Other Features





- VME System bus interface

- DVMA (direct virtual memory access) from VME Bus

- optional DES encryption processor (AMD 9518)

- up to 128K bytes EPROM (27128, 27256, 27512)

- five programmable 16-bit timers (AMD 9513)

- software interrupt capability

- software readable identification PROM
- (storing serial number and other information)




### Diagnostic Features





- diagnostic LED display

- bus error register

- watchdog reset timer

- bus timeout timer




## VME-Bus Specification


### Master Capabilities


- Data Bus Size:		D16 MASTER	16-bit/8-bit data

- Address Bus Size:	A24 MASTER	24-bit/16-bit addresses

- Timeout Option:		TOUT(100 USEC)	100 microsecond timeout period

- Sequential Access:	None

- Interrupt Handler:	IH(1-7) STAT	Level 1 through 7, jumperable

- Requestor Option:	ROR R(3)	Release on Request, level 3


### Slave Capabilities


- Data Bus Size:		D16 SLAVE	16-bit/8-bit data

- Address Bus Size:	A24 SLAVE	24-bit-only addresses

- Sequential Access:	None

- Interrupter Options:	None


### System Controller Capabilities


- Clock Option:		SYSCLK		16 MHz, jumperable

- Arbiter Option:		ONE		Bus Request Level 3 Only

Note:	The 2060 Board must be the System Controller in a VME System.


### Power Monitor Capabilities


- ACFAIL Option:		ACFAIL		asserted when VCC < 4.5V

- SYSRESET Option:	SYSRESET	asserted during CPU Reset

- SYSFAIL Option:		SYSFAIL		not used


### Environmental Characteristics


- Operating Temperature:	10 - 55 C

- Humidity:		0 - 90 %, non-condensing


### Power Characteristics


- 12 Amp max at +5 Volt +- 5%

- 0.5 Amp max at +12 Volt +- 5%

- 0.5 Amp max at -12 Volt +- 5%


### Physical Characteristics


- Height:	366.67 mm (14.44")

- Width:	400.00 mm (15.75")

- Depth:	40.64 mm (1.6")

- Weight: 1788 g (64 oz)


---

# User Guide


## Programming


The 2060 Board implements the Sun-2 Architecture, Machine Type 3.
The full architecture is documented in the Sun-2 Architecture Manual
and no attempt is made to repeat this information here.
However, this section does describe the features specific
to this implementation of the architecture.


## MMU Implementation


The MMU of this machine type implements a page number field of 12 bits.
It thus supports a physical address of 23 bits, capable of addressing 8 MBytes.
The other physical address bits in the page map are not implemented.
When read, the not implemented bits are not defined.


## Physical Address Assignments


```


Type	Address		Device				Wait States
------------------------------------------------------------------------------
0	23-bit		Memory Bus

	[0x000000]	Physical Memory	1..8 MBytes	1
------------------------------------------------------------------------------
1	23-bit		I/O Bus

	[0x000000]	Video Memory			1 (Write), 4..8 (Read)
	[0x020000]	Video Control Register		4

	[0x7F0000]	EPROM				4
	[0x7F0800]	Ethernet Interface		4
	[0x7F1000]	Encryption Processor		4..8
	[0x7F1800]	Keyboard/Mouse Interface	4
	[0x7F2000]	Serial Port			4
	[0x7F2800]	Timer				4
	[0x7F3000]	Reserved			4
	[0x7F3800]	Reserved			4
------------------------------------------------------------------------------
2	23-bit		P1-Bus or System Bus

	[0x000000]	0..8 MByte VME 24-bit address	2 + device access time
------------------------------------------------------------------------------
3	23-bit		P1-Bus or System Bus

	[0x000000]	8..16 MByte VME 24-bit address	2 + device access time
	[0x7F0000]	64 KByte VME 16-bit address	2 + device access time
------------------------------------------------------------------------------
			Accesses to the VME Bus incur an additional 2 wait states
			access time if the 2060 board is not currently bus master.

```


## Interrupt Assignments


The following table summarizes the interrupt level assignments
for the devices that have been described in this manual.
All these interrupts are autovectored.


```

-----------------------------------------------------
    7	TIMER1
    6	Serial Port
    5	TIMER2..5
    4	VIDEO
    3	Ethernet or system enable register EN.INT3
    2 	System enable register EN.INT2
    1 	System enable register EN.INT1
------------------------------------------------------

```


In addition, the VME-Bus can cause vectored interrupts on all levels.
Individual VME-Bus interrupt levels can be disabled with jumpers.


## Performance Data


### CPU Speed


The Sun-2060 Board features a CPU clock cycle of 62.5 nsec (16 MHz).


### Video Memory Access Time


Read accesses are unbuffered and will cause 4 to 8 wait states.
Write accesses to the video memory are buffered and thus
execute at the speed of main memory (1 wait state).
However, subsequent write accesses will have to wait
until the video memory has completed the requested operation.
Write accesses to the video memory via the copy mode will cause the
same behavior as direct write accesses.


### P1-Bus Access Times


This section describes the access times of the P1-Bus.
The time to complete a P1-Bus access consists of three elements:
overhead, the cost of P1-Bus acquisition if the 2060 Board
is not currently P1-Bus master,
and the actual access time of the P1-Bus device.

The total number of wait states for a P1-Bus access can be computed
by the following formula:

2 WS (overhead)
+ 2 WS (bus acquisition time if board does not have bus mastership and bus is idle)
+ access time of P1-Bus device divided by the clock period of the CPU
rounded up to the nearest integer number.


### DVMA Access Time


DVMA cycles from the P1-Bus are serviced after the current CPU cycle
completes and after pending memory refresh cycles and
pending Ethernet cycles are executed.
Thus DVMA cycles exhibit a variable access time that ranges from
a best case of 0.5 microseconds to a worst case of 5 microseconds
with an average estimated at 0.65 microseconds.
Thus the 2060 Board offers an average DVMA bandwidth of 3 Megabytes
on 16-bit word transfers.


### P1-Bus Reset


The 2060 Board can be configured either as a P1-Bus Reset Master or Slave.

As a P1-Bus Reset Master, the 2060 Board issues Reset to the VME Bus.
Power-On Reset, Watchdog Reset, and 68020 Reset will all assert P1-Bus Reset.
Other P1-Bus devices may also assert P1-Bus Reset, but this will have
no effect on the on-board CPU and devices.

As a P1-Bus Reset Slave, the 2060 Board receives Reset from the VME Bus,
but does not drive Reset to the VME Bus. The VME Bus Reset
has the same effect as an on-board power-on-reset.

---

## Connectors


This section documents the pinout of all the connectors used on the
Sun 2060 board.


### J603: Serial Port A


```

	1 -
	2 TXDA[]
	3 RXDA[]
	4 RTSA[]
	5 CTSA[]
	6 DSRA[]
	7 GND
	8 DCDA[]
	9 -
	10 -
	11 -
	12 -
	13 -
	14 -
	15 DBA[]
	16 -
	17 DDA[]
	18 -
	19 -
	20 DTRA[]
	21 -
	22 -
	23 -
	24 DDA[]
	25 VEE

```


### J604: Serial Port B


```

	1 -
	2 TXDB[]
	3 RXDB[]
	4 RTSB[]
	5 CTSB[]
	6 DSRB[]
	7 GND
	8 DCDB[]
	9 -
	10 -
	11 -
	12 -
	13 -
	14 -
	15 DBB[]
	16 -
	17 DDB[]
	18 -
	19 -
	20 DTRB[]
	21 -
	22 -
	23 -
	24 DAB[]
	25 VEE

```


### J605: Keyboard/Mouse


```

	1 RXD0[]
	2 GND
	3 TXD0[]
	4 GND
	5 RXD1[]
	6 GND
	7 TXD1[]
	8 GND
	9 GND
	10 VCC
	11 VCC
	12 VCC
	13 -
	14 VCC
	15 VCC

```


### J700: Ethernet


```

	1 -
	2 E.COL+[]
	3 E.TXD+[]
	4 -
	5 E.RXD+[]
	6 GND
	7 VCC (optional)
	8 -
	9 E.COL-[]
	10 E.TXD-[]
	11 -
	12 E.RXD-[]
	13 +12V
	14 -
	15 -

```


### J1800: Video


```

	1 V.VIDEO+[]
	2 V.VIDEO[]
	3 V.HSYNC[]
	4 V.VSYNC[]
	5 VCC
	6 V.VIDEO-[]
	7 GND
	8 GND
	9 GND

```


---

## Jumpers


This section describes all the jumpers used on the board.
In the following listing, each group of jumpers denotes
exclusive combinations. That means, within each group only
one jumper combination may be active at a time.
The default jumper positions are indicate with an asterisk (*).


### Test Jumpers


The following jumpers are factory installed and intended for
test purposes. They are normally not modified.


```


----------------------------------------------------------------
LABEL	PINS	DESCRIPTION IN/OUT
----------------------------------------------------------------
*J200	1-2	connect/disconnect UART clock
----------------------------------------------------------------
*J200	3-4	connect/disconnect CPU clock
----------------------------------------------------------------
*J200	5-6	connect/disconnect FPP clock
----------------------------------------------------------------
 J200	7-8	connect/disconnect Ethernet clock to oscillator
*J200	9-10	connect/disconnect Ethernet clock to CPU clock
----------------------------------------------------------------
 J200	11-12	connect/disconnect FPP clock to oscillator
*J200	13-14	connect/disconnect FPP clock to CPU clock
----------------------------------------------------------------
*J200	15-16	connect/disconnect Refresh Requests
----------------------------------------------------------------
*J201	1-2	connect/disable Timeouts
----------------------------------------------------------------
 J500	1-2	PROM TYPE = 27128/27256+27512
*J500	3-4	PROM TYPE = 27256+27512/27128
*J500	5-6	PROM TYPE = 27128+27256/27512
 J500	7-8	PROM TYPE = 27512/27128+27256
----------------------------------------------------------------
*J1200	1-2	main memory responds to 0M-2M
 J1200	3-4	main memory responds to 2M-4M
*J1200	5-6	main memory responds to 0M-4M
 J1200	7-8	main memory responds to 4M-8M
----------------------------------------------------------------
*J1801	1-2	connect/disconnect 100 MHZ Video Clock
----------------------------------------------------------------

```


---

### Configuration Jumpers


These jumpers allow configuration of the 2060 Board
for specific applications. Default Jumpers are marked with an asterisk (*).


```

----------------------------------------------------------------
LABEL	PINS	DESCRIPTION IN/OUT
----------------------------------------------------------------
*J702	1-2	enable/disable 5 Volt to Ethernet
----------------------------------------------------------------
*J704	1-2	Level 2/Level 1 Ethernet Transceiver
----------------------------------------------------------------
*J800	1-2	DVMA Address Comparator A20=0/1
*J800	3-4	DVMA Address Comparator A21=0/1
*J800	5-6	DVMA Address Comparator A22=0/1
*J800	7-8	DVMA Address Comparator A23=0/1
----------------------------------------------------------------
*J800	9-10	enable/disable VME Arbiter
----------------------------------------------------------------
*J800	11-12	enable/disable VME Reset Master
 J800	13-14	enable/disable VME Reset Slave
----------------------------------------------------------------
*J800	15-16	enable/disable VME System Clock
----------------------------------------------------------------
*J1000	1-2	enable/disable VME Interrupt Level 1
*J1000	3-4	enable/disable VME Interrupt Level 2
*J1000	5-6	enable/disable VME Interrupt Level 3
*J1000	7-8	enable/disable VME Interrupt Level 4
*J1000	9-10	enable/disable VME Interrupt Level 5
*J1000	11-12	enable/disable VME Interrupt Level 6
*J1000	13-14	enable/disable VME Interrupt Level 7
----------------------------------------------------------------
*J1600	1-2	Video Register Sense Bit 0
*J1600	3-4	Video Register Sense Bit 1
*J1600	5-6	Video Register Sense Bit 2
*J1600	7-8	Video Register Sense Bit 3
----------------------------------------------------------------

```


---

# Theory of Operations


This chapter describes the theory of operations of the 2060 Board
and the conventions that are used in the schematics.

## Conventions


This section describes the conventions employed in the schematics
and the documentation of this board.
The discussion assumes that the reader has a working knowledge
of digital electronics and has access to descriptions of the components
used on the board.


---

### Schematics


The schematics is contained in the file with extension ".PRE".
The suffix of the schematics file names reflects the drawing page number.


### Signal Conventions


Whenever possible, standard drawing conventions are employed.
Signal flow is shown from left to right, and top to bottom.

Both active-high and active-low signals are used.
A signal name that is followed by a minus ("-") indicates
that the signal is asserted active low (<0.4V), e.g. OE-.
Conversely, a signal that is not followed by a minus is an
active high signal (>2.0V).

For signals with multiple meanings or synonyms,
the synonyms are listed separated by a slash "/".
For example, the signal name for a read-write signal
that is active low for write is "READ/WRITE-".

Signals that are part of busses are indicated by a common prefix
followed by a number. For example, a 16 bit data bus might be labelled
"D0", "D1", "D2", and so on to "D15".
A group of signals that are part of a signal vector are denoted by
a common prefix separated by the suffix with ".".
For example, all P1 signals start with the prefix "P1.".

Connector signals are distinguished by a suffix of "[]" with an
optional string enclosed inside the square brackets identifying
the connector name.

---

### Component Conventions


Components are identified by component name (e.g. 74LS00),
component location (e.g. U100), and properties if required (e.g. 100-OHM).

Component names (also referred to as Body Name in the wirelist)
indicate the type of component being used. The component name is
derived from the "generic" or industry standard name.
Component names are translated into Diptypes that specify
the physical component associated with the component name.
There is only one diptype for components that are sections
of the same physical package (e.g. four 74LS00 gates form one 74LS00 diptype).
Diptypes are translated by the parts list into manufacturer codes and part names.

Component locations provide a unique designator for the component.
They are chosen to indicate the schematics page on whch the component is located.
For example, component U100 is most likely positioned on page 1.
Component locations consist of one letter followed by one to four digits.
The letter indicates the type of component and is one of:


```

Letter	Component Type
--------------------------------
C	Standard Capacitor
D	Diode
K	Electrolytic Capacitor
L	Inductance
X	Decoupling Capacitor
J       Jumper or Connector
R       Resistor
S       single-in-line component
U       dual-in-line component
--------------------------------

```


Location labels are cross-indexed in the wirelist
into diptype and component names and locations on the schematics.

Component Properties help to further specify a generic component.
Three types of properties are used:


```

Property Meaning		Example	Interpretation
-----------------------------------------------------------------------------
:	Value Specification	:10-UF	This capacitor has a value of 10 UF
=	Reference		=A500	This part is referred as part A500
+	Additive Property	+S40	Add a 40-pin socket to this component
-----------------------------------------------------------------------------

```


---

### State Diagrams


State Diagrams are drawn to the following conventions:

1. Left to right with incrementing state numbers along the horizontal axis.

2. Signal transitions represent the actual logic levels of the named signal.

3. Signals are represented without propagation delays.


---

## Major Blocks


The major logic blocks are:


Power

Initialization

Clocks

CPU

MMU

I/O Devices

Ethernet Interface

Bus Interface

Interrupts

Memory

Video Subsystem


---

## Power


The 2060 Board uses +5V for all of its onboard logic.
It also requires a +12V for the Ethernet transceiver
and a -5V for the RS423 drivers and the Video ECL circuitry.
The -5V is generated from the -12V supply by on-board
regulator [LM337:U137].
Signal [-5VR] connects to the UART connectors pin 25
to terminate that line.

---

## Initialization


The 2060 Board includes a power-on/power-off reset generator
that provides an accurate reset pulse.
The circuit uses a dual comparator [LM393:U133], a 1.2 Volt
reference voltage [LM385:D101], charge capacitor [K:K100],
and resistor network [R:R100..R107].

The first comparator forms a power-on reset generator
by comparing the voltage from the charge capacitor with the
reference. This comparator asserts its output until the
voltage across the charge capacitor corresponds to a VCC of 4.5 Volt.
The second comparator forms a power-off reset generator
by comparing the +5V supply with the reference.
This comparator asserts its output when the +5V supply voltage
is below 4.5 Volt without the charge delay incurred by the
first comparator.
The output of both comparators is wire ORed so that signal
power-on-reset [POR] is active when either comparator
asserts its output.


---

## Oscillators


The 2060 Board has 5 independent clock oscillators on board. They are:


[K1114A:U200], (19.6608 MHz): Constant clock for UARTs and Timer

[K1114A:U201], (64.0000 MHz): CPU clock (4X)

[K1114A:U202], (32.0000 MHz): FPP clock (2X)

[K1114A:U203], (16.0000 MHz): Ethernet clock and VME system clock

[K1114A:U1800], (100.0000 MHz): Video clock


In addition, the Ethernet frontend chip has a local 100.000 MHZ oscillator.

All clock oscillators have disconnect jumpers for ATE test purposes,
which are combined in jumper block [J.16:U200] and jumper [J.2:U1801].
Clock oscillator [K1114A:U202] does not need to be used if the
floating point processor runs at the same speed as the CPU.
It is bypassed by connecting jumper [J.16:U200:11-12] instead
of [J.16:U200:13-14].
Clock oscillator [K1114A:U203] does not need to be used if the
CPU runs at 64.0000 MHZ.
It is bypassed by connecting jumper [J.16:U200:9-10] instead
of [J.16:U200:7-8].


## Derived Clocks


The 64-MHz CPU clock is divided by four in flipflop [74F74:U201]
into two 16-MHz CPU clock trains [C.60,C.60B], separated by one
64-MHz clock period (15.625 nsec). Clock [C.60] is the system clock.

Counter [74LS393:U224] divides the system clock into clocks for
the timeout counter and the refresh clock.
Counter [74LS393:U827-0] divides the constant clock [C.51]
into clock [C.204] for the UART and the Timer.

The clock signals [C.S2, C.S3, C.S4, C.S5, etc] are derived from transitions
on the system clock. The first clock in the chain, [C.S2],
is enabled with processor address strobe [P.AS], whereas
subsequent clocks are enabled with the respective previous clock.
All clocks are cleared when [Q.AS] goes away,
as illustrated in the figure below for a 8-state cycle.


```


68020 State	0   1   2   3   4   5   6   7   0

C.60		----____----____----____----____----

P.AS-		----________________________--------

C.S2		________--------------------________

C.S3		____________----------------________

C.S4		________________------------________

C.S5		____________________--------________

C.S6		________________________----________


```


### RAS Generation


[P2.RAS] is set with [RASON] on the rising edge of [C.60],
corresponding to state 2.
[P2.RAS] stays asserted until [RASOFF] becomes active.
[RASOFF] is asserted when C.S6 is set on the rising edge of [C.60B].
[RASOFF] stays asserted until [P.AS] is deasserted and
clears [C.S6].


```


68020 State	0   1   2   3   4   5   6   7   0

C.60		----____----____----____----____----

C.60B		__----____----____----____----____--

P.AS-		----________________________--------

P.ASON		____------------------------________

C.S6		________________________----________

P.ASOFF		__________________________--________

P2.RAS-		--------__________________----------


```


---

## CPU


### Reset


CPU Reset is generated by PAL [P16R4:U109] under three conditions:


*Power-On-Reset:* The power-on-reset generator asserts [POR]
that causes PAL [P16R4:U109] to assert processor reset.

*External Reset:* If the 2060 Board is configured as a reset slave,
then VME System Reset [P1.SYSR] asserts `RESIN` that causes PAL
[P16R4:U109] to assert processor reset.

*Watchdog Reset:* If the CPU halts it asserts [P.HALT].
In this case, PAL [P16R4:U109] automatically generates processor reset
to continue processing.


The timing diagram below illustrates the watchdog reset circuit
as implemented in PAL [P16R4:U109].
Two internal PAL signals are used in this design.
[S.WD0] is set if [P.HALT] is asserted and [INIT] is deasserted
during [C.16000] active.
[S.WD0] is hold to its previous value when [C.16000] is inactive.
[S.WD1] is set if [S.WD0] is asserted while [C.16000] is inactive.
It remains set during [C.16000] active and at this time also
asserts [INIT] to the CPU.


```


C.16000		________--------________--------________--------

P.HALT-		-----------_____________________----------------

S.WD0-		-----------_____________------------------------

S.WD1-		----------------________________----------------

INIT-		------------------------________----------------


```


### Special Cycles


In the discussion below, reference will be made to "special cycles".
A special cycle is one in which the 68020 function code is
neither program or data. Special cycles are:
CPU space cycles (FC=7), MMU space cycles (FC=3),
and supervisor program fetches in BOOT state.

These conditions are decoded in PAL [P16L8:U106] and cause
signal [Q.SPEC] to be asserted. This inhibits memory CAS
via decoder [74F138:U317], inhibits read-write strobes by
disabling decoder [74F138:U520], and causes the
appropriate DSACK handshaking via PAL [P16L8:102].


### DSACK


The 68020 CPU uses two signals for Data Transfer and Size Acknowledge:
[DSACK0] and [DSACK1].
[DSACK1] is asserted for both 16-bit and 32-bit transfers,
[DSACK0] is asserted for 32-bit transfers only.
Otherwise, the timing for [DSACK0] and [DSACK1] is identical.

[DSACK1] and [DSACK1] is generated by one of three sources:
by PAL [P16L8:U102] for most cycles,
by PAL [P16L8:U106] for MMU cycles,
and by the FPP [68881:U101] for floating point processor cycles.
[DSACK] is asserted as follows:


```

-----------------------------------------------------------------------
Condition			Device		Size	DSACK
-----------------------------------------------------------------------
¬SPEC * (TYPE=0) * READ		Read Memory	32-bit	CS3
¬SPEC * (TYPE=0) * WRITE	Write Memory	32-bit	CS3 * ¬P2.WAIT
¬SPEC * (TYPE=1) * ¬IO * READ	Read Video M.	32-bit	CS7 * ¬P2.WAIT
¬SPEC * (TYPE=1) * ¬IO * WRITE	Write Video M.	32-bit	CS3 * ¬P2.WAIT
¬SPEC * (TYPE=1) * IO		Input/Output	16-bit	CS11 * ¬P2.WAIT
¬SPEC * (TYPE=2 or 3) 		VME Bus		16-bit	CS7 * P1.DTACK
 SPEC * Q.INTA			VME Interrupt	16-bit	CS7 * P1.DTACK
 SPEC * OE.PROM			Boot PROM	16-bit	CS11
 SPEC * R.DMAEN			Refresh Cycle	16-bit	CS3
-----------------------------------------------------------------------
 SPEC * (FC=3)			MMU Access	16-bit	CS5
-----------------------------------------------------------------------
 SPEC * Q.FPP			FPP Access	32-bit	68881
-----------------------------------------------------------------------

```


### BERR


CPU Bus Error, or [P.BERR] is generated by PAL [P16L8:U103] if
an error condition was detected that prevents the current cycle
from completing normally.


```

-----------------------------------------------------------------------
Condition				Description
-----------------------------------------------------------------------
¬SPEC * Q.ERROR				Error on non-special CPU cycle
 SPEC * Q.F7 * P.A17- * P.A16-		Breakpoint Cycle
 SPEC * Q.F7 * P.A17- * P.A16		Ringprotection Cycle
 SPEC * Q.F7 * P.A17  * P.A16- * ¬Q.FPP	Unimplemented Coprocessor Cycle
 S.BERR					Bus Cycle Rerun
 TOUT					Timeout
-----------------------------------------------------------------------

```


When one of these error conditions is present after clock state 5 [C.S5],
PAL [P16L8:U103] asserts [P.BERR], thereby aborting the current bus cycle.
In addition, for all error conditions during CPU cycles except bus cycle rerun,
PAL [P16L8:U103] generates [Q.BERRCLK]
which latches the error condition into the bus error register [ALS534:U511].
The processor can subsequently read this register to determine the cause
of the bus error.
Notice that in case of stacked bus errors the bus error register
will only contain the most recent error condition.

Signal [Q.ERROR] is asserted by gate [74F20:U820]
under one or more of the following conditions:


Invalid Page Entry

Protection Error

Parity Error (any byte)

VME Bus Error


[Q.ERROR] inhibits read-write-strobe decoder [74F138:U520],
aborting any read-write strobe in progress.

---

## P2-Bus Interface


### Introduction


The P2-Bus is the internal bus which interconnects the CPU to
main memory, video memory, and expansion memory.
Going off-board, the P2-Bus is physically routed via
connector [P96:P1102], pins 1 through 32 and 65 through 96,
and connector [P96:P1103], pins 33 through 64).


### P2 Signals


The P2-Bus consists of a number of address lines,
bidirectional data-lines including parity,
timing signals, enable signals, and a handshake line.

Address Lines, Data Lines, Handshake Line:


```

---------------------------------------------------------------------------
P2.Signal	Description
---------------------------------------------------------------------------
P2.A00.23	Address Lines (24)
P2.D00.31	Data Lines (32)
P2.P00.24	Data Lines (4)
P2.WAIT		Negative Handshake
---------------------------------------------------------------------------

```


Timing Signals:


```

---------------------------------------------------------------------------
P2.Signal	Description		Asserted on	Deasserted On
---------------------------------------------------------------------------
P2.RAS		Row-Address-Strobe	C.S2		C.S6 + 15 nsec
P2.R/C		Row/Column-Address	C.S3		¬Q.AS
P2.CAS		Column-Address-Strobe	C.S4		¬Q.AS
P2.R/W		Read/Write Strobe	C.S2		next C.S2
---------------------------------------------------------------------------

```


Enable Signals:


```

---------------------------------------------------------------------------
P2.Signal	Description		Enabled on	Disabled On
---------------------------------------------------------------------------
P2.EN00..24	Byte Enables(4)		Q.AS		¬Q.AS
P2.CASEN	CAS Enable		C.S3		¬Q.AS
P2.RD		P2-Bus Read Strobe	C.S5		¬Q.AS
P2.WR		P2-Bus Write Strobe	C.S5		C.S7
---------------------------------------------------------------------------

```


All timing signals are asserted on every cycle.
The enable signals qualify accesses to main memory and to other
devices on the P2-Bus, such as the video memory.

The P2-Bus byte enables [P2.EN00, P2.EN08, P2.EN16, P2.EN24]
are generated by PAL [P16L8:U107] decoding the
size information on [P.SIZ0, P.SIZ1] in conjunction
with the low-order address bits [P.A00, P.A01] to
enable access to the appropriate bytes.

CAS enable [P2.CASEN] indicates a valid main memory cycle.
CAS enable is generated by decoder [74F138:U317] when the MMU type field is 0
[TYPE0=0, TYPE1=0], the valid bit is set (VALID=1), it is not a special cycle
[Q.SPEC=1], no protection error is present [PROTERR=0], and strobe [C.S3]
is active.

P2-Bus read and write strobes are generated by decoder [74F138:U520] when
the following conditions are met:
the page type is 0 or 1 [TYPE1=0],
the reference is not to an I/O Device [CE.IO=0],
error is not asserted [Q.ERROR=0],
and strobe is asserted [Q.STB=1].


---

### P2-Bus Cycle


The timing for these signals is illustrated in the figure below for a standard
memory write cycle followed by a memory read cycle.


```


68020 State	0   1   2   3   4   5   6   7   0   1   2   3   4   5   6   7   0

C.60		----____----____----____----____----____----____----____----____--

P2.A00..11	xxxx____________________________xxxx____________________________xx

P2.A12..23	xxxxxxxxxxxxxxx_________________xxxxxxxxxxxxxxxx________________xx

P2.D00..31	xxxxxxxxxxxxxxx_________________xxxxxxxxxxxxxxxxxxxxxxxxxxx_____xx

P2.RAS-		--------_________________---------------_________________---------

P2.R/W-		--------________________________________--------------------------

P2.R/C-		------------________________----------------________________------

P2.CAS-		----------------____________--------------------____________------

P2.RD-		----------------------------------------------------________------

P2.WR-		--------------------________--------------------------------------


```


The timing above applies to main memory read cycles and main memory
write cycles that do not have the negative handshake [P2.WAIT] asserted.
Accesses to video memory are similar to main memory read cycles,
except that signal [P2.WAIT] is active.
[P2.WAIT] is asserted by the video memory interface
when it needs to delay the completion of the current cycle.
On read cycles to video memory, [P2.WAIT] is asserted
to delay the current cycle until valid read data is available.
On write cycles to the video memory, [P2.WAIT] is asserted whenever
the video memory is completing a buffered operation and is thus
not yet ready to accept a new cycle. The same mechanism is used
for write operations to main memory shadowed by video memory
(video copy mode).

---

## DVMA Logic


*Reference:* Schematics Page 2, Motorola 68020 Data Sheet.


### Overview


The DVMA Controller takes requests from DVMA devices,
obtains the processor bus from the 68020,
and performs a read/write cycle for the device,
generating appropriate function codes and strobes.

The DVMA Devices in their order of priority are:


- Refresh

- Ethernet

- VME-Bus


Figure [Figure](#a308) shows how the DVMA Controller and Strobe Generator
interface to the 68020.


![Placeholder: a308.press]()


*Figure: **DVMA Controller***

<a id="a308"></a>


---

### DVMA Cycles


DVMA requests are posted in the request flipflops
[74F74:U208-0,U208-1,U209-1]
with the rising edge of the signals [R.REF, E.AS, X.DMA], respectively.
The request flipflops are reset by signals
[R.DMAEN, E.CLR, X.DMAEN], respectively.

Posted DVMA requests are synchronized with register [74F374:U213]
before entering the DVMA controller PAL [P16R8:U214].
The DVMA controller PAL prioritizes the incoming requests,
issues a bus request to the 68020 [P.BR],
then waits for the 68020 releasing the processor bus by
watching 68020 bus grant [P.BG] and the end of 68020 address strobe [P.AS],
before asserting the DVMA enable corresponding to the request.

In addition, the DVMA controller PAL generates a DMA-cycle signal [S.DMA]
that enables the tri-state buffers in the DVMA strobe PAL [P16L8:U215]
to drive the function codes [P.FC0..2], address strobe [P.AS],
and size codes [P.SIZ0,P.SIZ1].
Function Codes and size codes are asserted as follows:


```

-----------------------------------------------------------
    DVMA	Size	FC	Space
-----------------------------------------------------------
    REFRESH	2	7	CPU Space
    ETHERNET	2	5	System Data
    EXTERNAL	2	5	System Data
-----------------------------------------------------------

```


### DVMA Cycle


Arbitration occurs concurrently with ongoing bus activity.
The 68020, after receiving a bus request [P.BR] issues a bus grant [P.BG].
When the DVMA controller sees bus grant and address strobe
[P.AS] from the CPU deasserted, it acquires the bus and asserts the DMA Enable
corresponding to the DMA Request.

Defining the state in which DMA Enable is asserted as state (-1),
DMA address strobe [P.AS] is asserted at state (1)
and stays asserted for one state after signal [S.ASOFF]
is asserted from the DVMA controller PAL.
[S.ASOFF] is asserted when signal [P.DSACK1] is received, indicating
normal completion, or signal [S.BERR], indicating an error completion.
On a normal memory cycle, [S.ASOFF] is asserted on state (7)
and [P.AS] thus will be asserted at state (8).
The DMA Enable is then deasserted at state (9).
This timing, using a refresh cycle as an example, is shown in the diagram below.


```


State	    2   3   4   5   6   7   8   9   0   1   2   3   4   5   6   7   8   9

C.60	    ----____----____----____----____----____----____----____----____----____

R.DMAREQ-   xxxx________________________________------------------------------------

S.RREQ-	    ----________________________________________----------------------------

P.BR-	    ------------________________________------------------------------------

P.BG-	    --------------------________________________----------------------------

P.AS-	    ____________________----------------____________________________--------

P.DSACK-    ----________________------------------------________________------------

S.ACK-	    ------------________________------------------------________________----

S.ASOFF-    ____________________________________________________________------------

R.DMAEN-    ----------------------------________________________________________----

P.BACK-	    ----------------------------________________________________________-----


```


---

## Parity Logic


The parity logic generates parity for memory write operations
and checks parity for memory read operations. Note that the
parity error logic is used only for memory accesses (page type 0).
The parity logic consists of
parity generators [74F280A:U401, U403, U405, U407],
tri-state buffer [ALS244:U410],
parity checkers [74F280A:U400, U402, U404, U406],
parity error latch [74F374:U408]
and parity error PALs [P16R4:U411, U412].

On write cycles to memory, parity out [POUT00..24]
is generated with parity generators, and the parity bits
are driven to memory via the tri-state driver.
If parity generation is enabled [EN.PARGEN=1],
then odd parity is generated.
Odd parity means that the sum of all data bits and the
parity bit is odd.
If parity generation is disabled [EN.PARGEN=0],
then even parity is generated.
This allows to test the parity function.

On read cycles from memory, read data and the read parity bits
are checked in the parity checkers.
The output of the parity checkers is used
for two purposes, synchronous and delayed parity error handling.

Synchronous parity errors are used to abort bus cycles
from DVMA devices (Ethernet or VME-Bus) within the same bus cycle,
that is synchronous. Synchronous parity errors are handled
by PAL [P16R4:U412] which asserts synchronous error [S.ERROR]
when it detects a parity error on a memory read cycle.
[S.ERROR] is also asserted if [Q.ERROR] or [TOUT] are asserted.

Delayed parity error handling is required for the 68020 CPU,
because by the time the parity error is detected the current
cycle can no longer be aborted.
The parity error register [74F374:U408]
and the delayed parity pal [P16R4:U411]
provide the function of latching the parity error information
until it is recognized by the CPU.

The parity error register latches the output of the parity checkers
[PIN00.24] at the trailing edge of [C.S5].
In addition, the type field [TYPE1,TYPE0],
the processor bus error signal [P.BERR],
and the DMA enable signal [S.DMA] are latched at the same time.

If the information stored in the parity error register indicates
a parity error (any one of PIXX asserted) on a memory read cycle
[TYPE0=0,TYPE1=0,P2.R/W-=0] then PAL [P16R4:U411] sets
the parity error bit corresponding to the byte in error
on the next rising edge of [C.S2].

This will cause a bus error to the 68020 on the next cycle in which
the 68020 can recognize a pending parity error.
This is the case when the 68020 executes a non-special cycle.
Under this condition, PAL [P16L8:U103] asserts [P.BERR] and
signal [Q.BERRCLK] which clocks the parity error bits
into the bus error register [ALS534:U511]. The [P.BERR]
asserted in this cycle is clocked into the parity error register
at the end of this cycle, clearing the parity error bit
on [C.S2] at the beginning of the next cycle.

Parity checking can be disabled by deasserting
bit [EN.PARERR] in the system status register.
With [EN.PARERR] deasserted, both synchronous and asynchronous
parity errors are disabled.

---

## Data Ciphering Processor


The Data Ciphering Processor [9518:U506] has special timing requirements
that are implemented by PAL [P16L8:U607].
One requirement of the DCP is that its data strobe [MDS]
may only be deasserted within 70 nsec after trailing edge of its clock [C250].
Other requirements of the DCP are long hold times on data and read/write;
those are achieved by turning off the DCP data strobe early before
the end of the cycle.
The state diagrams below illustrate these timings.


### 68020 Address Load to DCP


```


STATE		 1   3   5   7   9   11  13  15  17

C.60-		_--__--__--__--__--__--__--__--__--__

CS9		_________________--------------------

WR.DCP		---------____________________--------

MAS-		---------________--------------------


```


### 68020 Read/Write to DCP, Best Case


```


STATE		 1   3   5   7   9   11  13  15  17

C.60-		_--__--__--__--__--__--__--__--__--__

C120		_----____----____----____----____----

C240		_____--------________--------________

S5		_________----------------------------

S9		_________________--------------------

MDS_STRT-	----------________________-----------

MDS_END-	----------___________________--------

MDS- 		----------_____________________------

TIME160-	---------------------________--------

TIME240-	-------------------------________----

WAIT- (RD)	---------____________----------------

WAIT- (WR)	---------____________________--------


```


---

## Ethernet Interface


*Reference:* Schematics Page 7, Intel 82586 Ethernet Controller Manual.


### Overview


The Ethernet Interface is built around the Intel 82586
VLSI Ethernet Controller [U700] and the Fujitsu MB502
Phase Lock Loop Decoder [U701], as shown in Figure [Figure](#a312).
The Ethernet Control Register [ALS273:U716, ALS244:U717]
controls the overall operation of the Ethernet interface.


![Placeholder: a312.press]()


*Figure: **Ethernet Interface***

<a id="a312"></a>


### Ethernet Transceiver Interface


The Ethernet Connector [J700] follows the standard Ethernet definition.
Jumper [J.2:J702] supplies +5V to the Ethernet connector for
transceivers that require this voltage.
The Ethernet transceiver drop cable is terminated with resistor
networks [R4.SIP:R704, R705].


### Ethernet Phase Lock Loop Decoder


The Ethernet Frontend uses a digital phase lock loop with 10 samples
per bit cell. An internal oscillator with external crystal X700
together with tank circuit [C:C700,C703,C704,L:L700]
supplies the 100 MHz input frequency to the PLL chip.
Jumper [J.2:J701] selects between Ethernet Level 1 and Level 2
interface characteristics (Level 2 if jumpered).
The Ethernet frontend is interfaced to the Ethernet data link controller
with inverters [74F04:U709] and flipflops [74F74:U710, U712].


### Ethernet Data Link Controller


The Intel 82586 Ethernet Data Link Controller is configured as follows:
Maximum Mode [MN/MX-=0], asynchronous ready [READY=0],
directly enabled [HLDA=HOLD], and always clear to send [CTS-=0].
The 82586 receives an 8 MHz clock from flipflop [74F74:U713-1].
Pullup [R9-SIP:S700] supports the VOH-level required by the 82586.
For a complete description of this part, refer to the Intel 82586 Data Sheet.

The Ethernet read and write buffers are byte swapped between
the processor data bus and the Ethernet data bus.
This means that the processor data bits 0..7 are connected
to Ethernet data bits 8..15 and vice versa.


### Ethernet DVMA Cycle


When the Ethernet controller wants to access main memory,
it asserts either Ethernet read control [E.RD] or write control [E.WR].
Ethernet read and write controls are ored together with gate
[74LS00:U715-3] to generate Ethernet data strobe [E.DS].
The leading edge of Ethernet Data Strobe [E.DS] then
sets the Ethernet DVMA request flipflop [74F74:U207-1].
In addition, the 82586 Hold request [E.HOLD],
ANDed with Ethernet error inactive [E.ERR-] in gate [74F08:U716-0],
presents signal [E.REQ] to the DVMA Arbiter.
This will cause the Arbiter to continuously request the bus from the CPU
until the 82586 drops [E.HOLD].

Ethernet Data Strobe is also clocked at the next
rising edge of the 8 MHz Ethernet clock [E.C-125] to generate
Ethernet address strobe [E.AS].
The leading edge of Ethernet address strobe latches the 24-bit
Ethernet address into the Ethernet address register [ALS374:U702,U703,U704]
to generate Processor Address [P.A01 through P.A23] when enabled
with Ethernet DMA enable [E.DMAEN].
In addition, Ethernet write control [E.WR] is latched into the same
register to generate Processor Read/Write strobe [P.R/W-] when enabled.

At this point, the Ethernet has requested a DVMA cycle
and is waiting for Ethernet DMA enable.
On a write cycle (Ethernet to Memory), the DVMA controller will
enable the Ethernet write data buffers [ALS244:U707,U708]
with Ethernet output enable [E.OE].
On a read cycle (Memory to Ethernet), the DVMA controller will
latch the data read from memory into the Ethernet read data buffers
[ALS374:U705,U706] at the leading edge of acknowledge 8 [S.ACK8].
The Ethernet ready flipflop is set on both read and write cycles
with acknowledge 6 [S.ACK6].

The Ethernet read buffers are output enabled by Ethernet read-1 [E.RD1]
to the Ethernet controller chip. This timing is illustrated in
the diagram below.


```


82586 State	|   T0   |  T1   |  T2   |  T3   |  T4   |

C-125		_----____----____----____----____----____--

E.RD-		-____________________----------------------

E.RD0-		---------________________------------------

E.RD1-		-----------------________________----------


```


If a bus error is encountered during an Ethernet DVMA cycle,
the Ethernet bus error flipflop is set [ALS74:U719-1] causing
the Ethernet Error signal to be asserted [E.ERR].
This signal prevents future Ethernet DVMA requests to be set
in the Ethernet DVMA request flipflop [74F74:U207-1].
The Ethernet bus error flipflop can only be reset by an
Ethernet reset command [E.RESET].

---

## VME Bus Interface


*Reference:* Schematics Page 8, 9, 10, VME Bus Manual.

The VME Bus interface consists of the following functions:


VME Bus Utility Functions (page B08A)

VME Arbiter (page B08A)

VME Master Interface (page B08B)

VME Slave Interface (page B08C)

VME Address and Data Buffers (page B09)

VME Interrupt Handler (page 10)


Figure [Figure](#a313) shows how these functions are interconnected.


![Placeholder: a313.press]()


*Figure: **VME Interface***

<a id="a313"></a>


---

### VME Bus Utility Functions


The VME Bus Utility functions are implemented by these four utility lines:
System Clock [P1.SYSCLK], AC Fail [P1.ACFAIL], System Reset [P1.SYSR],
and System Fail [P1.SYSF].

System Clock [P1.SYSCLK] is driven from the 16 MHz oscillator signal [C.62]
via a high-current driver [74F244:U817-4].
It can be disconnected from the VME Bus by removing jumper [J.16:J800-15.16].

AC Fail [P1.ACFAIL] is driven to the VME Bus by open collector driver
[74ALS6411:U818] whenever Power-On-Reset [POR] is active.
It cannot be disconnected from the VME Bus.

System Reset [P1.SYSR] is either driven to the VME Bus or
received from the VME Bus, depending whether the 2060 Board is configured
as a VME-Bus Reset Master or VME-Bus Slave.

As a VME-Bus Reset Master, the 2060 Board drives [B.RESOUT]
via open collector driver [74ALS6411:U818]
to the VME Bus via jumper [J.16:J800:11-12].
[B.RESOUT] is asserted whenever Processor-Reset is active, which is on
Power-On Reset, Watchdog Reset, and 68020 Reset.
Other VME-Bus devices may also assert VME-Bus Reset, but this will have
no effect on the 2060 board.

As a VME-Bus Reset Slave, the 2060 Board receives Reset from the VME Bus,
but does not drive Reset to the VME Bus. VME-Bus Reset [P1.SYSR] drives
[B.RESIN] via jumper [J.16:J800:13-14].
[B.RESIN] drives [POR] via open collector driver [74ALS6411:U818]
and thus has the same effect as an on-board power-on-reset.

System Fail is not used or generated by the 2060 Board.


### VME Arbiter and Requestor


The VME Arbiter and Requestor functions are implemented as asynchronous
state machine consisting of register [74F374:U812,U813]
PROM [AM27S33A:U811] and PAL [P16L8:U814].
Out of the options possible within the VME Bus Spec,
the arbiter implements the [ONE ROR] arbiter option.
[ONE] means that the arbiter monitors bus request level 3 [P1.BR3] only
and accomplishes arbitration via the level 3 daisy chain [P1.BG3IN,P1.BG3OUT].
[ROR] means "release on request", that is, the arbiter only releases the bus
when a request from another master is pending.

When the CPU wants to access the VME Bus, either for a read cycle [RD.P1],
a write cycle [WR.P1], or for a interrupt acknowledge cycle [Q.INTA]
it asserts signal Bus Select [B.BSEL] via gate [74F20:U820].

If the arbiter currently does not own VME Bus mastership,
it requests bus mastership by asserting VME Bus request out [B.BROUT]
and going through the normal VME Bus arbitration sequence.
If the arbiter already owns bus mastership, it will keep the
bus mastership.
Bus mastership is released when another VME Bus master requests it by asserting
one of the VME Bus request lines [P1.BR0..3], there is no
VME Bus Cycle in progress [P1.AS=0], and the 2060 Board is not
accessing the VME Bus [B.SEL=0].

---

### VME Master Interface


Once the 2060 Board obtains VME Bus mastership, the
VME Master Interface allows the 2060 Board to access VME Slaves
on the VME Bus. The interface consists of address
latches [AM29821:U900,U901,U902],
write data latches [AM29821:U903,U904],
and read data buffers [ALS244:U913,U914].
and control signal driver [74F244:U817-0].

On a normal CPU to VME cycle, in the case the 2060 Board already
owns VME Bus mastership, the following operations happen in sequence.


After [C.S2], PAL [P16L8:U905] asserts signals [B.ACLKEN] and
[B.DCLKEN].

At the rising edge of [C.60] flipflop [74F74:U906] asserts
outputs address clock [B.ACLK] and data clock [B.DCLK].

[B.ACLK] and [B.DCLK] latch the processor address, status,
and input output data lines into the VME address and write data
registers, respectively. On a write cycle, the VME write data
register is output enabled to the VME Bus with [B.DOE].
On read cycles, the register stays disabled and the data
in the write data register is ignored.

At state 5, if the CPU wants to access the VME Bus,
decoder [74F138:U520] asserts [RD.P1] for a read cycle
or [WR.P1] for a write cycle.
For VME interrupt acknowledge cycles, PAL [P16L8:U107]
asserts [Q.INTA] starting at state 4.
[RD.P1], [WR.P1], and [INTA] are or-ed in
gate [74F20:U820] to form bus select [B.BSEL].

At state 6, if [B.SEL] is active, PAL [P16L8:U816]
the VME strobes [B.AS,B.LDS,B.UDS].
These strobes are gated in [74F32:U822] with
[B.CEN] and [B.CS6] before reaching the VME Bus
via driver [74F244:U817].
In addition, the data strobes are gated with address strobe
to guarantee the VME specification.


At this point, the 2060 Board has addresses, write data on write cycles,
and strobes asserted to the VME Bus.
The VME Slave Device being addressed will respond to the transfer
by asserting either data transfer acknowledge [P1.DTACK]
or bus error [P1.BERR].
To recognize the slave acknowledge signals, PAL [P16L8:U816]
must assert [B.DEN] which indicates that [P1.DTACK] and [P1.BERR]
were idle.

[P1.DTACK] and [P1.BERR] are gated with rerun timeout [C.TO3] and
are synchronized in self-latching flipflops [74F74:U823] before
reaching the 68020 CPU.
DTACK reaches the CPU via PAL [P16L8:U102]
and BERR via gate [74F20:U820] and PAL [P16L8:U103].


### 68020 Cycle to VME Bus, Currently Busmaster


```


68020 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C.60		----____----____----____----____----____----____----____----____

P.AS-		----________________________________________________________----

B.BSEL-		--------------------________________________________________----

B.AEN-		________________________________________________________________

B.CEN-		------------------------________________________________________-

P1.AS-		------------------------____________________________________----

P1.DTACK-	-------------------------------------------------_______________


```


### 68020 Cycle to VME Bus, Not Currently Busmaster


```


68020 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C.60		----____----____----____----____----____----____----____----____

P.AS-		----________________________________________________________----

B.BSEL-		--------------------________________________________________----

B.REQ-		------------------------____________________________________----

B.AEN-		--------------------------------________________________________

B.BEN-		----------------------------------------________________________

B.CEN-		----------------------------------------____________________----

P1.AS-		----------------------------------------____________________----

P1.DTACK-	-------------------------------------------------_______________


```


---

### Rerun Cycles


The VME Master interface features a backoff/rerun capability.
This capability is utilized for two cases:
VME Bus deadlock and VME accesses that take longer than 2 usec.


### Deadlock Case


In the deadlock case, the condition is that the CPU is attempting
to access the VME Bus while another master on the VME Bus
is attempting to access the 2060 Board as a slave device.
Since the VME Bus has no rerun capability, the
68020 must yield to the VME Bus request to resolve the deadlock.

The deadlock case is detected in PAL [U815:P16L8] if [B.SEL]
is asserted simultaneously with [X.DMA] and [X.HOLD] is not
asserted. [X.HOLD] indicates that a VME-DMA cycle has been completed.
Under these conditions, a CPU rerun cycle is performed as indicated
in the timing diagram below.


```


68020 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C.60		----____----____----____----____----____----____----____----__

P.AS-		----________________________________________-------------------

X.DMA-		______________________________________________________________

B.RERUN-	------------------------________________________--------------

S.RERUN-	----------------------------________________________----------

S.BERR-		------------------------------------________________----------

S.HALT-		------------------------------------________________________--

P.BERR-		------------------------------------________________----------

P.HALT-		------------------------------------________________________--


```


### Freeze Rerun


In case of a VME access that is not completed within 2 usec,
either because it could not obtain bus mastership or because
it is accessing a slow slave device, a rerun is executed
to allow on-board DVMA devices to access the on-board bus.
Specifically, this allows memory refresh
and Ethernet memory accesses to occur while the CPU is waiting for the bus.
After the onboard DVMA devices complete their operation,
the CPU continues with its VME access.
This operation is transparent to the VME Bus, except for
a slight loss of performance while the rerun is performed.

The VME rerun operation proceeds as follows.


Starting [C.S6] of a VME cycle, counter [74LS393:U827]
starts counting with the falling edges of [C-250X].

After eight input transitions the counter asserts [B.C3].
This signal disables [P1.DTACK] and [P1.BERR]
from reaching the processor any longer.

If either one of the self-latching acknowledge flipflops is set
[74F74:U823] the CPU will complete the cycle as normal
and no rerun will be performed.

If the acknowledge flip-flops [74F74:U823] are not set,
then the rerun sequence will continue.
After four additional clock transitions, counter [74LS393:U827]
asserts both [B.C2] and [B.C3].
This combination is decoded in PAL [P16L8:U815]
and causes an assertion of [B.FREEZE] and [B.RERUN].

[B.FREEZE] causes the VME control signals to be latched
in PAL [P16L8:U816] and the VME addresses and write data
to be latched via PAL [P16l8:U905]
until the CPU resumes the cycle after completion of the rerun.

[B.RERUN] is synchronized in two stages of [74F374:U813]
before entering PAL [P16R4:U109] which asserts [P.HALT]
and [S.BERR]. [S.BERR] causes [P.BERR] via PAL [P16L8:U103].

When the CPU accepts the rerun condition, it will drop address strobe
which clears [C.S6] which clears [B.RERUN] in PAL [P16L8:U815].

At this point the rerun is completed. If bus requests are pending,
such as memory refresh or Ethernet,
the CPU will give up its bus and allow the DVMA activity.
If no more bus requests are pending, the CPU will restart the
frozen VME cycle.


The timeout counter [74LS393:U826] counts the number of bus reruns.
Each assertion of [B.FREEZE] increments the counter by one.
When the counter reaches 128 it asserts VME timeout [B.TOUT].

A timing diagram for a freeze/rerun cycle appears below.


```


C.60		----____----____----____----____----____----____----____----__

P.AS-		----____........____________________--------------------------

P.DTACK-	--------------------------------------------------------------

C.TO3 		____________________------------------------__________________

B.FREEZE-	--------------------__________________________________--------

B.RERUN-	--------------------________________--------------------------

S.RERUN-	----------------------------________--------------------------

P.BERR-		----------------------------________________------------------

P.HALT-		----------------------------________________________----------


```


---

### VME Slave Interface


The VME Slave Interface allows the 2060 Board to be accessed
by other VME Masters on the VME Bus. Such a reference proceeds as follows.


The other VME master obtains mastership of the VME Bus,
asserts the address it wants to access on the 2060 Board,
asserts write data on write cycles,
and asserts VME Address strobe and data strobes
[P1.AS] and [P1.DS].

On the 2060 Board, address comparator [F521:U809] matches the
four high-order address lines from the bus [P1.A20..A23]
against the base address bits [X.A0..A3]
selected by switches [J.16:J800]. In addition,
the VME address modifiers 4 and 5 must be set, [P1.AM4=1, P1.AM5=1],
indicating a 24-bit address space cycle,
the VME interrupt acknowledge must be not set [P1.IACK=0],
and the 2060 Board must not be bus master [B.AEN=0].

If the address comparator matches as described above
and VME address strobe [P1.AS] is asserted
and either VME data strobe [P1.DS0, P1.DS1] is asserted then
signal [X.DMA] is asserted, indicating that a VME Slave Interface
request is pending.

The rising edge of [X.DMA] sets the external DMA request flipflop
[74F74:U208-1] posing an external DMA request [X.DMAREQ] to the
DVMA controller.

In response, the DVMA controller requests the on-board bus from the CPU
and executes an on-board cycle using the external DVMA address
stored in register [ALS374:U910,U911,U912].

On a write cycle, the DVMA controller uses the data buffer
[ALS244:U913,U914] to enable data from the VME bus onto the
internal IO bus and from there on to the processor data bus.

On a read cycle, the data read from memory is stored in register
[AM29821:U903,U904] at a clock edge corresponding to state 8.

At state 9, the VME slave handshaking flipflops are set
with the trailing edge of [X.DMAEN].
If a synchronous bus error [S.ERROR] is present at this time,
the bus error flipflop [74F74:U819-1] is set, asserting [X.BERR].
Otherwise, the DTACK flipflop [74F74:U819-0] is set,
asserting [X.DTACK]. [X.DTACK] and [X.BERR]
are driven to the VME bus with open-collector driver [ALS6411:U818].
Signal [X.DMA] stays asserted until the VME Master drops its data strobes.
This in turn clears the Bus Error and DTACK flipflops [74F74:U819].


---

## Interrupts


The 2060 Board uses both autovectored and vectored interrupts.
Autovectored interrupts are used for all on-board devices;
vectored interrupts are used by the VME Bus.
To the VME Bus, the 2060 Board is a VME Interrupt Handler.
It responds to interrupts on the VME Bus, but does not generate
any interrupts to the VME Bus.
Each VME Interrupt request levels can be individually
enabled or enabled via jumper J1000.

An interrupt is caused if an enabled VME interrupt request line
[B.IRQ1..7] or an on-board interrupt request is asserted.
VME interrupt requests are prioritized by priority decoder [74LS148:U1001]
and generate encoded interrupt lines [B.IPL0..2] feeding PROM [27S33A:U1000].
Onboard interrupt requests feed diretly into PROM [27S33:U1000].
The purpose of the PROM is to encode the highest priority off-board
or on-board interrupt level pending and encode this level
on the 68020 interrupt lines [P.IPL0..2].
The PROM outputs are enabled with [EN.INT] asserted.
If [EN.INT] is deasserted, then the PROM outputs are tri-stated
and pulled up to a inactive high logic level with terminator [R9.SIP:S1001].

Once the 68020 recognizes an interrupt request on [P.IPL0..2],
it starts an interrupt acknowledge cycle. At this point, the logic needs
to arbitrate whether to acknowledge an autovectored or a vectored interrupt,
since both can be pending at the same level at the same time.
This is accomplished by selector [74F151:U1002]
in conjunction with flipflop [74F74:U1000] and PAL [P16L8:U107].

On an interrupt acknowledge cycle, the 68020 issues function code 7 and
sends out the interrupt level being acknowledged on address lines [P.A01..03].
Selector [74F151:U1002] decodes whether an external interrupt request
is pending at the level the 68020 acknowledges.
Selector output [B.XIRQ] is asserted if an offboard interrupt
request is pending at the level being acknowledged by the 68020.
[B.XIRQ] is clocked with [C.S3] in the
onboard/offboard interrupt flipflop [74F74:U1000-0],
asserting output [B.LOCAL-] if input [B.XIRQ] was inactive.
PAL [P16L8:U107] decodes [B.LOCAL-], qualified with [C.S4],
and asserts [P.AUTOV-] for on-board, autovectored cycles [B.LOCAL-=0]
or [Q.INTA-] for off-board, vectored, cycles [B.LOCAL-=1].
Notice that, if both on-board and off-board interrupts are pending,
preference is given to the off-board interrupt.

If [Q.INTA] is asserted, a VME interrupt acknowledge cycle is begun,
including bus acquisition if necessary.
VME interrupt acknowledge cycles that are not completed within the
timeout interval are terminated with a timeout bus error,
causing the 68020 CPU to fetch a spurious interrupt vector
and continue processing.


---

## Memory


### Introduction


The memory subsystem consists of the following functions:


memory array

address multiplexor and driver

control signal driver

CAS decoder


The interconnection of these pieces is shown in the Figure [Figure](#a315).


![Placeholder: a315.press]()


*Figure: **Memory Interface***

<a id="a315"></a>


---

### Memory Interface


The CPU interfaces to the memory via the P2-Bus.
This means that all interface signals are available
on the P2-connector [P96:P1102], allowing a memory
expansion board to be interfaced to the same bus.
The following description applies equally to
the memory on the CPU Board as well as to the expansion memory.


### Memory Organization


Memory is organized as 4 banks of 36 RAM chips of 256K Bits each,
making a total of 144 chips.
Each bank stores 32 data bits plus 4 parity bits
which corresponds to one magabyte plus parity.
Thus total memory capacity is four megabytes.

These banks are decoded as follows:


```

--------------------------------------------------
  RAS Address	A02..A10
  CAS Address	A11..A19
  CAS Bank	A20..A22
--------------------------------------------------

```


### CAS Decoding


CAS to a RAM chip must only be asserted when a valid
read or write cycle to that RAM is executed.
This decoding function is accomplished by the
CAS decoders [74F138:U1200,U1201,U1202,U1203].

Each CAS decoder receives the CAS Bank addresses
[P2.A20,P2.A21,P2.A22], CAS [P2.CAS], and CAS Enable [P2.CASEN]
as inputs. Every decoder also receives an individual byte enable
[P2.EN00..24] corresponding to the RAM chips it selects.


### Memory Signal Drivers


The Address Lines, RAS, and the Write Enable lines are driven by
74F244 drivers with 33 OHM series termination.
Each 18 RAM chips has its own set of drivers for these signals.
CAS is driven directly by the CAS decoders
with 33 OHM series termination.

---

## Video


*Reference:* Schematics Page 16, 17, 18, 19


### Overview


The video subsystem consists of the following functions:


video memory (128 KByte)

video memory controller

data multiplexor

P2-Bus interface

video sync controller

video shifter


The interconnection of these pieces is shown in the Figure [Figure](#a316).


![Placeholder: a316.press]()


*Figure: **Memory Interface***

<a id="a316"></a>


---

### Video Memory and Addressing


The 128 KByte video memory on the board, chips [4416:U1700-U1707, U1710-U1717],
is dual ported for processor access and video refresh.
The memory is organized as 16 kilowords of 64 bits each.
Processor update cycles read 32 bits at a time
or write 8, 16, or 32 bits at a time.
Video refresh cycles read 64-bits at a time.

The address for processor cycles is stored in register [ALS574:U1634]
for the row-address and in register [ALS574:U1635] for the column address.
Register [ALS373:U1636] demultiplexes the multiplexed
row-column address that is taken from main memory bank 0.
This design was necessary to reduce wiring congestion on the printed circuit board.

The address for video cycles comes from counters [74LS393:U1630, U1631],
driven to video RAM address lines via latches [74ALS374:U1632, U1633]
for row and column address, respectively.
Notice that the organization of the 4416 RAM chips requires
an 8-bit row address and a 6-bit column address.
Address lines [V.A0] and [V.A7] are not used for column addressing.

The video address counters are incremented every 640 nsec
with the falling edge of [V.INC-] except during states
without display enable. They are reset to 0 with signal [V.VCLR].


### Video Memory Controller


The video memory controller state machine generates the timing for the
video memory and other basic timing strobes for the video subsystem.
It consists of PROMs [P5X8:U1604,U1605]
and latches [74F374:U1606,U1607].
The state machine is clocked with [V.C-40].

The memory controller has a total of 16 states, enumerated 0 through 15,
that are continuously executed in sequence.
Each state has a duration of 40 nsec, making the 16 state cycle
repeat every 640 nsec.

The memory controller can execute three basic types of cycles:
Idle cycles, Processor update cycles, and Video refresh cycles.
The memory controller executes an idle cycle or
a processor update cycle between states 0 through 7
and a video refresh cycle between states 8 through 15.

*Idle Cycles* are executed between state 0 through 7
if no request is pending [V.SREQ=0]. During an idle cycle,
memory control signals are not asserted.

*Processor Update Cycles:*
Processor Update Cycles are executed between states 0 and 7
if synchronous request is asserted [V.SREQ=1].
During a processor cycle, signals [V.PRA] and [V.PCA] enable the
processor row and column address from the processor address latches
[ALS574:U1634,U1635], respectively,
in time for [V.RAS] and [V.CAS], the row and column address strobe.

*Read Cycle:* A read cycle is executed if a read signal
[V.READ=1] is latched in the request latch [ALS374:U1615].
On a read cycle, all video memory RAMs are cycled,
accessing 64 bits of data that are latched in the read data port
[74LS374:U1740..U1747] at the rising edge of signal [V.ACK].
PAL [P16L8:U1620] decodes word select [V.BS] to enable
which half of the read data port is enabled to the P2-Bus data lines.
If [V.BS=0] then [V.RD0] is asserted enabling data bits [0..31],
else if [V.BS=1] then [V.RD1] is asserted enabling data bits [32..63].

*Write Cycle:* A write cycle is executed if no read signal
[V.READ=0] is latched in the request latch [ALS374:U1615].
The operation of a write cycle is the same as on a read cycle,
except that those RAMs to be written into are write enabled
and the corresponding write data is driven to the RAMs by
enabling the appropriate outputs of the write data port
[74LS374:U1730..U1737].
This is accomplished by decoding the word select line [V.BS]
and the four byte enable strobes [V.EN00..24] in PAL [P16L8:U1616],
generating the appropriate write enable strobes [V.W00..56] when
RAM write enable [V.WE-] is asserted.
Notice that [V.WE] becomes active at state 3 for early write-cycle timing.

*Video Refresh Cycle:*
Video refresh cycles are executed during every memory controller cycle
between state 8 and 15.
During a video refresh cycle, signals [V.PRA] and [V.PCA] enable the
video row and column address contained in counters [74LS393:U1630]
and [74LS393:U1631].
Video memory data is read out 64-bits in parallel and
is latched at the end of state 15 in the video data register
[74LS374:U1720-U1727] with the trailing edge of [V.VCA-].
In addition to executing the video refresh cycle,
the current memory controller state is decoded in decoder [74F138:U1728]
to enable consecutive bytes from the video data register
onto video output bus [V.O0-V.O7] via control lines
[V.OE00..56].
The sequence of output enables is [V.OE24,16,08,00,56,48,40,32].
One byte from the video data register is enabled every two states
and latched into the video shifters [74F194:U1805, U1806].


---

### Video State Machine


```

SREQ=0
--------------------------------------------------------------------------------
State		0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
--------------------------------------------------------------------------------
V.OE		0       1       2       3	4       5       6       7

V.C-40		--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__

V.RAS-		--------------------------------------------____________________

V.CAS-		____------------------------------------------------____________

V.VRA-		--------------------------------________________----------------

V.VCA-		------------------------------------------------________________

V.PRA-		________________------------------------------------------------

V.PCA-		----------------________________--------------------------------

V.G-		____------------------------------------------------____________

V.W-		----------------------------------------------------------------

V.HCLK		________--------________________________________________________

V.ENREQ		----____________________________________________________________

SREQ=1
--------------------------------------------------------------------------------
State		0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
--------------------------------------------------------------------------------
V.OE		0       1       2       3	4       5       6       7

V.C-40		--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__

V.RAS-		------------____________________------------____________________

V.CAS-		____----------------________________----------------____________

V.VRA-		--------------------------------________________----------------

V.VCA-		------------------------------------------------________________

V.PRA-		________________------------------------------------------------

V.PCA-		----------------________________--------------------------------

V.G-		____----------------________________----------------____________

V.W-		------------________________________________--------------------

V.ACK-		____________________________________----________________________

V.HCLK		________--------________________________________________________

V.ENREQ		----____________________________________________________________


```


---

### P2-Bus Interface


Major components of the P2-Bus Interface Logic are
Address Decoding, Request Generation, and Interrupt Logic.


### P2-Bus Address Decoding


The video board responds to three types of accesses:
direct reads, direct writes, and copy writes.

For direct reads and direct writes, the video logic is selected
if the four most significant P2 address bits [P2.A20..A23] are all ones.
In that case, decoder [ALS138:U1621] produces signal [V.BSEL-],
which generates a video request via PAL [P16L8:U1620].

Copy writes occur if the copy comparator [LS2521:U1623]
matches P2 address bits [P2.A17..P2.A22] with video base address bits
[V.BASE1..6] and if copy mode is set [V.COPY=1] in the control register.
If all of these conditions are true then
comparator [LS2521:U1623] generates [V.CSEL-]
which generates a video request via PAL [P16L8:U1620].

PAL [P16L8:U1620] also decodes [P2.A17] in direct mode [V.BSEL=1]
to generate the read/write strobes for the video control register
[ALS273:U1610,U1611].


### P2-Bus Read/Write Cycles


The video board implements buffered write cycles and unbuffered reads.
Reads follow the traditional conventions of memory systems.
When the processor reads from the video board,
the video board performs the desired access and returns the data read
to the processor. Since the memory on the video board is dual-ported
and asynchronous to the processor, the processor will have to wait
until the read data is available. This is implemented by the video
board asserting the [P2.WAIT] signal until the read data is ready.

Write cycles, on the other hand, are buffered.
The video board provides a set of registers that store all information
related to a write cycle, effectively implementing a 1-deep FIFO.
This means that on a write cycle the processor does needs not to wait
until the dual-ported video memory is available. Instead, the write cycle
is automatically completed with the data stored in the registers.
A second write, however, can only be initiated when the
first write cycle has been completed.
This is done by asserting the [P2.WAIT] signal
if a write cycle to the video board is attempted
while a previous request is still in progress.

An interesting case occurs if a write cycle is immediately
followed by a read cycle. In this case, the write cycle is
still in progress while the new read cycle is pending.
The design of the request logic assures that the read cycle
is only begun after the write cycle has been completed.

This read/write cycle handshaking is implemented in PAL [P16L8:U1620].
A request is set when the video section is addressed in with a
read or write cycle in direct mode [V.BSEL] or
with a write cycle in copy mode [V.CSEL]. Signal [BUSY], causing
[P2.WAIT], is set while a request is in progress.

The leading edge of the request signal [V.REQ]
clocks the demultiplexed processor address
into the processor address register [ALS534:U1634, U1635].
It also clocks the long-word address bit [P2.A02],
the byte enable bits [P2.EN00..24],
and the P2-Bus write line [P2.WR] into register [74F374:U1615].

[V.REQ] is sampled with signal [V.ENREQ] into flipflop
[74F74:U1624-0]. The sampled signal is reclocked on the next clock edge
of [V.C-40] into flipflop [74F74:U1624-1] and
becomes signal [V.SREQ]. This signal
controls the memory state machine to perform either
a CPU cycle [V.SREQ=1] or an idle cycle [V.SREQ=0].


---

### P2-Bus Interface Timing


```


-------------------------------------------------------------------
READ CYCLE

P2.RD-	-------________________________----------------------------

V.RDACK------------------------________----------------------------

V.REQ-	-------________________------------------------------------

V.ACK-	-----------------------____--------------------------------

V.BUSY-	-------________________------------------------------------

-------------------------------------------------------------------
WRITE CYCLE

P2.WR-	-------____------------------------------------------------

V.RDACK------------------------------------------------------------

V.REQ-	-------________________------------------------------------

V.ACK-	-----------------------____--------------------------------

V.BUSY-	-----------____________------------------------------------

-------------------------------------------------------------------
WRITE CYCLE FOLLOWED BY WRITE CYCLE

P2.WR-	-------____--------____________----------------------------

V.RDACK------------------------------------------------------------

V.REQ-	-------________________----______________------------------

V.ACK-	-----------------------____--------------____--------------

V.BUSY-	-----------____________--------__________------------------

-------------------------------------------------------------------
WRITE CYCLE FOLLOWED BY READ CYCLE

P2.WR-	-------____------------------------------------------------

P2.RD-	-------____--------____________________________------------

V.RDACK------------------------------------------______------------

V.REQ-	-------________________----______________------------------

V.ACK-	-----------------------____--------------____--------------

V.BUSY-	-----------______________________________------------------


```


---

### Video Controller


The video controller generates the timing for the video monitor.
The following description applies to the "standard Sun-2 video monitor".
This video monitor has the following attributes:


```

    Visible Display	1152 pixels by 900 lines
    Video Clock:	10 nsec		100 MHz
    Horizontal Cycle:	16.00 usec    	62.5 kHz
    Vertical Cycle:	15000 usec	66.66 Hz
    Horizontal Retrace:	4.48 usec
    Vertical Retrace:	600 usec

```


Video controller latch [74F374:U1812] latches the outputs of
horizontal and vertical decoding PROM on the rising edge of [V.HCLK].


### Horizontal State Machine


Horizontal counter [74LS393:U1810] is advanced every 640 nsec with the
falling edge of clock [V.HCLK].
Horizontal counter is reset with [V.HRESET] generated by video controller latch.

Horizontal decode PROM [P9X4:U1811] decodes horizontal counter inputs
[V.H0] through [V.H6], plus vertical blank [VBLANK]
from the vertical state machine.
Horizontal decode PROM outputs are [V.HRESET, V.HSYNC, V.DISPEN].


### Horizontal State Machine Timing Diagram


```


Signal	State

STATE+1	0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2
	0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5

HCLK 	-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

DISPEN	------------------------------------________________

HSYNC	____________________________________--------________

HRESET	--__________________________________________________


```


### Vertical State Machine


Vertical counter [74LS393:U1813,U1814] is advanced on falling
edge of horizontal sync [V.HSYNC].
Vertical counter is reset with [V.VRESET] from video controller latch.

Vertical decode PROM [P9X4:U1815] decodes vertical counter states
[V.VSTATE1..7], the AND of [V.VSTATE8..9], and [V.VSTATE10].
Vertical decode PROM outputs are [V.VSYNC, V.RESET, V.VBLANK].RESET-.
The vertical decode PROM function is defined in PROM A1815.


### Vertical State Machine Timing Diagram


```

Signal	State

STATE+1	0 0 0 0 0 0 0 0 ... 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 ... 9 9 9 9
	0 0 0 0 0 0 0 0 ... 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 ... 3 3 3 3
	0 1 2 3 4 5 6 7 ... 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 ... 5 6 7 8

VCLK	-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

VBLANK	____________________--------------------------------------------

VSYNC	________________________--------------------____________________

VRESET	______________________________________________________________--


```


### P2-Bus Interrupt Logic


Interrupt flipflop (74F74:U1803-1) is set at the leading edge
of [V.VBLANK] as long as interrupt enable [V.INTEN] is enabled.

---

### Video Clock and Shifter


The 100 MHz video clock [V.C-10] that is generated by crystal oscillator
[K1114A:U1800] is buffered by gate [74F08:U1808-0] and is then
divided into a 50 MHz clock by flipflop [74F112:U1801-0].

The video data [V.O0..7] is loaded into two 50 MHz shift register,
[74F194:U1805, U8106],
one shifting the odd and one the even bits, respectively.
A pair of odd and even bits [V.VID0,V.VID1]
together with 10 nanosecond clock [V.C-10-]
and 20 nanosecond clock [V.C-20] is converted from TTL
to ECL levels by converter [10H124:U1807]
and drives the 100 MHz shift register [10H141].
Since both true and inverted data is loaded into the shifter,
differential output levels [VIDEO-,VIDEO+] are available on its outputs.
The differential outputs are terminated with 390-OHM resistors
[R:R1800,R1801] to [-5V] and are intended to drive
differential ECL terminated with 100-OHM.

The timing is illustrated in the figure below.


```


V.C-10		--__--__--__--__--__¬-__--__--__--__--__--__--__--__--__--__--__

V.C-20		----____----____----____----____----____----____----____----____

V.C-40		--------________--------________--------________--------________

V.STATE0	________________----------------________________----------------

V.DISPEN	--------------------------------________________________________

V.LOAD		________________----------------________________________________

V.LDEN		________________________--------________________________________

V.LD		________________________________--------________________________

V.ELD		----____----____----____----____----____----____----____----____

V.ECLK		__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--


```
