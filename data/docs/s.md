---


---


# The Sun-2 Workstation Architecture


Flexible system architecture, based on 32-bit processor,
demand paged virtual memory, high-resolution bitmap graphics,
Ethernet networking, and Berkeley Unix 4.2 operating system
offers a high-performance, compatible family of engineering workstations.


Andreas Bechtolsheim

V.P. Technology

Sun Microsystems, Inc.


>
DVMA, Sun and the combination of Sun with a numeric suffix are trademarks of
Sun Microsystems Inc.
UNIX is a trademark of Bell Laboratories.


---


---

# Introduction


#### Moving from Mainframes to Workstations


The arrival of 32-bit microprocessors is changing computer systems
in fundamental ways. The latest 32-bit VLSI CPUs compete in processor
power with a superminis and small mainframes of the recent past
at a fraction of the cost.
More aptly named micromainframes, 32-bit micros are revolutionizing
the way computers are being used.

Previously, high-performance computers
were so expensive that a key issue was how to amortize the cost of
their installation.
This has been achieved by the mechanism of timesharing,
whereby each user gets a percentage of the machine in turn,
spreading the cost of its installations over a large base
of simultaneous users.

The problem with timesharing is that each user only gets a fraction
of the CPU. In addition, every additional user
causes inefficiencies when the system switches between tasks.
Thus the amount of available compute power diminishes
rapidly as the number of users increases.
This makes timeshared computers difficult to use in compute-intensive,
interactive applications as they are found in engineering.

For the new generation of micromainframes, the cost of the computer
is too small to be worth the effort of sharing.
Instead, the power of the computer can be used to maximize the productivity
of the individual using it.
Features such as high-resolution displays with multi-window environments
and graphical input, coupled with very fast response times,
previously considered too expensive in the context of a timeshared system,
are now becoming highly desirable because they increase the productivity
of the ultimately most precious resource: the human being using the system.

Dedicating mainframe processor power to a single user solves the processing
bottlenecks associated with timeshared systems. However, moving the
processor to the user does not yet allow a transition
from timesharing to personal workstations.
The user of a dedicated workstation would be isolated if he
could not communicate with his fellow workers and access shared information.
To fully replace a timeshared computing environment,
a dedicated workstation system must also provide equivalent
communication and sharing capabilities previously available
only on timeshared systems.

This requirement is achieved by interconnecting workstations
with local-area-networks or LANs.
High bandwidth local-area-networks such as the Ethernet
effectively act as an extended system bus between the workstations,
allowing workstations to exchange messages such as computer mail and to
access shared peripheral resources such as fileservers and laserprinters.


---

#### Here Comes the Sun


The Sun Workstation is a new generation of workstations
specifically designed to meet the needs of engineers and scientists.
Sun Workstations are being used in such diverse applications
as CAD/CAM, typesetting, movie making, expert systems, and
many other engineering and R&D applications.

As a desk-top unit combining mainframe processing power,
high-resolution graphics display and Ethernet networking,
the Sun-2 Workstation dedicates a new level of computer capabilities at
the fingertips of the professional engineer.

Designed around a 32-bit VLSI microprocessor, the Motorola 68010, the
Sun-2 Workstation provides approximately 1 MIPS performance,
a demand paged virtual memory space of 16 MBytes,
physical memory of 1 to 4 MBytes, and a highperformance bitmap graphics system.
For input/output, the Sun Workstation supports three standards:
the Ethernet local-area network, the SCSI system bus, and high-speed serial lines.

With the Berkeley version of the UNIX(TM) operating system,
the Sun Workstation supports a high-performance, distributed computing
environment that includes support for networking, graphics,
multiple windows, and a large number of languages and utilities.

The Sun Workstation features an advanced user interface
that includes multiwindow high-resolution "bitmap" graphics capability
and a "mouse" pointing device for graphical input.
With a resolution of 1152 by 900 dots on a 19" display monitor,
the Sun Workstation can display up to two pages of characters and graphics,
including variable width fonts, foreign alphabets, mathematical symbols,
vectors, curves, shaded regions, and even photographs.


#### Diskless Operation


In a typical installation, a number of Sun Workstations,
interconnected by Ethernet, share a common file-server which
provides mass-storage for the workstations and other services such as hardcopy
The workstations themselves do not require any local secondary storage devices.


![s1.press](../svg/s1.drw.O.svg)


*Figure: **Sun-2 Network Architecture***


