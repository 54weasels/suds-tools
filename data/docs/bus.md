---


# IOXbus Specification


Preliminary Draft

Sun Microsystems Inc.

Version of [date]

Company Confidential


>
The IOXbus is a low-cost input/output expansion bus
that interconnects a CPU with I/O modules.
It has the following main features:


32-bit data and address (non-multiplexed)

three DMA channels with parallel arbitration

5 microsecond maximum latency

up to 16 megabyte actual bandwidth

7 interrupt levels

geographical addressing (no jumpers)


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.

Sun and the combination of Sun with a numeric suffix are trademarks of
Sun Microsystems Inc.


---


---

## Overview


The IOXbus provides a cost-efficient means for interfacing
VLSI input/output chips to high-performance CPU/memory systems.
When coupling a VLSI I/O chip to a system, the key issue is how
long does it take to get the bus.
In addition, the bus needs to support the bandwidth required
by all components in the system.

Traditional system busses, such as VMEbus or Multibus,
are not suitable for this application because of their
unpredictable latency and throughput.
This is because of two reasons: one,
there is no time limitation on how long a master can retain bus mastership,
and two, for asynchronous busses there is typically
no time limitation of the length of the transfer cycle.
Unfortunately, both of these factors cause the bus
to exhibit an unpredictable response time that does not
allow it to connect directly to high-speed I/O chips,
such as Ethernet controllers or disk interfaces.
The slow arbitration of traditional busses is fundamentally incompatible
with VLSI components that have tight real-time requirements.

The IOXbus specification solves this problem by a design that
provides concise latency and bandwidth specifications.
This allows several high-bandwidth I/O devices to be directly
connected to a main memory system.
An example configuration that the IOXbus can support with simultaneous
input/output is two Ethernets, one disk interface, and one high-speed
serial line, without locking out the CPU.

This document is intended as an overview and as a specification
of the IOXbus.
Please report any errors so they can be corrected in future revisions.

---

## Goals


32-bit address/data (non-multiplexed)

Latency: 5 usec maximum

Bandwidth: 10 to 16 MByte/sec, depending on clock frequency:


```


	Clock	BusCyc.	Bandwidth (32-bit)
	[MHz]	[Mcyc]	[Megabyte/sec]
       ----------------------------------
 	12.5	2.5	10
	16.6	3.3	13.2
	20.0	4	16
       ----------------------------------


```


System can support any configuration of I/O modules
as long as total available bandwidth is not exceeded and
the latency requirement of each individual board is met

Timeout period for slaves: 2 usec.

ALS/LS-TTL driving and speed considerations

geographical addressing (no addressing jumpers)

7 level interrupt requests (autovectored)

rerun support (for devices that may deadlock)

I/O modules use standard single-height Eurocards (100x160mm)

bus uses single 96-pin DIN connector


---

## Example Requirements


The following list summarizes the bandwidth and latency requirements
of a number of interesting devices.


```


--------------------------------------------------------------------------
Description		Width	Latency	AvgRate	MaxRate	Inter.	Connector
			[bit]	[usec]	[Kcyc]	[Kcyc]	[Level]	[Type]
--------------------------------------------------------------------------
MASTER/SLAVE BOARDS:
--------------------------------------------------------------------------
802.3 Ethernet 10 MBit	8/16	6.4	666	800	3	D-15/COAX
802.4 MAP 5/10 Mbit	8/16	?	250	500	?	?
802.5 Tokenring 16 MBit	32	?	1000	1500	?	?
Tokenbus (100 MBit)	32	?	BUF.	BUF.	?	?
T1-Serial (1.5/2 MBit)	8/32	?	125	250	?	?
Applenet (232.4 KBit)	8/32	?	20	40	?	D-9
SCSI (disconnect)	16	10	1000	?	2	D-50
ESDI (direct disk)	16	5	666	800	2	?
Image Compressor	32	5	1000	?	?	?
Audio 			32	10	100	?	?	?
Floating Point		32	?	?	?	?	?
Graphics Processor	32	?	?	?	?	?
Coprocessor		32	?	?	?	?	?
NTSC Readout		32	?	?	?	?	?
NTSC Frame Grabber	32	?	?	?	?	?
Laserprinter		32	?	?	?	?	?
------------------------------------------------------------------------
SLAVE BOARDS:
------------------------------------------------------------------------
GPIB 			8	10	100	?	?	?
Centronix		8	20	50	?	?	?
8-line Async (19.2 KB)	8	?	20	?	?	50-pin
Modem (1200/2400 baud)	8	?	1	?	?	RJ-11
--------------------------------------------------------------------------


```


