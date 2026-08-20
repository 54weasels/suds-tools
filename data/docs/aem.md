---


---


# Sun-2 Single Board Computer


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


# state.mss


---

## Major Blocks


```


- Power
- Initialization
- Clocks
- CPU
- MMU
- I/O Devices
- Ethernet Interface
- Bus Interface
- Memory
- Video Subsystem


```


## Power


The Sun-2 Single board uses a single 5 Volt power supply only.
On-board charge pumps `7660:U612,U614` generate a -5V voltage
for the RS423 interface drivers `26LS29:U609,611`.


## Initialization


## Clock Generation


## CPU


Initialization

Clocks

Interrupts

P2-Control Signals

Parity Generator

DVMA Arbitration

Rerun Cycles

RasterOp Processor


---

## 68010 Cycle to Memory


```


68010 State	0   1   2   3   4   5   6   7   0

C-80		----____----____----____----____--

P.AS\		--------____________________------

P.DS\ (READ)	--------____________________------

P.DS\ (WRITE)	----------------____________------

P.DTACK\	----------------____________------


```


## 68010 Write Cycle to Video Memory, Best Case


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12

C-80		----____----____----____----____----____----____----

P.AS\		--------____________________________________--------

P.DS\ (READ)	--------____________________________________--------

P.DS\ (WRITE)	----------------____________________________--------

P.DTACK\	------------------------____________________--------


```


## 68010 Cycle to I/O


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----____

P.AS\		--------____________________________________________________----

RD/WR.IO\	--------------------________________________________________----

P.DTACK\	--------------------------------------------________________----


```


## Q.RAS Generation


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----____

P.AS\		--------____________________________________________________----

TYPE1		----------------------------------------------------------------

C.S7		____________________________------------------------------------

Q.RAS\		------------________________------------------------------------


```


---

## 68010 Address Load to DCP


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----____

P.AS\		--------____________________________________________________----

RD/WR.DCP\	--------------------________________________________________----

CS11		____________________________________________--------------------

MAS\		--------------------________________________--------------------


```


## 68010 Write to DCP, Best Case


```


State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17

C-80	----____----____----____----____----____----____----____----____----____

C-80\	____----____----____----____----____----____----____----____----____----

C-160	----________--------________--------________--------________--------____

C-320	____________----------------________________----------------____________

P.AS\	--------____________________________________________________________----

WR.DCP\	--------------------________________________________________________----

MDS\	--------------------__________________________________________----------

STATE0\	----------------------------_________________________________-----------

STATE1\	--------------------------------------------___________________---------

P2.WAIT\--------------------________________________________--------------------

P.DTACK\----------------------------------------------------________________----


```


## 68010 Read from DCP, Best Case


```


State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17

C-80	----____----____----____----____----____----____----____----____----____

C-80\	____----____----____----____----____----____----____----____----____----

C-160	----________--------________--------________--------________--------____

C-320	____________----------------________________----------------____________

P.AS\	--------____________________________________________________------------

WR.DCP\	--------------------________________________________________------------

MDS\	--------------------__________________________________________----------

STATE0\	----------------------------_________________________________-----------

STATE1\	--------------------------------------------___________________---------

P2.WAIT\--------------------________________________----------------------------

P.DTACK\--------------------------------------------________________________----


```


---

## 68010 Cycle to System Bus, Currently Busmaster


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----____

P.AS\		--------____________________________________________________----

P.DS\ (READ)	--------____________________________________________________----

P.DS\ (WRITE)	----------------____________________________________________----

B.BSEL\		--------------------________________________________________----

B.AEN\		________________________________________________________________

B.CEN\		------------------------________________________________________-

P1.AS\		------------------------____________________________________----

P1.DTACK\	-------------------------------------------------_______________


```


## 68010 Cycle to System Bus, Not Currently Busmaster


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----____

P.AS\		--------____________________________________________________----

P.DS\ (READ)	--------____________________________________________________----

P.DS\ (WRITE)	----------------____________________________________________----

B.BSEL\		--------------------________________________________________----

B.REQ\		------------------------____________________________________----

B.AEN\		--------------------------------________________________________

B.BEN\		----------------------------------------________________________

B.CEN\		----------------------------------------____________________----

P1.AS\		----------------------------------------____________________----

P1.DTACK\	-------------------------------------------------_______________


```


---

## 68010 Rerun Cycle, External Rerun Case


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----__

P.AS\		--------____________________________--------------------------

P.DS\ (READ)	--------____________________________--------------------------

P.DS\ (WRITE)	----------------____________________--------------------------

P.DTACK\	--------------------------------------------------------------

S.AS\		----------------________________________----------------------

B.RERUN\	--------\\\\___________________/////--------------------------

S.RERUN\	------------________________________--------------------------

S.BERR\		--------------------________________________------------------

S.HALT\		--------------------________________________________----------

P.BERR\		--------------------________________________------------------

P.HALT\		--------------------________________________________----------


```


## 68010 Rerun Cycle, Waiting for System Bus Case


```


68010 State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----__

P.AS\		--------________________________________________---------------

P.BR\		----------------______________________________________________

B.BROUT\	------------------------________________________--------------

B.RERUN\	------------------------________________________--------------

S.RERUN\	----------------------------________________________----------

S.BERR\		------------------------------------________________----------

S.HALT\		------------------------------------________________________--

P.BERR\		------------------------------------________________----------

P.HALT\		------------------------------------________________________--


```


---

## DVMA Arbitration Cycle


```


DVMA-State	0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----____

X.DMAREQ\	\\\\\\\\________________________________////////----------------

S.DMAREQ\	--------________________________________________----------------

P.BR\		----------------____________________________--------------------

P.BG\		----------------\\\\\\\\________________////////----------------

S.BGIN\		------------------------________________________----------------

P.AS\		____________________________////----------------________________

S.ASIN\		________________________________------------------------________

X.DMAEN\	----------------------------------------________________________

P.BACK\		----------------------------------------________________________


```


## DVMA Cycle, Synchronous Memory


```


S-State		0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----____

X.DMAEN\	________________________________________------------------------

S.AS\		--------________________________--------------------------------

S.ASIN\		----------------________________________------------------------

Q.DS\		----------------________________--------------------------------

Q.S7		____________________________------------------------------------

P.BACK\		________________________________--------------------------------

68010-0\	------------------------------------------------________________

68010-AS\	--------------------------------------------------------________


```


## DVMA Cycle, Memory Refresh


```


S-State		0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15

C-80		----____----____----____----____----____----____----____----____

R.DMAEN\	________________________________--------------------------------

S.AS\		--------________________----------------------------------------

S.ASIN\		----------------________________--------------------------------

Q.DS\		----------------------------------------------------------------

Q.S7		____________________________------------------------------------

P.BACK\		________________________----------------------------------------

68010-0\	----------------------------------------________________________

68010-AS\	------------------------------------------------________________


```


## DVMA Cycle, RasterOp Cycle


```


State		0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3 3 3
		0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3

C-80		--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__

G.ROP		--------------------------------------------------------------------

(UDATA*WRITE)\	--______________----------------------------------------------------

G.ROPCYC\	---_____________----------------------------------------------------

LDSRC\		----------_____-----------------------------------------------------

G.READ\		---_______________________________________--------------------------

G.FIRST\	------------------------__________________--------------------------

G.DMAREQ\	---____________________________________________---------------------

S.GREQ\		----____________________________________________--------------------

P.BR\		--------____________________________________________----------------

P.BG\		----------------________________--------________________________----

S.BGIN\		--------------------____________________________--------------------

G.DMAEN\	------------------------____________________--------________________

P.BACK\		------------------------________________________________________----

P.AS\		______________--------------____________----------------____________


