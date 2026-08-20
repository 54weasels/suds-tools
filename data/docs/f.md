---


# Ferrari Engineering Manual


Company Confidential

Sun Microsystems Inc.

Part Number: 800-XXXX-01

Revision: 01 of [date]


>
This manual describes the Sun-3 Ferrari CPU and I/O Expansion Board.
Ferrari is a workstation computer that supports color, greyscale,
and monochrome displays with a resolution of 1152*900 pixels.
In addition, Ferrari supports monochrome displays with 1600*1280 resolution.
The Ferrari CPU Board combines a 20.0 or 16.7 MHz 68020 CPU,
a 68881 FPP with an independent clock,
the Sun-3 virtual memory management with 8 contexts of 256 Megabytes each,
4, 8, or 12 megabytes of main memory,
1 megabyte of color or greyscale video memory,
256 kilobyte of monochrome and overlay video memory,
an integral Ethernet interface,
two serial I/O lines,
a real-time clock,
and various system utilities.
The Ferrari I/O Expansion Board supports three slots for Sun I/O modules.


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


- 68020 CPU, 20.0 MHz or 16.7 MHz
-
- 68881 FPP, independent clock

- Sun-3 MMU (8 contexts of 256 megabytes each)
-
- 4, 8, or 12 Megabytes of main memory (1 MBit RAMs)
-
- 1 Megabyte of color/gresycale video memory

- 128 or 256 Kilobyte of monochrome video memory

- 128 Kilobyte of overlay video memory

- Memory cycle time: 200 nanoseconds


### Display


- Five display configurations:

- Color: 1152*900*8 resolution, 16 million colors

- Greyscale: 1152*900*8 resolution, 256 shades of grey

- Monochrome: 1152*900*1 resolution, 1 bit per pixel
-
- Highres Monochrome: 1680*1280*1 resolution, 1 bit per pixel

- Server (nodisplay)

- 66 Hz non-interlaced video refresh on all displays


### I/O


- integral Ethernet interface with onboard transceiver

- I/O Expansion board supports three I/O modules

- two programmable serial I/O ports with full modem control

- two additional serial interfaces for keyboard and mouse


### Other Features


-
- 64K Bytes EPROM

- 2K Bytes EEPROM

- real-time-clock with battery backup

- extensive self-diagnostic capabilities


---

## Introduction


Ferrari is a workstation computer that supports color,
greyscale, and monochrome displays.
Ferrari consists of a single-board design CPU
and an optional input/output expansion board.
The CPU board includes the CPU, virtual memory management,
optional processor enhancements,
4 to 12 megabytes of main memory, 1.25 megabytes of video memory,
Ethernet, RS-423 interfaces, and various other system utilities.

The processor is the Motorola 68020 32-bit VLSI Central Processing Unit (CPU)
and the Motorola 68881 IEEE Floating Point Processor (FPP).
The CPU runs has a clock of 16.7 or 20 MHz.
The FPP has its own independent oscillator
with a range of 12.5 to 20 MHz.
Ferrari includes a Sun-3 memory management unit (MMU)
that provides eight simultaneous contexts with up
to 256 megabyte virtual memory space each.

The Ferrari CPU board includes 4, 8, or 12 megabytes of main memory.
Main memory is based on 1 MBit RAMs and features byte parity error detection.
In addition, the Ferrari CPU board has 1.25 megabyte of video memory.
Two kinds of video memory are provided: pixel and plane organized.
The pixel video memory (1 megabytes) is for color/greyscale
with each byte representing one pixel on the display.
The plane memory (256 kilobytes) provides two planes,
one for monochrome and one for overlay.
The overlay plane determines pixel by pixel whether the pixel memory
or the monochrome memory plane is used for color/greyscale displays.

The Ferrari CPU board supports five display options:
color, greyscale, monochrome, high-res monochrome, and server (nodisplay).
All displays feature Sun standard resolution (1152*900)
and flickerfree, non-interlaced 66 Hz refresh.
For color, an integral lookup table provides 256 simultaneous
color out of a palette of more than 16 million.
For gresycale, the lookup table provides 256 shades of grey.

The Ferrari CPU board includes an integral Ethernet interface.
This interface uses a VLSI Ethernet controller that features
high-performance frame handling and extensive diagnostic capabilities.
Ethernet packets are directly transferred in and out of main memory
through the use of direct virtual memory access (DVMA).
The Ferrari I/O expansion board provides three additional slots
for Input/Output devices such as SCSI or other networks.

For serial I/O, two serial communication channels are provided
featuring software programmable baud rates from 75 Baud to 19.2 KBaud
and supporting asynchronous, synchronous, or bit-stuffing protocols.
Two additional ports are provided for keyboard and mouse interfaces.

Other features of the board include a real-time clock with battery backup,
an EEPROM, and an identification PROM providing software-readable serial number
and Ethernet address.

