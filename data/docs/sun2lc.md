# sun2lc.mss

---
To:	Distribution
From:	Andy Bechtolsheim
Date:	August 1, 1983
Subj:	Low-Cost Sun-2


I think we need a lower-cost Sun-2 workstation.
Our current desk-top model was optimized for performance
and for expansion, rather than cost.
This resulted in a powerful system, yet also one
that is highly constrained in terms of space, power, and
manufacturability.

The goal of the low-cost Sun-2, or Sun-2/LC, or Sun-2/25,
is to optimize cost and manufacturability, rather than performance.
I think a lower cost Sun-2 is very important because:

* it will keep us competitive against lower-cost designs
* it reduces the entry cost of a Sun Workstation
* it is key for the educational/university market place
* it has potential for office automation applications
* it has potential for volume manufacturing

There are rumors of several companies attempting $5000 workstations,
including Pixel and TI.
I do not believe that we can achieve a $5000 workstation at this time,
based on our minimal system requirements. However, I think we can achieve
a workstation with 33% less cost than the current desk-top model,
making it a $7500 workstation.

This cost target is achieved simply be dropping features
and by using lower-cost components.
It does not involve any esoteric technologies such as custom LSI.
The main cost reduction is achieved in three ways:

   1) putting the frame buffer into main memory
   2) dropping the SCSI interface
   3) using cheaper video monitors, keyboards, and mice.

The strategy to arrive at the low-cost Sun-2 is to identify our minimal
system requirements and then to optimize the implementation for cost.
The following discusses an initial system specification.
To obtain realistic cost figures, a design based on these specifications
was done and its costs are listed in the appendix.

---
Sun-2/LC Minimal System Requirements:

1)  Sun-2 CPU and MMU

2)  1 or 2 MByte RAM (64K), or 2, 4 or 8 MByte RAM (256K)

3)  Ethernet interface

4)  keyboard/mouse interface

5)  2 serial lines with modem control


In detail:

1) The Sun-2/LC must be member of the Sun-2 family of workstations
   in order to be compatible with Sun-2 software. In addition, it appears that
   there are virtually no cost savings in not being a Sun-2 architecture.

2) The minimal memory our Unix system needs is 1 MByte.
   There is no cost in being upwards compatible with 256K RAMs.

3) The Sun-2/LC uses Ethernet as its primary interface mechanism
   to peripherals and services. This means that the Sun-2/LC is geared
   as a node for a network environment and always requires a fileserver.
   Not including alternate mass-storage interface is one of the key points
   in reducing the cost of the Sun-2/LC.

4) Plan is to use same serial keyboard/mouse interface we have now

5) These are for local options, such as hardcopy.

---
Sun-2/LC Non-Features

					Chips	Cost savings

1)	no separate frame buffer	35	$140

2)	no SCSI Interface		25	$60

3)	no expansion capability		20	$40

4)	no P1-Bus			15	$30

5)	no real-time-clock		5	$10

6)	no secondary serial		5	$20

7)	4-layer PCB instead of 6	-	$80

8)	autoinsertable layout		-	$20

			Total:			$400

In detail:


1) This saves the most chips and cost but also reduces performance.
   The degree of performance reduction depends on the video clock and resolution.
   For more information see the table under video monitors.
   Putting the frame buffer into main memory does not reduce
   the amount of main memory available since the separate frame buffer
   keeps a copy of the frame buffer in main memory as well.

2) Our current SCSI interface was designed for minimal chip count,
   but it still is expensive and power-hungry (20 Watts).
   Dropping SCSI saves second only to the frame buffer.

3) No expansion capability means that there are no connectors and
   there needs to be no spare power for expansion options, leading
   to surprisingly larger savings.

4) These are the chips it takes to interface to the P1 Bus.

5) Since this is a network node, it doesn't need a time-of-day clock.

6) The desktop Sun-2 has four serial lines. Two seem enough.

7) and 8) Reducing the chips by the numbers above and keeping the same size
   board results in a 4-layer PC board that is suitable for autoinsertion.

---
System Capabilities

The basic design seems able to cover three low-cost systems:

   1) a workstation with high-resolution black-and-white display
   2) a color workstation with 4 bit-planes
   3) a low-cost fileserver or peripheral server (microserver)

Video Capabilities

Putting the frame buffer into main memory gives complete flexibility
with screen resolution. The visible display area can be as large
as 512K, allowing displays such as 1024 by 1280 or 1280 by 1536.
Of course, video overhead goes up as display size increases.

I think the minimal spec should call for 768 by 512 pixels, non-interlaced.
A more desirable spec would be 832 by 612, non-interlaced, or 1024 by 800.
The highest spec I am thinking off is 1152 by 900, non-interlaced.
Other formats are fine, too, as long as they satisfy the following constraints:

    1) horizontal width is a multiple of 64
    2) horizontal to vertical ratio is approximately 4:3.

