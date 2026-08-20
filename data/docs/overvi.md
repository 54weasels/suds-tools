---


# Ferrari: a High-performance, Low-cost Workstation


Andy Bechtolsheim

Sun Microsystems Inc.

Draft Version of [date]

Company Confidential


>

This document presents a summary of Ferrari,
a high-performance single-board workstation
that supports a wide number of displays and
features a low-cost input/output expansion.


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.

Sun and the combination of Sun with a numeric suffix are trademarks of
Sun Microsystems Inc.


---


---

## Introduction


Ferrari is:


- a high-performance, inexpensive, single board color Workstation

- supports color, greyscale, and monochrome displays, and server

- display resolution: standard (1152*900) and enhanced (1600*1280)

- input/output: low-cost P2 input/output modules (on second board)


Ferrari Specifications: same as Carrera except for:

-


- 20.0 MHz 68020 CPU with 1 wait state (100 nsec RAM) or

- 16.6 MHz 68020 CPU with 1 wait state (120 nsec RAM)

- 4 or 8 or 16 MByte main memory (1 MBit RAM)

- 1 MByte pixel video memory for color/greyscale

- 256 KByte video memory for monochrome and overlay plane

- integrated color DAC/lookup table with 8-bit input/24-bit output

- Ethernet with on-board transceiver
-
- no VME Interface

-


Ferrari P2-Input/Output Modules


-
- P2 input/output modules provide low-cost I/O expansion

- Functions include SCSI interface and second Ethernet for gateways

- Ferrari package includes space for three P2 input/output modules


Committed Features for First Product:


-
- 16.6 MHz CPU clock

- 4 Megabyte main memory

- standard resolution displays


---

## Marketing Overview


Target Markets and Customers:


- CAD/CAE (color)

- Typesetting (greyscale)

- Document Retrieval (highres)

- Federal Government (color, greyscale, highres)

- Universities and Research Labs (color)

- desk-top AI (large memory, highres)

- high-performance server (with P2IO options)

- multi-user server (with P2IO options)

- network gateway (with P2IO options)


Price list items with estimated cost (2H86, unburdened) and list price


- Ferrari/C19	@\Color Display 19"	@\$3300	@\$12900

- Ferrari/C14	@\Color Display 14"	@\$2500	@\$9900

- Ferrari/G	@\Greyscale Display	@\$2500	@\$9900

- Ferrari/MX	@\Monochrome HighRes	@\$2200	@\$8900

- Ferrari/M	@\Monochrome Display	@\$2000	@\$7900

- Ferrari/S	@\Server (Nodisplay)	@\$1500	@\$5900

- IO Option	@\IO Expansion Board	@\$100	@\$490

- SCSI Option	@\SCSI IO-Module	@\$100	@\$490

- Ether Option	@\Ethernet IO-Module	@\$125	@\$490


Announcement Target: 1Q86


---

## Ferrari CPU Performance


Performance model is based on memory bandwidth.
The Sirius performance number assumes an average cache miss cost of 1 wait state.
Actual Sirius performance is highly application dependent.


```

------------------------------------------------------------------------------
CPU     CPU     32-bit  Wait    Effect.	Over-   Actual  Perf.   Comment
	Clock   Cycle   States  Cycle   head    Cycle
	[MHz]   [nsec]  [#]     [nsec]  [%]     [nsec]
------------------------------------------------------------------------------
80286   6.6     666     1       1000    0       1000    0.8     IBM PC/AT
80286   8.0     500     1       750     0       750     1.06    IBM PC/AT+

68010   10.0    800     0       800     0       800     1.0     Sun-2/CPU

68020   12.5    240     1       320     25%     400     2.0     LCWS/12.5
68020   14.6    204     1       272     20%     326     2.45    LCWS/15.6

68020   12.5    240     1.5     360     0       360     2.22    Carrera/12.5
68020   16.6    180     1.5     270     0       270     2.96    Carrera/16.6

68020   12.5    240     1       320     0       320     2.5     Ferrari/12.5
68020   16.6    180     1       240     0       240     3.33    Ferrari/16.6
68020   20.0    150     1       200     0       200     4.00    Ferrari/20.0

68020	20.0	150	1	200	0	200	4.00	Sirius/20.0
------------------------------------------------------------------------------

```


Performance Summary (Sun-2 = 1.0)

-

-
-

- IBM-PC/AT/6.6-MHz	@\0.8

- Sun-2/10-MHz		@\1.0

- LCWS/12.5 MHz		@\2.0

- Carrera/16.6 MHz	@\2.96

- Ferrari/16.6 MHz	@\3.33

