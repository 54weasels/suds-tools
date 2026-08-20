---


---


# Sun-2 CPU Board


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


This chapter describes the theory of operation of the Sun-2 CPU Board.
The discussion assumes that the reader is familiar with the architecture,
the installation, and the programming of the Sun-2 CPU Board.
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
For example, all P1 signals start with the prefix "P1.".

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

# Power, Initialization, Clocks


## Power


The Sun-2 video board uses a single 5 Volt power supply.
On-board charge pump/voltage converter `7660:U612,U614`
generate a -5V supply for the RS423 interface drivers `26LS29:U609,611`.


## Initialization


Upon application of power, capacitor `K:C100` begins to charge through
resistor `R:R100`.
When the voltage accross the capacitor reaches the threshold voltage of the
voltage comparator `8211:U120`, output POR\ is deasserted.
Feedback resistor `R:R101` and summing resistor `R:R102` introduce
a schmitt-trigger threshold into the operation of the voltage comparator.


## Clock Generation


All system clocks are derived from 19.6608 MHZ crystal oscillator
`K1114A:U200`. The oscillators output frequency, `C(50.0-25)`,
is divided into clock `C(100.0-50)` by flipflop `74F74:U201-0`.
This clock (and its inverse) drives the 68010 CPU, the timing flipflops,
as well as synchronizers and state machines on the board.

Clocks `C.S3, C.S4, C.S5, C.S6,` and `C.S7` are activated during
the corresponding 68010 states S3 through S7.
However, clocks `C.S4` and `C.S6` are only enabled for standard cycles.
They are not asserted for cycles that do not have the `VALID` bit asserted
or for non-standard or disabled cycles. Disabled cycles are either
`BOOTEN` or Boot Enable cycles (supervisor program access in boot state)
or `FC0 AND FC1` active cycles (MMU accesses and interrupt acknowledge cycles).
These conditions are decoded by PAL `P16R4:U316` and are indicated
by signal `DIS` asserted.


```


--------------------------------------------------------------------------------
Signal	Function	Comments
--------------------------------------------------------------------------------
P.AS	RAM-RAS		Asserted for all 68010 and all DVMA cycles.
			This means that memory is cycled in sync with P.AS.
--------------------------------------------------------------------------------
C.S3	RA/CA MUX	Row Address to Column Address multiplexor
			Asserted on every cycle.
--------------------------------------------------------------------------------
C.S4	CAS Enable	Asserted only on standard cycles with VALID bit set.
--------------------------------------------------------------------------------
C.S5	Strobe Enable	Asserted on every cycle, but decoder 74F138:U400 is only
			enabled when ERR indicates there are no errors pending.
--------------------------------------------------------------------------------
C.S6	Statistic Bit	Enables writing of accessed/modified bits
	Enable		Only asserted on standard cycles with VALID bit set.
--------------------------------------------------------------------------------
C.S7	XACK Enable	Enables XACK generation in PAL Q-U212.
--------------------------------------------------------------------------------


```


The timing of clock `C.S3` is special in that it is
not asserted on the `C(100.50-0)` clock edge
but rather on the `C(50.30-5)` clock edge which is
derived from clock `C(50.0-25)` via inverter `74F00:U102-1`.
The timing diagram below illustrates when `C.S3` and the other clocks
become active.


```


C(50.0-25)	----____----____----____----____----____----____----____

C(50.30-5)	-____----____----____----____----____----____----____---

C(100.0-50)	-________--------________--------________--------_______

C(100.50-0)	_--------________--------________--------________-------

AS		_________////////---------------------------------\\----

C.S3		_____________________-----------------------------\\____

C.S4		_________________________-------------------------\\____

C.S5		_________________________________-----------------\\____

C.S6		_________________________________________---------\\____

C.S7		_________________________________________________-\\____


```


## DTACK Generation


68010 DTACK, or data transfer acknowledge, is generated by
multiplexor `74F251:U111` as follows.

On non-standard cycles (see above), `C.S4`
is not asserted selecting `C.S5` as `P.DTACK`, thereby causing
one wait state.

On standard cycles, `TYPE0` and `TYPE1` select `DTACK` as follows:


```

TYPE	MEANING		DTACK SOURCE
----------------------------------------
   0	P2-BUS MEMORY	P2.WAIT\
   1	LOCAL I/O	IOACK
   2	P1-BUS MEMORY	XACK
   3	P1-BUS I/O	XACK
----------------------------------------

```