The board also includes extensive facilities for software
and hardware diagnostics.
Among them are a diagnostic switch, a diagnostic display for
displaying error messages, and a watchdog timer for automatic restart.


---

## Sun-3 Architecture Overview


Ferrari implements a Sun-3 architecture machine.
The complete specification of the architecture is contained
in the Sun-3 Architecture Manual.
The figure below illustrates how the CPU, MMU, and devices
are interconnected on the Ferrari Board.

The CPU sends out a virtual address that is translated by the MMU
into a physical address.
The CPU, Ethernet Interface, and I/O Modules
arbitrate for and share the virtual address bus on the left side of the MMU.
Main Memory, Video Memory, and I/O Devices
are addressed with physical addresses on the right side of the MMU.
All CPU accesses to Device Space pass through the MMU
and thus are translated and protected in an identical fashion.
In addition, direct memory accesses by DVMA masters such as the Ethernet
and I/O Modules also pass through the memory management and thus
operate in a fully protected environment.


```


	-------------		-----------		------------
	| 68020	    |		| 68881   |		| Main     |
	| CPU	    |>>>>>>>>>>>| FPP	  |	    >>>>| Memory   |
	-------------	|	-----------	    |	------------
			|	-----------	    |
	-------------	|	|	  |	    |	------------
	| Ethernet  |	|	| Sun-3	  |	    |	| Video    |
	| Interface |>>>|>>>>>>>| MMU	  |>>>>>>>>>|>>>| Memory   |
	-------------	|	|	  |	    |	------------
			|	-----------	    |
	-------------	|			    | 	------------
	| I/O       |   |			    |	| I/O      |
	| Masters   |>>>>			    >>>>| Slaves   |
	-------------					------------


```


---

## Specification Summary


### CPU





- M68020 CPU, 20.0 or 16.7 MHz

- M68881 FPP, 12.5 MHz, 16.6 MHz or 20.0 MHz




### Memory





- Main Memory: 4, 8, or 12 M Bytes (1 MBit RAM), parity error detection

- Color/Greyscale Video Memory: 1M Bytes (256K Video RAM)

- Monochrome Video Memory: 128K Bytes (256K Video RAM)
-
- Overlay Video Memory: 128K Bytes (256K Video RAM)

- Cycle Time: 200 nsec (20 MHz) or 240 nsec (16.7 MHz)




### Memory Management Unit





- type: Sun-3

- number of contexts: 8

- virtual address space: 256M Bytes




### Display Options





- /C: Color: 1152 by 900 by 8, 256 colors out of over 16 million

- /G: Greyscale: 1152 by 900 by 8, 256 shades of grey

- /M: Monochrome: 1152 by 900 resolution

- /MX: Highres Monochrome: 1600 by 1280 resolution

- /S: Server (no-display).

- All displays feature 66 Hz non-interlaced video refresh




### Ethernet Interface





- VLSI Ethernet controller (AMD 7990)

- packets transferred directly in and out of main memory (DVMA)

- extensive diagnostic capabilities




### IOXbus Interface





- three slots for I/O Modules

- supports slave, master, and interrupter functions

- data transferred directlty in and out of main memory (DVMA)




### Serial I/O Ports





- two programmable serial I/O ports

- based on synchronous communication controller (AMD 8530)

- software programmable baud rates (75 baud to 19.2 kilobaud)

- asynchronous, synchronous, and bit-stuffing protocols

- two serial ports for keyboard and mouse




### Other Features





- 64K Bytes EPROM (27512)

- 2K Bytes EEPROM (2816)

- read-only identification PROM




### Diagnostic Features





- diagnostic LED display

- diagnostic switch

- watchdog reset timer




### Environmental Characteristics


- Operating Temperature:	10 - 55 C

- Humidity:		0 - 90 %, non-condensing


### Power Characteristics


- 20 Amp max at +5 Volt +- 5%
-
- 4 Amp max at -5 Volt +- 5%


### Physical Characteristics