```


---

## Ethernet Interface


*Reference:* Schematics Page 7, Intel 82586 Ethernet Controller Manual.


### Overview


The Ethernet Interface is built around the Intel 82586
VLSI Ethernet Controller (U700) and the Fujitsu MB502
Phase Lock Loop Decoder (U701).
The Ethernet Control Register (74ALS273:U716, 74ALS244:U717)
controls the overall operation of the Ethernet interface.


### Ethernet Transceiver Interface


The Ethernet Connector (J700) follows the standard Ethernet definition.
Jumper (J.2:J702) allows to supply +5V to the Ethernet connector for
transceivers that require this voltage.
The Ethernet transceiver drop cable is terminated with resistor
networks (R4.SIP:R704, R705).


### Ethernet Phase Lock Loop Decoder


The Ethernet Frontend uses a digital phase lock loop with 10 samples
per bit cell. An internal oscillator with external chrystal X700
together with tank circuit (C:C700,C703,C704,L:L700)
provides the 100 Mhz input frequency to the PLL chip.
Jumper (J.2:J701) allows to select between Ethernet Level 1 and Level 2
interface characteristics (Level 2 if jumpered).
The Ethernet frontend is interfaced to the Ethernet data link controller
with Inverters (74F240:U709) and Flip-Flops (74F74:U710, U712).


### Ethernet Data Link Controller


The Intel 82586 Ethernet Data Link Controller is configured as follows:
Maximum Mode (MN/MX\=0), asynchronous ready (READY=0),
directly enabled (HLDA=HOLD), and always clear to send (CTS\=0).
For a complete description of this part, refer to the Intel 82586 Data Sheet.


### Ethernet DVMA Cycle


When the Ethernet controller wants to access main memory,
it asserts either Ethernet read control (E.RD) or write control (E.WR).
Ethernet read and write controls are ored together with gate
(74LS00:U715-3) to generate Ethernet data strobe (E.DS).
The leading edge of Ethernet Data Strobe (E.DS) then
sets the Ethernet DVMA request flipflop (74F74:U207-1).
In addition, Ethernet Data Strobe is clocked at the next
rising edge of the 8 MHz Ethernet clock (E.C-125) to generate
Ethernet address strobe (E.AS).

The leading edge of Ethernet address strobe latches the 24-bit
Ethernet address into the Ethernet address register (74ALS374:U702,U703,U704)
to generate Processor Address (P.A01 through P.A23) when enabled
with Ethernet DMA enable (E.DMAEN).
In addition, Ethernet write control (E.WR) is latched into the same
register to generate Processor Read/Write strobe (P.R/W\) when enabled.

At this point, the Ethernet has requested a DVMA cycle
and is waiting for Ethernet DMA enable.
On a write cycle (Ethernet to Memory), the DVMA controller will
enable the Ethernet write data buffers (74ALS244:U707,U708)
with Ethernet output enable (E.OE).
On a read cycle (Memory to Ethernet), the DVMA controller will
clock the data read from memory into the Ethernet read data buffers
(74ALS374:U705,U706) at the trailing edge of Ethernet write enable (E.WE).
The Ethernet read buffers are output enabled by Ethernet read 1 (E.RD1)
to the Ethernet controller chip. This timing is illustrated in
the diagram below.

The Ethernet read and write buffers are byte swapped between
the processor data bus and the Ethernet data bus.
This means that the processor data bits 0..7 are connected
to Ethernet data bits 8..15 and vice versa.

If a bus error is encountered during an Ethernet DVMA cycle,
the Ethernet bus error flipflop is set (ALS74:U719-1) causing
the Ethernet Error signal to be asserted (E.ERR).
This signal prevents future Ethernet DVMA requests to be set
in the Ethernet DVMA request flipflop (74F74:U207-1).
The Ethernet bus error flipflop can only be reset by an
Ethernet reset command (E.RESET).


```


82586 State	|   T0   |  T1   |  T2   |  T3   |  T4   |

C-125		_----____----____----____----____----____--

E.RD\		-____________________----------------------

E.RD0\		---------________________------------------

E.RD1\		-----------------________________----------


```


---

## VME Bus Interface


*Reference:* Schematics Page 8, 9, VME Bus Manual.

The VME Bus interface consists of the following functions:

- VME Bus Utility Functions

- VME Arbiter

- VME Master Interface

- VME Slave Interface

- VME Interrupt Handler


### VME Bus Utility Functions


The VME Bus Utility functions are implemented by these four utility lines:
System Clock (P1.SYSCLK), AC Fail (P1.ACFAIL), System Reset (P1.SYSR),
and System Fail (P1.SYSF).

System Clock is driven from the 16 MHz Ethernet clock signal (C-62A)
via a high-current driver (74F244:U919).
System Clock has no phase relationship with any other VME signals.
It can be disconnected from the VME Bus by removing jumper (J.16:J900-15.16).

AC Fail is driven to the VME Bus by open collector driver (7438:U814-2).
It is asserted while Power-On-Reset is active.
It cannot be disconnected from the VME Bus.

System Reset is driven to the VME Bus by open collector driver (7438:U814-3).
It is asserted whenever Processor-Reset is active.
It cannot be disconnected from the VME Bus.

System Fail is not used by this board.


### VME Arbiter


The VME Arbiter allows multiple masters on the VME Bus to
request and access the bus.
Out of the many arbiter options possible within the VME Bus Spec,
the arbiter implements the ONE ROR option.
ONE means that the arbiter monitors only bus request level 3 (P1.BR3)
and accomplishes arbitration via the level 3 daisy chain (P1.BG3IN,P1.BG3OUT).
ROR means "release on request", that is, the arbiter only releases the bus
when a request from another master is pending.

The arbiter is implemented as a state machine (74F374:U812, P9X4:U811).
When the CPU wants to access the VME Bus, either for a standard
read/write cycle or for a interrupt acknowledge cycle,
Bus Select (B.BSEL) is asserted by PAL (P16L8:U810).

<state machine description>


### VME Master Interface


The VME Master Interface allows the 2050 Board to access VME Slaves
on the VME Bus.


### VME Slave Interface


The VME Slave Interface allows the 2050 Board to be accessed
by other VME Masters on the VME Bus.


### VME Interrupt Handler


The VME Interrupt Handler responds to Interrupts on the VME Bus.
The 2050 Board does not generate any interrupts to the VME Bus.

---

## Memory Section


*Reference:* Schematics Page 11, 12, 13, 14, 15>


### Memory Interface


The memory interfaces to the CPU via the P2.Bus.
This means that all interface signals are available
on the P2-connector (P96:P1102), allowing a memory
expansion board to be interfaced to the same bus.
The following description applies equally to
the memory on the CPU Board as well as to the expansion memory.


### Memory Organization


Memory is organized as 8 banks of 18 RAM chips each,
making a total of 144 chips.
Each bank stores 16 data bits and 2 parity bits.

RAM chips can be either 64K or 256K Bits.
With 64K RAMs, each bank stores 128K Bytes plus parity,
and all of memory stores one Megabyte.

With 256K RAMs, each bank stores 512K Bytes plus parity,
making total memory capacity four Megabytes.


### Memory RAM and Bank Decoding


Due to the pipelined RAS-CAS access, memory is CAS decoded
because the translated address bits that select
which bank of memory is accessed are only available
in time for the CAS address strobe.
For special cycles (Q.SPEC active), such as MMU updates,
CAS is not asserted.

Decoding for 64K and 256K RAM chips is as follows:


```

--------------------------------------------------
  Decoding	64K RAMs	256K RAMs
--------------------------------------------------
  RAS Bank	A01		A01
  RAS Address	A02..A09	A02..A10
  CAS Address	A10..A17	A11..A18
  CAS Bank	A01,20,21	A01,A20,A21
--------------------------------------------------

```


### Memory Section Decoding


To allow the memory to respond to arbitrary 1 MByte sections
within the 8 MByte memory address space, memory select decoder
(74F151:U1200) decodes the three high-order address bits (P2.A20..A22)
and reads from the select jumper (J16:J1200) whether the
addressed 1 MByte section of memory is enabled or not.
If it is enabled, the Memory Select signal (M.SEL)
enables the CAS decoder and the read/write buffers.


### Memory Drivers


The RAM signals are driven as follows:

RAS, WEL, WEU, and the Address Lines are driven by
74F244 drivers with 33 OHM series termination.
Each bank of memory has its own set of drivers for these signals.

CAS is driven directly by the CAS decoder (74F138:U1201)
with 33 OHM series termination.
DataIn is driven by ALS244 drivers with 68 OHM series termination.

---

## Video Interface


```


-------------------------------------------------------------------
READ CYCLE

P2.RD\	-------________________________----------------------------

RDACK\	-----------------------________----------------------------

REQ\	-------________________------------------------------------

ACK\	-----------------------____--------------------------------

BUSY\	-------________________------------------------------------

-------------------------------------------------------------------
WRITE CYCLE

P2.WR\	-------____------------------------------------------------

RDACK\	-----------------------------------------------------------

REQ\	-------________________------------------------------------

ACK\	-----------------------____--------------------------------

BUSY\	-----------____________------------------------------------

