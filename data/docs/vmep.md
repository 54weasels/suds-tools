---


---


# Sun 2250 CPU Board


# Engineering Manual


Company Confidential

Sun Microsystems Inc.

Part Number: 800-XXXX-01

Revision: Draft of [date]


>
This manual describes the Sun 2250 VME CPU board. On a standard
VME Eurocard formfactor, the 2250 CPU board contains a 68010 CPU,
Sun-2 MMU, a VLSI Ethernet interface, a Master/Slave VME interface,
VMEBus arbiter and system controller capabilities,
a programmable serial port with full modem control,
a multi-function timer, boot PROMs, IDPROM, diagnostic LEDs,
and a watchdog timer.

The Sun 2250 CPU board works in conjunction with the Sun 2251 memory board.
On a standard VME Eurocard, the 2251 memory board contains two megabytes
of high-speed dynamic main memory with byte parity error detection.
CPU and memory boards communicate via a private P2-Bus.
From one to four 2251 memory boards can be used,
providing a total of two to eight megabytes of main memory.


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


- 32-bit VLSI CPU

- 10 MHz operation with no wait states to main memory

- multiprocess, demand paging virtual memory management

- 16M bytes virtual address space per process


### I/O


- integral Ethernet interface transfers directly into memory

- one programmable serial I/O ports with full modem control


### Other Features


- VME System Bus Interface

- DVMA (direct virtual memory access) from VME Bus

- five programmable 16-bit timers

- 32K to 128K Bytes EPROM

- extensive self-diagnostic capabilities

- standard VME Eurocard form factor


---

## Introduction


The Sun-2250 CPU board in conjunction with the Sun 2251 memory board
is a high-performance implementation
of the Sun-2 architecture on standard VMEbus Eurocards.

The 2250 CPU board is based on the Motorola 68010 32-bit VLSI CPU,
extended with the Sun-2 virtual memory management unit (MMU).
The processor executes from the 2251 memory baards
at 10 MHz without wait states.
The Sun-2 MMU was specifically optimized to support the
demand paging requirements of the the 4.2 BSD version of the Unix (TM)
operating system. It provides multiple, simultaneous process contexts
with up to 16 megabyte virtual memory space each. In addition,
the MMU provides separate address spaces for the system and for the user.

The 2251 memory board contains two megabytes of high-speed dynamic
main memory, based on 256K RAM technology.
CPU and memory boards communicate via a private P2-Bus.
A 2050 CPU board supports up to four 2251 memory boards,
providing a total of two to eight megabytes of main memory.
Memory is equipped with byte parity error detection.

The Sun-2250 CPU board includes an integral Ethernet interface.
This interface uses a VLSI Ethernet controller that features
high-performance frame handling and extensive diagnostic capabilities.
Ethernet packets are directly transferred in and out of main memory
through the use of direct virtual memory access (DVMA).
For serial I/O, a highly programmable serial communication channel is provided
featuring software programmable baud rates from 75 Baud to 19.2 KBaud
and supporting asynchronous, synchronous, or bit-stuffing protocols.

The Sun-2250 Board includes a bidirectional interface to the VME Bus
with master and slave capabilities.
The board provides 24-bit address and 16-bit data transfer capabilities
in both directions. It also implements system controller functions such as
arbitration, interrupt handling, reset, and power monitoring.

Other features of the board include programmable timers,
an identification PROM (IDPROM) providing
software-readable serial number and Ethernet address,
and extensive facilities for software and hardware diagnostics.
Among them are a bus-error register, a diagnostic display for
displaying error messages, and a watchdog timer for automatic restart.


---

## Sun-2 Architecture Overview


The 2250 Board implements a Sun-2 architecture machine.
The complete specification of the architecture is contained
in the Sun-2 Architecture Manual.
The following is a brief overview of the architecture and its
implementation on the 2250 Board.

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
The ID-PROM contains a unique serial number and configuration
data for a particular implementation of the architecture.

The Device space of the Sun-2 architecture defines what devices
exist in the architecture and how they are accessed.
These devices include main memory, the system bus, and I/O devices.

All CPU accesses to device space pass through the MMU
and thus are translated and protected in an identical fashion.
In addition, direct memory accesses by I/O devices
also pass through the memory memory management and thus
operate in a fully protected environment.

---

## 2250 Board Block Diagram


