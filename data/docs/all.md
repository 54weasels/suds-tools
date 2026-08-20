---


---


# Sun-2 System Specifications


Draft Version 1.0

Company Confidential

Sun Microsystems Inc.

[date]


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.

Sun and the combination of Sun with a numeric suffix are trademarks of
Sun Microsystems Inc. UNIX is a trademark of Bell Laboratories.


---


---

# Introduction


The Sun-2 is a family of high-performance workstations that feature
powerful local processing with 32-bit architecture and virtual memory,
high-resolution bitmap graphics, keyboard, and mouse interface,
and integral Ethernet networking interface.

The Sun-2 supports the Berkeley Unix(TM) 4.2 operating system,
supporting virtual memory, networking capabilities,
a high-performance filesystem, and a large number of utilities.
In addition, the Sun-2 version of the 4.2 system supports
multi-window capabilities, CORE graphics, and the ability
to run disk-less in a network environment.

The Sun-2 hardware is based on a 32-bit VLSI processor, the 68010,
extended with demand paging multiprocess virtual memory management.
Processes up to 16 MBytes of virtual memory are supported.
Main memory is at least one Megabyte and is expandable
to two or four Megabyte, depending on the model.

The display subsystem features 1152 by 900 pixel resolution on a 19" display
monitor that features 60 Hz non-interlaced refresh.
A special "RasterOp" or "Bitblt" processor performs
high-speed bit-map manipulation in hardware.

An Ethernet network interface, a SCSI disk interface,
and two or more serial lines are available for input/output.

The Sun-2 Workstation is initially available in three models.

The first, the model 50, is a desktop system in which the electronics is contained
on a single board in the base of the display. This system is primarily intended
as a disk-less node working in conjunction with a fileserver in a network
environment.

The second system, the model 120, combines the electronics with
an optional XX MByte 5.25" Winchester disk and 1/4" tape.
This system features an IEEE-796 system bus with a 9-slot
cardcage and a 5 Volt 60 Amp power supply for system expansion.
With its local mass-storage, the model 120 can be used for stand-alone
applications as well as a server for network configurations.

The third system, the model 170, is a 19" rackmount system also
based on the IEEE-796 Bus, featuring a 15-slot cardcage and a 5 Volt
100 Amp power supply. This configuration is primarily intended for
large servers that are equipped with large-capacity disk drives,
1/2" Tapes, and other peripherals.

Options available and expansion capabilities vary with the model.

The following specifications first describe the generic features
of the Sun-2 workstation family, followed by details on
the individual models.

---

# Sun-2 Specifications (All Models)


## Software


Berkeley Unix 4.2

all standard utilities

Disk-less Operation

Multiwindow System

SunCore Graphics

Languages: C, F77, Pascal

Extensive System Diagnostics


## Display


19 inch screen

Full-screen bit-mapped display

1152 by 900 dots resolution

60 Hz non-interlaced refresh

anti-glare screen


## Keyboard


Detached, standard typewriter-style

N-key rollover

Sculptured, non-glare keytops

Full ASCII character set

29 function keys

All keys programmable


## Mouse


Solid-state optical mouse

Maintenance-free

Three buttons


## Processor


32-bit VLSI CPU (10 Mhz 68010)

400 nanosecond instruction cycle (no wait state operation)

Multiprocess, demand paging virtual memory management

16 MBytes virtual memory space per process

1 Mbyte of main memory (minimum configuration)

Main memory expandable to 2 or 4 MByte (depending on model)

Parity error detection


## Graphics Subsystem


Dedicated, dual-ported frame buffer

High-speed RasterOp (Bitblt) Processor


## Network Interface


Standard 10 MBit/sec Ethernet interface

Highperformance VLSI controller


## SCSI Interface


High-performance SCSI interface

16-bit data transfers

Data is transferred directly to memory


## Serial I/O Interface


Two RS-423 serial I/O ports with full modem control

Full modem control and synchronous capabilities on two channels

Baud rates software-programmable.


## Other Features


Time of day clock with battery backup

Built-in speaker with software-controlled sound generator

Extensive diagnostic capabilities


## Physical Dimensions


Display Unit


Width:	18.5 in. (470 mm)

Depth:	15.5 in. (393 mm)

Height:	15.5 in. (393 mm)

Weight:	50 lb. (22 kg)


Keyboard Unit


Width:	21 in. (533 mm)

Depth:	7  in. (178 mm)

Height:	1  in. (25  mm)

Weight:	4  lb. (1.8 kg)


Base Unit