`P2.WAIT\` indicates that an asychronous P2-Bus device has not yet
completed the transfer.
Signal `IOACK` is generated by `PAL16R4:U602` and is normally
asserted at time `C.S7`, causing 2 wait states for On-Board I/O accesses.
`XACK` comes from the P1-Bus `P1.XACK` qualified with `AEN` via gate
`74F32:U101-0`. Thus `XACK` is only asserted when the CPU board is bus master.

In addition, during RasterOp cycles signal `EN.DTACK` is only
asserted when the RasterOp processor completes its operation.
This happens when signal `OE.ROP` is asserted, which is in state 15.
RasterOp cycles thus incur a total of 6 wait states.


## BERR Generation


68010 BERR, or Bus Error, can occur under four conditions:
1) Protection Error (`PROTERR`),
2) Timeout Error (`TIMEOUT`),
3) Parity Error Low Byte (`PARERRL`),
4) Parity Error Upper Byte (`PARERRU`).
These four conditions are combined with gate `74LS20:U114-0`.

Bus Errors are only recognized during standard cycles,
and they are suppressed during non-CPU cycles.
The former is achieved via gate `74F00:U102-2` and the
latter via signal `P.BACK\` setting synchronization flipflop `74F74:U206`.

In addition, `P.BERR` is asserted during rerun cycles via signal `XBERR`.
See description of rerun cycles for further information.


## VPA Generation


68010 VPA, or Valid Peripheral Address, is asserted on two conditions.
One, on interrupt acknowledge cycles as decoded by `74LS138:U321`
the assertion of `P.VPA` causes the 68010 to execute autovectored
interrupts as defined by the architecture of the CPU Board.
Second, read and write access to the real-time-clock `58167:U420`
causes `P.VPA` to be asserted via gates `74LS08:U422-0,U422-1`
thereby generating the appropriate low-speed access to the real-time-clock.

---

# Memory Management Unit


The memory management unit comprises the following components:


```

------------------------------------------------------------
    Device			Type	Location
------------------------------------------------------------
    User Context Register	LS2518	U300
    System Context Register	LS2518	U301
    User/System CX Multiplexor	74F257	U302
    Segment Map			2168	U303, U304
    Segment Map R/W Buffer	AM2949	U314
    Page Map			2168	U305, U306, U307, U308, U309, U310
    Page Map R/W Buffers	AM2949	U317, U318, U319, U320
    Protection Decoder		74F151	U315
    Statistic Bit Logic		P16R4	U316
    ID PROM			74S288	U411
    Bus Error Register		74LS534	U412
    System Enable Register	74LS273	U413
    System Enable Readback	74LS244	U414
    Diagnostic Register		74LS273	U802
------------------------------------------------------------

```


Accesses to these devices are decoded via MMU strobe decoder
`74LS138:U322, U323, U324` in MMU Function Code, as decoded by
Function Code Decoder `74LS138:U321`.


---

# On-board I/O Devices


The on-board I/O devices comprise the following components:


```

------------------------------------------------------------
    Device			Type	Location
------------------------------------------------------------
    PROMs			27256	U406, U407
    Floating Point Processor	80287	U600
    Data Ciphering Processor	9518	U601
    Timer Controllr		9513	U604
    Input Port			74LS244	U800, U801
    Serial Communication Contr.	Z8530	U605
    RasterOp Processor		85000	U511
    Real-Time Clock		58167	U420
------------------------------------------------------------