-------------------------------------------------------------------
WRITE CYCLE FOLLOWED BY WRITE CYCLE

P2.WR\	-------____--------____________----------------------------

RDACK\	-----------------------------------------------------------

REQ\	-------________________----______________------------------

ACK\	-----------------------____--------------____--------------

BUSY\	-----------____________--------__________------------------

-------------------------------------------------------------------
WRITE CYCLE FOLLOWED BY READ CYCLE

P2.WR\	-------____------------------------------------------------

P2.RD\	-------____--------____________________________------------

RDACK\	-----------------------------------------______------------

REQ\	-------________________----______________------------------

ACK\	-----------------------____--------------____--------------

BUSY\	-----------______________________________------------------


```


---

## Video State Machine


```

XREQ=0
--------------------------------------------------------------------------------
State		0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
--------------------------------------------------------------------------------
V.OE		0       1       2       3	4       5       6       7

V.C(40.0-20)	--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__

V.RAS\		--------------------------------------------____________________

V.CAS\		____------------------------------------------------____________

V.VRA\		--------------------------------________________----------------

V.VCA\		------------------------------------------------________________

V.PRA\		----------------------------------------------------------------

V.PCA\		----------------------------------------------------------------

V.G\		____------------------------------------------------____________

V.W\		----------------------------------------------------------------

V.HCLK		________--------________________________________________________

V.ENREQ		----____________________________________________________________

XREQ=1
--------------------------------------------------------------------------------
State		0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
--------------------------------------------------------------------------------
V.OE		0       1       2       3	4       5       6       7

V.C(40.0-20)	--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__

V.RAS\		------------____________________------------____________________

V.CAS\		____----------------________________----------------____________

V.VRA\		--------------------------------________________----------------

V.VCA\		------------------------------------------------________________

V.PRA\		________________------------------------------------------------

V.PCA\		----------------________________--------------------------------

V.G\		____----------------________________----------------____________

V.W\		------------________________________----------------------------

V.ACK\		----------------------------________----------------------------

V.HCLK		________--------________________________________________________

V.ENREQ		----____________________________________________________________


```


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

## Video Clock and Shifter


```


V.C(10.0-5)	--__--__--__--__--__¬-__--__--__--__--__--__--__--__--__--__--__

V.C(20.0-10)	----____----____----____----____----____----____----____----____

V.C(20.10-0)	____----____----____----____----____----____----____----____----

V.C(40.0-20)	--------________--------________--------________--------________

V.STATE0	________________----------------________________----------------

V.DISPEN	--------------------------------________________________________

V.LOAD		________--------________________________________________________

V.LDEN		________________--------________________________________________

V.LD0		____________________--------____________________________________

V.LD1		________________________--------________________________________


```


---

# Jumpers


This chapter describes all the jumpers used on the board.
In the following listing, each group of jumpers denotes
exlusive combinations. That means, within each group only
one of of the jumpers combinations may be active at a time.


## Test Jumpers


The following jumpers are test jumpers only and are not
modified for normal machine operation.
Jumper positions labelled with * indicate combinations
used for testing purposes.


```


------------------------------------------------------
LABEL	PINS	IN/OUT	DESCRIPTION
------------------------------------------------------
J200	1-2	in	UART Clock 19.6608MHZ Enabled
J200	1-2	out *	UART Clock 19.6608MHZ Disabled
------------------------------------------------------
J200	3-4	in	CPU Clock = 19.6608MHZ
J200	5-6	in	CPU CLock = 25.0000MHZ
J200	7-8	in	CPU CLock = Video CLock / 4
J200	9-10	in	CPU Clock = 16.0000MHZ
J200	3-10	out *	CPU Clock disabled
------------------------------------------------------
J200	11-12	in	Ethernet Clock Enabled
J200	11-12	out *	Ethernet Clock Disabled
------------------------------------------------------
J200	13-14	in	One Refresh every 256 clocks
J200	15-16	in	One Refresh every 512 clocks
J201	13-16	out *	Refresh Disabled
------------------------------------------------------
J1800	1-2	in	100.000MHz Clock Enabled
J1800	1-2	out *	100.000MHz Clock Disabled
------------------------------------------------------


```


## Jumpers


This section lists the regular jumpers.


```

------------------------------------------------------
J500	1-2	in	PROM TYPE = 27128
J500	3-4	in	PROM TYPE = 27256 or 27512
J500	5-6	in	PROM TYPE = 27128 or 27256
J500	7-8	in	PROM TYPE = 27512
------------------------------------------------------
J702	1-2	in	5 Volt on Ethernet Enabled
J702	1-2	out	5 Volt on Ethernet Disabled
------------------------------------------------------
J704	1-2	in	Ethernet Level 2 Transceiver
J704	1-2	out	Ethernet Level 1 Transceiver
------------------------------------------------------
J800	1-2	in	Enable VME Interrupt Level 1
J800	1-2	out	Disable VME Interrupt Level 1
------------------------------------------------------
J800	3-4	in	Enable VME Interrupt Level 2
J800	3-4	out	Disable VME Interrupt Level 2
------------------------------------------------------
J800	5-6	in	Enable VME Interrupt Level 3
J800	5-6	out	Disable VME Interrupt Level 3
------------------------------------------------------
J800	7-8	in	Enable VME Interrupt Level 4
J800	7-8	out	Disable VME Interrupt Level 4
------------------------------------------------------
J800	9-10	in	Enable VME Interrupt Level 5
J800	9-10	out	Disable VME Interrupt Level 5
------------------------------------------------------
J800	11-12	in	Enable VME Interrupt Level 6
J800	11-12	out	Disable VME Interrupt Level 6
------------------------------------------------------
J800	13-14	in	Enable VME Interrupt Level 7
J800	13-14	out	Disable VME Interrupt Level 7
------------------------------------------------------
J900	1-2	in	DVMA Address Comparator A20=0
J900	1-2	out	DVMA Address Comparator A20=1
------------------------------------------------------
J900	3-4	in	DVMA Address Comparator A21=0
J900	3-4	out	DVMA Address Comparator A21=1
------------------------------------------------------
J900	5-6	in	DVMA Address Comparator A22=0
J900	5-6	out	DVMA Address Comparator A22=1
------------------------------------------------------
J900	7-8	in	DVMA Address Comparator A23=0
J900	7-8	out	DVMA Address Comparator A23=1
------------------------------------------------------
J900	9-10	in	Provide Bus Grant In Function
J900	9-10	out	Use VME Bus Grant In Function
------------------------------------------------------
J900	11-12	in	Enable Rerun Requests on BR0\
J900	11-12	out	Disable Rerun Requests on BR0\
------------------------------------------------------
J900	15-16	in	Enable Driving System Clock
J900	15-16	out	Disable Driving System Clock
------------------------------------------------------
J1600	1-2	i/o	Video Register Sense Bit 0
J1600	3-4	i/o	Video Register Sense Bit 1
J1600	5-6	i/o	Video Register Sense Bit 2
J1600	7-8	i/o	Video Register Sense Bit 3
------------------------------------------------------
J1801	1-2	in	900 vertical line mode
J1801	3-4	in	1024 vertical line mode
------------------------------------------------------
J1801	5-6	in	video interrupts enabled
J1801	5-6	out	video interrupts enabled
------------------------------------------------------
J1801	7-8	in	100 MHZ Video Clock enabled
J1801	7-8	out	100 MHZ Video Clock disabled
------------------------------------------------------

```


---
## PROMs


This section describes the language for specifying PROMs.
The content of these elements is defined in a high-level
functional language which is automatically translated
into bitpatterns for programming.

Without attempting to give a full definition of the language,
the following explanation should provide sufficient information
to understand the programs.

*begin "name"* begins a program with the name *name*.

*require "prom.sai" source!file* requests inclusion of the prom library.

*$#1$#2* defines a PROM with *#1* addressable locations *#2* bits wide.

*adrs(bit, polarity, name)* assigns *<name>* to address bit *<bit>*.
If polarity is 1 then the function of the name is true, if 0, inverted.

*define "name" = [definition]* defines expressions or equations
that describe the function of the PROM.
The following are reserved identifiers: *D#* is the value of
data bit *#*, *A#* is true if address bit *#* is present in the
current value of the location counter (see below).
All standard operators, including logical AND and OR, are allowed
in expressions. Conditional and case expressions are also possible.

*prombegin* tells the program to evaluate the following statements
until *promend* for each location value of the location counter.

*bit(#1, #2, expression)*
puts the value of *expression* into PROM *#1* bit position *#2*.
A single program can define the contents of multiple PROMs by using
multiple PROM numbers *#1*.

*promend* terminates the evaluation of statements.

*writeprom("file",#)* writes the object code of PROM *#* into file *file*.
Each separate PROM needs to be written into a separate file.

*end* terminates the program.

The PROM source code is followed by the generated
hexadecimal object code which also includes a 16-bit checksum.


## PROM: A811 Sourcefile

> 📄 **Source:** `a811.sai`
```
comment This information proprietary to SUN MICROSYSTEMS INC.;
begin "a811"

