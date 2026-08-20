---


---


# The Sun-2 Workstation Architecture


Flexible system architecture, based on 32-bit processor,
demand paged virtual memory, high-resolution bitmap graphics,
Ethernet networking, and Berkeley Unix 4.2 operating system
offers a high-performance, compatible family of engineering workstations.


Andreas Bechtolsheim, Sun Microsystems, Inc.


>

**Moving from Mainframes to Workstations.**
How 32-bit microprocessors are changing the way computers are used.

**The Sun Workstation: A Replacement for Superminis.**
Applications, features, and capabilities of the Sun Workstation.

**Diskless Operation.** The advantages and benefits of fileservers.

**The Sun-2 Architecture.** Family concept, planning for growth,
virtual memory architecture, MMU, virtual I/O, DVMA,
Graphics Architecture, 0-Wait State Performance, Diagnostics.

**Graphics.** The Sun-2 Network, The Sun-2 Architecture,
The Sun-2 MMU, The Sun-2 Family.


>
DVMA, Sun and the combination of Sun with a numeric suffix are trademarks of
Sun Microsystems Inc.
UNIX is a trademark of Bell Laboratories.
Multibus is a trademark of Intel Corporation.


---


---

#### Moving from Mainframes to Workstations


The arrival of 32-bit microprocessors marks a fundamental change
in computer systems. They are making the power of superminis
and small mainframes available at a fraction of the cost.

Previously, high-performance computers were so expensive
that amortizing their cost was a key issue. This was achieved
with timesharing, where each user gets a percentage of the machine in turn,
spreading the cost of an installation over a large base of simultaneous users.

However, timesharing has severe limits.
Because each user gets only a fraction of the CPU,
the amount of available computing power diminishes
rapidly as the number of users increases.

For the new generation of 32-bit microcomputers, the cost of the CPU
is too small to be worth the effort of sharing.
Now, the power of the computer can be used to maximize the productivity
of the individual using it.
Features such as high-resolution displays with multi-window environments
and graphic input, coupled with very fast response times,
previously considered too expensive in the context of a timeshared system,
are now becoming a requirement because they increase the productivity
of the ultimately most precious resource: the human being.

Dedicating mainframe processor power to a single user solves the processing
bottlenecks associated with timeshared systems. However, simply moving the
processor to the user does not constitute a transition
from timesharing to personal workstations.
The user of a dedicated workstation would be isolated if he
could not communicate with his fellow workers and access shared information.
To fully replace a timeshared computing environment,
a dedicated workstation system must also provide communication
and sharing capabilities equal to those of timeshared systems.

This requirement is achieved by interconnecting workstations
with local-area-networks, such as Ethernet,
and a operating system that provides network services.
In such a system the Ethernet effectively acts as an extended bus
between the workstations,
allowing workstations to exchange messages, such as computer mail, and to
access shared peripheral resources, such as fileservers and laserprinters.


---

#### The Sun Workstation: A Replacement for Superminis


The Sun family of workstations are general purpose workstations,
designed to support virtually any applications.
Today, Suns are used in such diverse applications
as CAD/CAM, typesetting, movie making, expert systems, and
many other engineering and scientific applications.

Based on a 32-bit VLSI microprocessor, the Motorola 68010, the
Sun-2 Workstation provides approximately 1 MIPS performance,
a demand paged virtual memory space of 16 MBytes,
physical memory of 1 to 4 MBytes, and a high-resolution bitmap graphics system.
For input/output, the Sun Workstation supports three standards:
the Ethernet local-area network, the SCSI system bus, and serial lines.

With the Berkeley 4.2 UNIX operating system,
the Sun Workstation supports a high-performance, distributed computing
environment that includes support for networking, graphics,
multiple windows, and a large number of languages and utilities.

The Sun Workstation features an advanced user interface consisting
of a multiwindow graphics output and a "mouse" pointing device for input.
With a resolution of 1152 by 900 dots on a 19" display monitor,
the Sun can display up to two pages of characters and graphics,
including variable width fonts, foreign alphabets, mathematical symbols,
vectors, curves, shaded regions, and even photographs.


#### Diskless Operation


In a typical installation, Sun Workstations are diskless,
interconnected by Ethernet, and share a common file-server.
This approach minimizes the cost of secondary storage
due to the economy of scale exhibited by mass storage devices.
At the same time, it centralizes the physical location of the disks
and the logistics of backup.

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

The key to successful operation of a disk-less environment
is high-performance networking software and hardware which makes
peripheral devices accessible as if they were directly connected to a workstation.
The Berkeley 4.2 bsd UNIX operating system
with its networking facilities has been adapted to the Sun Workstation
to link Sun Workstations, Sun Fileservers, and other vendor's hardware
into a single, unified, yet distributed system.