```


Accesses to these I/O devices are decoded via type decoder `74F138:U400`,
read decoder `74LS138:U401`, and write decoder `74LS138:U402`.
The only exception to this is the decoding of the PROMs for supervisor
program accesses in boot state. These cycles enable the PROM
via gates `74F32:U101` and `74LS08:U422`.

---

# P2-Bus Interface


## P2-Bus Decoding


Note that `P2.RAS` and `P2.CAS` are asserted before the
page map type field is decoded and before the protection field is
evaluated. Thus `P2.CAS` indicates a valid address, but not
necessarily a valid reference.


## RasterOp Processor


The Sun-2 CPU Board is equipped with a RasterOp processor `85000:U511`
that performs high-speed bitmap manipulation on P2-Bus memory when utilized.

For setup and state saving, the CPU addresses the RasterOp processor
as an I/O device using signals `RD.ROP\, WR.ROP\` and address lines
`P.A1..P.A4`.
In actual raster operation, the RasterOp chip is controlled by the
three control signals `LD.DST\, LD.SRC\, and OE.ROP\`.

These control signals are generated by the RasterOp state machine
comprising PROM `74S288:U518`, register `74F374:U519`
and pullup resistor `R9.SIP:S500`. This state machine executes
a rasterop cycle when signal `ROPCYC\` is asserted and it executes
a regular memory write cycle when signal `ROPCYC\` is not asserted.

`ROPCYC` is asserted when four conditions are met:
1) The CPU executes a Write Cycle (`R\/W` true),
2) RasterOp state is set (`ROP` is true),
3) The CPU is in user state (`P.FC2` false), and
4) the current cycle is not a disabled cycle (`DIS` false).
Thus RasterOp cycles occur only in user state on writes to memory
when RasterOp state has previously been set.

On a RasterOp cycle, a normal write operation to memory is changed
into three steps. In the first step, the write data normally destined
for memory is loaded into the source register of the rasterOp processor
by means of signal `LD.SRC`.
In the second step, the data buffers from the processor to the rasterOp chip
`74F244:U512,U515` are disabled by signal `DIS.D`.
At the same time, the data read from the memory location accessed
is loaded into the destination register by means of signal `LD.DST`.
In the third step, the modified data is read out of the rasterOp processor
with signal `OE.ROP` and written into memory by asserting `WR.M`.
The 68010 CPU cycle is holdup by not asserting P.DTACK until the third step begins.


## Parity Error Logic


The P2-Bus and the memory boards on the P2-Bus are equipped with Byte Parity.
Parity errors abort the 68010 via the bus error mechanism.

All bus errors except parity errors are recognized by the 68010
in the same 68010 cycle as they occur.
Parity errors cannot be recognized in the same cycle because
they are only detected at the very end of the cycle,
when it is too late to abort the current cycle.
Since they are not recognized in the current cycle, parity errors
need to be latched until they are recognized by the CPU.
This is done in the parity error flipflop `74F74:U512`, providing
a separate flipflop for upper and lower parity errors, at the end
of a memory read cycle.

In order to recognize bus error, the 68010 must execute
a "non-disabled" cycle or a cycle in which C.S4 is asserted.
The parity error flipflop will be cleared if BERR is true and
DS is deasserted, which indicates a CPU cycle terminated by BERR.
Note that the BERR will not be set on non-CPU cycles because P.BACK
will keep the bus error flipflop `74F74:U206` in its idle state.

Parity generation and checking can be disabled without affecting
system operation. To initialize parity in main memory, all of
memory needs to be written with parity generation enabled.
Separate enable bits are provided for parity generation and parity checking
to allow software testing of the parity function.

---

# P1-Bus Interface


## P1-Bus Address and Data Drivers


Inverting flow-through latches `74LS533:U700,U701,U702`
latch 68010 address bits P.A1..P.A10 and translated address bits
MA11..MA19 during clock C.S3-6.
In addition, (LDS AND UDS) is latched to form P1.BHEN, and
P.LDS\ is latched to form P1.A0. See below.

Inverting bidirectional drivers `8303B:U712,U713,U714` exchange
data bits D0..D15 between on-board data bus und P1-Bus.
Buffer `8303B:U714` is the byte swap buffer that is enabled whenever the 68010
or DVMA performs a byte-swap transfer.
Both address and data buffers are enabled with AEN\ from
bus arbiter `8289:U718` indicating bus mastership.


## Byte order and A0 Address Generation


The Sun-2 CPU Board uses 68010 Byte order on the P1-Bus
to offer a consistent memory model for the 68010.
Notice that the 68010 byte order is incompatible with the P1-Bus byte order
in that the 68010 numbers the upper byte (Data bits 8 through 15) the even byte
whereas the P1-Bus calles the lower byte (Data bits 0 thru 7) the even byte.


```

			 D15 ........D8	 D7 ..........D0
			---------------------------------
68010 Byte Order	|  Byte 0	| Byte 1	|
			---------------------------------
P1-Bus Byte Order	|  Byte 1	| Byte 0	|
			---------------------------------

```


In addition, the 68010 differs from the P1-Bus in that it transfers
even bytes on data lines D8 through D15 and odd bytes on D0 through D7,
whereas the P1-Bus transfer both odd and even bytes via D0 through D7.
Finally, the 68010 does not output address bit A0. This address bit needs
to be reconstructed from the 68010 data strobes. To achieve 68010 byte-order
on the P1-Bus, the A0 on the P1-Bus must be the inverse of 68010 A0
for byte transfers.

The following table summarizes the state of different signal lines
for word and byte transfers between 68010 and P1-Bus.


```