The table below gives estimates for the respective vertical, horizontal,
and video frequencies. The overhead for running the video out of main memory
is given, too, in percent of the processor performance for a 10 MHz CPU.

Spec		768 by 512	832 by 612	1024 by 768	1152 by 900
----------------------------------------------------------------------------
vertical freq	60 Hz		60 Hz		60 Hz		60 Hz
horizontal freq	32 kHz		38.25 kHz	48 kHz		56 kHz
video clock	32 MHz		40 MHz		64 MHz		80 MHz
video cycle	2 usec		1.6 usec	1.0 usec	0.8 usec
overhead	15 %		20 %		30 %		37.5%
----------------------------------------------------------------------------

Our experience with the Sun-2/50 indicates that 60 Hz refresh causes flicker
that is unacceptable for most users. Increasing the vertical frequency
from 60 Hz to 70 Hz or more increases all other values proportionally.


Color Capabilities

By adding a minimal amount of logic, the basic Sun-2/LC design can provide
a high-resolution color display with 4 bitplanes.
This is achieved by reading 512K banks of memory out in parallel.
Each 512K section provides one bit-plane, 2 MByte thus provide 4 bit planes.

The color display incurs the same overhead as the same resolution
black and white display. The added cost for color is almost entirely
in the color display monitor.


Fileserver Capabilities

By adding an ST506 interface chip and a Floppy or other backup interface,
the same basic design could perform the function of a low-cost server as well.
Our current SCSI interface is less suitable for this application because of
chipcount, power consumption, and cost of the host adaptors.

---
Implementation Considerations

Initially, the Sun2/LC can use the same packaging, video monitor,
keyboard, and mouse as the desktop Sun-2. To achive even further cost reduction,
the Sun-2/LC needs a lower cost video monitor, keyboard, mouse, and package.
Using a smaller video monitors such as 15" or 17", the Sun-2/LC
can be physically significantly smaller than the Sun-2/50,
making it more suitable for desk-top use.

Video Monitor:

This is a most crucial element for cost reduction.
Cost reduction of the video monitor is potentially as large
as all the electronics cost reduction combined.
Also, the specification of the lowest-cost high-quality video monitor
we can get will influence the decision on the resolution of the Sun-2/LC.

Keyboard:

The Sun-2/LC initially can use the current Sun-2 serial keyboard.
In the longer term, we need to find a lower-cost keyboard than Microswitch.
We should also reconsider how many optional keys are required,
since keyboards with fewer keys are cheaper and the overall keyboard is smaller.

Mouse:

Sun-2 serial mouse initially. Evaluate Xerox optical mouse.

Packaging:

The goals here are cost-reduction, too, as well as aesthetics.
Avoiding a fan for forced air cooling saves cost as well as noise.
The overall system should be easy to ship and easy to install by the user.

Ethernet:

A potential for cost reduction exists by incorporating the 3COM local transceiver.
This saves about $150 cost per Ethernet connection.

---
Design Partitioning/Electronics Cost Data

A very nice way to partition the Sun2/LC is to split it into two boards:
* CPU/0.5 MByte memory board
* 1.5 MByte memory expansion board

With 256K RAMs, these two boards become:
* CPU/2 MByte memory board
* 6 MByte memory expansion board

The following cost data is the electronics component cost only.
Additional savings for the Sun-2/LC result from 4-layer PC Boards
and reduced assembly work. These savings are estimated to be around $100.


		Sun-2/LC with 512K RAM

Total Estimated Cost:  608.70
Total Types of Parts:      89
Total Number of Parts:	    423
Total Number of Pins:	   4494
16-pin equivalents:	 280.88
Power Estimate:		8 Amp at 5V.

		Sun-2/LC 1.5 MByte RAM Expansion Board

Total Estimated Cost:  691.82
Total Types of Parts:      12
Total Number of Parts:	    478
Total Number of Pins:	   4225
16-pin equivalents:	 274.06
Power Estimate:		4 Amp at 5V.


Comparision between equivalent Sun-2/25 and /50, 1 MByte RAM each

		Sun-2/Model 25 (1 MB)	Sun-2/Model 50 (1 MB)

Total Estimated Cost:  824.70		1106.42		-25%
Total Types of Parts:      89		123		-27%
Total Number of Parts:	    495		740		-33%
Total Number of Pins:	   5646		8417		-33%
16-pin equivalents:	 352.88		526.06		-33%
Power Estimate:		9 Amp		17 Amp		-45%


Comparision between equivalent Sun-2/25 and /50, 2 MByte RAM each

		Sun-2/Model 25 (2 MB)	Sun-2/Model 50 (2 MB)

Total Estimated Cost:  1300.52		1561.00		-17%
16-pin equivalents:	 555		710		-22%
Power Estimate:		12 Amp		20 Amp		-40%