---

## Configuring IOXbus Systems


In configuring IOXbus systems, several constraints must be observed.

1. The IOXbus must accomodate the average data rate of all devices connected.
This rate is typically determined by the data input/output rate of the device.

2. The IOXbus must accomodate the peak rate of all simulatenously active
devices for the length of the latency period.
The peak rate is determined by the speed and nature of the device's
data transfer mechanism.

3. The latency requirements of all devices must be met.
Latency is the time the device can wait until it requires service.
Latency is a function of the data rate and of the amount of buffering.

Example: Consider a system with four IOXbus devices:
2 Ethernet, MAPnet, and ESDI.
Starting with the total available bandwidth, the average and the
maximum rate used by each device is subtracted.
In the average case, about 30% of total bandwidth remain for the CPU.
In the worst case, about 15% remains.


```

-------------------------------------------------------------------
Device		AvgRate	AvgRate	AvgRate	MaxRate	MaxRate	MaxRate
		Before	Used	Remain	Before	Used	Remain
-------------------------------------------------------------------
Ethernet1	3.33	0.66	2.66	3.33	0.80	2.53
Ethernet2	2.66	0.66	2.00	2.53	0.80	1.73
Mapnet		2.00	0.25	1.75	1.73	0.50	1.23
ESDI		1.75	0.66	1.09	1.23	0.8	0.43
-------------------------------------------------------------------

```


---

## IOXbus Architecture


The IOXbus supports two cycles: Master and Slave.
In addition, it supports an interrupt mechanism.
An I/O module may implement one or more of these functions.

For master cycles, the I/O module issues a direct-memory-access
request to the central arbiter in the system.

For slave cycles, the CPU addresses the I/O modules and
performs a read or write operation.
The maximum access time of the I/O modules is limited to 2.5 usec
to not violate the latency limit of the bus.

I/O modules are geographically addressed with fixed decoding per board-slot.
I/O modules are identified by a read-only TYPE register that
is located at byte address 0 of each module.
The type register presents a unique ID for each module.
In addition, the most significant bit of the type register
indicates whether the board has an active interrupt asserted to the bus
(interrupt bit is active high).


```

       TYPE REGISTER

       7   6   5   4   3   2   1   0
       ---------------------------------
       | I |    ID OF BOARD            |
       ---------------------------------
       I = INTERRUPT PENDING BIT

```


A IOXbus device requests interrupt service by asserting one
or more of the seven interrupt request lines.
Interrupt requests are level requests, that is, they stay
asserted until the source of the interrupt is cleared by
the software interrupt handler.
The pending interrupt requests are processed by the CPU interrupt logic.
If the interrupt pending is higher priority than the CPU interrupt level
then the CPU starts interrupt exception processing.
On initialization, interrupts are disabled.


---

## Sun-3 Implementation


In the Sun-3 Architecture, the 32-bit address lines of the IOXbus
are mapped between the I/O device and the system as follows:


```


IOXbus		System
-----------------------------
A00..27	28-bit virtual address
A28..30	3-bit context number
A31	FC2 (1=system, 0=user)
------------------------------


```


For master cycles, I/O devices that are system devices only
should drive A28 to A31 to all 1s.
I/O devices that are user devices should be able to drive
A28 to A30 to a programmable context number.
I/O devices that are not allowed to be system devices
must not drive A31 active.

Slave cycles use the same address mapping as master cycles:
the 68020 CPU provides a 28-bit virtual address and the
supervisor function code, and the context register provides
a 3-bit context number.
A slave module is selected with a geographical (fixed)
select line that is derived from the IOX device type.
The IOX device type provides 16 one-page entries,
each one selecting a geographically distinct IO module.
Geographical decoding means that I/O modules are addressed by board-slot.
Each slot can have any one IO device, and multiple slots can have
identical IO devices.