--------------------------------------------------------------------------
68010		68010	68010	68010	P1-Bus	WORD\	BYTE\	P1-Bus
Transfer	P.UDS\	P.LDS\	P.A0	P1.A0	Buffer	Buffer	Transfer
--------------------------------------------------------------------------
16-bit D0..15	0	0	0	0	0	1	D0..15
8-bit D0..7	1	0	1	0	0	1	D0..7
8-bit D8..15	0	1	0	1	1	0	D0..7
--------------------------------------------------------------------------


```


From the table it can be seen that Word Buffer\ = 68010 LDS\
and that P1.A0 = P.LDS\.


## P1-Bus Multimaster Logic


The P1-Bus provides multiple master on the bus, exchanging bus mastership
via a standard protocol (see IEEE-796 Bus standard).
The Sun 68010 Board uses the Intel 8289 arbiter chip  `U718` to
implement this protocol.

The 8289 was adapted to the 68010 CPU as follows:
8289 is configured in "RESB" mode (IOB high and RESB high).
This means the P1-Bus is requested whenever the processor status
lines go active and SYSB is asserted low (B/L\ low); and
allows the P1-Bus to be surrendered if SYSB low (B/L\ low),
during idle (S0\, S1\, S2\ high), for common bus requests,
and if there is a higher priority bus request.
8289 S0\, S1\, and S2\ are tied to AS\, generating an I/O command
for AS asserted and an idle cycle for AS deasserted.
8289 LOCK\ and 8289 CBRQL are not used, ANYREQ is enabled,
allowing the bus to be given up on common bus requests.

When the 8289 obtains mastership it asserts `AEN\`.
This enables the address drivers immediately and the
data drivers via `P20L10:U212`.
The driver fro the bus control signals, `74F244:U717`
is enabled after a minimum 100 nsec delay created by synchronizer
`74F74:U709`, but no earlier than processor state (C.S7) since
`C.S4` must be active before the synchronizer can recognize `AEN\`.
This is necessary because on write cycles 68010 signals `P.LDS, P.UDS`
are only valid at the beginning of state S5.


## P1-Bus Clocks


The Sun 68010 Board normally generates P1-Bus BCLK and CCLK
via driver `74F244:U717`.
In a multimaster system, only one master may drive these clocks.
To configure the Sun 68010 board for such a system,
BCLK can be disconnected by removing jumper `J702` and
CCLK can be disconnected by removing jumper `J703`.

---

# Refresh and DVMA Operation


The Sun-2 CPU Board offers hardware refresh and DVMA operation from
the P1-Bus. These features are implemented primarily by
Timer Controller `P20X10:U211`, Refresh Counter `74LS491:U210`,
DVMA Decoder `P20L10:U212`, DVMA Controller `P16R4:U213`, and
DVMA Address Drivers `74LS244:U705,U707,U708`.

The following table illustrates the primary signals generated by these components
and their enable conditions. `CPU`, `REN`, and `XEN` indicate
a CPU, a Refresh, and a DVMA cycle, respectively.


```


--------------------------------------------------------------------------------
	COMPONENT		ENABLE	SIGNALS
--------------------------------------------------------------------------------

	68010 CPU		CPU	P.AS, P.LDS, P.UDS, P.R/W\
				CPU	P.FC0, P.FC1, P.FC2
				CPU	P.A1..P.A23


	DVMA Controller		---	REN, XEN, BR, BGACK
	U213			XEN,REN	P.AS
				XEN	P.FC1


	DVMA Decoder		XEN	P.LSD, P.UDS, P.R/W\
	U212


	DVMA Address		XEN	P.A1..P.A23
	U705,U707,U708		XEN	P.FC2


	Refresh Counter		REN	P.A1..P.A11
	U210
--------------------------------------------------------------------------------

```


## Driving and Termination of 68010 Bus Signals


All tri-statable 68010 signals are terminated via pullups `R9.SIP:S103,S104,S105`.
This causes these signals to assume a defined state when they are not driven,
e.g. when the 68010 is being reset or when bus mastership is exchanged between
the 68010 and the DVMA Controller.

During a *Refresh* cycle, the 68010 bus signals are driven as follows:


```

	P.AS			PAL	U213
	P.UDS, P.LDS, P.R/W	PULLUP	S103
	P.FC0, P.FC1, P.FC2	PULLUP	S103
	P.A1 THROUGH P.A10	COUNTER	U210
	P.A11 THROUGH P.A23	PULLUP	S104, S105