Due to the economy of scale exhibited by mass storage devices,
this approach minimizes the cost of secondary storage and
at the same time centralizes the physical location of the disks and
the logistics of backup.
Separating physical filestorage from logical access
means that files are accessible from anywhere in the network and are not
tied to any particular machine.
The same approach applies to other peripherals, such as printers, plotters,
and so on. These functions can be added to a cluster of workstations as
required and immediately become available to all users.

Decoupling peripherals from the workstations means that devices can be
located according to their function and that peripherals can be selected
to provide the best cost/performance for an entire computing installation
rather than for an individual workstation. In addition, it separates
the office environment of the workstations from the machine room environment
of the peripherals.

The key to successful operating in a disk-less environment
is high-performance networking software and hardware which makes
peripheral devices accessible as if they were directly connected to a workstation.
The Berkeley 4.2 bsd UNIX operating system (see article in July 26 Electronics)
with its networking facilities has been adopted to the Sun Workstation
to link Sun Workstations, Sun Fileservers, and even other vendor's hardware
into a single, unified, yet distributed system.


---

# The Sun-2 Architecture


A major goal in the design of the Sun-2 workstation was to
develop an architecture that is compatible across
a family of workstations with different capabilities.
Because of this common architecture, all current and future
members of the Sun-2 family are able to execute the same software
and can be intermixed in network installations.
This family concept is very important in preserving
the software investment on part of the workstation's users.

The Sun-2 architecture was designed to lend itself both
to high-performance and low-cost implementations,
to support Berkeley Unix, virtual memory, and bitmap graphics in an effective way,
and, last not least, to have a long useful lifetime.

The Sun-2 architecture specifies and standardizes all objects
of the system that are accessible to user programs.
This includes the user-level instruction set of the 68010,
the Unix kernel calls and other services offered by the system,
but also things such as the representation of bitmap rasters
in memory. In addition, the Sun-2 architecture defines a set
of utilities that are available to the system, including
the memory management unit and a standard set of input/output devices.

Due to the fact that the Sun-2 is based on highly integrated
technology which is evolving quickly, we faced a surprising challenge
in how to maintain architectural stability when the underlying
technology changes. The solution adopted was to provide layers
of compatibility similar to the layers of protection in an operating system.
This allows aspects of the Sun-2 system architecture, such as I/O devices,
to change in future implementations. It allows the architecture
to be extended over time as new technology becomes available.

In the following, aspects of the Sun-2 architecture
will be discussed including an overall system block diagram,
the virtual memory architecture,
the input/output architecture, and the graphics architecture.


---

#### Sun-2 System Block Diagram


On the left side are the devices that generate virtual addresses:
the CPU and I/O Controllers with direct memory access such as the
Ethernet interface and the SCSI interface.

In the center is the memory management unit that translates
the virtual addresses into physical addresses and fulfills
the functions of protection, sharing, and resource allocation.

On the right side is main memory, the display memory or frame buffer
which is part of main memory, all input/output devices,
and an interface to a backplane system bus if one is present.


![s2.press](../svg/s2.drw.O.svg)


*Figure: **Sun-2 System Architecture***


---

#### Virtual Memory Architecture


The Sun-2 virtual memory architecture was specifically designed to support
the virtual memory and demand paging environment which is essential for
engineering, CAD/CAM, and expert systems applications.

Virtual memory, pioneered by the mainframes of the late '60s and early '70s,
allows user programs larger than physical memory.
This is accomplished by a storage hierarchy in which the virtual image
of a program is stored in secondary storage and main memory only
stores those program pieces that are in active use.

In paged virtual memory schemes memory is divided up into equal size "pages",
mapping each page of virtual memory separately into a page
of physical memory. Active pages are brought in from secondary storage
on demand (demand paging), replacing pages resident in main memory
that are no longer active. The page replacement algorithm
typically utilizes statistical information maintained in hardware
about which pages have not been accessed recently.

A big advantage of virtual memory is that an application does not
have to be aware of how much physical memory the underlying machine has.
Of course, performance will degrade if there is insufficient physical memory
to contain the active pieces of the program (the working set) at one time.
Exactly how well a given application will perform with a given amount
of physical memory is very difficult to predict. The Sun-2 architecture
provides a set of performance measurement tools in hardware to assist
in real-time performance analysis of user and system tasks.


#### Memory Management Unit


Modelled after the memory management units of mainframe computers,
the Sun-2 MMU provides address translation, protection, sharing,
and memory allocation for a multiprocess operating system.