require "prom.sai" source!file;
$512$4;

adrs(0,0,bgout);
adrs(1,0,bbout);
adrs(2,0,brout);
adrs(3,0,aen);
adrs(4,0,bbin);
adrs(5,0,brin);
adrs(6,0,bas);
adrs(7,0,sel);
adrs(8,0,bgin);

define

IDLESTATE	=[(¬bgout ∧ ¬bbout ∧ ¬brout ∧ ¬aen)],
BUSGRANTSTATE	=[(bgout)],
BUSREQUESTSTATE	=[(brout)],
WAITFORBUSSTATE	=[(bbout ∧ ¬aen)],
BUSMASTERSTATE	=[(bbout ∧ aen)],

comment		All undefined states will go to IDLESTATE;

BUSGRANTSTATE$	=[(BUSGRANTSTATE ∧ ¬(¬brin ∨ bbin ∨ ¬bgin)
		∨  IDLESTATE ∧ brin ∧ ¬bbin ∧ bgin
		∨  BUSMASTERSTATE ∧ brin ∧ ¬sel)],

BUSREQUESTSTATE$=[(BUSREQUESTSTATE ∧ ¬(¬bbin ∧ ¬bas ∧ sel) ∧ ¬sel
		∨  IDLESTATE ∧ bbin ∧ sel
		∨  IDLESTATE ∧ sel ∧ ¬bgin)],

WAITFORBUSSTATE$=[(WAITFORBUSSTATE ∧ ¬(¬bas ∧ sel) ∧ ¬sel
		∨  IDLESTATE ∧ sel ∧ ¬bbin ∧ bas ∧ bgin)],

BUSMASTERSTATE$	=[(BUSMASTERSTATE ∧ sel
		∨  BUSMASTERSTATE ∧ ¬sel ∧ ¬brin ∧ bgin
		∨  IDLESTATE ∧ ¬bbin ∧ ¬bas ∧ sel ∧ bgin
		∨  WAITFORBUSSTATE ∧ ¬bas ∧ sel
		∨  BUSREQUESTSTATE ∧ ¬bbin ∧ ¬bas ∧ sel ∧ bgin)],

bgout$	=[(BUSGRANTSTATE$)],
bbout$	=[(BUSMASTERSTATE$ ∨ WAITFORBUSSTATE$)],
brout$	=[(BUSREQUESTSTATE$)],
aen$	=[(BUSMASTERSTATE$)];

prombegin

bit(0,0,	¬bgout$);
bit(0,1,	¬bbout$);
bit(0,2,	¬brout$);
bit(0,3,	¬aen$);

promend;
writeprom("a811",0);
end "a811";

```


## PROM: A811 Objectfile

> 📄 **Source:** `a811.hex`
```
:1000000005050F0F05050F0F0F0F0F0F0F0F0F0B2C
:1000100004050E0F04050E0F0E0F0E0F0E0F0E0C23
:1000200005050F0F05050F0F0F0F0F0F0F0F0F0B0C
:1000300005050F0F05050F0F0F0F0F0F0F0F0F0DFA
:1000400005050F0F05050F0F05050F0F05050F0B14
:100050000405040504050E0F0405040504050E043B
:1000600005050F0F05050F0F05050F0F05050F0BF4
:100070000505050505050F0F0505050505050F0512
:100080000A0A0B0B0E0E0F0F09090B0B0D0D0F0FAC
:100090000A0A0A0B0E0E0E0F08090A0B0C0D0E0EA3
:1000A00001010B0B05050F0F09090B0B0D0D0F0FB0
:1000B00001010B0B05050F0F09090B0B0D0D0F0FA0
:1000C0000A0A0B0B0E0E0F0F09090B0B0D0D0F0F6C
:1000D0000A0A0A0B0E0E0E0F08090A0B0C0D0E0E63
:1000E00001010B0B05050F0F09090B0B0D0D0F0F70
:1000F00001010B0B05050F0F09090B0B0D0D0F0F60
:1001000005050F0F05050F0F0F0F0F0F0F0F0F0B2B
:1001100005050F0F05050F0F0F0F0F0F0F0F0F0B1B
:1001200005050F0F05050F0F0F0F0F0F0F0F0F0B0B
:1001300005050F0F05050F0F0F0F0F0F0F0F0F0BFB
:1001400005050F0F05050F0F05050F0F05050F0B13
:1001500005050F0F05050F0F05050F0F05050F0B03
:1001600005050F0F05050F0F05050F0F05050F0BF3
:1001700005050F0F05050F0F05050F0F05050F0BE3
:100180000A0A0B0B0E0E0F0F09090B0B0D0D0F0FAB
:100190000A0A0B0B0E0E0F0F09090B0B0D0D0F0F9B
:1001A0000B0B0B0B0F0F0F0F09090B0B0D0D0F0F87
:1001B0000B0B0B0B0F0F0F0F09090B0B0D0D0F0F77
:1001C0000A0A0B0B0E0E0F0F09090B0B0D0D0F0F6B
:1001D0000A0A0B0B0E0E0F0F09090B0B0D0D0F0F5B
:1001E0000B0B0B0B0F0F0F0F09090B0B0D0D0F0F47
:1001F0000B0B0B0B0F0F0F0F09090B0B0D0D0F0F37
:0000000000
PROM 	a811	Checksum 	1648


```


## PROM: A811 Timingfile

> 📄 **Source:** `a811.tim`
```
A0	¬bgout	_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
A1	¬bbout	__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--
A2	¬brout	____----____----____----____----____----____----____----____----
A3	¬aen	________--------________--------________--------________--------
A4	¬bbin	________________----------------________________----------------
A5	¬brin	________________________________--------------------------------
A6	¬bas	________________________________________________________________
A7	¬sel	________________________________________________________________
A8	¬bgin	________________________________________________________________

D0	¬bgout$	----------------_-_-_-_-_-_-_-__--------------------------------
D1	¬bbout$	__--__----------__--__---------___--__----------__--__---------_
D2	¬brout$	---------------_-------------------------------_----------------
D3	¬aen$	__--__----------__--__----------__--__----------__--__----------

D0	¬bgout$	----------------_-_-_-_-_-_-_-__--------------------------------
D1	¬bbout$	__--__--__--__--______--______-___--__--__--__--______--______-_
D2	¬brout$	---------------_-------------------------------_----------------
D3	¬aen$	__--__--__--__--______--______-___--__--__--__--______--______-_

D0	¬bgout$	__--__----------___-___-_-_-_-__--------------------------------
D1	¬bbout$	--------__--__----------__--__--__--__--__--__--__--__--__--__--
D2	¬brout$	____----____----____----____----____----____----____----____----
D3	¬aen$	--------------------------------__--__----------__--__----------

D0	¬bgout$	__--__----------___-___-_-_-_-__--------------------------------
D1	¬bbout$	--------__--__----------__--__--__--__--__--__--__--__--__--__--
D2	¬brout$	____----____----____----____----____----____----____----____----
D3	¬aen$	--------------------------------__--__----------__--__----------

D0	¬bgout$	----------------------------------------------------------------
D1	¬bbout$	__--__----------__--__----------__--__----------__--__----------
D2	¬brout$	---------------_---------------_---------------_---------------_
D3	¬aen$	__--__----------__--__----------__--__----------__--__----------

D0	¬bgout$	----------------------------------------------------------------
D1	¬bbout$	__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--
D2	¬brout$	---------------_---------------_---------------_---------------_
D3	¬aen$	__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--

D0	¬bgout$	__--__----------__--__------------------------------------------
D1	¬bbout$	--------__--__----------__--__----------__--__----------__--__--
D2	¬brout$	____----____----____----____----____----____----____----____----
D3	¬aen$	----------------------------------------------------------------