```


During a *DVMA* cycle, the 68010 bus signals are driven as follows:


```

	P.AS			PAL	U213
	P.UDS, P.LDS, P.R/W	PAL	U212
	P.FC0			PULLUP	S103
	P.FC1			PAL	U213
	P.FC2			DRIVER	U705
	P.A1 THROUGH P.A23	DRIVERS	U705, U707, U708

```


## P1-Bus DVMA Decoder


The DVMA Decoder `P16L8:U212` recognizes P1-Bus DVMA requests
and generates the signals `P.LDS\, P.UDS\, and P.R/W\` during DVMA cycles.
In addition, the DVMA Decoder controls the enable and the direction of the
P1-Bus data buffers `8303B:U712, U713, U714` for both DVMA cycles and
CPU cycles via signals `P1TOP\` and `CE.BYTE\ and CE.WORD\`.


```


    SIGNAL	DVMA READ CYCLE			DVMA WRITE CYCLE
----------------------------------------------------------------------------

    P1.MRDC\	----____________________------------------------------------
    P1.MRWC\	-----____________________-------_____________________-------
    XREQ\	--------__________________-------_____________________------
    XEN\	_______-----__________________----_______________________---
    P1TOP\	-----------------------------------_______________________--
    P.L|UDS\	-------------______________--------____________________-----
    CE.WORD\	--------------______________--------____________________----
    P.WR\	------------------------------------____________________----


```


### DVMA Decoder Signals


`AEN`, or address enable, is generated by bus arbiter `8289:U718`
and signals bus mastership for the CPU Board.

`XEN`, or external enable, is driven from DVMA controller `P16R4:U213`
and signals that an external cycle is enabled. `XEN` enables the
external address buffers `74LS533:U705,U707,U708` and four control
signal generated by the DVMA Decoder PAL: `P.R/W\, P.LDS\, P.UDS\ and P1.XACK\`.

`CE.WORD` enables the 16-bit data buffer between the P and P1 bus.
It is asserted on AEN Word and Low-Byte transfers,
on AEN Writes, and on XEN Word transfers.
The AEN Write case guarantees data hold on the P1-Bus if the write
operation was directed to the P1-Bus.

`CE.BYTE` enables the 8-bit swap buffer between the P and P1 bus
for upper byte AEN read cycles from P1 to P and for upper byte XEN transfers.

`P1TOP` means enable the direction of the data bus buffers from P1 to P.
It is asserted on non-XEN P1 memory read `MRDC` and input/output read
`IORC` cycles, as well as on XEN write cycles.

`XREQ` is asserted when an external request is recognized and stays
asserted while the external strobe `P1.MRWC` is active.
To recognize an external request the following conditions must be met:
`EN.DVMA` asserted, `P1.A19` and `P1.A18` deasserted,
`P1.MRWC` active, and `AEN` and `XEN` deasserted.
The `XEN` condition guarantees that no new `XREQ` can become active
while the `XEN` associated with a previous request is still asserted.

The following signals are tri-stated and only enabled to be driven
by the DVMA decoder when `XEN` is asserted.

`P.R/W` is asserted on DVMA write cycles. The signal is latched
before state `C.S7` and held until `P1.MRDC` comes true or
until `XEN` goes away.

`P.LDS` is asserted for even byte and word transfers.

`P.UDS` is similar to `P.LDS` except that it is asserted
for odd byte and word transfers.

`P1.XACK` signals to the external DMA device that the onboard
cycle successfully completed. This is the case when `C.S7`
is asserted, protection error `PROTERR` is false, and, in the
case of read cycles, parity error `PARERR` is false.

---

## DVMA Controller


The DVMA Controller `P16R4:U213` is at any time in one of three states:
IDLE, REN or XEN.
REN state is active while executing refresh cycles,
XEN state while executing P1-Bus DVMA cycles.
The state machine is in IDLE state if it is not in REN or XEN state.


```


	CPU CYCLE	REFRESH CYCLE		DVMA CYCLE
----------------------------------------------------------------------------

