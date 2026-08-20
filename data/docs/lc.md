---


---


# Low-Cost Sun Workstations


Company Confidential

Sun Microsystems Inc.

[date]


>


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.

Sun and the combination of Sun with a numeric suffix are trademarks of
Sun Microsystems Inc.


---


---

## Introduction


Sun needs a low-cost workstation.

Our current products, the Sun-2/120 and the Sun-2/50,
were optimized for performance and expandibility, rather than cost.
It is possible, with components available today, to design
a low-cost workstation with essentially the same functionality,
for a little over half the cost of the Sun-2/50.
The only difference of such a low-cost workstation to a Sun-2/50
is less display resolution, somewhat less performance, and no bus expandibility.
The only expansion offerered is memory expansion.

A first cut at the design of a low-cost workstation with a 68010 CPU,
Sun-2 MMU, 1 MByte RAM, video out of main memory, and integral Ethernet
resulted in a design with a chip count of 125 ICs.
The Sun-2/50 has a chip count of 416, and the Sun-2/120
has a chip count of over 500 for essentially the same functionality.

Comparing these numbers, we find that the low-cost workstation
is by a factor of 3 to 4 less material intensive than a 2/50 or 2/120.
We can also conclude that the low-cost workstation is by a similar factor
easier to design, easier to test, and easier to manufacture.

One way to visualize the size of a low-cost workstation is to realize
that the entire low-cost workstation has fewer chips than the
Sun-2 Multibus CPU Card!

The chip count of 125 for the low-cost workstation
was achieved with commercial, off-the shelf components.
By integrating logic functions into two gate arrays,
one for the video buffer and one for the MMU,
we can save another 40 chips reducing the total chip count to 85.
This number, with an allowance for the larger memory and the Ethernet interface,
matches the chipcount of Apple's MacIntosh computer.

This document summarizes my thoughts about Sun's low-cost
workstation products, about their architecture, components,
implementation, and specification.

---

## Goals


low-cost by design

acceptable performance

implements Sun-2 Architecture

high volume manufacturability


*Low-cost by design* means optimizing the design for minimal chip count,
using low-cost components, using gate-arrays for cost reduction,
while satifying all other goals.

*Acceptable performance* means 2/3 or 66% of a Sun-2/120.

*Implements Sun-2 Architecture* means conformance to
the Sun-2 Architecture specification, minimizing impact on software.

*High volume manufacturability* means absolute worst case design,
autoinsertable PCB, simple PCB design rules, and design for ATE.

---

## Products


The low-cost workstation family consists of three products:


A Black-and-White Workstation

A Color Workstation

A Server Node


The idea is to leverage the base design of the low-cost workstation
into three packages, possibly by sharing the same printed circuit boards.
A different package is required because the package itself is primarily
determined by the respective video monitor or by the presence of disks and tapes
in the server node.

From a design standpoint, the differences between these three products
is quite minor: The black-and-white workstation
has one bitplane of memory, the color workstation has four,
and the server node needs none, although the video refresh performs
the function of memory refresh.

The server node requires a SCSI interface for its disks, tapes and possibly
other input/output options such as serial lines or network gateways.
For the workstations, SCSI is an option, desirable for stand-alone
applications but not required for networked nodes.

In addition, there will be two generations of the base design:
The first based on the 68010 CPU, the second on the 68020 CPU.
The 68020 design will have better than twice the performance
of the 68010 designs.
Currently we expect volume availability of 68020s CPUs in Mid-85.

---

## Architecture


The following gives a brief overview of the architecture for
the low-cost workstations family.

The main characteristic of the low-cost workstation architecture
is that video is refreshed directly out of main memory, leading
to a the tight coupling between CPU, MMU, Memory, Video.
This tight coupling is required because video refresh out
of main memory is the major cost reduction over current designs.

When video is refreshed out of main memory, the memory
is not available for processor accesses during video refresh cycles.
The critical question in the design of the video refresh
is how much video refresh impacts processor performance.
This overhead depends on resolution, refresh rate,
and the length of the video refresh cycle.
We shall analyse this overhead in detail below.


### Display Resolution


Display resolution is programmable in the horizontal and vertical
state machines of the video controller.
The only constraints on display resolution are:


The horizontal width must be a multiple of 64 bits, and
should be a multiple of 128 bits

The ratio of vertical to horizontal resolution
must be between 0.7 and 0.8 to achieve square pixels.

The ratio of vertical to horizontal resolution
should be compatible with previous Sun workstations.


These constraints allow the following values:


1152*900

1024*800

896*700

768*600

640*500


---

## Components


### Chipcount


This section breaks down the 125 chip count estimate (M/C: Memory Controller).


CPU: 8
MMU: 26
I/O: 10
M/C: 18
RAM: 32
Vid: 30


### 68010


The part of choice is a 10 MHz 68010.
This part requires 150 nanosecond RAMs,
which is the lowest speed 256K RAMs typically offered,
and is directly compatible with the AMD/Mostek Ethernet interface.
There is very little cost saving in going to a slower 68010 CPU.