---

#### The Sun-2 Architecture


A major goal in the design of the Sun-2 workstation was to
develop an architecture that is compatible across
a family of workstations with different capabilities.
Because of this common architecture, current and future
members of the Sun-2 family are able to execute the same software
and can be intermixed in network installations.
This family concept is very important in preserving
the software investment on part of the workstation's users.

The Sun-2 architecture was designed to lend itself both
to high-performance and low-cost implementations,
to support Berkeley Unix, virtual memory, and bitmap graphics in an effective way,
and, last not least, to have a long useful lifetime.

The Sun-2 architecture specifies all objects
of the system that are accessible to user programs.
This includes the user-level instruction set of the 68010,
the Unix kernel calls and other services offered by the system,
and features such as the representation of bitmap rasters
in memory. In addition, the Sun-2 architecture defines a set
of utilities that are available to the system, including
the memory management unit and a standard set of input/output devices.

Because the Sun-2 is based on highly integrated
technology which is evolving quickly, we faced a challenge
in how to maintain architectural stability while allowing growth
in the underlying technology. The solution adopted was to provide layers
of compatibility similar to the layers of protection in an operating system.
This allows aspects of the Sun-2 system architecture, such as I/O devices,
to be extended over time as new technology becomes available.


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
Thus the performance of a given application will depend on the amount
of physical memory available.


#### Virtual I/O Architecture


The concept of virtual memory is applied in the Sun-2 architecture
to input/output as well.
All I/O devices are addressed with virtual addresses in an identical fashion
to virtual memory. Most I/O devices are individually mapped virtual objects
that can be mapped directly into a user's process space.
This allows user processes to have direct access to particular devices
without kernel overhead in a fully protected fashion.
In addition, certain devices that are not present in a particular
system configuration can be emulated by software if so desired.


#### DVMA: Direct Virtual Memory Access


Not only does the processor access I/O devices with virtual addresses,
but I/O devices with direct memory access use virtual addresses
as well to communicate with the rest of the system.
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

Rasters in the Sun-2 can be stored anywhere in main memory or in
video memory. The video memory appears as a part of main memory
to the CPU. Rasters in memory can be of any size and aspect ratio,
and are addressed directly with all CPU addressing modes.


#### Execution without Wait States


The performance goal of the Sun-2 architecture was
no-wait states execution. This means that the CPU performs
at its maximum speed, without being slowed down by a memory
system of insufficient performance.
Since every wait state reduces system performance by about 25%,
this was a key issue.
This performance goal drove both the architecture and the implementation
since no-wait state operation requires a very tight coupling
between CPU, memory management, and main memory.


#### Diagnostics


An important goal of the Sun-2 architecture
was to provide software diagnostic capabilities.
This was achieved by registers that have read-back capability,
a watchdog timer that restarts the CPU automatically should it ever halt,
and an 8-LED display for diagnostic messages.
These features allow power-up diagnostics to
verify correct machine operation before starting UNIX.

---

#### Box: Sun Workstation Network Architecture


In a typical installation, Sun Workstations are connected
via an Ethernet network to a fileserver.
The workstations themselves have no secondary storage.
The fileserver can provide other services as well, such as hardcopy
and communications.


![s1.press](../svg/s1.drw.O.svg)


*Figure: **Sun-2 Network Architecture***


---

#### Box: Sun-2 System Block Diagram


This block-diagram gives as overview of the Sun-2 system architecture.

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


*Figure: **Sun-2 System Architecture Block Diagram***


---

#### Box: The Sun-2 Memory Management Unit


Modelled after the memory management units of mainframe computers,
the Sun-2 Memory management unit (MMU)
provides address translation, protection, sharing,
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


---

#### Box: The Sun-2 Family


For now, the Sun-2 family include three models.
All models look identical to software and can be intermixed in networks.
Also, all models share the same ergonomical packaging for display,
keyboard, and mouse.

The first, the model 50, is a desktop system in which the electronics is contained
on a single board in the base of the display.  The only available option
on this system is memory expansion and floating point.
This system is most useful as a disk-less network node.

The second system, the model 120, puts the electronics into a deskside
pedestral unit. Featuring an Intel Multibus cardcage with 9 slots,
the system accomodates expansion boards and various options.
An optional 50 MByte 5.25" Winchester disk and 1/4" tape is available
for stand-alone applications.

The third system, the model 170, is a 19" rackmount system that
has a 15-slot Intel Multibus cardcarge, allowing ample room for expansion.
This configuration is typically used for fileservers
that are equipped with large-capacity disk drives, 1/2" Tapes,
and other peripherals.
