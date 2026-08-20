---


---


# Sun 2251 Memory Board


# Engineering Manual


Company Confidential

Sun Microsystems Inc.

Part Number: 800-XXXX-01

Revision: Draft of [date]


>
This manual describes the Sun 2251 memory board.
On a standard VME Eurocard formfactor,
the 2251 memory board features two megabytes
On a standard VME Eurocard, the 2251 memory board contains two megabytes
of high-speed dynamic main memory with byte parity error detection.

The Sun 2251 memory board works in conjunction with the Sun 2250 CPU board.
CPU and memory boards communicate via a private P2-Bus.
Up to four 2251 memory boards can be used for one 2250 CPU board,
providing a total system memory of two to eight megabytes.


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.

Sun and the combination of Sun with a numeric suffix are trademarks of
Sun Microsystems Inc.


---


---

## Specification Summary


### Memory





- 2M Bytes of main memory

- high-speed, no-wait state operation with 2250 CPU

- transparent hardware memory refresh with 2250 CPU

- byte parity error detection




### Environmental Characteristics


- Operating Temperature:	10 - 55 C

- Humidity:		0 - 90 %, non-condensing


### Power Characteristics


- 3 Amp max at +5 Volt +- 5%


### Physical Characteristics


- Height:	233.33 mm

- Width:	160.00 mm

- Weight: 500 g


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

## Memory


The 2251 memory board consists of the following functions:


2M bytes memory array

RAM address multiplexor and driver

RAM control signal driver

RAM data drivers

board select logic


The interconnection of these pieces is shown in the Figure [Figure](#a315).


![Placeholder: a315.press]()


*Figure: **Memory Interface***

<a id="a315"></a>


---

### Memory Interface


The CPU interfaces to the memory via the P2-Bus.
For a description of the P2-Bus, see the 2250 CPU Board manual.


### Memory Organization


Memory is organized as 4 banks of 18 256K RAM chips each,
making a total of 72 chips.
Each bank stores 512K bytes plus parity,
making total memory capacity two megabytes.


### Memory RAM and Bank Decoding


Due to the pipelined RAS-CAS access, memory is CAS decoded
because the translated address bits that select
which bank of memory is accessed are only available
in time for the CAS address strobe.


```

---------------------------------
| Decoding	256K RAMs	|
---------------------------------
| RAS Bank	A01		|
| RAS Address	A02..A10	|
| CAS Address	A11..A19	|
| CAS Bank	A01,A20		|
---------------------------------

```


### Memory Board Select


Decoder [74F138:U200] and jumper [J.8:J200] decode the high-order
address lines [P2.A21..A23] to select one of four two megabyte sections.
If enabled, the Memory Select signal [M.SEL]
enables CAS decoder [74F138:U201] and read/write decoder
[ALS138:U202].


### Memory Drivers


The RAM signals are driven as follows:

[RAS, WEL, WEU], and the Address Lines are driven by
74F244 drivers with 33 Ohm series termination.
Each bank of memory has its own set of drivers for these signals.

CAS is driven directly by the CAS decoder [74F138:U201]
with 33 Ohm series termination.
Data to the RAMs is driven by [ALS244:U210..U214] drivers
with 68 Ohm series termination [R:R1200-R1217].