Width:	21    in. (533 mm)

Depth:	17.25 in. (438 mm)

Height:	3.625 in. (92  mm)

Weight:	24    lb. (11 kg)


## Phase In


CSA and VDE approval

DES encryption hardware and software


---

# Sun-2/Model 50 (Desk-Top System)


## Packaging


Desk-Top packaging, electronics is contained in base of display

Integral Ethernet and SCSI interface


## Expandibility


Memory is expandable from 1 MByte to 2 MByte

no Sun-supported SCSI devices available at this time


## Options


Additional 1 Mbyte main memory

2 additional serial channels (serial data only, no modem control)


## Power


115 or 220 VAC, customer switchable

48 to 68 Hz

300 Watt


## Environmental Requirements


Ambient temparature: 40 deg. F (5 deg. C) to 100 deg. F (38 deg. C)

Relative humidity: 0-80%, noncondensing


## Phase In


256K RAM version with up to 4 MByte memory


---

# Sun-2/Model 120 (Tower System)


## Packaging


Electronics and Mass-storage options are contained in a small package
  that can be put under or next to a desk (the "tower")

Display, Keyboard, and Mouse can be up to 15 feet from electronics package

System is based on IEEE-796 Bus and is designed for expandibility


## Expandibility


9-slot IEEE-796 Bus backplane

basic system requires 4 slots (processor, memory, video, ethernet)

350 Watt power supply (60 Amps at 5 Volt)

sufficient power for all configurations


## Options


Additional 1 Mbyte main memory, up to 3 expansion boards (3,F)

Additional 1 MByte Ethernet buffer memory (1,F)

Color display, 640*480*8, RS-170 (1,F)

Hardware Floating Point (1,F)

Quad RS423 Board (1,F)

SCSI with 5.25" Winchester Disk XX MByte unformatted

SCSI with 5.25" Winchester Disk and 1/4" Tape


## Physical Dimensions


Width:	9.25  in. (235 mm)

Depth:	21.625 in. (550 mm)

Height:	26 in. (660  mm)

Weight:	73 lb. (33 kg)


## Power


115 or 220 VAC, customer switchable

48 to 68 Hz

500 Watt


## Environmental Requirements


Ambient temparature: 40 deg. F (5 deg. C) to 100 deg. F (38 deg. C)

Relative humidity: 0-80%, noncondensing


## Phase In


High-performance SMD Disk Controller with SMD Disk Subsystem

1/2" Tape Controller with 1/2" Tape Subsystem


---

# Sun-2/Model 170 (19" Rackmount System)


## Packaging


Electronics and Mass-storage options are packaged in a 19" rackmount enclosure

Display, Keyboard, and Mouse can be up to 15 feet from electronics package

System is based on IEEE-796 Bus and is designed for expandibility


## Expandibility


15-slot IEEE-796 Bus backplane

basis system requires 4 slots (processor, memory, video, ethernet)

650 Watt power supply (100 Amps at 5 Volt)

sufficient power for all configurations


## Options


Additional 1 Mbyte main memory, up to 3 expansion boards (3,F)

Additional 1 MByte Ethernet buffer memory, up to 2 expansion boards (2,F)

Color display, 640*480*8, RS-170 (1,F)

Hardware Floating Point (1,F)

Quad RS423 Board (1,F)

SCSI with 5.25" Winchester Disk

SCSI with 5.25" Winchester Disk and 1/4" Tape

SMD Interface (1,F)

1/2" Tape Interface (1,F)

plus other options on current pricelist


## Physical Dimensions


Width:

Depth:

Height:

Weight:


## Power


115 or 220 VAC, customer switchable

48 to 68 Hz

1000 Watt


## Environmental Requirements


Ambient temparature: 40 deg. F (5 deg. C) to 100 deg. F (38 deg. C)

Relative humidity: 0-80%, noncondensing


---

# Network Configuration Rules


Sun-2 Workstations (Model 50, 120, and 170) can be interconnected
via the Ethernet into a clusters of Sun-2 workstations.
The following rules apply:


All nodes must be physically on the same Ethernet cable
(no repeaters or gateways between nodes)

It is recommended to make this a private Ethernet for use only by the
Sun workstation and fileservers in order to maintain performance.

A model 120 or 170 with mass-storage and standard Ethernet board
supports one other diskless node.

A model 120 or 170 with mass-storage and 1 MByte Ethernet buffer memory
supports up to 7 diskless nodes.

A model 170 with mass-storage and 2 MByte Ethernet buffer memory
supports up to 15 diskless nodes.
