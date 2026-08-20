---


---


# Sun 1/4" Tape Board


# Engineering Manual


SUN MICROSYSTEMS INC.

November 1982


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


This chapter provides a description of the Sun 1/4" Tape Controller Board circuit operation.
The discussion assumes that the reader is familiar with the architecture,
the installation, and the programming of the Sun 1/4" Tape Controller Board.
In addition, the discussion assumes that the reader has a working knowledge
of digital electronics and has access to descriptions of the components
used on the board.

A set of schematic diagrams for the Sun 1/4" Tape Controller Board are included
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
For example, all Multibus signals start with the prefix "BUS.", and
all signals on the 50-pin flat cable are prefixed with "C.".


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
location labels consist of one letter followed by two digits.
The letter indicates the type of component and is one of:


	Letter	Component Type
	--------------------------------
	C,K,X   Capacitor
	J       Jumper of Connector
	R       Resistors. Discrete or SIPS.
	U       Dual-in-line component
        M       64K rams.


If the tens digit is a 0 through 4,
the two digits give the approximate component position on the board,
with the first digit indicating the row position and the last digit
indicating the column position.
If the tens digit is a five or six, the U-number is derived by counting from
50 and following a path that begins with the dipswitch below U40 and moves up
and down and works its way to the right-hand side of the board.
If the tens digit is a seven,
Chips U70 through U74 can be found lying horizontally between the Intel 8203
memory controller and the column of chips U14 through U44; U70 is towards the
top of the card (away from the 796-Bus).
The memory array
is numbered with M100 being the upper-left hand corner, and M408 being the
lower-right hand corner.

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


---

## Power


The Sun 1/4" tape controller board is designed for 5V-only operation.


## Initialization


When the signal "BUS.INIT\" is received from the Multibus, 'D' flip-flops at
U31 section #0 and U22 section #1 are cleared. The first flip-flop disables
interrupts, and the second performs a fake acknowledge on the "Data Request"
flip-flop for the tape. The first access to the tape sub-section should clear
the write control register. This will take the board out of "Burst" mode whereby
the board performs the proper data transfer handshaking with the 1/4" streaming
tape. The interrupt flip-flop is permanently re-enabled as soon as bit 5 in the
write control register ("Catch_Edge_Of_Ready") is enabled; from now on,
interrupts are generated depending on the state of the interrupt enable bits
in the write control register (U73).

Parity is always enabled on power-up.


## Memory Controller


The 256K-bytes of multibus memory on the card are controlled directly by the
Intel 8203 memory controller chip. This chip introduces an average of four
wait states in accessing the 64K rams, but it performs refresh on its own, and
is simple to use.

The memory on the board is largely independent of the tape circuitry. The two
sections share the multibus address and data bus buffers, and the read-back of
the parity-enable bit uses an extra bit position in the tape read-control
register.

Parity is always generated when writing to the ram array, and on a parity error,
no Multibus acknowledge is issued so that the data request will timeout.


---

## Tape Timing


Timing for the tape controller is asyncronous.
During normal operation, reads and writes can be performed to the data register
or any of the control registers at any time. A second mode of the board is
"Burst-Mode". During burst mode, reads and writes can still be performed on the
control registers at any time, but reading or writing to the data register will
cause the board to implicitly handle the XFER/ACKNOWLEDGE handshaking with the
tape unit. All command request handshaking must be performed explictly in
software, and for diagnostic purposes, data hand-shaking can be performed explicitly
by not setting the "Burst" bit in the write control register.

**Burst Mode Read Timing**


```

	BURST

	IOREAD

	REQ

	C.ACK\

	C.XFER\

	CLK_READ

	BUS.XACK\

```


**Burst Mode Write Timing**


```

	BURST

	IOWRITE

	REQ

	C.ACK\

	C.XFER\

	WR_DAT\

	BUS.XACK\

```


---

# Schematics


This chapter contains the signal summary, the parts list,
the parts location diagram, and the schematics of the Sun 1024 Video Board.


## Signal Summary


--------------------------------------------------------------------------------
Mnemonic	Description
--------------------------------------------------------------------------------