To configure a Sun-3 IOXbus system, software first reads the type register
on each board to determine what boards are present.
The type register, which stores a read-only unique code per board,
is the first byte within each board's address space.
Boards that are not present will cause a timeout/buserror exception.

The 7 interrupt levels are mapped to a set of reserved 68020 vectors.

---

## Clock Signal


```


CLK		----____----____

-------------------------------------------------------------------
Timing Specs			Min	Max	Derivation
-------------------------------------------------------------------
1  CLK PERIOD			50	80	20 MHz/12.5 MHz
2  CLK HIGH TO CLK LOW		20	50	40/60%
3  CLK LOW TO CLK HIGH		20	50	40/60%
-------------------------------------------------------------------


```


The clock on the bus is active low. It is driven from the CPU clock
with one AS1004 driver per module. Clock skew from CPU is 3.5 nsec maximum.


## Hold Signal


```


HOLD-		----__________________------

-------------------------------------------------------------------
Timing Specs			Min	Max	Derivation
-------------------------------------------------------------------
1  HOLD LOW 			0	16000	One refresh time
2  HOLD HIGH 			1000
-------------------------------------------------------------------

```


Hold keeps the CPU off the bus while asserted, thus maximizing
the bandwidth available for I/O modules.
The maximum hold time is specified to guarantee CPU interrupt response time.


---

## Master Cycle


To cause a Master Cycle, the I/O Module asserts D.REQ.
The central arbiter sees D.REQ and will arbitrate for bus mastership.
Once bus mastership is obtained, the arbiter sends D.ACK to the module.
D.ACK enables address, size, read/write, and write data
(in the case of a write cycle) to the bus.
At state 5, the acknowledge lines are asserted indicating that the
cycle will complete during the next clock cycles.
If the cycle caused a protection error, then bus error will also
be asserted at this time.
At state 7, DAS is deasserted, and at state 9 DACK is deasserted.
A separate request line HOLD is provided that keeps the CPU
off the bus while it is asserted.

The nominal length of a Master Cycle is 10 states.
Under certain infrequent conditions, such as memory refresh,
the actual length can increased to a maximum of 24 states.
The extra states for longer cycles are asserted between at state 0.
The time from DAS active until DAS inactive is constant
as a function of the clock rate.
They are sufficiently infrequent to not affect the average throughput
of the bus.


```


STATE		-2  -1	0   1	2   3	4   5	6   7	8   9	10/0

CLK	(IN)	----____----____----____----____----____----____----

DREQ-	(OUT)	X_____________---------------------------------_____

DACK-	(IN)	----________________________________________--------

ADRS	(OUT)	XXXX________________________________________XXXXXXXX

WRDATA	(OUT)	XXXXXXXXXXXXXXXX____________________XXXXXXXXXXXXXXXX

DAS-	(IN)	----------------------------________----------------

BERR-	(IN)	----------------------------________----------------

RDDATA	(OUT)	XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX_______XXXXXXXX

--------------------------------------------------------------------
Timing Specs			Min	Max	Derivation
--------------------------------------------------------------------
1  CLK LOW TO DACK LOW		0	15	PAL(CLK-Q)
2  CLK LOW TO DACK HIGH		0	15	PAL(CLK-Q)
3  CLK LOW to ADRS VALID	0	40	68020_6-ALS245
4  DACK LOW to ADRS VALID	0	25	(3)-(1)
5  DACK HIGH to ADRS INVALID	0	25	ALS652(OE-Q)
6  CLK HIGH to WRDATA VALID	0	15
7  DACK HIGH to WRDATA INVALID	0	35	same as (5)
8  CLK LOW TO DAS LOW		0	15	PAL(CLK-Q)
9  CLK LOW TO DAS HIGH		0	15	PAL(CLK-Q)
10 CLK LOW TO BERR LOW		0	25	F374+ALS244
11 DAS HIGH TO SACK/BERR HIGH	0
12 S7 TO READDATA VALID 		10
13 S9 TO READDATA INVALID	0
14 DACK HIGH TO READDATA HOLD	0
15 DREQ LOW UNTIL DACK LOW	1 clk	5000
16 DAS LOW UNTIL DREQ HIGH	0	50
17 DACK HIGH UNTIL DREQ LOW	0
--------------------------------------------------------------------

```