![s3.press](../svg/s3.drw.O.svg)


*Figure: **Sun-2 Memory Management***


The Sun-2 MMU uses a two-level segment/page address translation.
The purpose of the segment map is to translate the 24-bit virtual address
emitted by the CPU into an intermediate address which is then translated
via the page map into a physical memory address.

Protection is associated with the page map; each page entry
can specify read, write, and execute access capabilities both
for the supervisor and user.
Two statistics bits, accessed and modified, are automatically
maintained for each page to assist in page replacement algorithms.

Rapid switching between multiple processes and between system and
user tasks is accomplished via the context register.
The context register selects one of 8 sections of the
segment map and thus can immediately switch among up to 8 simultaneously
mapped processes of up to 16 MBytes each.
Of course, the total number of processes in a system can be
much larger than 16 and is not limited. The tables for
currently not mapped processes are stored in main memory.


#### Virtual I/O Architecture


The concept of virtual memory is applied in the Sun-2 architecture
to input/output as well.
All I/O devices are addressed with virtual addresses in an identical fashion
to virtual memory. Most I/O devices are individually mapped virtual objects
that can be mapped directly into a user's process space.
(certain system resources are only available to the system).
This allows user processes to have direct access to particular devices
without kernel overhead in a fully protected fashion.
In addition, certain devices that are not present in a particular
system configuration can be emulated by software if so desired.


#### DVMA: Direct Virtual Memory Access


Not only does the processor access I/O devices with virtual addresses,
but I/O devices with direct memory access use virtual addresses
as well to communicate with the rest of the system, instead of
accessing physical memory directly.
All data transfers between an I/O device and physical memory
are performed with "direct virtual memory access", or DVMA,
using the same virtual address translation as the processor itself.
This maintains a fully protected system environment and means
that all accesses in the system are mapped and protected in an identical fashion,
avoiding the dual mapping problems with conventional direct memory access devices.


#### Graphics Architecture


The Sun-2 architecture defines two aspects of graphics:
the representation of rasters or bitmaps in memory and the
basic operations for manipulating these rasters.

The Sun-2 graphics architecture is based on the "RasterOp" principle.
RasterOp, also called BitBlt for Bit Block Transfer,
means that rectangular areas of display data ("raster")
are modified or combined according to a preselected operation ("Op").
This concept originated in the early history of the Xerox Smalltalk
language in an attempt to unify the treatment of text and graphics
in bitmap displays.
The RasterOp function provides complete generality to paint characters,
manipulate windows, scroll screens, and to draw vectors.

Rasters in the Sun-2 can be stored anywhere in main memory or the
frame buffer. The frame buffer appears as a part of main memory
to the system. Rasters in memory can be any size and aspect ratio,
and are addressed directly with all CPU addressing modes.

To implement RasterOps at high speed, the Sun Workstation includes
a special rasterOp processor which performs
the actual level raster manipulation in hardware.
This processor is implemented as a custom-designed single-chip
NMOS component and includes all the shift and function units
required for raster data manipulation (*** see box ***).


#### Box: A single-chip RasterOp Processor


This component, which was developed in collaboration between
Sun Microsystems Inc and Silicon Compilers Inc, performes
the functions required for the inner loop of the Raster Operation.


![s4.press](../svg/s4.drw.O.svg)


*Figure: **Sun-2 RasterOp Processor***


The chip is a data-flow device. It is only concerned with
data manipulation, not addressing.
Addressing of the raster is performed by the 68010 CPU.

The chip performs arbitrary boolean combination functions between
source data (new data to be stored in a raster) and destination data
(the data already existing in the frame buffer).
The source data passes through a combinatorial shifter that shifts
the data by a preselected amount before it is combined with the
destination data.

A separate masking unit allows to deal with the boundary conditions
at the right and left border of the raster.

---

# Implementation Issues


#### Box: The Sun-2 Family


The initial family members of the Sun-2 architecture include three models.
All models look identical to software and can be intermixed in networks.
Also, all models share the same ergonomical packaging for display,
keyboard, and mouse.

The first, the model 50, is a desktop system in which the electronics is contained
on a single board in the base of the display. This system is primarily intended
as a disk-less node working in conjunction with a fileserver in a network
environment.