CLK	--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__--__
RREQ\	----____________________--------------------------------------------
XREQ\	------------------------------------\\\\_____________________///----
SDS\	----------------------------------------________________________----
BR\	----________________--------------------________--------------------
BG\	--------________________--------------------________----------------
AS\	----__________----------________--------------------_________///----
SAS\	--------________------------________--------------------________----
REN\	--------------------____________------------------------------------
XEN\	------------------------------------------------________________----
BGACK\	--------------------____________----------------________________----
SACK\	------------------------____________----------------________________


```


`CLK` is the 100 nanosecond clock to the DVMA Controller.
All input to the DVMA Controller state machine are synchronous to this clock
except input `XREQ` which is used asynchronously only.

`RREQ` indicates a refresh request from the timer controller `P20X10:U211`.

`XREQ` indicates an asynchronous external request from the DVMA decoder
`P20L10:U212`.

`SDS` is the synchronized version of `XREQ` via flipflop `74F74:U207-0`.

`BR`, or bus request, is asserted from the DVMA controller to the 68010
when XREQ or RREQ is pending but BGACK is inactive.

`BGACK and SACK`.
When the machine enters state XEN or REN it asserts BGACK
one PAL delay after entering the state.
In the next state after BGACK is asserted, the synchronous version of BGACK,
SACK, is asserted.
BGACK stays asserted during the entire refresh or DMA
cycle, and causes the AS and FC1 to be tri-state enabled.
When XEN or REN is deasserted, BGACK is
deasserted one PAL delay later and then SACK is deasserted one clock
later.

`AS` is asserted one PAL delay after SACK.
AS remains asserted while in the REN state and SACK is asserted,
or while in XEN state and SACK and XREQ is asserted.

`XEN` state is entered
when the state machine is in IDLE state, a GRANT is issued,
no refresh request is pending, and synchronous data strobe or SDS is pending.
The state machine will stay in XEN state until SDS goes away.

`REN` state is entered
REN state is entered when the state machine is in IDLE state, a GRANT is issued,
and a refresh request is pending.  Note that if a refresh request and a
synchronous data strobe are pending at the same time, refresh request will
take priority over the synchronous data strobe.  The state machine will stay
in REN state for two additional states; the first while SACK is
not asserted, the second while SAS is not asserted.

`FC1` FC1 is driven low in XEN state.
Since FC0 and FC2 are pulled up by external
pull up resistors, the effective function code in XEN state is 5 or supervisor data.
FC1 is drive high in REN state thus the effective function code for REN state is 7
or supervisor reserved.

`XBERR`,
or external bus error, is asserted if SDS, XHALT, and SYSB is active.
This condition indicates that the CPU is attempting  access to the P1 bus
while a DMA device is attempting access
to the CPU bus.  XBERR will stay asserted until SYSB becomes inactive.

`XHALT`,
or external halt, is asserted if SDS is active and SYSB is active,
indicating CPU access to the P1 bus.  It will stay asserted while XBERR is
asserted.


## Rerun Conditions


CPU cycle are rerun under two conditions: bus deadlock and refresh deadlock.
Bus deadlock occurs when the CPU attempts to access the P1-Bus while
a master on the P1-Bus attempts to access the CPU board via DVMA.
Refresh deadlock occurs if a refresh request is pending while the CPU
is waiting for P1-Bus access.

In both cases, the current CPU cycle is aborted via the 68010 bus cycle
rerun mechanism. This is done by asserting HALT and BERR and keeping
them asserted until the current 68010 bus cycle is terminated.
The 68010 then performs normal bus arbitration, letting the pending
DVMA or refresh cycle proceed, and after regaining the bus,
will retry the previously aborted cycle.

Refresh deadlock cycles will only be rerun if signal `BEN` has not
been asserted yet. `BEN` enables the P1-Bus strobes.
If `BEN` is already active, rerun is no longer possible because
P1-Bus cycles, once begun, cannot be restarted.
However, if `BEN` is not yet asserted and the rerun condition is true
then `BEN` will not be asserted subsequently.
This is guaranteed because the rerun condition, caused by signal `RREQ`,
is simultaneously recognized by DVMA controller `Q-U213` and
inhibits assertion of enable flipflop `74F74:U709-1` via gate `74F00:U102-2`.
Also, `RREQ` will stay asserted until after `C.S4` is deasserted,
clearing enable flipflop `74F74:U709` via gate `74F08:U703-2`.
The timing diagram below illustrates this exchange.


```


		NO RERUN CASE			RERUN CASE
--------------------------------------------------------------------------------