A0..A7		Address lines output from 8203 to 64K rams
ACK50		C.ACK delayed 50 nsec
ACK100		C.ACK delayed 100 nsec
B.A0..A19	Buffered address lines from multibus
B.D0..D15	Buffered data lines from multibus
B.INIT		Buffered multibus INIT signal
B.INT		Interrupt line before it is channelled to an interrupt level
B.POH		Latched parity output bit on high byte of memory
B.POL		Latched parity output bit on low byte of memory
BANK		Selects between first or second 128K of memory
BHEN		Buffered "byte-high-enable" line from multibus
BURST_REQ	Sets tape request flip-flop on data accesses in burst-mode
BUS.A0-19	Multibus address lines
BUS.BHEN	Multibus byte high enable
BUS.CCLK	Unused
BUS.D0-15	Multibus data lines
BUS.INIT	Multibus initialization signal
BUS.INT0-7	Multibus interrupt lines
BUS.INTA	Unused
BUS.IORC	Multibus I/O read strobe
BUS.IOWC	Multibus I/O write strobe
BUS.MRDC	Multibus memory read strobe
BUS.MWTC	Multibus memory write strobe
BUS.XACK	Multibus transfer acknowledge
C.ACK		Tape Drive acknowledge
C.D0-7		Tape Drive data bus
C.DIRC		Tape Drive direction; Low on writes to tape
C.INT		Tape Drive exception
C.ONLINE	Tape Drive online
C.READY		Tape Drive Ready
C.REQUEST	Tape Drive request
C.RESET		Tape Drive reset
C.XFER		Tape Drive transfer hand-shaking signal
C.XFER2		Used as C.XFER when not in burst-mode. From write control reg.
C.XFER50	XFER signal output during burst-mode reads.
CAS		64K ram column-address strobe
CLK		20 MHz signal used to clock Intel 8203
CLK_READ	Clock to capture tape data during burst-mode reads
CSH		Chip select high. On word or high-byte access to ram.
D.BURST		Write control reg output. Puts board into "Burst-Mode".
D.I_RDY		Write control reg output. Enable interrupts from edge of "C.Ready".
D.INTEN		Write control reg output. Enable interrupts from tape exception.
D.ITOG		Write control reg output. Catch edge of "C.Ready".
DAT		Access to data reg.
DATREQ		Access to data reg. Asserted as R/W strobe is deasserted.
DEVSEL		Tape or memory selected.
HBYTE		Memory access to high byte of memory word. Controls data XCVR.
INTS_EN		Cleared on multibus init. Disables all interrupts.
IOREAD		Buffered I/O read strobe
IOREQ		I/O Request.
IOSEL		I/O device (Tape) selected.
IOWRITE		Buffered I/O write strobe
MEM.ACK		Memory R/W acknowledge. Inhibited on parity errors.
MEMREQ		Memory Request
MEMSEL		Memory Selected
MREAD		Buffered memory read strobe
MWRITE		Buffered memory write strobe
NEWREQ		New request. True on IOREQ and after previous request serviced.
NEWREQ50	New request delayed 50 nsec.
PAR_EN		Parity Enable.
PAR_ERR		Parity Error.
PARERRH		Parity Error on high byte of memory.
PARERRL		Parity Error on low byte of memory.
PU		Pull-Up.
PU2		Pull-Up.
R.PIH		Parity bit input on high byte of memory.
R.PIL		Parity bit input on low byte of memory.
R.POH		Unlatched Parity bit output on high byte of memory.
R.POL		Unlatched Parity bit output on low byte of memory.
R0-15		64K ram outputs.
RAS.0		Memory row address strobe for first 128K of ram.
RD.CTL1		Output enable for read-back of "write control register"
RD.CTL2		Output enable for "read control register"
RD.DAT		Output enable for data register reads.
RDIR		Read direction. True if tape drive thinks we are reading from it.
RDY_INT		Ready Interrupt. True after leading edge of "C.Ready".
REQ		Burst-mode data request.
S1-28		Temporary signal name.
TP_RST		Tape reset. Performs a fake data acknowledge on burst-mode transfers
VCC		+5 Volts.
WDIR		Write Direction. Tape Drive thinks we are writting to it.
WEH		Write enable on high-byte of memory.
WEL		Write enable on low-byte of memory.
WE		Write enable.
WORD		Low-byte or word access to device, controls data bus transceivers.
WR_PAR		Clock for enabling/disabling parity..
WR.CTL1		Clock for writing to tape write control register.
WR.DAT		Clock for writing to tape data register.
X.INT		Interrupt unless multibus init just seen.
Z.IOREAD	I/O read and I/O select.
Z.MREAD		Memory read and memory select.
Z.READ		Device read signal stretched 50 nsec.