---

## Slave Cycle


On a slave cycle, the I/O module receives an address,
a read/write line, write data in case of write cycles,
and a select line SEL.
The selected module performs the requested operation
and responds by asserting slave acknowledge (SACK),
which is one of DSACK0 (transfer acknowledge 8-bit/32-bit),
DSACK1 (transfer acknowledge 16-bit/32-bit), BERR (bus error),
or RERUN (deadlock).
If there is no response by state 80 (timeout state),
the CPU will complete the cycle itself with a bus-error/timeout.
Slave modules can perform 8-bit, 16-bit, and 32-bit transfers
using the dynamic bus sizing mechanism of the 68020.

The timing diagram below shows a 12-state slave cycle,
in which SEL is asserted at state 5 and SACK is asserted at state 7.
Slave cycles can be up to 2 microseconds long, which is the timeout period.


```


STATE		0   1   2   3   4   5   6   7   8   9   10  11  12/0

CLK	(IN)	----____----____----____----____----____----____----

ADRS	(IN)	XXXXXXXXXXXXXXXX________________________________XXXX

R/W	(IN)	XXXXXXXXXXXXXXXX________________________________XXXX

WRDATA	(IN)	XXXXXXXXXXXXXXXX________________________________XXXX

SEL-	(IN)	--------------------________________________--------

RDDATA	(OUT)	XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX______XXXXXXXX

SACK-	(OUT)	---------------------------_________________---------

ARWS: Address, Read/Write, Writedata, and Select
SACK: DSACK0, DSACK1, BERR, RERUN
--------------------------------------------------------------------
Timing Specs                    Min     Max	Derivation
--------------------------------------------------------------------
1  CLK LOW TO SEL LOW		0       25	F374+F32+F32+F32
2  CLK LOW TO SEL HIGH		0       35	68020_DS+F32+F32
3  CLK LOW TO SACK LOW	 	0	20	Synchronous DSACK 1)
4  ARWS VALID TO SEL LOW	25
5  SEL HIGH TO ARWS HOLD 	0
6  CLK HIGH TO ARWS HOLD 	0
7  READDATA TO CLK LOW SETUP	20		ALS245+68020_27
8  SEL HIGH TO READDATA INVALID	0	50	68020_29+LS652
9  SEL HIGH TO DSACK HIGH	0	50
10 SEL LOW TO SACK ACTIVE		2000	Timeout
--------------------------------------------------------------------
1) in order to be recognized on the next clock edge.

```

Slaves with 0 nsec hold time on address, read/write, and write data,
can be controlled directly by das and one gate delay.
Devices requiring longer hold time need to be designed either
with latches on the respective signals or with a shorter strobe.


---

## IOXbus Signals


The I/O modules have the following signals, as seen from the I/O Board:


```


Name	I/O	Description			Type	Pullup
---------------------------------------------------------------------
D00..31	I/O	32-bit Data Bus			TS
A00..31	I/O	32-bit Address Bus		TS
SIZ0..1	I/O	2-bit Transfer Size		TS
R/W-	I/O	Read/Write- Signal		TS
DAS-	I	Address Strobe
SEL-	I	Board Select
CLK	I	System Clock
INIT-	I	Initialization

HOLD-	O	Bus HOLD			OC	Pullup on CPU
DREQ-	O	DMA Request			STD	Pullup on CPU
DACK-	I	DMA Acknowledge

IRQ1..7- O	Interrupt Request		OC	Pullup on CPU

ACK0-	O	Transfer Acknowledge 8-bit	TS/OC	Pullup on CPU
ACK1-	O	Transfer Acknowledge 16-bit	TS/OC	Pullup on CPU
BERR-	O	Transfer Error			TS/OC	Pullup on CPU
RERUN-	O	Rerun Cycle			TS/OC	Pullup on CPU

SPARE	I/O	Spare Pin				Reserved for future

72 pins

```


---

## P2IO Module PinOut


This is the pinout for the P2IO module connector.