D0	¬bgout$	__--__----------__--__------------------------------------------
D1	¬bbout$	--------__--__----------__--__----------__--__----------__--__--
D2	¬brout$	____----____----____----____----____----____----____----____----
D3	¬aen$	----------------------------------------------------------------


```


## PROM: A1604 Sourcefile

> 📄 **Source:** `a1604.sai`
```
comment This information proprietary to SUN MICROSYSTEMS INC.;
begin "a1604"

require "prom.sai" source!file;
$32$8;

adrs(0,1,	state0);
adrs(1,1,	state1);
adrs(2,1,	state2);
adrs(3,1,	state3);
adrs(4,1,	xreq);

define

state	=[(state0*d0 + state1*d1 + state2*d2 + state3*d3)],
nstate	=[((state + 1) MOD 16)],
pra	=[(xreq ∧ (0≤nstate≤3))],
pca	=[(xreq ∧ (4≤nstate≤7))],
vra	=[(8≤nstate≤11)],
vca	=[(12≤nstate≤15)],
voe(n)	=[((nstate DIV 2 )=n)],
ras	=[(xreq ∧ (3≤nstate≤7) ∨ (11≤nstate≤15))],
cas	=[(xreq ∧ (5≤nstate≤8) ∨ (13≤nstate≤15) ∨ nstate=0)],
g	=[(xreq ∧ (5≤nstate≤8) ∨ (13≤nstate≤15) ∨ nstate=0)],
webuf	=[(xreq ∧ (nstate=8))],
w	=[(xreq ∧ (3≤nstate≤8))],
hclk	=[(2≤nstate≤3)],
load	=[(¬(nstate LAND d0))],
enreq	=[(nstate=0)],
ack	=[(xreq ∧ (7≤nstate≤8))];

prombegin

bit(0,0,	nstate LAND d0);
bit(0,1,	nstate LAND d1);
bit(0,2,	nstate LAND d2);
bit(0,3,	nstate LAND d3);
bit(0,4,	¬pra);
bit(0,5,	¬pca);
bit(0,6,	¬vra);
bit(0,7,	¬vca);

bit(1,0,	¬ras);
bit(1,1,	¬cas);
bit(1,2,	¬g);
bit(1,3,	¬w);
bit(1,4,	hclk);
bit(1,5,	load);
bit(1,6,	enreq);
bit(1,7,	¬ack);

promend;

writeprom("a1604",0);
writeprom("a1605",1);

end "a1604"

```


## PROM: A1604 Objectfile

> 📄 **Source:** `a1604.hex`
```
:10000000F1F2F3F4F5F6F7B8B9BABB7C7D7E7FF078
:10001000E1E2E3D4D5D6D7B8B9BABB7C7D7E7FE028
:0000000000
PROM 	a1604	Checksum 	1830


```


## PROM: A1605 Timingfile

> 📄 **Source:** `a1604.tim`
```
A0	state0	_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
A1	state1	__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--
A2	state2	____----____----____----____----____----____----____----____----
A3	state3	________--------________--------________--------________--------
A4	xreq	________________----------------________________----------------

D0	nstate 	-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_________________________________
D1	nstate 	_--__--__--__--__--__--__--__--_________________________________
D2	nstate 	___----____----____----____----_________________________________
D3	nstate 	_______--------________--------_________________________________
D4	¬pra	----------------___------------_________________________________
D5	¬pca	-------------------____---------________________________________
D6	¬vra	-------____------------____-----________________________________
D7	¬vca	-----------____------------____-________________________________


```


## PROM: A1605 Objectfile

> 📄 **Source:** `a1605.hex`
```
:10000000BFAFAFAFAFAFAFAFAFAFAEAEA8A8A8E9CD
:10001000BFAFA6A6A0202001AFAFAEAEA8A8A8E9AA
:0000000000
PROM 	a1605	Checksum 	1459


```


## PROM: A1605 Timingfile

> 📄 **Source:** `a1605.tim`
```
A0	state0	_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
A1	state1	__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--
A2	state2	____----____----____----____----____----____----____----____----
A3	state3	________--------________--------________--------________--------
A4	xreq	________________----------------________________----------------

D0	¬ras	----------_____---_____---_____-________________________________
D1	¬cas	------------____----____----____________________________________
D2	¬g	------------____----____----____________________________________
D3	¬w	------------------______--------________________________________
D4	hclk	-_______________-_______________________________________________
D5	¬webuf	-----------------------_--------________________________________
D6	enreq	_______________-_______________-________________________________
D7	¬ack	---------------------___--------________________________________


```


## PROM: A1811 Sourcefile

> 📄 **Source:** `a1811.sai`
```
begin "a1811"

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
$512$4;

adrs(0,1,h0);
adrs(1,1,h1);
adrs(2,1,h2);
adrs(3,1,h3);
adrs(4,1,h4);
adrs(5,1,h5);
adrs(6,1,h6);
adrs(7,1,h7);
adrs(8,1,vblank);

define

state	=[((h0*d0 + h1*d1 + h2*d2 + h3*d3 + h4*d4 + h5*d5 + h6*d6 + h7*d7) MOD 24)],
nstate	=[((state + 1) MOD 24)],

dispen	=[(¬vblank ∧ (0≤nstate≤17))],
hsync	=[(18≤nstate≤21)],
hreset	=[(nstate = 0)];

prombegin

bit(0,0,	hsync);
bit(0,1,	dispen);
bit(0,2,	¬dispen);
bit(0,3,	hreset);

promend;
writeprom("a1811",0);
end "a1811";

```


## PROM: A1811 Objectfile

> 📄 **Source:** `a1811.hex`
```
:1000000002020202020202020202020202020202D0
:10001000020505050504040A0202020202020202A8
:100020000202020202020202020505050504040A98
:1000300002020202020202020202020202020202A0
:10004000020505050504040A020202020202020278
:100050000202020202020202020505050504040A68
:100060000202020202020202020202020202020270
:10007000020505050504040A020202020202020248
:100080000202020202020202020505050504040A38
:100090000202020202020202020202020202020240
:1000A000020505050504040A020202020202020218
:1000B0000202020202020202020505050504040A08
:1000C0000202020202020202020202020202020210
:1000D000020505050504040A0202020202020202E8
:1000E0000202020202020202020505050504040AD8
:1000F00002020202020202020202020202020202E0
:1001000004040404040404040404040404040404AF
:10011000040505050504040C040404040404040493
:100120000404040404040404040505050504040C83
:10013000040404040404040404040404040404047F
:10014000040505050504040C040404040404040463
:100150000404040404040404040505050504040C53
:10016000040404040404040404040404040404044F
:10017000040505050504040C040404040404040433
:100180000404040404040404040505050504040C23
:10019000040404040404040404040404040404041F
:1001A000040505050504040C040404040404040403
:1001B0000404040404040404040505050504040CF3
:1001C00004040404040404040404040404040404EF
:1001D000040505050504040C0404040404040404D3
:1001E0000404040404040404040505050504040CC3
:1001F00004040404040404040404040404040404BF
:0000000000
PROM 	a1811	Checksum 	0768


```


## PROM: A1811 Timingfile

> 📄 **Source:** `a1811.tim`
```
A0	h0	_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
A1	h1	__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--
A2	h2	____----____----____----____----____----____----____----____----
A3	h3	________--------________--------________--------________--------
A4	h4	________________----------------________________----------------
A5	h5	________________________________--------------------------------
A6	h6	________________________________________________________________
A7	h7	________________________________________________________________
A8	vblank	________________________________________________________________

D0	hsync	_________________----____________________----___________________
D1	dispen	-----------------______------------------______-----------------
D2	¬dispen	_________________------__________________------_________________
D3	hreset	_______________________-_______________________-________________

D0	hsync	_----____________________----____________________----___________
D1	dispen	-______------------------______------------------______---------
D2	¬dispen	_------__________________------__________________------_________
D3	hreset	_______-_______________________-_______________________-________

D0	hsync	_________----____________________----____________________----___
D1	dispen	---------______------------------______------------------______-
D2	¬dispen	_________------__________________------__________________------_
D3	hreset	_______________-_______________________-_______________________-

D0	hsync	_________________----____________________----___________________
D1	dispen	-----------------______------------------______-----------------
D2	¬dispen	_________________------__________________------_________________
D3	hreset	_______________________-_______________________-________________

D0	hsync	_________________----____________________----___________________
D1	dispen	________________________________________________________________
D2	¬dispen	----------------------------------------------------------------
D3	hreset	_______________________-_______________________-________________