- Ferrari/20.0 MHz	@\4.00

- Sirius/20.0 Mhz		@\4.00
-
-

Ferrari at 20.0 MHz:

-

-
- similar performance to Sirius

- 35% faster than Carrera at 16.6 MHz,

- 100% faster than LCWS at 12.5 MHz.

-

Ferrari at 16.6 MHz:

-

-
- 10% faster than Carrera at 16.6 MHz,

- 66% faster than LCWS at 12.5 MHz.

-


---

## Ferrari Graphics Performance


The following compares performance for five graphics primitive benchmarks.
The data is inner-loop time only, no higher-level overhead is included.
For all comparisions, the screen size is 1152*900 pixels.


The five benchmarks are:


Screen Clear: Fill entire screen with a constant pattern.

Screen Scroll: Scroll entire screen.

Screen Copy: Copy a full screenful from memory on screen.

Vector Draw: Average time to draw one pixel.

Character Paint: Time to draw one 16*8 pixel character.


Color/Greyscale Benchmarks:


```

------------------------------------------------------------------------
System		CPU	LWord	Screen	Screen	Screen	Vector	Char
		Clock	Cycle	Clear	Scroll	Copy	Draw	Paint
		[MHz]	[nsec]	[msec]	[msec]	[msec]	[usec]	[usec]
------------------------------------------------------------------------
Sun-2/color	10.0	800	45	107	666	5.0	170
Carrera/color	16.6	270	22	54	246	1.8	60
Ferrari/color	16.6	240	62	125	125	2.5	120
Ferrari/color	20.0	200	52	104	104	2.0	100
------------------------------------------------------------------------

```


Result for Ferrari at 20 MHz:

-


- screen clear/scroll about same speed as Sun-2, about 0.5 times Carrera

- screen copy is six times Sun-2, two times Carrera

- vector drawing is 2.5 times Sun-2, 0.9 times than Carrera

-

Monochrome Benchmarks:


```

------------------------------------------------------------------------
System		CPU	LWord	Screen	Screen	Screen	Vector	Char
		Clock	Cycle	Clear	Scroll	Image	Draw	Paint
		[MHz]	[nsec]	[msec]	[msec]	[msec]	[usec]	[usec]
------------------------------------------------------------------------
Sun-2/mono	10.0	800	52	104	104	5.0	170
Carrera/mono	16.6	270	21	21	21	1.8	60
Ferrari/mono	16.6	240	7.8	15.6	15.6	1.6	55
Ferrari/mono	20.0	200	6.5	13	13	1.3	40
------------------------------------------------------------------------

```


---

## Ferrari Transform Performance


Performance Model:

-


- 32-bit Floating Point

- 2d transform is 4 multiplications and 4 additions

- 3d transform is 12 multiplications and 12 additions

-


```

------------------------------------------------------------------------
		32bit+	32-bit*	2D	3D	2D	3D
		[usec]	[usec]	[usec]	[usec]	[#/sec]	[#/sec]
------------------------------------------------------------------------
Sun-2/software	80	80	640	1920	1562	520
Sun-2/SKYboard	25	25	200	600	5000	1666
68881-16MHz	3	3	25	130	40000	7692
FPA		1.25	1.25	10	16	100000	62500
GPI		1	1.0	8 	13	125000	76923
------------------------------------------------------------------------

```


68881-16MHz is one third of GPI for 2D and one tenth for 3D.

GPI has the added advantage of parallel processing
of graphics primitive generation and transforms.


---

## Ferrari Graphics Architecture


Ferrari has the following extensions for graphics:


- Pixel oriented color memory (1 or 2 megabyte)

- One byte of color memory is one pixel on screen

- Plane oriented monochrome memory (256 kilobytes)

- Monochrome video memory compatible with current monochrome

- Plane oriented overlay plane (256 kilobytes)

- Overlay plane determines if color or monochrome is displayed

- Color Map read/written directly by CPU during vertical retrace

- 2D/3D Transforms done in 68881

- No additional hardware support, no rasterop chips


---

## Ferrari Implementation


Package:

-


- M50 (2-slot VME) package (flat-top)

- slot 1 for CPU Board

- slot 2 for IO expansion (3 modules)

- minor modification to power supply required

-

Monitor:

-


- 14" color monitor: Hitachi HM4615-64KHz, 1152*900, packaged

- 19" color monitor: Hitachi HM4619-64KHz, 1152*900, same as today

- 19" greyscale monitor: Moniterm with analog board

- 19" high-res: under evaluation

-

Keyboard/Mouse:

-


- standard Sun-3 Keyboard/Mouse

-