Figure [Figure](#a11) illustrates how the CPU, MMU, and devices
are interconnected on the 2250 Board.


![a11.press](../svg/a11.drw.O.svg)


*Figure: **Sun 2250 Board Architecture***

<a id="a11"></a>


The CPU sends out a virtual address that is translated by the MMU
into a physical address.
The CPU, Ethernet Interface, and VME Slave Interface
arbitrate for and share the virtual address bus on the left side of the MMU.
The VME Master Interface, P2-Bus Main Memory, and I/O Devices
are addressed with physical addresses on the right side of the MMU.


---

## Sun-2 MMU Overview


The Sun-2 Memory Management Unit provides address translation, protection,
sharing, and memory allocation for multiple processes executing on the CPU.

The memory management consists of a context register, a segment map,
and a page map.
Virtual addresses from the processor are translated into intermediate
addresses by the segment map and then into physical addresses by the page map.

The memory management uses a page size of 2K Bytes and
a segment size of 32K Bytes (giving 16 pages per segment).
Up to 8 contexts can be mapped concurrently.
The maximum virtual address space for each context is 16M Bytes.

Figure [Figure](#a12) shows how virtual addresses are translated into
physical ones.


![a12.press](../svg/a12.drw.O.svg)


*Figure: **Sun-2 Memory Management***

<a id="a12"></a>


---

## Specification Summary


### CPU





- M68010 CPU, 10 MHz




### Memory





- 2M to 8M Bytes of main memory with 2251 memory boards

- high-speed, no-wait state operation

- transparent hardware memory refresh

- byte parity error detection

- private, high-speed bus to memory




### Memory Management Unit





- Sun-2 memory management unit

- two-level, multiprocess virtual memory management

- full support for demand paging

- 16M Bytes virtual address space per process

- separate address spaces for supervisor and user

- valid, accessed, and modified tags to assist paging algorithms

- separate read, write, and execute tags for user and supervisor accesses




### Ethernet Interface





- VLSI Ethernet controller (82586)

- digital phase decoder

- packets transferred directly in and out of main memory

- extensive diagnostic capabilities




### Serial I/O Ports





- one programmable serial I/O port

- based on synchronous communication controller (8530)

- software programmable baud rates (75 baud to 19.2 kilobaud)

- asynchronous, synchronous, and bit-stuffing protocols




### Other Features





- VME System bus interface

- DVMA (direct virtual memory access) from VME Bus

- up to 128K Bytes EPROM (27128, 27256, 27512)

- five programmable 16-bit timers (AMD 9513)

- software interrupt capability

- software readable identification PROM
- (for serial number, EThernet address, and other information)




### Diagnostic Features





- diagnostic LED display

- bus error register

- watchdog reset timer

- bus timeout timer




### VMEbus Master Capabilities


- Data Bus Size:		D16 MASTER	16-bit/8-bit data

- Address Bus Size:	A24 MASTER	24-bit/16-bit addresses

- Timeout Option:		TOUT(5 USEC)	5 microsecond timeout period

- Sequential Access:	None

- Interrupt Handler:	IH(1-7) STAT	Level 1 through 7, jumperable

- Requestor Option:	ROR R(3)	Release on Request, level 3


### VMEBus Slave Capabilities


- Data Bus Size:		D16 SLAVE	16-bit/8-bit data

- Address Bus Size:	A24 SLAVE	24-bit-only addresses

- Sequential Access:	None

- Interrupter Options:	None


### VMEBus System Controller Capabilities


- Clock Option:		SYSCLK		16 MHz, jumperable

- Arbiter Option:		ONE		Bus Request Level 3 Only

Note:	It is recommended that the 2250 Board is the VME System Controller


### VMEBus Power Monitor Capabilities


- ACFAIL Option:		ACFAIL		asserted on powerup

- SYSRESET Option:	SYSRESET	asserted during CPU Reset

- SYSFAIL Option:		SYSFAIL		not used


### Environmental Characteristics


- Operating Temperature:	10 - 55 C

- Humidity:		0 - 90 %, non-condensing


### Power Characteristics


- 6 Amp max at +5 Volt +- 5%

- 0.5 Amp max at +12 Volt +- 5%

- 0.5 Amp max at -12 Volt +- 5%


### Physical Characteristics


- Height:	233.33 mm

- Width:	160.00 mm

- Weight: 500 g


---

# User Guide


## Programming


The 2250 Board implements the Sun-2 Architecture, Machine Type 2.
The full architecture is documented in the Sun-2 Architecture Manual
and no attempt is made to repeat this information here.
However, this section does describe the features specific
to this implementation of the architecture.


## MMU Implementation


The MMU of this machine type implements a page number field of 12 bits.
It thus supports a physical address of 23 bits, capable of addressing 8M Bytes.
The other physical address bits in the page map are not implemented.
When read, those bits not implemented remain undefined.


## Physical Address Assignments


```


Type	Address		Device				Wait States
------------------------------------------------------------------------------
0	23-bit		Memory Bus

	[0x000000]	Physical Memory	2..8M Bytes	0
------------------------------------------------------------------------------
1	23-bit		I/O Bus

	[0x7F0000]	EPROM				2
	[0x7F0800]	Ethernet Interface		2
	[0x7F1000]	reserved			2
	[0x7F1800]	reserved			2
	[0x7F2000]	Serial Port			2
	[0x7F2800]	Timer				2
	[0x7F3000]	Reserved			2
	[0x7F3800]	Reserved			2
------------------------------------------------------------------------------
2	23-bit		P1-Bus or System Bus

	[0x000000]	0..8M Bytes VME 24-bit address	1 + device access time
------------------------------------------------------------------------------
3	23-bit		P1-Bus or System Bus

	[0x000000]	8..16M Bytes VME 24-bit address	1 + device access time
	[0x7F0000]	64K Bytes VME 16-bit address	1 + device access time
------------------------------------------------------------------------------
			Accesses to the VME Bus incur an additional 2 wait states
			access time if the 2250 board is not currently bus master.

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
    4	reserved for VIDEO
    3	Ethernet or system enable register EN.INT3
    2 	System enable register EN.INT2
    1 	System enable register EN.INT1
------------------------------------------------------

```


In addition, the VME-bus can cause vectored interrupts on all levels.
Individual VME-bus interrupt levels can be disabled with jumpers.


## Performance Data


### CPU Speed


```


CPU clock cycle:	101.72 nsec (9.8304 MHz)
CPU basic cycle:	406.90 nsec


```


### P1-Bus Access Times


This section describes the access times of the P1-Bus.
The time to complete a P1-Bus access consists of three elements:
overhead, the cost of P1-Bus acquisition if the 2250 Board
is not currently P1-Bus master,
and the actual access time of the P1-Bus device.

The total number of wait states for a P1-Bus access can be computed
by the following formula:

1 WS (overhead)
+ 2 WS (bus acquisition time if board does not have bus mastership and bus is idle)
+ access time of P1-Bus device divided by the clock period of the CPU
rounded up to the nearest integer number.


### DVMA Access Time


DVMA cycles from the P1-Bus are serviced after the current CPU cycle
completes and after pending memory refresh cycles are executed.
Thus DVMA cycles exhibit a variable access time that ranges from
0.7 microseconds in the best case to 1.5 microseconds worst case
with an average of about 1.0 microseconds.

After a DVMA cycle has executed, a CPU cycle will start
before another DVMA cycle is granted. This means that the cycle time
for DVMA is one DVMA cycle plus at least one CPU cycle.
Thus the DVMA cycle time will be in the range of 1.1 to 1.9 microseconds
with an average of 1.4 microseconds,
as long as the DVMA master can generate transfers at this rate.


### P1-Bus Reset


The 2250 Board can be configured either as a P1-Bus Reset Master or Slave.

As a P1-Bus Reset Master, the 2250 Board issues Reset to the VME Bus.
Power-On Reset, Watchdog Reset, and 68010 Reset will all assert P1-Bus Reset.
Other P1-Bus devices may also assert P1-Bus Reset, but this will have
no effect on the on-board CPU and devices.

As a P1-Bus Reset Slave, the 2250 Board receives Reset from the VME Bus,
but does not drive Reset to the VME Bus. The VME Bus Reset
has the same effect as an on-board power-on-reset.

---

## Connectors


This section documents the pinout of all the connectors used on the
Sun 2250 board.


### J1: Serial Port


```

	---------------------------------
	| PIN |	SIGNAL	| PIN |	SIGNAL  |
	---------------------------------
	|  1  |	----	| 14  | ----	|
	|  2  | TXDA[]	| 15  | DBA[]	|
	|  3  | RXDA[]	| 16  | ----	|
	|  4  | RTSA[]	| 17  | DDA[]	|
	|  5  | CTSA[]	| 18  | ----	|
	|  6  | DSRA[]	| 19  | ----	|
	|  7  | GND	| 20  | DTRA[]	|
	|  8  | DCDA[]	| 21  | ----	|
	|  9  | ----	| 22  | ----	|
	| 10  | ----	| 23  | ----	|
	| 11  | ----	| 24  | DAA[]	|
	| 12  | ----	| 25  | ----	|
	| 13  | ----	| --  | ----	|
	---------------------------------

```


### J3: Ethernet


```

	---------------------------------
	| PIN |	SIGNAL	| PIN |	SIGNAL  |
	---------------------------------
	|  1  |	----	|  9  | E.COL-	|
	|  2  | E.COL+  | 10  | E.TXD-	|
	|  3  | E.TXD+	| 11  | ----	|
	|  4  | ----	| 12  | E.RXD-	|
	|  5  | E.RXD+	| 13  | +12V	|
	|  6  | GND	| 14  | ----	|
	|  7  | VCC	| 15  | ----	|
	|  8  | ----	| --  | ----	|
	---------------------------------

```


---

## Jumpers


This section describes all the jumpers used on the board.
These jumpers allow configuration of the 2250 Board
for specific applications.
Default Jumpers are marked with an asterisk (*).


```

---------------------------------------------------------
| LABEL | PINS	| DESCRIPTION IN/OUT			|
---------------------------------------------------------
| J500	| 1-2	| PROM TYPE = 27128			|
|*J500	| 3-4	| PROM TYPE = 27256 or 27512		|
|*J500	| 5-6	| PROM TYPE = 27128 or 27128		|
| J500	| 7-8	| PROM TYPE = 27512			|
---------------------------------------------------------
| J800	| 1-2	| Enable/Disable VME Reset Slave	|
|*J800	| 2-3	| Enable/Disable VME Reset Master	|
|*J800	| 4-5	| Enable/Disable VME System Clock	|
|*J800	| 6-7	| Enable/Disable VME Arbiter		|
---------------------------------------------------------

```


The jumper positions for different PROM sizes are summarized in the table below.


```

---------------------------------
| PROM 	| JUMPER| JUMPERED PINS	|
---------------------------------
| 27128	| J500	| 1-2 and 5-6	|
| 27256	| J500	| 3-4 and 5-6	|
| 27512	| J500	| 3-4 and 7-8	|
---------------------------------

```


---

# Theory of Operations


This chapter describes the theory of operations of the 2250 Board
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

IO-Bus Interface

MMU

I/O Devices

P2-Bus Interface

Ethernet Interface


---

## Power


*Reference:* Schematics Page 19

The 2250 Board uses +5V for all of its onboard logic.
It also requires a +12V for the Ethernet transceiver
and +-12V for the RS423 drivers.

---

## Clock Oscillators


*Reference:* Schematics Page 2

The 2250 Board has 2 independent clock oscillators on board. They are:


10-MHz CPU clock and system clock (19.6608 MHz) [K1114A:U200].

Ethernet clock and VME system clock (16.0000 MHz) [K1114A:U202].


In addition, the Ethernet PLL [82501:U701] has its own
crystal oscillator with a frequency of 20 MHz.


## Derived Clocks


The system clock is divided by two in flipflop [74F74:U202-0].
Counter [74LS590:U211] divides the system clock into clocks for
the UART, the timer, and the refresh clock.

The clock strobes [C.S4, C.S5, etc] are derived from transitions
on the system clock and enabled with processor address strobe [P.AS]
as illustrated in the figure below for a 12-state cycle.


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12

C.100		----____----____----____----____----____----____----

P.AS-		--------____________________________________--------

C.S4		________________----------------------------________

C.S5		____________________----------------------------____

P.DTACK-	----------------------------________________--------


```


---

## CPU


*Reference:* Schematics Page 1


### Reset


CPU Reset is generated by PAL [P16R4:U109] under three conditions:


*Power-On-Reset:* The power-on-reset driver [ALS641:U818] asserts [POR]
that causes PAL [P16R4:U109] to assert processor reset.

*External Reset:* If the 2250 Board is configured as a reset slave,
then VME System Reset [P1.SYSR] asserts `RESIN` via [ALS641:U818]
that causes PAL [P16R4:U109] to assert processor reset.

*Watchdog Reset:* If the CPU halts it asserts [P.HALT].
In this case, PAL [P16R4:U109] automatically generates processor reset
to continue processing.


### Special Cycles


In the discussion below, reference will be made to *special cycles*.
A special cycle is one in which the 68010 function code is
neither program or data. Special cycles include CPU space cycles
(FC=7) and MMU space cycles (FC=3).
Supervisor program fetches in Boot state,
which are forced to read from the Boot PROM,
are also treated as special cycles.

Special cycles are recognized in PAL [P16L8:U101] and cause
signal [Q.SPECIAL] to be asserted. [Q.SPECIAL] inhibits
the assertion of [Q.CAS] in flipflop [74F74:U205-0],
inhibits the assertion of [P.BERR] in PAL [P16L8:U103],
and selects signal [SPWAIT] as source for DTACK in selector [74F151:U118].
Thus during special cycles no bus errors can occur,
and the source for the [DTACK] is [SPWAIT].


### DTACK


The CPU uses a number of handshake signals to generate
the timing required by the devices it is accessing.
The following table gives the source of the DTACK
for the different page types and special cycles.


```

-------------------------------------------------------
Condition	Device		DTACK
-------------------------------------------------------
TYPE=0		Main Memory	CS4 * (READ + ¬P2.WAIT)
TYPE=1		I/O		CS7 * ¬P2.WAIT
TYPE=2		VME		P1.DTACK
TYPE=3		VME		P1.DTACK
FC=6 ∧ BOOT	EPROM		CS7
FC=3		MMU Access	CS7
FC=7 ∧¬A19	Breakpoint	Internal
FC=7 ∧ LOCAL	Autovector	Internal
FC=7 ∧¬LOCAL	VME Interrupt	P1.DTACK
-------------------------------------------------------

```


The handshaking is implemented with selector [74F151:U118]
in conjunction with PAL [A101=P16L8:U101]
and PAL [A106=P16L8:U106].


### BERR


Bus error can occur under the following conditions:


Invalid Page Entry

Protection Error

Parity Error Lower Byte

Parity Error Upper Byte

VME Bus Error

Timeout


These error conditions, together with signal [Q.SPECIAL]
are ORed in gate [74ALS30:U130] asserting [Q.ERROR].
Whenever [Q.ERROR] is active it disables all read-write strobes
by disabling strobe decoder [74F138:U400] and I/O decoder
[LS2521:U403].

If [Q.ERROR] occurs in a non-special 68010 cycle, three things happen.
First, PAL [A103=P16L8:U103] asserts [Q.BERR] after state [C.S5],
thereby aborting the current cycle.
Second, the PAL generates [Q.BERRCLK]
which latches the error condition into the bus error register [ALS534:U511].
Third, the PAL cleares the parity error flipflops [74F74:U424]
with signal [Q.PARCLR] in case they were set.


### Address Error Cycles


During address error cycles, the 68010 asserts address strobe
but no data strobes. The effect of this is that a normal cycle
is executed; however, since no data strobes are active no
read or write strobes are asserted via decoder [74F138:U400].
The statistic bits in the MMU are updated on address error cycles.


### 68010 Cycle to Memory


68010 cycles to memory execute normally without wait states
by asserting DTACK at state 4.


```


68010 State	0   1   2   3   4   5   6   7   0

C.100		----____----____----____----____--

P.AS-		--------____________________------

P.DS- (READ)	--------____________________------

P.DS- (WRITE)	----------------____________------

P.DTACK-	----------------____________------


```


### 68010 Cycle to I/O


68010 Cycles to I/O generate DTACK at state 9, causing 2 wait states.


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12

C.100		----____----____----____----____----____----____----

P.AS-		--------____________________________________--------

RD/WR.IO-	--------------------________________________--------

P.DTACK-	------------------------------------________--------


```


---

## DVMA Logic


*Reference:* Schematics Page 2, Motorola 68010 Data Sheet.


### Overview


The DVMA Controller takes requests from DVMA devices,
obtains the processor bus from the 68010,
and performs a read/write cycle for the device,
generating appropriate function codes and strobes.

The DVMA Devices in their order of priority are:


- Refresh

- Ethernet

- VME-bus


Figure [Figure](#a308) shows how the DVMA Controller and Strobe Generator
interface to the 68010.


![Placeholder: a308.press]()


*Figure: **DVMA Controller***

<a id="a308"></a>


---

### DVMA Cycles


DVMA requests are synchronized with register [74F374:U213]
before entering the DVMA controller PAL [P16R8:U214].
The DVMA controller PAL prioritizes the incoming requests,
issues a bus request to the 68010 [S.BR],
then waits for the 68010 to release the processor bus by
watching 68010 bus grant [P.BG] and the end of 68010 address strobe [P.AS],
before asserting the DVMA enable corresponding to the request.

In addition, the DVMA controller PAL generates a DMA-cycle signal [S.DMA]
that enables the tri-state buffers in the DVMA strobe PAL [P16L8:U215]
to drive the function codes [P.FC0..2], address strobe [P.AS],
data strobes [P.UDS, P.LDS], and read/write srtobe [P.R/W].
Function Codes, data strobes, and device codes are asserted as follows:


```

-----------------------------------------------------------
    DVMA	DMA	LDS	UDS	FC	Space
-----------------------------------------------------------
    REFRESH	3	0	0	7	CPU Space
    ETHERNET	2	1	¬E.A0	5	System Data
    EXTERNAL	1	X.LDS	X.UDS	5	System Data
-----------------------------------------------------------

```


### DVMA Arbitration Cycle


Arbitration occurs concurrently with ongoing bus activity.
The 68010, after receiving a bus request [P.BR-] issues a bus grant [P.BG-].
When the DVMA controller sees bus grant and address strobe
[P.AS] deasserted, it acquires the bus and asserts the DMA Enable.


```


DVMA-State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C.100		----____----____----____----____----____----____----____----____--

X.DMA-		-\\\\\\\________________________________________________////////--

S.XREQ-		--------________________________________________________________--

P.BR-		----------------________________________________________________--

P.BG-		--------------------------------________________________----------

S.BGIN-		----------------------------------------________________________--

P.AS-		____________________________________________--------------------__

S.ASIN-		________________________________________________------------------

X.DMAEN-	--------------------------------------------------------__________


```


---

### VME DVMA Cycle


```


S-State		0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C.100		----____----____----____----____----____----____----____----____

X.DMA-		____________________________________----------------------------

X.DMAEN-	________________________________________________----------------

S.AS-		--------____________________________----------------------------

68010_S0-	--------------------------------------------------------________


```


### DVMA Cycle, Memory Refresh


Memory refresh requests are generated every 12.8 microseconds
by a low-to-high transition of output [C.12800]
of synchronous counter [74LS590:U211].
This transition sets signal [R.DMAREQ] in flipflop [74F74:U203-0],
which in turn is sychronized in register [74F374:U213] and causes
a refresh cycle in DVMA controller [P16R8:U214].
During the refresh cycle [R.DMAEN] is asserted which output-enables
refresh counter [74LS590:U210] and with its trailing edge
advances the refresh counter to its next state.
The refresh counter drives address lines [P.A02..09] which
constitute the row-address refresh addresses of the RAM chips.
During refresh cycles, both banks of memory are enabled.
This is done via PAL [P16L8:U108] asserting both [Q.BANK0, Q.BANK1]
causing the RAS generation logic to assert both [P2.RAS0, P2.RAS1].

Refresh cycles are shorter than other DVMA cycles
in that they only last for eight states.
This is shown in the timing diagram below.


```


S-State		0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C.100		----____----____----____----____----____----____----____----____

R.DMAEN-	________________________________--------------------------------

S.AS-		--------________________----------------------------------------

S.ASIN-		----------------________________--------------------------------

P.BACK-		________________________________--------------------------------

68010_0-	------------------------------------------------________________

68010_AS-	--------------------------------------------------------________


```


---

## I/O-Bus


*Reference:* Schematics Page 1

The I/O data bus [IO.D00..15] connects to the following devices:


all input/output devices,

all MMU devices, and

the VME data port.


The I/O data bus is connected to processor data bus [P.D00..15]
via bidirectional transceivers [8308:U110, U111].
These bus buffers are enabled via PAL [P16R4:U102] as follows.
The I/O Bus is driven from the processor data bus
on all processor write cycles and all DVMA read cycles.
The processor data bus is driven from the I/O-bus
on all DVMA write cycles and all processor read cycles from
I/O devices, MMU devices, and VME Bus.

---

## MMU and MMU Space Devices


*Reference:* Schematics Page 3


### Overview


The MMU consists of user context register [LS2518:U300],
system context register [LS2518:U301],
user/system context multiplexor [74F158:U302],
segment map RAM [2168:U303, U304],
and page map RAM [2168:U305 through U310].

Other MMU space devices are
the bus error register [ALS534:U511],
the system enable register [ALS534:U511] with readback [ALS244:U513],
the diagnostic register [AlS273:U514] with LEDs [LED4:J515, J516],
and the ID PROM [P5X8:U510].


### Decoding


The MMU and MMU space devices are accessed via decoders
[ALS138:U322, U323, U324].
Decoder [ALS138:U324] is the read decoder,
decoder [ALS138:U323] is the upper byte write decoder, and
decoder [ALS138:U322] is the lower byte write decoder.
All MMU space devices are connected to the lower byte.


### MMU Operation


During a normal address translation cycle,
the processor system function code [P.FC2]
selects between the user [P.FC2=0] and supervisor [P.FC2=1] context.
The selected context value, together with address lines [P.A15..23]
index the segment map RAM which produces a page-map-entry-group [IA16..23].
The page-map-entry-group, in conjunction with address lines [P.A11..15]
index the page map RAM, producing as its output
the valid bit [VALID],
protection codes [PROT0..5],
type field [TYPE0..1],
accessed bit [ACC],
modified bit [MOD],
and mapped address lines [MA11..22].

The protection field is checked with decoder [74F151:U315].
If the protection bit corresponding to the state of the read/write line
[Q.R/W] an the processor function codes [P.FC1, P.FC2] is not set,
then output [PROTERR] will be asserted.

The accessed and modified bits are updated on all non-special cycles.
For this operation, the current value of the type field, which is in
the same nibble as the accessed and modified bit, is latched into
register [ALS374:U316] with clock [C.S5].

The actual update starts with [C.S5] and ends with [C.S7].
During this time, PAL [P16L8:U103] asserts both [WR.UPDATE],
which turns on write enable to RAM [2168:U307],
and [WR.STAT] which output enables register [ALS374:U316]
with the new data to be written into RAM [2168:U307].

---

## I/O Devices


*Reference:* Schematics Page 4, 5, 6, 7


### Overview


Input/Output devices comprise the PROMs,
the Ethernet Control Register, the Keyboard/Mouse UART,
the Serial Communication Controller,
and the Timer chip.
All input/output devices connect to the IO-Bus.


### Decoding


Input/output devices are selected with a MMU type field of 1
[TYPE1=0], [TYPE0=1], and address lines [MA16..22] all ones.
This condition is decoded with comparator [LS2521:U403]
in conjunction with gate [74F32:U433-3] producing signal [CE.IO].

[CE.IO] in conjunction with [Q.R-/W] enables I/O read decoder [ALS138:U401]
and in conjunction with [Q.R/W-] I/O write decoder [ALS138:U402].
Both the I/O read and write decoder decode mapped address lines
[MA11..13] to select one of eight possible devices.


### PROMs


Since the PROMs are larger than a single 2K page, they are addressed
directly with the low-order bits of the non-translated (virtual) address
from the CPU, [P.A01..A14].
The PROMs are constantly chip enabled with CE tied to ground.
The PROMs are output-enabled with signal [OE.PROM] generated in
PAL [P16L8:U101] during boot cycles [BOOT=1,FC=6] and during
read-PROM cycles [RD.PROM=1].


### Timer


Timer chip [AM9513:U504] provides five 16-bit timers.
The timer is driven by a 4.9152 MHz input clock [C.204],
generated from the 19.6608 MHz clock oscillator [K1114A:U200]
via binary counter [74LS393:U212], independent of the CPU clock.

Gate input 1 of the timer chip is wired to the timer [FOUT] signal.
Output [OUT1] is connected to interrupt request 7 [IRQ7],
and outputs [OUT2..5] drive interupt request 5 [IRQ5]
via open-collector inverters [74LS05:U505].


### Serial Communication Controller


The serial port [8530:U601] is implemented with the
AMD/Zilog 8530 serial communicatiin controller (SCC).

The serial port occupies channel A of the UART, in conjunction
with drivers [9636:U608,U609], and receiver [26LS32:U606].
Channel B of the UART is not used.


### Ethernet Control Register


The Ethernet Control Register [ALS273:U716, ALS244:U717]
controls the overall operation of the Ethernet interface.
Register [ALS273:U716] is reset with processor reset.
Further information on the Ethernet operation is contained
in the section on Ethernet.

---

## P2-Bus Interface


*Reference:* Schematics Page 4, 10 ,11.


### Introduction


The P2-Bus is the internal bus which interconnects the CPU to main memory.
Physically, the P2-Bus is brought out on connector
[P96:P1102], pins 1 through 32 and 65 through 96.


### P2 Signals


The P2-Bus consists of a number of address lines,
bidirectional data lines, parity lines,
timing signals, enable signals, and a handshake line.

Address Lines, Data Lines, Read/Write Line, and Handshake Line:


```

---------------------------------------------------------------------------
P2.Signal	Description
---------------------------------------------------------------------------
P2.A00.23	Address Lines (24)
P2.D00.15	Data Lines (16)
P2.DIL, DIU	Parity from CPU to Memory (2)
P2.DOL, DOU	Parity from Memory to CPU (2)
P2.R/W		Read/Write Strobe
P2.WAIT		Negative Handshake
P2.INIT		Procesor Reset
P2.INT4		Interrupt Request Level 4
P2.INT6		Interrupt Request Level 6
---------------------------------------------------------------------------

```


Control Signals:


```

---------------------------------------------------------------------------
P2.Signal	Description		Asserted on
---------------------------------------------------------------------------
P2.RAS0		Row-Address-Strobe 0	C.S3 ∧ ¬P.A01 ∨ C.S3 ∧ REFRESH
P2.RAS1		Row-Address-Strobe 1	C.S3 ∧  P.A01 ∨ C.S3 ∧ REFRESH
P2.R/C		Row-Column Select	C.S3 + 30 nsec
P2.CAS		Column-Address-Strobe	C.S4 + 15 nsec ∧ ¬Q.SPEC
P2.RD		P2-Bus Read Strobe	C.S5 ∧ ¬ERROR ∧ ¬CE.IO ∧ ¬TYPE1
P2.WEU		P2-Bus Write Strobe	C.S5 ∧ ¬ERROR ∧ ¬CE.IO ∧ ¬TYPE1
P2.WEL		P2-Bus Write Strobe	C.S5 ∧ ¬ERROR ∧ ¬CE.IO ∧ ¬TYPE1
---------------------------------------------------------------------------

```


These control signals are generated centrally on the 2250 CPU board.
RAS0/1 is generated by and-or gates [74F64:U218,U219] in conjunction
with inverter [74F04:U221].
[P2.RAS0/1] is asserted when processor address strobe is active (P.AS=1)
and the clock is low (C.100=0). This is the case at the beginning
of processor state 3. After RAS is first asserted, it is
latched via inverter [74F04:U221] until the later of
[C.S7] or [P.AS] being deasserted.

[CAS] is generated by flipflop [74F74:U204-1].
It is asserted at time [C.S4] delayed by 15 nanoseconds
via delay line [MTTLDL:U207] on non-special cycles [Q.SPECIAL=0].
[CAS] is inhibited during special cycles because the column address is not
guaranteed to be stable during memory management updates and thus would cause
invalid decoding in memory.

The upper and lower write enable to memory, [P2.WEU-, P2.WEL-]
are generated in decoder [74F138:U400] in conjunction with
gates [74F32:U433-1, U433-2].
The write strobes are asserted with [C.S5]
and data strobe [Q.DS] active, with no error condition [Q.ERROR] present.
They are turned off with the processor upper and lower data strobe,
[P.UDS, P.LDS].

Accesses to the P2-Bus are decoded in decoder [F138:U400].
A read or write reference to the P2-Bus [RD.P2, WR.P2] is generated when:
the page type is 0 or 1 [TYPE1=0],
data strobe is asserted [Q.DS=1],
no bus error condition exists [Q.ERROR=0],
and clock state 5 is asserted [C.S5=1].


### P2-Bus Cycle


The timing of a P2-Bus cycle is illustrated in the figure below for a standard
memory write cycle followed by a memory read cycle.


```


68010 State	0   1   2   3   4   5   6   7   0   1   2   3   4   5   6   7   0

C.100		----____----____----____----____----____----____----____----____--

P2.A00..11	xxxxxxxx________________________xxxxxxxx________________________xx

P2.A12..23	xxxxxxxxxxxxxxx_________________xxxxxxxxxxxxxxxx________________xx

P2.D00..15	xxxxxxxxxxxxxxx_________________xxxxxxxxxxxxxxxxxxxxxxxxxxx_____xx

P2.RAS-		------------________________----------------________________------

P2.R/W-		--------________________________________--------------------------

P2.CAS-		----------------____________--------------------____________------

P2.WEU-, WEL-	--------------------________--------------------------------------

P2.RD-		----------------------------------------------------________------


```


During read-modify-write cycles, processor address strobe
and thus [P2.RAS0/1] and [P2.CAS] stay asserted for the
entire length of the cycle.

Note that both [P2.RAS] and [P2.CAS] are asserted before the
page map type field is decoded and before the protection field is
evaluated. Thus [P2.CAS] indicates a valid address, but not
necessarily a valid reference. Only the read/write strobes
qualify a reference.


---

### Parity Error Logic


*Reference:* Schematics Page 4

The Parity Error Logic generates parity for memory write operations
and checks parity for memory read operations. Note that the
parity error logic is only used for memory accesses (page type 0).

On writes, parity is generated with parity generators [74F280:U420, U421].
When signal [EN.PARGEN] is asserted, *odd* parity
is generated and stored in memory.
Odd parity means that the sum of all data bits and the
parity bit is odd.

On reads, parity is checked with parity checkers [74F280:U422, U423].
If the even output of the parity checkers is true, then a parity error
has occured. This parity error information is clocked into the
parity flipflops [74F74:U424-0, U424-1]
on memory read cycles [TYPE0=0, RD.P2=1]
with the leading edge of [C.S7], delayed by two inverter delays
[74F04:U221].

The parity error flipflops are self-latching. This means that they
remain set until they are cleared by signal [Q.PARCLR].
The parity error flipflops remain cleared if
parity checking is disabled [EN.PARERR=0].

The outputs of the parity error flipflops [PARERRL, PARERRU]
are ORed with the other bus error conditions in gate [74LS30:U130].
This generates signal [Q.ERROR] which in turn
generates bus error [Q.BERR] to the 68010 via PAL [P16L8:U103].

Parity errors are different from other bus errors in that they
cannot abort the 68010 cycle in which they occur.
This is because they are only detected at the end of a read cycle,
after a point at which the 68010 can abort the current cycle.
The parity error flipflops provide the function of latching
parity errors until they are recognized by the CPU.

In order to recognize the bus error caused by a pending parity error,
the 68010 must execute a "non-special" cycle [Q.SPECIAL=0].
Under this condition, PAL [P16L8:U103] generates
signal [Q.BERRCLK] which clocks the parity error flipflop state
into the bus error register [ALS534:U511]
and signal [Q.PARCLR] which clears the parity error flipflops.

Parity generation and checking can be disabled for testing purposes.
To initialize parity in main memory, all of
memory needs to be written with parity generation enabled.
When signal [EN.PARGEN] is not asserted, then *even*
parity is generated. This allows the parity error function to be tested.

---

## Ethernet Interface


*Reference:* Schematics Page 7, Intel 82586 Ethernet Controller Manual.


### Overview


The Ethernet Interface is built around the Intel 82586
VLSI Ethernet Controller [U700] and the Intel 82501
phase Lock Loop Decoder [U701].


### Ethernet Data Link Controller


The Intel 82586 Ethernet Data Link Controller is configured as follows:
Maximum Mode [MN/MX-=0], asynchronous ready [READY=0],
directly enabled [HLDA=HOLD], and always clear to send [CTS-=0].
The 82586 receives an 8 MHz clock from flipflop [74F74:U202-1].
Pullup [R:R202] supports the VOH-level required by the 82586.
For a complete description of this part, refer to the Intel 82586 Data Sheet.


### Ethernet DVMA Cycle


When the Ethernet controller wants to access main memory,
it asserts Hold request [E.HOLD]. This signal,
ANDed with Ethernet error inactive [E.ERR-] in gate [74F08:U718-0],
presents signal [E.REQ] to the DVMA Arbiter latch [74F374:U213].
This will cause the Arbiter to continuously request the bus from the CPU
until the 82586 drops [E.HOLD]. Once the arbiter obtains the bus from the CPU,
it asserts [E.DMAEN] which enables
the Ethernet address latch [74ALS374:U702,U703] and the 82586.
In response, the 82586 asserts either Ethernet read control [E.RD]
or write control [E.WR].
Ethernet read and write controls are or-ed together with gate
[74F08:U718-2] to generate Ethernet data strobe [E.DS].
Ethernet Data Strobe is clocked via [74F74:U719-0]
at the next rising edge of the 8 MHz Ethernet clock [C.125]
to generate Ethernet address strobe [E.AS].
The leading edge of Ethernet address strobe latches the multiplexed
Ethernet address into the Ethernet address register [ALS374:U702, U703].

The Ethernet data port is byte swapped between
the processor data bus and the Ethernet data bus.
This means that the processor data bits 0..7 are connected
to Ethernet data bits 8..15 and vice versa.

If a bus error is encountered during an Ethernet DVMA cycle,
the Ethernet bus error flipflop is set [ALS74:U719-1] causing
the Ethernet Error signal to be asserted [E.ERR].
This signal prevents future Ethernet DVMA requests.
The Ethernet bus error flipflop can only be reset by an
Ethernet reset command [E.RESET].


---

## VME Bus Interface


*Reference:* Schematics Page 8, 9, 10, VME Bus Manual.

The VME Bus interface consists of the following functions:


VME Bus Utility Functions

VME Arbiter

VME Master Interface

VME Slave Interface

VME Interrupt Handler


---

### VME Bus Utility Functions


The VME Bus Utility functions are implemented by these four utility lines:
System Clock [P1.SYSCLK], AC Fail [P1.ACFAIL], System Reset [P1.SYSR],
and System Fail [P1.SYSF].

System Clock is driven from the 16 MHz oscillator signal [C.62]
via a high-current driver [74F244:U817].
System Clock has no phase relationship with any other VME signals.
It can be disconnected from the VME Bus by removing jumper [J.8:J800-5.6].

AC Fail is driven to the VME Bus by open collector driver [74ALS6411:U818].
It is asserted while Power-On-Reset is active.
It cannot be disconnected from the VME Bus.

System Reset is driven to the VME Bus by open collector driver [74ALS6411:U818].
It is asserted whenever Processor-Reset is active.
It cannot be disconnected from the VME Bus.

The 2250 Board can be configured either as a P1-Bus Reset Master or Slave.

As a P1-Bus Reset Master, the 2250 Board issues Reset [B.RESOUT] to the VME Bus.
Power-On Reset, Watchdog Reset, and 68010 Reset will all assert P1-Bus Reset.
Other P1-Bus devices may also assert P1-Bus Reset, but this will have
no effect on the on-board CPU and devices.

As a P1-Bus Reset Slave, the 2250 Board receives Reset [B.RESIN]
from the VME Bus, but does not drive Reset to the VME Bus.
The VME Bus Reset has the same effect as an on-board power-on-reset.

System Fail is not used or generated by the 2250 Board.


### VME Arbiter and Requestor


The VME Arbiter and Requestor functions are implemented in one
state machine [74F374:U812, U813, P9X4:U811, P16L8:U814].
Out of the options possible within the VME Bus Spec,
the arbiter implements the ONE ROR arbiter option.
ONE means that the arbiter monitors bus request level 3 [P1.BR3] only
and accomplishes arbitration via the level 3 daisy chain [P1.BG3IN, P1.BG3OUT].
ROR or *release on request* means that the arbiter only releases the bus
when a request from another master is pending.
Filter [RC:R800,C800] eliminates high-frequency noise on the VMEbus
[P1.BUSY] signal that has been observed on VMEbus backplanes.

When the CPU wants to access the VME Bus, either for a standard
read/write cycle or for a interrupt acknowledge cycle,
it asserts signal Bus Select [B.BSEL] via PAL [P16L8:U810].

If the arbiter currently does not own VME Bus mastership,
it requests bus mastership by asserting VME Bus request [P1.BREQ]
and going through the normal VME Bus arbitration sequence.
If the arbiter already owns bus mastership, it will keep the
bus mastership until another VME Bus master requests it.

---

### VME Master Interface


Once the 2250 Board obtains VME Bus mastership, the
VME Master Interface allows the 2250 Board to access VME Slaves
on the VME Bus. The interface consists of address and address modifier
drivers [ALS244-1:U900, U901, U902, U903],
data buffers [ALS245:U908, U909],
and control signal driver [74F244:U817-0].
The VME Slave Device being addressed will respond to the transfer
by asserting either data transfer acknowledge [P1.DTACK]
or bus error [P1.BERR]. These two signals
are qualified in PAL [P16L8:U816] before reaching the 68010 CPU.


### 68010 Cycle to VME Bus, Currently Busmaster


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C.100		----____----____----____----____----____----____----____----____

P.AS-		--------____________________________________________________----

P.DS- (READ)	--------____________________________________________________----

P.DS- (WRITE)	----------------____________________________________________----

B.BSEL-		--------------------________________________________________----

B.AEN-		________________________________________________________________

B.CEN-		------------------------________________________________________-

P1.AS-		------------------------____________________________________----

P1.DTACK-	-------------------------------------------------_______________


```


### 68010 Cycle to VME Bus, Not Currently Busmaster


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C.100		----____----____----____----____----____----____----____----____

P.AS-		--------____________________________________________________----

P.DS- (READ)	--------____________________________________________________----

P.DS- (WRITE)	----------------____________________________________________----

B.BSEL-		--------------------________________________________________----

B.REQ-		------------------------____________________________________----

B.AEN-		--------------------------------________________________________

B.BEN-		----------------------------------------________________________

B.CEN-		----------------------------------------____________________----

P1.AS-		----------------------------------------____________________----

P1.DTACK-	-------------------------------------------------_______________


```


---

### VME Slave Interface


The VME Slave Interface allows the 2250 Board to be accessed
by other VME Masters on the VME Bus. The 2250 Board responds
to a 24-bit VME cycle that has four high-order address bits of 0.
This function is performaed by address comparator [LS2521:U930].
In addition to [P1.A20..23] being equal to 0,
the VME address modifiers 4 and 5 must be set, [P1.AM4=1, P1.AM5=1],
the VME interrupt acknowledge must be not set [P1.IACK=0],
and the 2250 Board must not be bus master [B.AEN=0].
If all these conditions are met and a VME data strobe [X.UDS OR X.LDS]
is asserted then signal [X.DMA] is asserted,
indicating that a VME Slave Interface request is pending.

[X.DMA] poses an external DMA request to the DVMA controller.
In response, the DVMA controller requests the on-board bus from the CPU
and once it obtains the bus asserts [X.DMAEN] which enables
the VME DVMA address register [ALS374:U904, U905, U906].

At state 8 of a VME DVMA cycle,
PAL [P16l8:U814] asserts one of [X.DTACK] or [X.BERR]
depending on the state of [Q.ERROR].
If [Q.ERROR] is active at this time,
then [X.BERR] is asserted, otherwise [X.DTACK] is asserted.
Both [X.DTACK] and [X.BERR] are driven to the VME bus
with open-collector driver [ALS6411:U818].


### VME Interrupt Handler


The VME Interrupt Handler responds to Interrupts on the VME Bus.
The 2250 Board does not generate any interrupts to the VME Bus.

Off-board and on-board interrupts are combined in PAL [P20L8:U109].
This PAL detects the highest priority interrupt pending, off-board
or on-board, encodes this interrupt level, and drives
it on lines [IPL0..2] to the CPU.

When the 68010 recognizes an interrupt request, it issues
function code 7 and sends out the interrupt level being acknowledged
on address lines [A01..A03].
If an on-board interrupt request is pending at the level the 68010
acknowledges, then PAL [P20L8:U109] asserts [ILOCAL],
else it does not assert [ILOCAL].
[ILOCAL] is sampled at state 4 in the onboard/offboard interrupt flipflop
[74F74:U205-1]. Output [Q.AUTOV] is asserted if an on-board interrupt
request was pending or if address bit [A19] is deasserted,
indicating a non-interrupt cycle.
If [Q.AUTOV] is asserted, then PAL [P16L8:U101] drives [Q.VPA]
to the processor for an autovector interrupt acknowledged cycle.
If [Q.AUTOV] is not asserted, then PAL [P16L8:U101] generates [Q.INTVEC]
which forces an interrupt vector aquisition via the VME Bus.

---

### 68010 Rerun Cycles


Rerun cycles are executed on VMEBus deadlock.
The condition here is that the CPU is attempting to access the VME Bus
while another master on the VME Bus is attempting to access the 2250 Board
as a slave device. Since the VME Bus has no rerun capability, the
68010 must yield to the VME Bus request to resolve the deadlock.
The condition is present if [B.SEL] and [X.DMA] are
simultaneously valid.

This condition is recognized in PAL [P16L8:U810] which
generates [B.RERUN]. Signal [B.RERUN] is synchronized
in flipflop [74F374:U813] before driving PAL [P16R4:U102]
which in turn generates the required [Q.BERR, P.HALT] signals
to cause a CPU rerun.


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C.100		----____----____----____----____----____----____----____----__

P.AS-		--------________________________________________---------------

P.BR-		------------------------______________________________________

B.BROUT-	------------------------________________________--------------

B.RERUN-	------------------------________________________--------------

S.RERUN-	----------------------------________________________----------

S.BERR-		------------------------------------________________----------

S.HALT-		------------------------------------________________________--

P.BERR-		------------------------------------________________----------

P.HALT-		------------------------------------________________________--


```