D0	hsync	_----____________________----____________________----___________
D1	dispen	________________________________________________________________
D2	¬dispen	----------------------------------------------------------------
D3	hreset	_______-_______________________-_______________________-________

D0	hsync	_________----____________________----____________________----___
D1	dispen	________________________________________________________________
D2	¬dispen	----------------------------------------------------------------
D3	hreset	_______________-_______________________-_______________________-

D0	hsync	_________________----____________________----___________________
D1	dispen	________________________________________________________________
D2	¬dispen	----------------------------------------------------------------
D3	hreset	_______________________-_______________________-________________


```


## PROM: A1815 Sourcefile

> 📄 **Source:** `a1815.sai`
```
begin "a1815"

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
$512$4;

adrs(0,1,v10);
adrs(1,1,v1);
adrs(2,1,v2);
adrs(3,1,v3);
adrs(4,1,v4);
adrs(5,1,v5);
adrs(6,1,v6);
adrs(7,1,v7);
adrs(8,1,v89);

define

line	=[(v1*d1 + v2*d2 + v3*d3 + v4*d4
	 + v5*d5 + v6*d6 + v7*d7 + v89*d8 + v89*d9)],

vsync	=[(900≤line≤909)],
reset	=[(line = 935)],
vblank	=[(line ≥ 900)],
vreset	=[(line = 935)];

prombegin

bit(0,0,	vsync);
bit(0,1,	¬reset);
bit(0,2,	vblank);
bit(0,3,	vreset);

promend;
writeprom("a1815",0);
end "a1815";

```


## PROM: A1815 Objectfile

> 📄 **Source:** `a1815.hex`
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
:1001A00006060606060606060606060606060606EF
:1001B00006060606060606060606060606060606DF
:1001C00006060606060606060606060606060606CF
:1001D00006060606060606060606060606060606BF
:1001E00006060606060606060606060606060606AF
:1001F000060606060606060606060606060606069F
:0000000000
PROM 	a1815	Checksum 	05FA


```


## PROM: A1815 Timingfile

> 📄 **Source:** `a1815.tim`
```
A0	v10	_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
A1	v1	__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--
A2	v2	____----____----____----____----____----____----____----____----
A3	v3	________--------________--------________--------________--------
A4	v4	________________----------------________________----------------
A5	v5	________________________________--------------------------------
A6	v6	________________________________________________________________
A7	v7	________________________________________________________________
A8	v89	________________________________________________________________

D0	vsync	________________________________________________________________
D1	¬reset	----------------------------------------------------------------
D2	vblank	________________________________________________________________
D3	vreset	________________________________________________________________

D0	vsync	________________________________________________________________
D1	¬reset	----------------------------------------------------------------
D2	vblank	________________________________________________________________
D3	vreset	________________________________________________________________

D0	vsync	________________________________________________________________
D1	¬reset	----------------------------------------------------------------
D2	vblank	________________________________________________________________
D3	vreset	________________________________________________________________

D0	vsync	________________________________________________________________
D1	¬reset	----------------------------------------------------------------
D2	vblank	________________________________________________________________
D3	vreset	________________________________________________________________

D0	vsync	________________________________________________________________
D1	¬reset	----------------------------------------------------------------
D2	vblank	________________________________________________________________
D3	vreset	________________________________________________________________

D0	vsync	________________________________________________________________
D1	¬reset	----------------------------------------------------------------
D2	vblank	________________________________________________________________
D3	vreset	________________________________________________________________

D0	vsync	____----------__________________________________________________
D1	¬reset	----------------------------------------------------------------
D2	vblank	____------------------------------------------------------------
D3	vreset	________________________________________________________________

D0	vsync	________________________________________________________________
D1	¬reset	----------------------------------------------------------------
D2	vblank	----------------------------------------------------------------
D3	vreset	________________________________________________________________


```


---
## PROMs


This section contains the definition of the PAL circuits used.
The function of these circuits is defined in a high-level
functional language which is automatically translated
into bitpatterns for programming.

Without attempting to give a full definition of the language,
the following explanation should provide sufficient information
to understand the programs.

*"%"* indicates a comment, everything to the right of it is ignored.

*"#include "pal...""* requests inclusion of the respective PAL definition file.

*"pin#"* is a reserved name for the pin with the number #.

*"#define symbol1 symbol2"* causes a verbatim substitution of symbol1 into symbol2.

*"{{ }}"*: the min-term within the double curly brackets is the
tri-state enable condition for the current output.

*"/"* is the negation operator, ("/ /") indicates double negation.

*"*"* is the AND operator which combines inputs into min-expressions.

*"+"* is the OR operator which combines min-expressions into max-expressions.

*":+:"* is the XOR operator which combines max-expressions into xor-expressions
for those PALs which offer this feature.

*":="* is the assignment operator which assigns the expression on the
right-hand-side to the output pin on the left.


## PAL: A101 Sourcefile

> 📄 **Source:** `a101.pal`
```
#include "pal16l8"

PALBEGIN
PALID = "A101.pal	1.0	84/01/01";

#define	FC0	pin1
#define	FC1	pin2
#define	FC2	pin3
#define	/BOOT	pin4
#define	/ILOCAL	pin5
#define	/DTACK	pin6
#define	AS	pin7
#define	CS7	pin8
#define	CS11	pin9
#define	/CEIO	pin11

#define	/MMU	pin19
#define	/UDATA	pin18
#define	/BOOTEN	pin17
#define	/SPECIA	pin16
#define	/INTVEC	pin15
#define	/AUTVEC	pin14
#define	/IOWAIT	pin13
#define	/SPWAIT	pin12

/MMU	:= {{ VCC }} / FC2 * FC1 * FC0 * AS

/UDATA	:= {{ VCC }} / FC2 * / FC1 * FC0 * AS

/BOOTEN	:= {{ VCC }}   FC2 * FC1 * / FC0 * / /BOOT * AS

/SPECIA	:= {{ VCC }}   FC1 * FC0				% INTA or MMU
	+    FC2 * FC1 * / FC0 * / /BOOT			% BOOT

/INTVEC	:= {{ VCC }}  FC2 * FC1 * FC0 * CS7 * /ILOCAL * AS

/AUTVEC	:= {{ VCC }}  FC2 * FC1 * FC0 * CS7 * / /ILOCAL * AS

/IOWAIT	:= {{ VCC }}  /CEIO * / CS7 * AS
	+  / /CEIO * / CS11 * AS

/SPWAIT	:= {{ VCC }} / FC2 * FC1 * FC0 * / CS7 * AS
	+    FC2 * FC1 * / FC0 * / /BOOT * / CS11 * AS
	+    FC2 * FC1 * FC0 * /ILOCAL * /DTACK * AS
	+    FC2 * FC1 * FC0 * / CS7 * AS

PALEND

```


## PAL: A102 Sourcefile

> 📄 **Source:** `a102.pal`
```
#include "pal16r4"

PALBEGIN
PALID = "A-U102.pal	0.9	84/01/01";

% Inputs

#define	/SPEC	pin2
#define	/CEIO	pin3
#define	/WRITE	pin4
#define	/DMA	pin5
#define	/POR	pin6
#define	/C10240	pin7
#define	/RERUN	pin8
#define	TYPE1	pin9

% Outputs

#define	/RDIO	pin19
#define	/WRIO	pin18
#define	/SBERR	pin17
#define	/SHALT	pin16
#define	/WDOG	pin15
#define	/INIT	pin14
#define	/PHALT	pin13
#define	/PRESET	pin12

/RDIO	:= {{ VCC }} /DMA * / /CEIO * /WRITE
	+  / /DMA * / /WRITE

/WRIO	:= {{ VCC }} /DMA * / /WRITE
	+  / /DMA * /CEIO * / TYPE1 * /WRITE

/SBERR	:= / /RERUN

/SHALT	:= / /RERUN
	+  / /SBERR

/WDOG	:= / /PHALT * /RERUN * /SHALT * /C10240
	+  / /WDOG * / /C10240

/INIT	:= / /POR
	+  / /WDOG
	+  / /SHALT

/PRESET	:= {{ / /INIT }} / /WDOG
	+  / /POR

/PHALT	:= {{ / /INIT }} / /WDOG
	+  / /POR
	+  / /SHALT

PALEND


```


## PAL: A103 Sourcefile