```


MODULE CONNECTOR
-----------------------------
PIN #	ROW A	ROW B	ROW C
-----------------------------
1	D00	D16	D08
2	D01	D17	D09
3	D02	D18	D10
4	D03	D19	D11
5	D04	D20	D12
6	D05	D21	D13
7	D06	D22	D14
8	D07	D23	D15
9	GND	GND	GND
10	CLK-	D24	DREQ-
11	GND	D25	A27
12	SACK1-	D26	A26
13	SACK0-	D27	A25
14	R/W-	D28	A24
15	BERR-	D29	A23
16	RERUN-	D30	A22
17	GND	D31	A21
18	DAS-	A28	A20
19	GND	A29	A19
20	SEL-	A30	A18
21	INIT-	A31	A17
22	HOLD-	SIZ0	A16
23	A07	SIZ1	A15
24	A06	IRQ7-	A14
25	A05	IRQ6-	A13
26	A04	IRQ5-	A12
27	A03	IRQ4-	A11
28	A02	IRQ3-	A10
29	A01	IRQ2-	A09
30	A00	IRQ1-	A08
31	-5V	DACK-	+12V
32	VCC	VCC	VCC
-------------------------------

```


---

## Ferrari Backplane Pinout


This is the pinout for the Ferrari backplane connector.


```


P2-Connector				P3-Connector
---------------------------------------------------------------------
PIN #	ROW A	ROW B	ROW C		PIN #	ROW A	ROW B	ROW C
-----------------------------		-----------------------------
1	A00	VCC	INIT-		1	VCC	D00	GND
2	A01		IRQ1-		2	VCC	D01	GND
3	A02		IRQ2-		3	VCC	D02	GND
4	A03		IRQ3-		4	VCC	D03	GND
5	A04		IRQ4-		5	VCC	D04	GND
6	A05		IRQ5-		6	VCC	D05	GND
7	A06		IRQ6-		7	VCC	D06	GND
8	A07		IRQ7-		8	VCC	D07	GND
9	A08		SEL0		9	VCC	D08	GND
10	A09		SEL1		10	VCC	D09	GND
11	A10		SEL2		11	VCC	D10	GND
12	A11	GND	SEL3		12	VCC	D11	GND
13	A12	VCC	HOLD-		13	VCC	D12	GND
14	A13		DREQ1-		14	VCC	D13	GND
15	A14		DACK1-		15	VCC	D14	GND
16	A15		DREQ2-		16	VCC	D15	GND
17	A16		DACK2-		17	VCC	D16	GND
18	A17		DREQ3-		18	VCC	D17	GND
19	A18		DACK3-		19	VCC	D18	GND
20	A19		RERUN-		20	VCC	D19	GND
21	A20		BERR-		21	VCC	D20	GND
22	A21	GND	ACK0-		22	VCC	D21	GND
23	A22		ACK1-		23	VCC	D22	GND
24	A23		GND		24	VCC	D23	GND
25	A24		DAS		25	VCC	D24	GND
26	A25		GND		26	+12V	D25	+12V
27	A26		CLK-		27	+12V	D26	+12V
28	A27		GND		28		D27
29	A28		SEL-		29		D28
30	A29		R/W-		30	-5V	D29	-5V
31	A30	GND	SIZ0		31	-5V	D30	-5V
32	A31	VCC	SIZ1		32	-5V	D31	-5V
---------------------------------------------------------------------

```


### Backplane to P2IO Adaptor


The following logic is required for the backplane to P2IO adaptor:


Clock buffer (one AS1004 for each I/O module)

Select Decoder (with base address/jumpers for multiple adaptors)

Sub-Arbiters (with jumpers for multiple adaptors)


---

## Electrical Specifications


```


Tri-State Drivers	Iol 	24 mA @ 0.5V
			Ioh	-2 mA @ 2.4V

Open Collector Outputs	Iol 	16 mA @ 0.5V

Inputs			Iil	-1.6 mA @ 0.0V
			Iih	0.1 mA @ 2.4V

Capacitive Load		Cmax	 25 pF

Power Limit		VCC:	3 Amps at +5Volt
			+12V:	0.2 Amp at +12Volt
			-5V:	0.2 Amp at -5 Volt


```


Specific systems may apply a separate limit on the
total available power to full configurations.


## Mechanical Specifications


```


Size		4" x 6" (100 x 160 mm)
Area		24 sq.in. (60 IC equiv at 0.4 sq.in/ICeq)
P1-Connector	96-pin DIN connector


```