The second system, the model 120, combines the electronics with
an optional 50 MByte 5.25" Winchester disk and 1/4" tape.
This system features an IEEE-796 system bus with a 9-slot
cardcage and a 5 Volt 60 Amp power supply for system expansion.
With its local mass-storage, the model 120 can be used for stand-alone
applications as well as a server for network configurations.

The third system, the model 170, is a 19" rackmount system also
based on the IEEE-796 Bus, featuring a 15-slot cardcage and a 5 Volt
100 Amp power supply. This configuration is primarily intended for
servers that are equipped with large-capacity disk drives,
1/2" Tapes, and other peripherals.

Options available and expansion capabilities vary with the model.
All systems allow memory expansion to 2 or 4 MBytes.
On the IEEE-796 based systems, options include color displays,
high-performance SMD disk drives, and 1/2" Tape controllers.


#### The Single-Board Machine


In the design of the bus-organized models of the Sun-2 family,
the Model 120 and 170, the goals were high-performance and expandibility.
For the single-board machine, the Model 50, the design challenge
was to maintain the same level of performance while squeezing the
workstation design on a single printed circuit board measuring 14.44" by 15.75".

This was achieved by maximizing the usage of LSI and VLSI components,
including a custom designed NMOS circuit for raster graphics processing
and extensive use of programmable logic such as PROMs and PALs.
More than half of all chips are LSI or VLSI circuits,
with MSI components (medium scale integration) accounting for one third
and SSI (small scale integration) for the rest.
The table below summarizes the actual numbers.


```

-------------------------------------------------------
Technology	# of components		# of 16-pin eq.
-------------------------------------------------------

LSI		208	54%		236	55%
MSI		129	33%		150	35%
SSI 		48	13%		42	10%
		-----------		-----------
Total:		385	100%		428	100%
-------------------------------------------------------

```


The picture below shows the floorplan of the single board PC layout,
identifying the major building blocks and the connectors.
Great care was taking in partitioning the design and the placement
of the components in order to make the board routable by an automatic
PCB layout system.


![s5.press](../svg/s5.drw.O.svg)


*Figure: **Sun-2 Single Board Floorplan***


---

#### Maximizing Performance


The performance goal of the Sun-2 Workstation was to maximize the
compute power delivered from its CPU, the 68010.
This goal was achieved in several ways.

The most important one is a tight coupling between CPU, memory management,
and main memory, allowing the CPU to execute without wait states.
(This topic is discussed in more detail below).
The next important one is a dedicated,
dual-ported frame buffer for the video refresh such that video
does not impact processor performance. This is especially critical
given the high bandwidth of video refresh (approaching 100 Mbit/second).
Finally, performance for certain functions is increased by dedicating hardware
for these functions, such as in the case of the RasterOp processor.


#### Execution without Wait States


Since every wait state reduces system performance by about 25%,
a major system goal of the Sun Workstation implementation was to
allow CPU operation without wait states.

Wait states result when processors synchronize with slower memories. In brief,
the CPU has a certain time allowance from sending out a valid memory address
until data needs to be returined to continue with the processor cycle.
If the CPU sends out an address to memory and the
memory does not respond within the allowed time window of the processor,
the processor has no choice but waiting for memory response, resulting
in so-called wait states. For the 10 MHz 68010, the time allowed
from sending out address strobe until valid data is required
is only about 180 nanoseconds.

In a virtual memory architecture, the available memory access time is
further decreased by the time required for address translation,
since the virtual address generated by the processor first needs
to be translated by the memory management unit before main memory
can be accessed. In the two-level memory management of the Sun workstation,
the situation is even more time-consuming because two tables need to be looked
up sequentially before a valid physical address is obtained.

The Sun workstation achieves no-wait state access to memory by using very
high-speed RAMs for the address translation buffers and by using a
private, high-speed memory bus between the processor and main memory.
This socalled P2 memory bus features data lines with byte parity
and high-speed synchronous operation.

In those implementations of the Sun Workstation that feature a standard
backplane bus such as the IEEE-796 Bus, this bus is used as input/output bus
for connecting the processor with its peripherals and expansion options.
Devices on this bus have direct access to main memory via DVMA.


#### Diagnostics


An important design goal in the Sun-2 were software diagnostic capabilities
to allow extensive power-up diagnostics to be run every time the machine
is being turned on or idling.
Emphasis was put on having read-back capability for most registers,
which also makes them easier to use by software.
Another feature is a watchdog timer reset capability that
restarts the CPU should it ever halt.
An 8-LED display panel on the back of the machine is provided
for error messages.