> 📄 **Source:** `a103.pal`
```

#include "pal16l8"

PALBEGIN
PALID = "A103.pal	1.0	84/01/01";

#define	ERROR	pin1
#define	/SPEC	pin2
#define	CS5	pin3
#define	CS7	pin4
#define	/DMA	pin5
#define	/WRPMAP	pin6
#define	/WRITE	pin7
#define	MOD	pin8
#define	/REF	pin9
#define	A1	pin11

#define	BANK0	pin19
#define	BANK1	pin18
#define	/BERR	pin17
#define	BERRCLK	pin16
#define	/WRSTAT	pin15
#define	/UPDATE	pin14
#define	/WRPMAX	pin13
#define	MOD1	pin12

BANK0	:= {{ VCC }} A1 * /REF

BANK1	:= {{ VCC }} / A1 * /REF

/BERR	:= {{ VCC }}  ERROR * CS5 * /SPEC

BERRCLK	:= {{ VCC }}  /BERR
	+  / /DMA

/UPDATE	:= {{ VCC }} / ERROR * CS5 * / CS7 * /SPEC
	+ / /WRPMAP * / /SPEC

/WRSTAT	:= {{ VCC }} / /UPDATE * /SPEC

/WRPMAX	:= {{ VCC }} / /UPDATE * / /SPEC

MOD1	:= {{ VCC }} / MOD * /WRITE

PALEND

```


## PAL: A214 Sourcefile

> 📄 **Source:** `a214.pal`
```
#include "pal16r8"

PALBEGIN
PALID = "A-U214.pal	0.9	84/01/01";

% Inputs

#define	/RREQ	pin2
#define	/EREQ	pin3
#define	/XREQ	pin4
#define	/GREQ	pin5
#define	/BGIN	pin6
#define	/ASIN	pin7
#define	/BERR	pin8
#define	QS7	pin9

% Outputs

#define	/REN	pin19
#define	/EEN	pin18
#define	/XEN	pin17
#define	/GEN	pin16
#define	/BR	pin15
#define	/BACK	pin14
#define	/ASOFF	pin13
#define	/DS	pin12

% FUNCTIONS

#define	IDLE	/REN * /EEN * /XEN * /GEN
#define	GRANT	/ /BGIN * /ASIN

/BACK	:=
	   / /REN * / /BACK * /ASIN
	+  / /EEN * / /BACK * / QS7 * /BERR
	+  / /XEN * / /BACK * / QS7 * /BERR
	+  / /GEN * / /BACK * / QS7 * /BERR

/BR	:= / /RREQ * /BACK
	+  / /EREQ * /BACK
	+  / /XREQ * /BACK
	+  / /GREQ

/REN	:= / /RREQ * GRANT * IDLE
	+  / /REN * /BACK

/EEN	:= / /EREQ * GRANT * IDLE * /RREQ
	+  / /EEN * /BACK

/XEN	:= / /XREQ * GRANT * IDLE * /RREQ * /EREQ
	+  / /XEN * /BACK

/GEN	:= / /GREQ * GRANT * IDLE * /RREQ * /EREQ * /XREQ
	+  / /GEN * /BACK

/ASOFF	:= / /EEN * QS7
	+  / /XEN * QS7
	+  / /REN * / /ASIN
	+  / /GEN * QS7
	+  / /BERR

PALEND


```


## PAL: A215 Sourcefile

> 📄 **Source:** `a215.pal`
```
#include "pal16l8"

PALBEGIN
PALID = "A800.pal	1.0	84/01/01";

#define	/REN	pin1
#define	/EEN	pin2
#define	/XEN	pin3
#define	/GEN	pin4
#define	/DMA	pin5
#define	/ASOFF	pin6
#define	/ASON	pin7
#define	/EA0	pin8
#define	/XLDS	pin9
#define	/XUDS	pin11

#define	/DMA0	pin19
#define	/DMA1	pin18
#define	FC0	pin17
#define	FC1	pin16
#define	FC2	pin15
#define	/AS	pin14
#define	/UDS	pin13
#define	/LDS	pin12

/DMA0	:={{ VCC }}	  / /EEN
		+ / /GEN

/DMA1	:={{ VCC }}	  / /XEN
		+ / /GEN

FC0	:={{ / /DMA }}	GND

FC1	:={{ / /DMA }}	/REN

FC2	:={{ / /DMA }}	/ /GEN

/AS	:={{ / /DMA }} / /ASON * /ASOFF

/UDS	:={{ / /DMA }}   / /GEN
		+ / /EEN * /EA0
		+ / /XEN * / /XUDS

/LDS	:={{ / /DMA }}   / /GEN
		+ / /EEN
		+ / /XEN * / /XLDS

PALEND

```


## PAL: A503 Sourcefile

> 📄 **Source:** `a503.pal`
```
#include "pal16l8"

PALBEGIN
PALID = "A-U503.pal	0.9	84/02/07";

% Inputs

#define	/RESET	pin1
#define	/UDATA	pin2
#define	/DMAEN	pin3
#define	/CEIO	pin4
#define	/WRROP	pin5
#define	D07	pin6
#define	/SEL	pin7
#define	CS5	pin8
#define	CS7	pin9
#define	CS9	pin11

% Outputs

#define	/LDSRC	pin19
#define	/ROP	pin18
#define	/DMAREQ	pin17
#define	/READ	pin16
#define	/WRITE	pin15
#define	/ROPCYC	pin14
#define	/WAIT	pin13
#define	/P2WAIT	pin12


/ROP	:= {{ VCC }} / /SEL * / /WRROP * D07 * /RESET	% Set
	+  / /ROP * /SEL * /RESET			% Hold
	+  / /ROP * /WRROP * /RESET			% Hold
	+  / /ROP * D07 * /RESET			% Hold

/ROPCYC	:= {{ VCC }} / /ROP * / /UDATA * / /WRITE * /DMAEN
	+ / /ROPCYC * / /READ * /DMAEN

/DMAREQ	:= {{ VCC }} / /ROPCYC				% Set at S5 + 35 nsec
	+  / /DMAREQ * /DMAEN				% Hold for 1st DMAEN
	+  / /DMAREQ * /WRITE 				% Hold til 2nd DMAEN

/LDSRC	:= {{ VCC }} / /ROPCYC * /CEIO * CS5 * / CS9

/READ	:= {{ VCC }} / /ROPCYC * /CEIO * CS5		% Set
	+  / /READ * / /DMAEN				% Hold for 1st DMAEN
	+  / /READ * / /ROPCYC

/WRITE	:= {{ / /DMAEN  }} /READ * / /DMAEN		% 2nd term for turnoff

/WAIT   := {{ VCC }} / /ROPCYC * / CS7   		% 2 Wait on LD←SRC

/P2WAIT := {{ / /WAIT }} / /WAIT

PALEND

```


## PAL: A507 Sourcefile

> 📄 **Source:** `a507.pal`
```
#include "pal16l8"

PALBEGIN
PALID = "A-U507.pal     0.9     84/01/01";

% Inputs

#define /RDDCP    pin1
#define /WRDCP    pin2
#define C160      pin3
#define C320      pin4
#define CS9       pin5
#define A01       pin6
#define A02       pin7
#define A03       pin8
#define A04       pin9

% Outputs

#define /MAS      pin19
#define /MDS_STRT pin18
#define /MDS_END  pin17
#define /TIME160  pin16
#define /TIME240  pin15
#define /WAIT     pin14
#define /P2WAIT   pin13
#define /ROPSEL   pin12


% Equations

/MAS      := {{ VCC }} A01 * / /WRDCP * / CS9           % Unclocked

/MDS_STRT := {{ VCC }} / /RDDCP * / CS9                 % Unclocked
           + / /WRDCP * / CS9
           + / /MDS_STRT * /TIME240

/MDS_END  := / /MDS_STRT * /TIME240                     % Clocked

/TIME160  := / /MDS_END * CS9 * / C320 * C160           % Clocked
           + / /TIME160 * /TIME240

/TIME240  := / /TIME160                                 % Clocked

/WAIT     := / /MDS_STRT * / /RDDCP * /TIME160 * / CS9  % Clocked
           + / /MDS_STRT * / /RDDCP * /TIME160 * C320
           + / /MDS_STRT * / /RDDCP * /TIME160 * / C160
           + / /MDS_STRT * / /WRDCP * /TIME240

/P2WAIT   := {{ / /WAIT }} / /WAIT                      % Unclocked

/ROPSEL   := {{ VCC }} A04 * A03 * A02 * A01            % Unclocked

PALEND

```