C(100.0-50)	----____----____----____	----____----____----____
RREQ		________________--------	________----------------
AEN		////--------------------	////--------------------
U709(6)		____--------------------	____--------------------
BEN		____________------------	________________________
XHALT		________________________	________________--------

```


---

# P2-Bus Description


## Functional Description


The P2-Bus connects the Sun Processor Board to Sun Memory Boards.
It is a single master bus; only one processor board can be connected to it.
It is a synchronous bus; all timing is generated by the Processor Board.
The protocol does not provide for a handshaking capability in the
traditonal sense, rather it provides a negative acknowledge or "WAIT"
capability that can hold the current cycle until it is deasserted.
In its signals and timings, the P2-Bus follows very closely the
characteristics of 64k dynamic RAMs.


## P2-Bus Signal Definition


The Sun P2-Bus consists of the following signals:


```


Type O means Output (signal direction from Processor to Memory)
Type I means Input  (signal direction from Memory to Processor)

-----------------------------------------------------------------------
NAME	TYPE	DESCRIPTION
-----------------------------------------------------------------------

P2.A0..7    O	Multiplexed address lines that transmit the
		row-address during the leading edge of RAS and
		the column address during the leading edge of CAS

P2.A17..22  O	High order address bits, valid at leading edge of CAS

P2.DI0..15  O	Data lines from processor to memory
P2.DIL	    O	Lower Byte Parity from processor to memory
P2.DIU	    O	Uppoer Byte Parity from processor to memory

P2.DO0..15  I	Data lines from memory to processor
P2.DOL	    I	Lower Byte Parity from memory to processor
P2.DOU	    I	Uppoer Byte Parity from memory to processor

P2.R/W\	    O	Read/Write\ Signal
P2.REN\	    O	Refresh Enable, current cycle is a refresh cycle

P2.RAS\	    O	Row Address Strobe
P2.CAS\	    O	Column Address Strobe
P2.WEL\	    O	Lower Byte Write Strobe
P2.WEU\	    O	Upper Byte Write Strobe
P2.WAIT\    I	Wait line, holds current cycle until deasserted


```


---

## P2-Bus Timing Diagram


```


Semantics:
		x := Signal Unstable
		= := Signal Stable
		- := High Level Signal
		_ := Low Level Signal


P2.A0..7	xxxxx====xxxxx================xxxxxxx

P2.A17..22	xxxxxxxxxxxxxx================xxxxxxx

P2.R/W\		xxxxx=========================xxxxxxx

P2.REF\		xxxxx=========================xxxxxxx

P2.DO0..15	xxxxxxxxxxxxxxxxxxxxxxxxxx====xxxxxxx

P2.DI0..15	xxxxxxxxxxxxxxxxxxxx==========xxxxxxx


P2.RAS\		-------_______________________-------

P2.CAS\		-------------_________________-------

P2.WEL\		--------------------------____-------

P2.WEU\		--------------------------____-------