---

## Parts List - Rev C


As an aid in specifying and ordering components, this parts list
translates diptypes into manufacturer names and manufacturer codes.
Only one manufacturer code is given, alternative sources
may be substituted. A manufacturer code of "ANY" is used
for generic parts with a large number of second sources.


```

--------------------------------------------------------------------------------
GENERIC	PINS SMIPART	QTY	MFPART	DESCRIPTION
--------------------------------------------------------------------------------

R	2   120-____     2	ANY	RESISTOR 1/8W	RESISTOR. 33 OHM.
C	2   110-0040    86	ANY	CAPACITOR	CAPACITOR. 0.1 UFD.
C	2   110-____    13	ANY	CAPACITOR	CAPACITOR. 10 UFD.
J.50	50  180-____     1	AUGAT	110-50001-102	50-PIN PCB HEADER
J.4	4   130-0273     2	BERG	STICK, 4 PINS
4164	16  501-0105    36	ANY	4164		64K-BY-1 RAM 150 NSEC
R9.SIP	10  120-0078     3	BURNS	4310R-101-XXX	RESISTOR SIP 1K OHMS
74S240	20  100+0027     4	TI	SN74S240N	OCTAL INVERTING BUFFER
7406	14  100-0009     1	TI	SN7406N		OPEN COLLECTOR INVERTER
K1114A	4   150-1000     1	MOTOROL	K1114A		OSCILLATOR 23.48 MHZ
74S153	16  100+____     1	TI	SN74S153N	MULTIPLEXOR
74S74	14  100+0072     2	TI	SN74S74N	DUAL D-TYPE FLIPFLOP
74S00	14  100+0021     1	TI	SN74S00N	QUAD 2-INPUT NAND GATES
TTLDL50	14  150-0602     1	ECC	MTTLDL-50	DELAY LINE, 50 NSEC
74S08	14  100+0023     2	TI	SN74S08N	QUAD 2-INPUT AND GATES
74S139	16  100+0024     2	TI	SN74S139N	DUAL 2-TO-4 LINE DECODER
74S32	14  100+0144     3	TI	SN74S32N	QUAD 2-INPUT OR GATES
74S04	14  100+1039     1	TI	SN74S04N	HEX INVERTER
74S02	14  100+0022     3	TI	SN74S02N	QUAD 2-INPUT NOR GATES
DIPSW	16  100-0076     4	CUTLER	SM-2AV-951-8	DIPSWITCH; 8 POSITIONS
74LS251	16  100-0063     1	TI	SN74LS251N	1-OF-8 DATA SELECTOR
LS2521	20  100-0096     2	AMD	AM25LS2521	EIGHT-BIT COMPARATOR
74S244	20  100+0028     2	TI	SN74S244N	OCTAL LINE DRIVER
8304B	20  100-0037     3	AMD/NAT	DP8304BN	OCTAL TRANCEIVER
74LS373	20  100-0599     3	TI	SN74LS373N	OCTAL LATCH
82S62	14  100-0035     2	AMD	N82S62N		9-INPUT PARITY CHECKER
DIPTERM	16  120-____     1	BECKMAN	XXX		TERMINATOR 220/330 OHM
74S240	20  100+0027     2	TI	SN74S240N	OCTAL INVERTING BUFFER
2953	24  100-____     2	AMD	AM2953DC	OCTAL REG WITH READ-BACK
74LS534	20  100-0597     1	AMD	SN74LS534N	OCTAL REGISTER INVERTING
8203	40  100-0603     1	INTEL	P8203		MEMORY CONTROLLER


```


---

## Parts Location Diagram - Rev C


---

## Schematic TI1 (page 1 of 4) - Rev C


---

## Schematic TI2 (page 2 of 4) - Rev C


---

## Schematic TI3 (page 3 of 4) - Rev C


---

## Schematic TI4 (page 4 of 4) - Rev C


---

## PC Layout Layer 1 (page 1 of 4) - Rev C


---

## PC Layout Layer 2 (page 2 of 4) - Rev C


---

## PC Layout Layer 3 (page 3 of 4) - Rev C


---

## PC Layout Layer 4 (page 4 of 4) - Rev C


---

# Wirelist


This chapter contains the Rev C wirelist of the Sun 1/4" Tape Controller Board.
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