## PAL: A800 Sourcefile

> 📄 **Source:** `a800.pal`
```
#include "pal16l8"

PALBEGIN
PALID = "A800.pal	1.0	84/01/01";

#define	/V1	pin1
#define	/V2	pin2
#define	/V3	pin3
#define	/V4	pin4
#define	/V5	pin5
#define	/V6	pin6
#define	/V7	pin7
#define	I1	pin8
#define	I2	pin9
#define	I3	pin11

#define	/IPL0	pin19
#define	/IPL1	pin18
#define	EN	pin17
#define	/I4	pin16
#define	/I5	pin15
#define	/I6	pin14
#define	/PIN13	pin13
#define	/IPL2	pin12

#define	/7	/V7
#define	/67	/7 * /V6 * /I6
#define	/567	/67 * /V5 * /I5
#define	/4567	/567 * /V4 * /V4
#define	/34567	/4567 * /V3 * / I3
#define	/234567	/34567 * /V2 * / I2

/IPL0	:={{ VCC ⎇⎇
	     I1 * EN * /234567
	+    I3 * EN * /4567
	+ / /I5 * EN * /67
	+ / /V1 * EN * /234567
	+ / /V3 * EN * /4567
	+ / /V5 * EN * /67
	+ / /V7 * EN

/IPL1	:={{ VCC ⎇⎇
	     I2 * EN * /34567
	+    I3 * EN * /4567
	+ / /I6 * EN * /7
	+ / /V2 * EN * /34567
	+ / /V3 * EN * /4567
	+ / /V6 * EN * /7
	+ / /V7 * EN

/IPL2	:={{ VCC ⎇⎇
	  / /I4 * EN * /567
	+ / /I5 * EN * /67
	+ / /I6 * EN * /7
	+ / /V4 * EN * /567
	+ / /V5 * EN * /67
	+ / /V6 * EN * /7
	+ / /V7 * EN

PALEND

```


## PAL: A810 Sourcefile

> 📄 **Source:** `a810.pal`
```
#include "pal16l8"

PALBEGIN
PALID = "A810.pal	1.0	84/01/01";

#define	/DTACK	pin1
#define	/BERR	pin2
#define	/BROUT	pin3
#define	/BR	pin4
#define	/DMA	pin5
#define	/BEN	pin6
#define	/BOFF	pin7
#define	/RD	pin8
#define	/WR	pin9
#define	/INTVEC	pin11

#define	/PIN19	pin19
#define	/BSEL	pin18
#define	/RERUN	pin17
#define	CS6	pin16
#define	/DEN	pin15
#define	BS7	pin14
#define	/CEN	pin13
#define	/PIN12	pin12

/BSEL	:= {{ VCC }} / /RD
	+  / /WR
	+  / /INTVEC

/CEN	:= {{ VCC }}
	   / /BSEL * / /BEN * /RERUN * CS6 * / /INTVEC
	+  / /BSEL * / /BEN * /RERUN * CS6 * / /RD
	+  / /BSEL * / /BEN * /RERUN * CS6 * BS7 * / /WR

/DEN	:= {{ VCC }} / /BERR
	+  / /DTACK
	+  / /DEN * / /RD
	+  / /DEN * / /WR
	+  / /DEN * / /INTVEC

/RERUN	:= {{ VCC }} / /BR * / /BROUT	% rerun while waiting for bus
	+  / /BSEL * / /DMA		% rerun due to bus deadlock
	+  / /BOFF * / /CEN		% rerun due to external deadlock
	+  / /RERUN * / /RD
	+  / /RERUN * / /WR
	+  / /RERUN * / /INTVEC

PALEND


```


## PAL: A1616 Sourcefile

> 📄 **Source:** `a1616.pal`
```
#include "pal16l8"

PALBEGIN
PALID = "A1616.pal	1.0	84/01/01";

#define	BS1	pin1
#define	BS2	pin2
#define	/WEL	pin3
#define	/WEU	pin4
#define	/RAS	pin5
#define	/WE	pin6
#define	/REQ	pin7
#define	DISPEN	pin8
#define	STATE	pin9
#define	/PIN11	pin11

#define	/RAS0	pin19
#define	/RAS1	pin18
#define	/RAS2	pin17
#define	/RAS3	pin16
#define	/WU	pin15
#define	/WL	pin14
#define	REQ	pin13
#define	/DISPEN	pin12

/RAS0	:= {{ VCC }} / BS1 * / BS2 * / /RAS * / STATE
	+  / /RAS * STATE

/RAS1   := {{ VCC }}   BS1 * / BS2 * / /RAS * / STATE
	+  / /RAS * STATE

/RAS2	:= {{ VCC }} / BS1 *   BS2 * / /RAS * / STATE
	+  / /RAS * STATE

/RAS3	:= {{ VCC }}   BS1 *   BS2 * / /RAS * / STATE
	+  / /RAS * STATE

/WU	:= {{ VCC }} / /WE * / /WEU * / STATE

/WL	:= {{ VCC }} / /WE * / /WEL * / STATE

REQ	:= {{ VCC }} /REQ

/DISPEN	:= {{ VCC }} / DISPEN

PALEND


```


## PAL: A1620 Sourcefile

> 📄 **Source:** `a1620.pal`
```


paltype pal16l8
palname A1620
palid 1.9 84/05/15

PALBEGIN

% Inputs

1  INPUT V.BSEL-
2  INPUT V.CSEL-
3  INPUT P2.RD-
4  INPUT P2.WEU-
5  INPUT P2.WEL-
6  INPUT V.WL-
7  INPUT P2.A17
8  INPUT V.WU-
9  INPUT V.ACK
11 INPUT Q.AS

10 GND
20 VCC

% Outputs

19 OUTPUT V.RD-
18 OUTPUT V.RDC-
17 OUTPUT V.WLC
16 OUTPUT V.WUC
15 OUTPUT V.REQ-
14 OUTPUT V.RDACK-
13 OUTPUT V.WAIT-
12 OUTPUT VREQ				% NAME OK, we gen both V.REQ and V.REQ-

EQUATIONS

ASSERT V.RD-				% Enable frame buffer read data to P2
ENABLE ALWAYS
OR	V.BSEL & P2.RD & / P2.A17

ASSERT V.RDC-				% Enable control reg read data to P2
ENABLE ALWAYS
OR	V.BSEL & P2.RD & P2.A17

ASSERT V.WUC				% Write upper byte control reg
ENABLE ALWAYS  				% De-morganize: V.BSEL & AS & A17 & WEU
OR	/ V.BSEL
OR	/ Q.AS
OR	/ P2.A17
OR	/ P2.WEU

ASSERT V.WLC				% Write lower byte control reg
ENABLE ALWAYS  				% De-morganize: V.BSEL & AS & A17 & WEL
OR	/ V.BSEL
OR	/ Q.AS
OR	/ P2.A17
OR	/ P2.WEL

ASSERT V.REQ-				% Frame buffer request
ENABLE ALWAYS
OR	V.BSEL & Q.AS & / P2.A17 & P2.RD  & / V.ACK & / V.RDACK
OR	V.BSEL & Q.AS & / P2.A17 & P2.WEU & / V.ACK
OR	V.BSEL & Q.AS & / P2.A17 & P2.WEL & / V.ACK
OR	V.CSEL & Q.AS            & P2.WEU & / V.ACK
OR	V.CSEL & Q.AS            & P2.WEL & / V.ACK
OR	V.REQ  				  & / V.ACK		% Hold til ack

ASSERT V.RDACK-				% Used to hold deassertion of V.WAIT
ENABLE ALWAYS
OR	V.ACK & / V.WL & / V.WU		% Set at end of read req
OR	P2.RD & V.RDACK			% Hold till RD gone

ASSERT V.WAIT-				% Inhibit DTACK
ENABLE ALWAYS
OR	V.BSEL & P2.RD & / P2.A17 & / V.RDACK 	% Set on RD
OR	V.WAIT & P2.RD & / V.RDACK		% Hold until V.RDACK
OR	/ P2.WEL & V.REQ			% Set at end of write
OR	/ P2.WEU & V.REQ			% Set at end of write
OR	V.WAIT & V.REQ & / V.ACK		% Hold till V.ACK

ASSERT VREQ				% Inverter
ENABLE ALWAYS
OR	V.REQ-

PALEND
venus % ↑
```