```


---

# Signal Summary


The signal summary describes the meaning of the named signal in the design.
Signal names are shown active high, and signal vectors are combined into
a single name.


--------------------------------------------------------------------------------
Mnemonic	Description
--------------------------------------------------------------------------------
AEN
AS
BEN
BERR
BOOTEN
BOOT
C()
C.S3
C.S4
C.S5
C.S6
C.S7
CE.BYTE
CE.WORD
CTSA
CTSB
CXS0..CXS3
CXU0..CXU3
D0..D15
DAA
DAB
DBA
DBB
DCDA
DCDB
DDA
DDB
DIL
DIS.D
DIS
DIU
DSRA
DSRB
DS
DTRA
DTRB
EN.DTACK
EN.DVMA
EN.INT
EN.INT1
EN.INT2
EN.INT3
EN.PARERR
EN.PARGEN
EN.S4
ERR
FOUT
FPPERR
L
H
IA16..IA23
IN0..IN15
INIT
INT.SCC
INT1..INT7
IOACK
IORC
IOWC
IPL0..IPL2
LD.SRC
LDS
LED0..LED7
MA11..MA22
MAS
MDS
MOD
MRDC
MWTC
NPRD
NPWR
OE.ROP
P.A1..P.A23
P.AS
P.BACK
P.BERR
P.BG
P.BR
P.D0..P.D15
P.DTACK
P.FC0..P.FC2
P.HALT
P.INTA
P.LDS
P.MMU
P.R/W
P.RESET
P.SPROG
P.UDS
P.VPA
P1.A0..P1.A19
P1.BCLK
P1.BHEN
P1.BPRN
P1.BPRO
P1.BREQ
P1.BUSY
P1.CBRQ
P1.CCLK
P1.D0..P1.D15
P1.INIT
P1.IORC
P1.IOWC
P1.MRDC
P1.MRWC
P1.MWTC
P1.XACK
P1TOP
P2.A01..P2.A22
P2.CAS
P2.DI0..P2.DI15
P2.DO0..P2.DO15
P2.R/W
P2.RAS
P2.WAIT
P2.WEL
P2.WEU
PARERR
PARERRL
PARERRU
PEACK
PEREQ
POR
PROT0
PROT5
PROTERR
Q0..Q5
RD.CXL
RD.CXU
RD.DCP
RD.ENABLE
RD.ERROR
RD.FPP
RD.IDPROM
RD.IO
RD.PMAP0L
RD.PMAP0U
RD.PMAP1L
RD.PMAP1U
RD.PORT
RD.PROM
RD.RAM
RD.ROP
RD.RTC
RD.SCC
RD.SMAP
RD.TIMER
REN
RESET
ROP
ROPCYC
ROPST0..ROPST2
RREQ
RTSA
RTSB
RXCA
RXCB
RXDA
RXDB
R/W
SACK
SAS
SDS
SFC2
SPAREA
SPAREB
SYSB
T1..T5
TIMEOUT
TXCA
TXCB
TXDA
TXDB
TYPE0..TYPE2
T
UDS
VALID
VCC
VCCX
VEEA
VEEB
WR.CXL
WR.CXU
WR.DCP
WR.DIAG
WR.ENABLE
WR.FPP
WR.IO
WR.M
WR.PMAP0L
WR.PMAP0U
WR.PMAP0X
WR.PMAP1L
WR.PMAP1U
WR.RAM
WR.ROP
WR.RTC
WR.SCC
WR.SMAP
WR.TIMER
X200
X400
XACK
XBERR
XEN
XHALT
XREQ
Z0..Z7


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

## PROM Q-U518, Sourcecode


```

begin "q1b"
require "prom.sai" source!file;
$32;

Comment	Idle State = 7


	ROPCYC\=0			    ROPCYC\=1

STATE	0   1   2   3   4   5   6   7       0   1   2   3   4   5   6   7

LD.SRC\	____----------------------------    ---------------------------------

DIS.D\	--------________________________    ---------------------------------

LD.DST\	------------____----------------    ---------------------------------

OE.ROP\	--------------------____________    ---------------------------------

WE.RAM\	------------------------________    _________________________________

;

define
state0	=[(a0)],
state1	=[(a1)],
state2	=[(a2)],

ropcyc_	=[(a4)],	ropcyc	=[((¬ropcyc_) LAND 1)],

state	=[(state0*d0 + state1*d1 + state2*d2)],
nstate	=[(if (state=6) then 6 else (state + 1) MOD 8)],
ldsrc	=[(ropcyc ∧ (nstate=0))],
disd	=[(ropcyc ∧ (2≤nstate≤7))],
lddst	=[(ropcyc ∧ (nstate=3))],
oerop	=[(ropcyc ∧ (5≤nstate≤7))],
weram	=[(ropcyc ∧ (6≤nstate≤7) ∨ ¬ropcyc ∧ (0≤nstate≤7))];

prombegin

prom(0,d0,	(nstate LAND d0));
prom(0,d1,	(nstate LAND d1));
prom(0,d2,	(nstate LAND d2));
prom(0,d3,	¬ (weram));
prom(0,d4,	¬ (ldsrc));
prom(0,d5,	¬ (lddst));
prom(0,d6,	¬ (oerop));
prom(0,d7,	¬ (disd));

promend;

writeprom("q1b",0);
end;

```


---

## PROM Q-U518, Objectcode


```

:10000000F97A5B7C3D3636E8F97A5B7C3D3636E83A
:10001000F1F2F3F4F5F6F6F0F1F2F3F4F5F6F6F0AA
:0000000000
PROM 	q1b	Checksum 	16EC


```


---

# PALs


## Introduction


This chapter contains the source files and object files for the
PAL circuits on the board.
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

All the PALs are included as a file with the extension ".PAL".

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

DIPTYPE	BODY NAME	# SECTION	TOTAL DIPS	#SPARE SECTIONS	  MA		  V

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