### MMU


The design uses the 55-nsec 4k-by-4 static RAMs.
These components are now available at low cost from many sources.


### 256K RAM


The choice is 256K RAMs with nibble mode to reduce video refresh overhead.
Most major manufacturers (Hitachi, Fujitsu, Motorola, and TI)
have announced 256K RAMs chips with compatible nibble mode.
We need to investigate when these and other parts will become available.
The design requires chips with 150 ns RAS access time and 75 ns CAS access
which is met by all announced parts.

The manufacturers and part numbers of 256K RAMs with nibble mode are:
Hitachi HM50257-15, Fujitsu MB81257-15, Motorola MCM6256-15, and Texas TMS4257-15.


### Ethernet


The low-cost workstation uses the AMD/Mostek Ethernet chip set
since we can't get enough Intel chips and because it is
easier to interface to the 68010.

An integrated Ethernet transceiver is essential to reduce cost
in the long run.


### Monitor


The issues are: availability, cost, and bandwidth.
The current Dotronix monitors with 50 Mhz video allow a resolution
of 896*700 at 60 Hz. For 1024*800 resolution, 64 MHz video is required.
Rumor is that there is a low-cost far-east monitor that achieves
the 1024*800 resolution.
Dotronix also is working on increasing the performance of their monitor.
I think that a 15" screen is fine.
I also think that interlaced monitors are out of consideration.

Before making the final choice on resolution, I think
we should identify a color monitor for the color workstation
capable of the same resolution as the black and white one.


### Keyboard


I think the current Sun-2 keyboard would be fine, except that it's
20" width is not form-factor compatible with a 15" display.
Microswitch offers an alternate low-profile keyboard with the
same technology that does not have the left, top, and right
function keys. Because it has fewer keys it is cheaper as well.

By maintaing the standard "Sun Keyboard Plug Interface" we can use
any keyboard that implements our protocol in case an OEM has
a specific keyboard requirement.


### Mouse


The current mice are fine.
We need to get volume on them to reduce their cost.


### Packaging


I think it is important that there be no fan in the low-cost workstation,
that there are no external cables between electronics and the display,
that the unit is easy to carry, easy to assemble, easy to ship.
It would be nice to have a similar package concept for the color version
of the workstation.

One idea is to package the low-cost workstation in a scaled-down
version of a Sun-2/50, but I am not sure this is easily achieved.
I think it is more important to optimize the low-cost workstation
for the required function and cost.
It seems a good concept is to package the electronics with the display,
using natural convection for cooling, avoiding external cables,
and being able to use one power supply for electronics and display.

Pieces: the electronics will occupy a PCB area of 80 square inches,
and there is a 20 sq.in. piggy-back board for memory expansion.
The maximum power consumed by the electronics is 10 Amps at 5 Volt or 50 Watts.


### Power Supply


A high-frequency switching power supply is essential to
reduce weight and cost. The requirement for the electronics
is estimated at 10 Amps at 5 Volt.


### Gatearray Strategy


Gatearrays are essential for implementing a SCSI interface;
a discrete SCSI implementation takes too many chips and too much
power to be compatible with the low-cost workstation philosophy.

The SCSI gatearray could also accomodate serial interfaces for
keyboard and mouse as well as timer functions and a real-time-clock
chip interface.

The video buffer portion lends itself to a gatearray implementation,
saving 20 chips for the black-and-white workstation and 80 for color.

The memory management logic can be put into a gatearray,
replacing about 20 IC packages as well.

Thus we have identified three opportunities for gatearray implementation.
We need to analyse each case in terms of its technology requirements
and in terms of cost-effectiveness. We should also make sure that
any gate array we develop is useable with a 68020 CPU as well.

In the meanwhile, I think, we should go ahead and build a "Phase I"
product without the use of gatearrays. This product will accept
a future "Phase II" PCB that contains the gatearrays without any
changes to the rest of the package. This allows us to decouple the
gatearray development from the rest of the product development and
allows us to phase the gatearrays in whenever they are ready.

---

## Specs


```


CPU:	68010, 10 MHz

MMU:	Sun-2 MMU

Memory:	1 Megabyte Main Memory (standard)
	1 or more Megabyte Expansion Memory (optional)

Ethernet:
	Integral Ethernet Transceiver

Display:
	15" display screen
	Resolution: 896 by 700 or 1024 by 800
	Refresh: 60 Hz non-interlaced or higher

Keyboard:
	Same serial interface as current keyboard.
	Form-factor compatible with display.
	Center Keyboard similar to current keyboard.
	Drop left/right/top function keys to reduce size.

Mouse:
	Same as current.

Package:
	Low-cost.
	Light weight.
	Easy to assemble, to ship, to install.
	No fan, no noise.
	Minimize plastic pieces and cables.
	Sun-2 family colors.


```