- Height:	366.67 mm (14.44")

- Width:	400.00 mm (15.75")

- Depth:	40.64 mm (1.6")

- Weight: 1788 g (64 oz)


# User Guide


## Connectors


This section documents the pinout of all the connectors.


### J-1: Keyboard/Mouse


```

	---------------------------------
	| PIN |	SIGNAL	| PIN |	SIGNAL  |
	---------------------------------
	|  1  |	RXD0[]	|  9  | GND	|
	|  2  | GND	| 10  | VCC	|
	|  3  | TXD0[]	| 11  | VCC	|
	|  4  | GND	| 12  | VCC	|
	|  5  | RXD1[]	| 13  | ----	|
	|  6  | GND	| 14  | VCC	|
	|  7  | TXD1[]	| 15  | VCC	|
	|  8  | GND	| --  | ----	|
	---------------------------------

```


### J-2: Serial Port A


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
	| 12  | ----	| 25  | VEE	|
	| 13  | ----	| --  | ----	|
	---------------------------------

```


### J-3: Serial Port B


```

	---------------------------------
	| PIN |	SIGNAL	| PIN |	SIGNAL  |
	---------------------------------
	|  1  |	----	| 14  | ----	|
	|  2  | TXDB[]	| 15  | DBB[]	|
	|  3  | RXDB[]	| 16  | ----	|
	|  4  | RTSB[]	| 17  | DDB[]	|
	|  5  | CTSB[]	| 18  | ----	|
	|  6  | DSRB[]	| 19  | ----	|
	|  7  | GND	| 20  | DTRB[]	|
	|  8  | DCDB[]	| 21  | ----	|
	|  9  | ----	| 22  | ----	|
	| 10  | ----	| 23  | ----	|
	| 11  | ----	| 24  | DAB[]	|
	| 12  | ----	| 25  | VEE	|
	| 13  | ----	| --  | ----	|
	---------------------------------

```


### J-XX: Ethernet Connector


A BNC connector provides a direct connection to Ethernet.


### J-XX: Color Video Connectors


Three BNC connectors provide Red-Green-Blue video,
and a fourth connector provides composite sync.
For greyscale, only the Red connector is used
with composite sync.


### J-XX: Monochrome Video Connector


```

	---------------------------------
	| PIN | SIGNAL  | PIN | SIGNAL  |
	---------------------------------
	|  1  | VIDEO+  |  6  | VIDEO-  |
	|  2  | ----    |  7  | GND     |
	|  3  | HSYNC   |  8  | GND     |
	|  4  | VSYNC   |  9  | GND     |
	|  5  | ----    |  -  | ----    |
	---------------------------------

```


### Space on Backplane


The connectors use up space on the backplane as follows:


```


	SerialA 25-pin  2.3
	SerialB 25-pin  2.3
	Keybd/M 15-pin  1.7
	Ether   BNC     0.8
	Video   9-pin   1.4
	RBGSync	4 BNC	2.8
	Diag LED+Switch 1.0
	-------------------
	Total:          12.3

Note: Dimensions include 0.2" clearance for each component.


```


---

# Theory of Operations


## Major Blocks


The major logic blocks are:


Power, Initialization, and Clocks

CPU and FPP

MMU

I/O Devices

Memory

Parity Logic

Video Subsystem

Ethernet Interface


---

## Power


*Reference:* Schematics Page 19

The Ferrari Board uses +5V for all of its onboard logic
and a -5V for the RS423 drivers and the Video ECL circuitry.


## Initialization


*Reference:* Schematics Page 19

The Ferrari Board includes a simple power-on reset generator.


---

## Clock Oscillators


*Reference:* Schematics Page 2

The Ferrari Board has 3 independent clock oscillators on board. They are:


CPU clock: [K1114A:U102] (80.0000 MHz or 66.6666 MHz)

FPP clock: [K1114A:U103] (33.3333 MHz)

UART clock: [K1114A:U602] (19.6608 MHz)

Video clock: [K1114A:U1800], (100.000 MHz or 200.000 MHz)


In addition, the Ethernet phase decoder has a on-chip
oscillator with an external 20.000 MHz cyrstal and the real-time
clock has an on-chip oscillator controlled by a 32,768 Hz crystal.


---

## CPU


*Reference:* Schematics Page 1


### Reset


CPU Reset is generated by PAL [RESET] under two conditions:


*Power-On-Reset:* The power-on-reset generator asserts [POR]
or power supplies deasserts power-ok [POK].

*Watchdog Reset:* If the CPU halts it asserts [P.HALT].
This is detected by the reset PAL and will cause a CPU reset
to continue processing.


In both cases, PAL [RESET] asserts [INIT] to reset on-board logic
and simultaneously asserts [HALT] and [RESET] to reset the CPU.


### Function Code Decode


In the Sun-3 architecture, the function codes encode the type of CPU cycle.
The function code is decoded in PAL [FCDECODE] as follows:


```


	EN.CPU := (FC==7)

	EN.CTL := (FC==3) * /A31

	EN.DEV := (FC==1,2,5,6) * (A28..A31==0000 + A28..A31==1111)

	CS.FPP := (FC==7) * A17 * /A16 * /A15 * /A14 * A13

	OE.PROM:= (FC==6) * EN.BOOT


```


Control space is enabled for FC==3 with the high-order address bit not set.
Device space is enabled for all data and program accesses.
The floating point processor is selected in CPU space with the appropriate
coprocessor and floating point id field on the address lines.
The boot PROM is enabled on supervisor program fetches in boot states.
RAS is disabled for floating point processor accesses.


### DSACK


The DSACK signal tells the CPU when the continue with the current
bus cycle and what data bus size the selected device responded to.
A list of the Ferrari devices, their addresses, data bus size,
and [DSACK] timing appears in the table below:


```

-------------------------------------------------------------------
Device		Type	Address		Size	DSACK	Wait States
-------------------------------------------------------------------
FPP		--	n.a.		32-bit	dyn.	var.
Control Space	--	n.a.		8-bit	C.S7	3
Interrupt Vector--	n.a.		8-bit	C.S7	3
Main Memory	0	0x00000000	32-bit	memack	1
Monochrome Video0	0xFF000000	32-bit	memack	1W, 2R
Overlay Video 	0	0xFF400000	32-bit	memack	1W, 2R
Color Video 	0	0xFF800000	32-bit	memack	1W, 2R
Keyboard/Mouse	1	0x00000000	8-bit	C.S21	9
Serial Port	1	0x00002000	8-bit	C.S21	9
EEPROM 		1	0x00004000	8-bit	C.S21	9
Clock 		1	0x00006000	8-bit	C.S21	9
Parity Register	1	0x00008000	8-bit	C.S21	9
Interrupt Reg.	1	0x0000A000	8-bit	C.S21	9
Ethernet Reg.	1	0x0000C000	8-bit	C.S21	9
Color Map	1	0x0000E000	8-bit	C.S5	2
EPROM		1	0x00010000	8-bit	C.S21	9
IOX Interface	1	0x0001A000	8-bit	d.ack01	var.
--------------------------------------------------------------------

```


### BERR


CPU bus error [BERR] is asserted under the following conditions:


```

---------------------------------------------
Signal	Space	Description
---------------------------------------------
EMULATE	CPU	invalid coprocessor, breakpoint, protection cycle
RERUN	DEVICE	rerun cycle
BERR.V	DEVICE	invalid page entry
BERR.P	DEVICE	protection error
BERR.T	DEVICE	timeout
BERR.X	DEVICE	IOXbus error
---------------------------------------------

```


On non-DMA cycles, the invalid page, protection, and timeout
conditions are also latched in the bus error register [F534:U323].


### CPU Derived Clocks


The clock strobes [C.S4, C.S5, C.S7, etc] are derived from transitions
of the CPU clock.
They are illustrated in the figure below for a 10-state cycle.


```


68020 State	0   1   2   3   4   5   6   7   8   9   0
C.CPU		----____----____----____----____----____----
P.AS-		----________________________________--------
C.S4-		----------------____________________--------
C.S5-		--------------------________________--------
C.S7-		----------------------------________--------


```


When the memory is not active for refresh or video cycles,
the clock strobes become active on the corresponding CPU states.
When the memory is active for refresh or video cycles,
the clock strobes do not start until the memory is synchronized
to the CPU. See memory timing below.


---

## DVMA Logic


*Reference:* Schematics Page 2, Motorola 68020 Data Book.


### Overview


The DVMA Controller takes requests from DVMA devices,
obtains the processor bus from the 68020,
and performs a read/write cycle for the device,
generating appropriate function codes and strobes.

The DVMA controller arbitrates among four DVMA requests.
DVMA request 0 is the on-board Ethernet.
The three other requests are reserved for I/O modules.
Requests are served in a round-robin priority fashion.


### DVMA Cycles


DVMA requests are synchronized with register [74F374:U213]
before entering the DVMA controller PAL [P16R8:U214].
The DVMA controller PAL prioritizes the incoming requests,
issues a bus request [BR] to the 68020,
then waits for the 68020 to issue bus grant [BG]
and the end of 68020 address strobe [AS],
before asserting the DVMA enable corresponding to the request.


---

### DVMA Arbitration Cycle


Arbitration occurs concurrently with ongoing bus activity.
The 68020, after receiving a bus request [BR-] issues a bus grant [BG-].
When the DVMA controller sees bus grant and address strobe
[P.AS] deasserted, it acquires the bus and asserts the DMA Enable.


```


DVMA-State	-12  -11 -10 -9  -8  -7  -6  -5  -4  -3  -2  -1  0   1
C.CPU		----____----____----____----____----____----____----____
D.REQx-		----________________________________________------------
D.Rx-		----________________________________________________----
BR-		------------________________________________________----
BG-		----------------------------____________________________
AS-		____________________________________----------------____
D.ACKx-		--------------------------------------------____________


```


### DVMA Cycle


```


DVMA-State	-2  -1  0   1   2   3   4   5   6   7   8   9   10  11
C.CPU		----____----____----____----____----____----____----____
X.DMAEN-	----________________________________________------------
AS-		------------________________________--------------------
68020_S(0)-	------------------------------------------------________


```


---

## IOXbus Interface


The IOXbus interface connects the CPU to the optional I/O modules.

The IOXbus data lines [D.D00..31] connect to the CPU data bus [D00..31]
via bidirectional transceivers [ALS245:U220,U222,U224,U226].
Series resistors [R8.DIP:U221,U223,U225,U227] control undershoot.
The bidirectional transceivers are enabled via PAL [P16L8:U215] as follows.
The IOXbus data lines are driven from the processor data bus
on all processor write cycles and all DVMA read cycles.
The processor data bus is driven from the I/O-bus on all DVMA
write cycles and all processor read cycles from I/O devices and
control space devices.

The IOXbus address lines [D.A00..27] connect to the CPU virtual address bus
[A00..27] via bidirectional bus buffers [ALS245:U204..U207].
In addition, IOXbus size lines [SIZ0..1] and read/write line [R/W]
connect to the corresponding CPU signals via buffer [ALS245:U208].
These bus buffers drive from the CPU bus to the I/O bus on non-DVMA cycles,
and from the I/O bus to the CPU bus on DVMA cycles.


---

## MMU and Control Space Devices


*Reference:* Schematics Page 3


### Overview


The MMU consists of context register [ALS374:U310],
segment map RAM [2188:U302..U303],
and page map RAM [2168:U304..U308].

Other control space devices are
the bus error register [F534:U323],
the system enable register [ALS273:U325] with readback [ALS373:U373],
the diagnostic register [ALS273:U327] with LEDs [LED4:U328..U329],
and the ID PROM [P5X8:U324].

The MMU RAMs and the MMU buffers are enabled via PAL [P16L10:U331].
The control space devices are accessed via read/write decoders
[ALS138:U334..U335].


### MMU Operation


During a device space cycle, the value of the context register
and the high-order processor address lines [A17..A27]
index the segment map and access a page-map-entry-group.
The page-map-entry-group, in conjunction with address lines [A13..16],
indexes the page map RAM.

The protection PAL [P16L8:U332]
checks whether the page map protection bits allow the type of cycle attempted.
If there is a protection error, the PAL asserts disable access [DISACC]
and the PAL asserts the relevant bus error signals [BERR.V, BERR.P].

The same PAL [P16R4:U332] updates the accessed and modified bits.
For the statistic bit update, the current value of the type field,
which is in the same nibble as the accessed and modified bit,
is latched by the statistic PAL with clock [C.S5].
Starting with [C.S5], the statistic PAL asserts [WE.STAT-],
which is the write enable for the statistic RAM [2168:U304],
and output-enables the new data to be written into the statistic RAM.
Series resistors are provided to limit current due to buffer overlap.


---

## I/O Devices


*Reference:* Schematics Page 4, 5, 6, 7, 8


### Overview


Input/Output devices comprise the EPROM, the EEPROM,
the time-of-day clock, the interrupt register,
the Keyboard/Mouse UART, the Serial Communication Controller,
the Ethernet Control Register, and the Color Map.


### Decoding


Input/Output devices are decoded by DECODE PAL [P16L8:U400],
by IODECODE PAL [P16L8:U401], and by decoders [74ALS138:U407,U408].


### EPROM


Since the EPROM is larger than a single 8K page, it is addressed
directly with the virtual address from the CPU, [A00..A15].
The EPROM is always chip enabled with CE tied to ground.
The EPROM are output-enabled with signal [OE.PROM] generated in
PAL [P20L8:U412] during boot cycles [OE.BOOT] and during
read PROM cycles.


### The Time-of-Day Clock


The time-of-day chip [7170:U402] maintains a real-time clock.
A battery powers the chip when the system is off.
The chip automatically switches to battery power when main power goes off.


### Interrupt Enable Register


The interrupt enable register [ALS273:U404] in conjunction with
readback [ALS373:U405] enables interrupt sources and controls
software interrupts in the system.


### Keyboard/Mouse


The serial keyboard/mouse UART [8530:U500] are implemented with
a SCC (serial communication controller).
The SCC features two high-speed, highly programmable serial channels
with built-in baud-rate generators.
The clock input to the SCC is a 4.9152 MHz input clock [C.SCC],
independent of the CPU clock.

The serial lines to and from the keyboard/mouse are driven and
received via inverters [74LS04:U508, U510].


### Serial Communication Controller


The RS-423 UARTS [8530:U501] are implemented with the same type
SCC as the keyboard/mouse interface.

Serial port A occupies channel A of the UART, in conjunction
with inverter [74LS04:U508], driver [26LS29:U509], and
receiver [26LS32:U506].

Serial port B occupies channel B of the UART, in conjunction
with inverter [74LS04:U510], driver [26LS29:U511], and
receiver [26LS32:U507].

Receiver [26LS32:U515] is shared between channel A and B
for synchronous UART applications.


---

# Memory


## Memory Organization


Memory includes main memory and video memory. Both feature
similar read, write, and refresh cycles.
The video memory features an additional video cycle
that transfers data to the serial port of the video RAM.


### Main Memory


Main memory consists of up to three banks of 36 1 MBit RAMs each (4 megabytes).
Each bank of main memory is RAS-decoded.
The low-order two address bits in conjunction with the size field
select which byte within the word of RAM chips is RAS enabled.
The banks are selected by CAS and the high-order address bits.
All RAM chips receive the same WE signals.

The decoding of the address lines is as follows:


```

-------------------------
| Decoding	Adrs	|
-------------------------
| RAS Byte	A00..01	|
| RAS Address	A02..11	|
| CAS Address	A12..21	|
-------------------------

```


### Plane Video Memory


Plane video memory consists of two banks of Video RAMs.
Two identical planes are provided:
one for the monochrome display plane and one for the overlay plane.
The monochrome plane can optionally be configured either as
128 KB or 256 KB for standard resolution and high resolution
displays, respectively.

Similar to main memory, plane video memory is RAS-decoded.
One (two) low-order address bit(s) in conjunction with the size field
select which set of Video RAM chips is enabled.
However, due to the organization of the Video RAM,
the other low-order address bits go into the CAS address,
and the high-order address bits go into the RAS address.


```

---------------------------------
| Decoding	128KB	256K	|
---------------------------------
| RAS Bank	A00..00	A00..01	|
| CAS Address	A01..08	A02..09	|
| RAS Address	A09..16	A10..17 |
---------------------------------

```


### Pixel Video Memory


Pixel video memory consists of 32 Video RAMs, providing 1 MByte of storage.

Similar to main memory, video memory is RAS-decoded.
The two low-order address bits in conjunction with the size field
select which byte within the word of Video RAM chips is enabled.
However, since pixel video memory is 128 bits wide,
two additional address lines are used to enable one of the words.
Again, due to the organization of the Video RAM,
the other low-order address bits go into the CAS address,
and the high-order address bits go into the RAS address.


```

---------------------------------
| Decoding	1 MB		|
---------------------------------
| RAS Bank	A00..03		|
| CAS Address	A04..11		|
| RAS Address	A12..19		|
---------------------------------

```


## Memory Interface Signals


The following signals interface to the memory:


```

---------------------------------------------------------------------------
Signal		Description			Asserted On	Off
---------------------------------------------------------------------------
A00..13		Virtual Address Lines (13)
PA13..23	Physical Address Lines (24)
SIZ0..1		Size Field (2)
D00..31		Data Lines (32), bidirectional
PO00,08,16,24	Parity (4), Output
PI00,08,16,24	Parity (4), Input
RAS		Row-Address-Strobe		S2		S6.5
CAS*		Column-Address Strobe		S4		S8
WE*		Write Enable			S2		S8+2
OE*		Output Enable			S4		S8
---------------------------------------------------------------------------
* Special timing for video cycles.

```


### Memory Control Signals


Memory control signals [RAS, CAS, VRAS, VCAS] are generated
by high-speed and-or gates [F64:U806,U807,U808,U809]
off clock-edges to achieve best timing control.
Memory control signals [WE] and [OE] are generated in PAL [P16R6:U802].
[C.S4ON] becomes active at [C.S3] when
a CPU cycle is in progress for which RAS has been asserted.
[C.S4ON1] is one clock period delayed from [C.S4ON].
The logic equations for these signals are as follows:


```


c.s4 =    c.s4on * c.cpu * en.vram-             % set on s4 for non-video cycle
	  c.s4on * c.cpu * write                % set on s4 for write cycles
	  c.s4on1 * c.cpu          		%  set on s6 for video read cyc
	  c.s4 * as                             % hold while as

ras =     m.as * c.cpu * cs.fpp- * m.cpuinh-	% Set on CPU cycle at m.s2
        + m.cack- * c.cpu * m.rasoff-  		% Set on V/R cycle at m.s2
        + ras * m.rasoff1- 			% Hold until m.s6 or end of vack
        + ras * c.cpub- 			% Hold until s+0.5

cas =     en.cas1 * en.cas2 * c.cpu * disacc-	% Set on CPU cycle at c.s4
        + cas * m.s7-                           % Hold til s7
        + cas * c.cpu * dma-			% Hold til s8 on nonDMA
        + cas * m.s5 * dma			% Hold til s9 on DMA

vras =    en.vras1 * en.vras2 * c.cpu * disacc-	% Set on CPU cycle at m.s4
        + m.cack- * c.cpu * m.s3  		% Set on V/R cycle at m.s4
        + vras * m.rasoff2-			% Hold until s8 or end of vack
        + vras * c.cpub- 			% Hold until s+0.5

vcas =    m.s5 * c.cpu * vras * m.rack-		% Set on non-rack cycle at s6
        + vcas * m.vras-			% Hold til end of vras
        + vcas * c.cpu				% Hold thru s(8).


```


## Memory Cycles


There are four cycles that apply to main memory and video memory:
Read Cycle, Write Cycle, Refresh Cycle, and Video Cycle.
These cycles are illustrated with timing diagrams below.

For read and write cycles, CAS is enabled only if there
is no protection error for the access.


### Read Cycle from Memory


Read cycles from Main Memory assert RAS at state 2 and CAS at state 4.
RAS is deasserted at state 6.5, and CAS at 8.


```


Memory State	0   1   2   3   4   5   6   7   8   9   10
C.CPU		----____----____----____----____----____----
A00..12		xxxx____________________________xxxxxxxxxxxx
PA13..23	xxxxxxxxxxxxxxx_________________xxxxxxxxxxxx
WE-		xxxx--------------------------------xxxxxxxx
RAS-		--------__________________------------------
CAS-		----------------________________------------


```


### Read Cycle from Video Memory


Read cycles from Video Memory start one clock period later than
read cycles from main memory due to the need to translate
the high-order addresses before they can be used as row address.
Output enable is asserted with VCAS to read the data.


```


Memory State	0   1   2   3   4   5   6   7   8   9   10
C.CPU		----____----____----____----____----____----
A00..12		xxxx____________________________________xxxx
PA13..23	xxxxxxxxxxxxxxx_________________________xxxx
VRAS-		----------------__________________----------
VCAS-		------------------------________________----
WE-		xxxx----------------------------------------
OE-		------------------------________________----


```


### Write Cycle to Memory


Write cycles to Video Memory, like read cycles, start one clock period later
due to the fact that the high-order addresses need to be translated
for the row address. However, different from read cycles, the CPU
does not need to wait for the write cycle to complete since
all necessary signals are latched until the cycle completes.


```


Memory State	0   1   2   3   4   5   6   7   8   9   10
C.CPU		----____----____----____----____----____----
A00..12		xxxx____________________________________xxxx
PA13..23	xxxxxxxxxxxxxxx_________________________xxxx
VRAS-		----------------__________________----------
VCAS-		------------------------________________----
WE-		----____________________________________----
OE-		--------------------------------------------
OE-		--------------------------------------------


```


### Refresh Cycle


A RAS-only refresh cycle is used with all Main Memory RAMs
receiving a RAS strobe at the same time and all Video Memory RAMs
receiving a RAS strobe one clock period later.
The refresh address counter is advanced at the end of every refresh cycle.
CAS and OE are not asserted for refresh cycles.


```


Memory State	0   1   2   3   4   5   6   7   8   9   10
C.CPU		----____----____----____----____----____--
RAS-		--------__________________----------------
VRAS-		----------------__________________--------
CAS-		------------------------------------------
VCAS-		------------------------------------------
OE-		------------------------------------------


```


### Video Cycle


This cycle applies to the video memory only.
During a video cycle, data is transferred from a memory row to the
serial shift register in the video RAM. This type of cycle is initiated
if the signal [OE] is asserted prior to the assertion of [VRAS].  [OE]
is deasserted synchronously with the falling edge of serial clock [SAC].
Since [SAC] is not synchronous to the CPU clock,
both [VRAS] and [VCAS] are held until the relevant [SAC] edge has occured.
During video cycles, [VRAS] is asserted for all Video RAM chips.
The address for video cycles comes from the video address counter.
The video address counter is advanced at the beginning
of every video cycle and is reset during vertical blanking.


```


68020 State	0   1   2   3   4   5   6   7   8   9   0
C.CPU		----____----____----____----____----____--
VRAS-		----------------__________________--------
R/W-		----------------------------------
CAS-		------------------------________________--
OE-		________________________________*---------
SAC		________--------________--------________--


```


### CPU Cycle followed by Refresh Cycle


This timing diagram shows a CPU cycle followed by a refresh cycle.


```


M State	0   1   2   3   4   5   6   7   0   1   2   3   4   5   6   7   0
C.CPU	----____----____----____----____----____----____----____----____-
C.CPUB	__----____----____----____----____----____----____----____----___
RAS-	--------__________________--------------__________________-------
CAS-	----------------________________---------------------------------
M.S3-	------------________________----------------________________-----
M.S5-	____----------------________________----------------_____________
M.S7-	____________----------------________________----------------_____
M.CACK-	____________________________-------------------------------------
M.RACK-	----------------------------_____________________________________


```


For more information, consult the transition diagram in the memory PAL.


---

## Parity Error Logic


*Reference:* Schematics Page 9

The parity error logic generates parity for write operations to main memory
and checks parity for read operations from main memory.
The parity error logic is not used for other accesses, such
as video memory or input/output.

On memory write cycles, parity generators [74F280:U710..713] generate
the parity bits that are driven via resistor [P8.DIP:U715] to memory.
During normal operation, signal [PAR.TEST] is not asserted,
causing *odd* parity to be generated and stored in memory.
(Odd parity means that the sum of all data bits and the parity bit is odd.)
If the signal [PAR.TEST] is asserted then *even* data is
generated and stored in memory. This allows to test the parity function.

On memory read cycles, the parity bits stored in memory
are checked with parity checkers [74F280:U710..713].
The output from the parity checkers, the size bits, and the low-order
two address bits are clocked into the parity register [74ALS374:U703]
at the trailing edge of [M.CAS-].

The information from the parity register is sampled in the
parity PAL [P16L8:U903] after the end of a read cycle from main memory.
To this end, PAL [P16L8:U902] asserts signal [PAR.SAMPLE]
on a qualified read cycle from main memory. A qualified read cycle
is one where parity checking is enabled and no previous parity errors
are pending.
Following the end of that cycle, signal [PAR.SAMPLE] stays asserted
for one clock phase of the CPU clock [C.CPU], i.e. until
state 2 of the next CPU cycle.

With [PAR.SAMPLE] active and during state 0 and 2 of the next CPU cycle,
PAL [P16R4:U704] checks the parity flags from the previous memory cycle.
If there is a parity error, the corresponding parity error output is set
[PAR.E00..24] as well as the parity error signal [PAR.ERR].
These parity error outputs remain set until cleared by parity error
clear [PAR.CLR] that is activated when parity checking is disabled
or when writing to the second word of the parity error register.
Parity error checking is also disabled following [INIT].

The following diagram illustrates the latching of the parity error:


```


68020 State	0   1   2   3   4   5   6   7   0   1   2

C.60		----____----____----____----____----____----
A00..12		xxxx____________________________xxxx________
PA13..23	xxxxxxxxxxxxxxx_________________xxxxxxxxxxxx
M.RAS-		--------__________________--------------____
M.R/W-		xxxx----------------------------xxxxxxxxxxxx
PAR.SAMPLE-	------------------------________________----
PAR.CHECK-	--------------------------------________----
PAR.ERROR-	----------------------------------------____


```


---

## Video


*Reference:* Schematics Page 17


### Video Clock Generation


The 100/200 MHz video clock is divided by shifter [8177:U1602]
into a 1-in-16 load pulse [W.LD].
This shift register is reinitialized when
a its output is "L". Since the serial input is tied to "L"
as well, the shifter is self-initializing.

A second shift register [8177:U1603] generates a clock [W.C16]
that is converted by ECL-TTL converter [10H125:U1605]
into a TTL clock [V.C16] for the video state machine.


---

### Video State Machine


The video controller generates the timing for the video monitor.
It was designed to support the following standard monitors:
standard color, standard greyscale, standard monochrome,
and enhanced monochrome. All the standard monitors share
the same specification.


```


-----------------------------------------------------------------------
Unit			Standard 	Enhanced
			Monochrome	Monochrome
-----------------------------------------------------------------------
Resolution		1152*900	1600*1280
-----------------------------------------------------------------------
Frequencies		[kHz]	[usec]	[kHz]	[usec]
-----------------------------------------------------------------------
Pixel Frequency         100000	0.010	200000	0.005
Horizontal Frequency    62.5    16.0	89.3	11.20
Vertical Frequency      66.7    14992	67.0	14929.6

Horizontal Timing	[Pixel]	[usec]	[Pixel]	[usec]
-----------------------------------------------------------------------
Horizontal Total        1600    16.0 	2240	11.20
Horizontal Visible      1152    11.52	1600	8.00
Horizontal Invisible    448     4.48	640	3.20
Horizontal Frontporch   0       0  	0	0
Horizontal Sync Width   128     1.28	256	1.28
Horizontal Backporch    320     3.20	384	1.92

Vertical Timing		[Lines]	[usec]	[Lines]	[usec]
-----------------------------------------------------------------------
Vertical Total          937     14992	1333	14929.6
Vertical Visible        900	14400	1280	14336
Vertical Invisible      37      592 	53	593.6
Vertical Frontporch     0       0  	0	0
Vertical Sync Width     10      160	10	112
Vertical Backporch      27      432	43	481.6
-----------------------------------------------------------------------


```


The video controller consists of horizontal PAL [P20X10:VIDEO1],
reload counter [P20X10:VIDEO2], vertical counter [P20X10:VIDEO3],
vertical PAL [P20X4:VIDEO4], and auxiliary PAL [P16R6:VIDEO5].
All these components are clocked with [V.CLK].

The horizontal PAL maintains seven bits of horizontal state [H0..H6],
and outputs horizontal reset [V.HRES], horizontal sintillation [V.SINT]
and horizontal sync [V.HSYN] signals.

The vertical counter provides 10 bits of vertical state [V0..V9].
The vertical PAL maintains an 11th bit of vertical state [V10],
which is used in conjunction with the state from the vertical counter
[V.V1..V.V9] to decode vertical reset [V.VRES], vertical blanking [VBLK],
and vertical sync [V.VSYN].

The auxiliary PAL generates horizontal, vertical, and composite syncs,
[V.HSYNC, V.VSYNC, V.CSYNC], blanking signals,
clock clear signals [V.CLKCLR], and the video request signal [V.VREQ].
