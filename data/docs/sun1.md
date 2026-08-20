---


# The SUN Workstation Architecture


# SUN Microsystems, Inc.


# July 1982


---


---

#### Introduction


SUN's goal for the 1980's is to offer a solution to the
general-purpose distributed computing environment. SUN is
offering a network system able to support such diverse applications as
computer-aided-design, manufacturing, engineering, and robotics, as well as
the graphics arts, typesetting, office automation, and executive administration.

SUN's network system is based on the SUN Workstation,
a powerful graphics computer tool designed to enhance
the productivity of an individual.
The SUN Workstation features an advanced user interface
that includes high-resolution "bitmap" graphics capability,
a "mouse" pointing device for graphical input,
a powerful processor based on state-of-the-art VLSI technology,
and an integral "Ethernet" local area network connection.

The display has 1024 by 800 pixel resolution and can show two pages
of characters and graphics, including variable width fonts,
foreign alphabets, mathematical symbols, vectors, curves, shaded regions,
and even photographs.
The processor is based on the Motorola 68000/68010 CPU, extended
with virtual memory management hardware.
The Ethernet connection allows SUN Workstations to share resources
and to access such services as electronic mail, file storage, and printing.

The key to SUN's network system is a standardized operating system
and networking software that allows SUN Workstations,
SUN peripherals, and even other vendors' equipment
to work together coherently and efficiently.
The SUN UNIX operating system
is based on the Berkeley 4.2bsd version of UNIX
and the ARPA IP/TCP protocols.
This means that the SUN network system will support the same software
that has been proven in hundreds of research installations
and is emerging as an industry standard.


![Placeholder: works3.press]()


*Figure: **A SUN Workstation Cluster***

<a id="SUN Workstation Cluster"></a>


One of the most important features of the SUN UNIX operating system
that it will allow SUN Workstations to execute
the Berkeley 4.2bsd operating system without requiring local disk storage,
accessing programs and files over the network.
To this end, SUN Workstations are organized
into SUN Clusters that are interconnected by a local, or private, Ethernet.

Figure [Figure](#SUN Workstation Cluster) shows
a typical SUN Cluster consisting of a number of SUN Workstations
and a SUN Fileserver connected to a local Ethernet.
The fileserver in turn is connected to other networks,
acting as a gateway between the local Ethernet and the remote networks.
The SUN Fileserver provides the UNIX file system and other functions
such as backup and printer services to the local network.


---

#### Design Rationale


The architecture of the 70's is not well-matched to the hardware of the 80's.
Powerful large-memory processors suited to a broad spectrum of applications
are becoming too cheap to be worth the effort of timesharing.
High-speed local networks permit mass storage, printers, special-purpose
processors, communications interfaces, and other resources to be located and
shared for optimal cost and speed of access.  High resolution high
performance displays previously hardly affordable are
becoming available to the ordinary user, presenting new opportunities for
effective user interfaces in such areas as document preparation, software
development, computer-aided design, and information management.

In todays designs, the qualitative depends heavily on the quantitative.
State of the art VLSI technology provides single chip CPUs with the power
of traditional mainframes and minicomputers.
It becomes difficult to justify buying a conventional mainframe,
allocating basement space for it, and pulling terminal cables
throughout the building, when for less money one can buy
30 computers and put them on the desks of their users.

The computer-per-desk model would of course be flawed if large, noisy,
and expensive peripherals had to go on the desk beside the computer.
This is where the network comes in. All the traditional peripheral
functions and services of a computing environment can be distributed
over the network, sharing resources for optimal cost,
replicating services where needed for performance and reliability reasons.

Thanks to the speed of today's networks, it has become
feasible to interpose a network between the computer and its disk drive.
A user should notice no performance difference between accessing a remote disk
via the network versus accessing a local disk, provided that the network disk
is not overloaded with other tasks.

Another parameter that affects design qualitatively is the display.
A high-resolution, high-speed display, which can show a full page of text
and images virtually instantaneously, provides a new and powerful
user interface capability and new alternatives for many tasks.
An example is a multi-window system in which the display represents
a working table with windows corresponding to pieces of paper,
each one connected to a particular task.
Such a system replaces the need for multiple terminals on a desk and
allows the user to control multiple tasks in parallel.

---

#### SUN Workstation Software


The operating system for the SUN Workstation is an advanced
version of the UNIX system.  UNIX, developed at Bell Laboratories,
is the emerging standard operating system for 16 and 32 bit machines,
and is being adopted for use by many manufacturers.
Factors contributing to this include the avoidance of assembly language
throughout the operating system, care in the structuring of data and control
in the system implementation, a rational balance between system complexity
and extent of functionality offered, and a high degree of portability between
machines.

The UNIX system which is supported for the SUN, 4.2bsd, is a significantly
enhanced version of the operating system.
It was developed at the University of California at Berkeley
to be a standard system for use in the ARPA research community
on the Digital Equipment VAX computer family.
The ARPA standard system is the most advanced version of UNIX available,
supporting such features as virtual memory, networking and remote filesystems.

The systems of the 1980's will be integrated using networking technology, and
will rely on common network protocols to communicate and share peripherals
among these systems.  The 4.2bsd version of UNIX provides a flexible and
efficient networking subsystem, permitting access to local and long-haul
communications networks.  The networking facilities allow SUN Workstations to
be placed in a SUN Cluster and to share disks, tapes, printers, and
other resources available through the network, providing a lower
per-workstation cost by centralizing those peripherals which have economy of
scale.  Standardized protocols for accessing devices over networks are just
emerging, and the flexible networking subsystem supported by 4.2bsd will
allow SUN to use new standards as they emerge.

The virtual memory support in 4.2bsd adapted UNIX to take advantage
of 32-bit architectures and to support applications previously only
feasible on expensive mainframes.
4.2bsd's new file system corrects the most noticeable shortcomings of the
original UNIX file system, substantially enhancing both its performance and
its robustness.
On the networking side 4.2bsd offers a full range of networking protocols,
from the Ethernet interface drivers through such datagram and stream protocols
as DOD's Internet Protocol (IP) and Transmission Control Protocol (TCP) up to
service software for mail, telnet, and net-transparent file operations.

4.2bsd UNIX has good tools for software development and text processing.
For software development these include the display editors Emacs and Vi, a
compiler and both low-level and high-level debuggers for C, and additional
language support for Fortran and Pascal, with anticipated support for Lisp
and Ada in the future.  For text processing there are the above-mentioned
editors, along with several text formatters, a spelling aid, and
a number of other UNIX text-processing utilities that work very effectively
as a combination.

The SUN 4.2bsd UNIX has all the drivers and other software
necessary to take full advantage of the SUN Workstation hardware.
Most importantly, the SUN 4.2bsd operating system can execute
without local disk, loading programs and accessing files over the network
via a remote SUN Fileserver.

On the graphics side, the SUN UNIX operating system
includes low-level support for vectors, region-filling, window
management, and pointing devices, along with an extensive library of
engineering graphics software for both monochrome and color graphics displays.
This library of engineering graphics software (LEGS)
is an implementation of the ACM CORE graphics specification plus
extensions.  The CORE is implemented for basic two-dimensional and
three-dimensional operations with segmentation.
Extensions to the CORE include textured polygon fill algorithms, quadratic
and cubic curve drawing, extended vector and matrix operations,
shaded surface polygon rendering and bicubic patch drawing with selectable
texture mapping and hidden surface elimination.
A "mouse" pointing device is supported for graphical input.

---

#### SUN Workstation Hardware


The SUN Workstation is divided into three basic components:
the processor, the graphics, and the Ethernet subsystem.
In addition, a color graphics subsystem is available as an option.
Each one of these subsystems is implemented as a single board
electrically and mechanically compatible with the
IEEE-796 Bus or Intel Multibus. The choice of the
Intel Multibus makes the SUN Workstation compatible
with the board-level products of over 100 board and system manufacturers.

A basic SUN Workstation consists just of these three board types.
When an application requires, a basic SUN Workstation can be enhanced with
additional capabilities, such as the SUN color graphics option,
SUN expansion memory, or other input/output options.


---

#### SUN Processor Board


The SUN Processor board is the main component of the SUN Workstation.
It combines a 10 MHz 68000/68010, virtual memory management,
256k bytes of main memory, and input/output
on a single board compatible with the IEEE 796 Bus.
On-board memory is expandable with the SUN 768K Memory expansion board
to 1M bytes (one expansion board) or 1.768 MByte (two expansion boards).
The expansion memory communicates with the main processor over a private,
high-speed bus connected via the 796-P2 connector.
A typical system is expected to have 1 MByte.
All memory is equipped with parity error detection.
The SUN 68000 processor operates at 10 MHz without wait states.

On-board input/output includes two high-speed programmable serial channels,
a 16-bit input port for configuration control,
and five 16-bit timers.  One of the timers can be configured as watch-dog timer
for auto-reload in remote applications.

**SUN Memory Management**

The SUN Memory Management Unit has been specifically designed to support
the UNIX multitasking operating system. The SUN memory management
provides address translation, protection, sharing, and
memory allocation for a multiprocess environment.
All accesses of the processor to on-board RAM memory, 796-Bus memory, and
796-Bus I/O space are translated and protected in an identical fashion.
Further, the SUN memory management provides
all the necessary mechanism for demand paging and virtual memory
for the 68010 virtual memory processor.

The memory management consists of a context register, a segment map,
and a page map.  Virtual addresses from the 68000 are translated
into intermediate addresses by the segment map and then into physical addresses
by the page map.
The organization of the memory management system is shown in Figure
[Figure](#SUN Memory Managament) below.

The page size is 2K bytes, the segment size is 32K bytes,
and up to 16 contexts can be mapped concurrently.
The maximum logical address space for a context on the SUN 68000 board
is 1024 pages or 2M bytes.
A total of 8M bytes can be addressed from the page map, however,
the maximum physical address space that can be mapped simultaneously is 2M bytes.


![Placeholder: 680002.press]()


*Figure: **The SUN 68000 Memory Management***

<a id="SUN Memory Managament"></a>


The context register is a four-bit register, accessible only in system state,
that can switch to any of the 16 sections of the segment map with
one 68000 move instruction.  This permits 16 contexts to be mapped
concurrently; more than 16 contexts can be handled by treating the segment
map as a context cache, replacing out-of-date contexts on a
least-recently-used or other basis.
Each context has its own virtual address space.
Sharing and intercontext communication may be implemented at either the segment
or page level.

Protection is associated with the segment map; each segment
has a protection code permitting one of 16 classes of access modes
allowing read, write, and/or execute cycles in supervisor and user states.

The page map handles paging and the allocation of physical memory.
A page map entry also indicates the physical address space in which a page is
located, such as on-board or off-board memory.
Further, the page map assists demand paging algorithms by maintaining
reference and modified bits for each page.

The organization of the memory management in conjunction with the page control bits
provides all the necessary mechanisms to implement demand paging and virtual memory.
If either the segment map or the page map indicates an invalid segment
or page during translation, the MMU will send a bus error signal to the
processor.  The operating system will then check whether the access was in
error or whether the fault was due to a missing page. In the latter case,
the missing page needs to be loaded into main memory.
If all physical pages are in use, a page must be replaced.

Full virtual memory capability is possible with the 68010 processor,
the virtual-memory version of the 68000.
The original 68000 processor cannot fully
recover from page faults because it does not save
sufficient state information to continue an aborted instruction.
SUN Processor boards equipped with the 68000 processor can be
retrofitted for the 68010 processor if full virtual memory is desired.


---

#### SUN Black&White Graphics Board


The SUN Graphics Subsystem combines a high-resolution display memory
of more than 1 Million Bits (1024 by 1024) with a high-speed
"RasterOp" update mechanism that allows screen clear in 50 milliseconds.

The stored image is displayed on a 17" landscape video monitor.
800 lines by 1024 pixels are actually displayed;
the remaining 224 by 1024 pixels are invisible and can be used to
store characters, cursors, and other graphical symbols.

The frame buffer is implemented as a special dual-port memory.
One port is dedicated to video refresh while the other port permits the frame
buffer to be updated.  In addition to the frame buffer memory, the SUN
graphics board provides the video refresh logic and special hardware to
assist in frame buffer updates.  Updates are performed by the special
hardware under control of the main 68000 processor at a rate of up to
32 MBit/sec (one read-modify-write cycle on a 16-bit operand per microsecond).

**RasterOp Architecture**

The SUN Graphics system incorporates the concept of "RasterOp".
RasterOp means that rectangular areas of display data ("Raster")
are modified or combined according to a preselected operation ("Op").
The RasterOp function provides complete generality to paint characters,
manipulate windows, scroll screens, and to draw vectors.
An example of RasterOp is shown in Figure [Figure](#SUN RasterOP),
in which source characters are copied to a destination in the frame buffer.


![Placeholder: graph0.press]()


*Figure: **A RasterOp Operation***

<a id="SUN RasterOP"></a>


---


RasterOp grew out of an attempt to unify the treatment of text and
bitmap graphics in the early history of the Xerox Smalltalk language.
It was then implemented on the Xerox Alto computer
as a microcoded instruction called BitBlt,
for Bit Boundary Block Transfer.
The Alto BitBlt instruction provides 8 Boolean functions
each combining a source raster with a destination.

The SUN graphics system implements a generalized version of RasterOP,
allowing one, two, or three operands which are referred to as
destination, source, and mask operand.
Any one of the 256 possible ternary Boolean functions on these
three operands can be selected.

The destination is the operand being changed in the frame buffer,
the source is an operand to be combined with the destination,
and the mask is a 16-bit pattern, aligned with the background,
that is also combined with source and destination.
Both source and mask operands can be loaded either from the frame buffer
or from main memory.

Other graphic functions such as vector drawing, text, cursors,
and multiple windows are provided for by software using the
basic RasterOp mechanism.

**Hardware/Software Interface**

RasterOps are implemented by the SUN graphics system through
a combination of hardware and software.
In brief, the hardware supports a one by 16-pixel RasterOp primitive
that can manipulate any row of consecutive pixels in the frame buffer.
This hardware primitive is applied under software control to perform
RasterOps on larger areas.
Variable width fonts may be conveniently handled by setting
a length register to the width of the character, causing the
operation to be performed only on the width of the raster indicated.

Notice that the graphics hardware does not incorporate anything
like a microcoded graphics processor.
Algorithmic control of the particular graphics operation,
such as manipulating rectangles or drawing vectors,
resides with the main workstation processor, making the SUN graphics
system completely user programmable.

The SUN graphics system has been optimized for an efficient interface
between processor and frame buffer by incorporating sufficient
registers to hold all state information relating to a particular raster
operation. This allows raster operations to proceed at full speed without
having to reload critical state information.

**Performance**

The speed of graphics operations is set both by hardware and software.
Rectangular area manipulation is performed at the rate of 16 pixels
per microsecond, filling the visible screen in 48 milliseconds.
Scrolling involves two accesses to the frame buffer,
thus a full-screen scroll takes 96 milliseconds.
A 16 by 16 pixel character can be written in 20 microseconds;
at this rate the visible screen is filled with characters in 64
milliseconds (excluding higher level overhead).
Arbitrary vectors are drawn at a rate of about three microseconds per pixel,
with orthogonal vectors drawn at one microsecond per pixel.

---

#### SUN Color Graphics Board


The SUN Color Graphics Subsystem features a display of
640 by 480 pixels with eight bits per pixel.
Up to three color boards can be stacked offering 24 bits per pixel.
A standard RS170 interface allows the SUN Color board to drive
any standard color monitor. An external sync option is available.

With 8 bits per pixel, the SUN color board can display 256 colors
at a time. In addition, there is a color lookup table that
translates the 8-bit pixels into 24-bits, with 8 bits each
defining the intensities of the red, green, and blue components.
Thus the board can generate over 16 Million different colors from a
palette of 256 simultaneous colors.

The color map is divided into four separate sections.
One of the sections is used for the display while another section
can be updated under software control. The section used for the
display can be switched to another section with one command.

The architecture of the SUN Color Graphics board is very similar
to the SUN black&white graphics board. As in the latter,
the color frame buffer is implemented as a dual-port memory
with one port dedicated to video refresh
and the other port permitting processor access.
Also, the color frame buffer is (x,y) addressable from the Multibus and
is equipped with special "RasterOp" hardware for fast display updates.
The RasterOp hardware executes any boolean combination function between
the new pixel value, the old pixel value, and a constant "color" register.

Pixels can be updated in less than 1 microseconds,
allowing image updates and vector drawing at speeds
exceeding one million pixels per second.
In addition, a special mode is available to write the same pixel value
into 5 consecutive pixel locations, allowing to clear the screen in
less than 60 milliseconds.


#### The SUN Mouse


The SUN Mouse is a hand-held pointing device for input of graphical information
into the SUN Workstation. As a user moves the mouse around, a software
controlled cursor on the display makes a corresponding motion.
Three buttons on top of the mouse allow the user to select from
a number of commands that are provided by the software.

The SUN Mouse is a completely optical mouse. It has no moving parts
and is therefore very reliable and precise.
It detects motion by moving across a patterned surface, the pad,
on which the mouse rests. The nature of the surface defines an
orthogonal reference system for the mouse, making the mouse
rotation-invariant.

The SUN Mouse is exceptionally easy and comfortable to use
compared to other pointing and digitizing devices.


---

#### SUN Ethernet Interface


The SUN Ethernet board is a high-performance interface to the experimental
Xerox 3 MBit/sec Ethernet-1. It is capable of supporting workstations, gateways,
terminal concentrators, and servers with heavy net traffic.
The board implements the Ethernet data link layer and physical
layer functions and provides packet buffering.  As shown in Figure [Figure](#SUN
Ethernet Board), the SUN Ethernet board in conjunction with a transceiver unit
provides a complete connection to the 3 MBit/sec Ethernet.
The Ethernet interface consists of a receiver/transmitter front end,
a receive-packet queue, and a transmit-packet buffer.


![Placeholder: ether0.press]()


*Figure: **The SUN Ethernet Interface***

<a id="SUN Ethernet Board"></a>


Figure [Figure](#Ethernet Packet) shows a 3 Mbit/sec Ethernet packet.
The packet contains a single start bit, followed by two 8-bit fields
for destination address and source address respectively, a variable-length
data field, and a 16-bit CRC code.
The data field can be from 16 bytes to 2048 bytes long.


![Placeholder: ether2.press]()


*Figure: **A 3 MBit/sec Ethernet Packet***

<a id="Ethernet Packet"></a>


---
**SUN Ethernet Board Functions**

The SUN Ethernet board performs all the Data Link Layer and Physical Layer functions
for the 3 Mbit/sec Ethernet. These functions include transmit data
encapsulation, transmit data encoding, transmit link management,
receive data decoding, receive data decapsulation, and receive link management.

The packet to be sent, including address and data fields, is prepared
by the host computer and loaded into the on-board packet buffer.
The SUN Ethernet interface then attempts to acquire the network and send the
data.  Successful delivery of a packet onto the network involves the functions
of carrier deference, collision detection, and randomized retransmission
according to the exponential backoff algorithm.
During transmission, the SUN Ethernet interface
computes the 16-bit CRC value and appends it at the end of the packet.
An interrupt is generated when the packet has been sent or when the
transmit attempt has been aborted due to timeout.

Data from the Ethernet is decoded on the SUN Ethernet
interface with a digital phase-locked loop and then converted from
bit-serial into word-parallel form.
After removing the start bit, the Ethernet interface checks
the destination address of an incoming packets against an address filter.
Accepted packets are placed into the receiver `FIFO` buffer together
with the packet status. The integrity of a received packet
is validated by generating a CRC on the received bit stream and
checking it against the CRC found in the packet.
An interrupt is generated whenever the receiver queue is non-empty.

The SUN Ethernet interface supports completely general multicast
address recognition with a "bit-vector" address filter.
This address filter is implemented as a 256-Bit RAM.
For each of the possible 256 Ethernet addresses, the filter contains one bit
that determines whether to accept packets with that address.

**High Performance**

The SUN Ethernet board has been designed to offer maximum performance
while minimizing the service load placed on the host computer.
To this end, the SUN Ethernet interface includes a 4 kilobyte receiver `FIFO`
that buffers the host computer system from the unpredictable arrival times
of network traffic.  A 4 kilobyte buffer size offers a latency of 5
milliseconds for packets with a maximum size of 2048 bytes.

The SUN Ethernet interface is capable of handling back-to-back packets
(multiple packets immediately following each other) and allows full-duplex
transmission and reception (loopback packets).
Thus it can receive packets sent to itself for complete self-testing.

Using a zero-access-time port, the host processor interface supports
high-speed data transfers at rates of up to 4 Mbyte/sec.
The SUN Ethernet interface can simultaneously transmit packets,
receive packets, and transfer packets on the IEEE-796 bus.


---

#### SUN Workstation Configurations


The smallest SUN Workstation comprises the
SUN processor and SUN graphics boards, a 17" display, a detachable keyboard,
and a 6-slot Multibus cardcage.
Also included is a PROM-based DEC VT100/Tektronix emulator.
This emulator allows the SUN workstation to be used as a standalone terminal
or in conjunction with existing graphics software as a standard graphics terminal.
It can also be used as a programmable graphics terminal by
downloading 68000 programs over the serial line provided.

To run UNIX on a standalone SUN Workstation, a local disk and disk controller
is required.  If the disk controllers uses a DMA interface,
a Multibus memory board is also required to hold the disk buffers.
The SUN Workstation normally uses SMD disk controllers for
compatibility with large, high-performance Winchester disk drives.
SUN currently offers the following disks (all sizes unformatted):
an 8+8 Mbyte drive (8 fixed, 8 removable), a 25+25 MByte drive
(8 fixed, 8 removable), an 84 Mbyte drive, and a 168 Mbyte drive.
Support of a 474 MByte drive is planned in the near future.

Adding an Ethernet interface to the basic SUN Workstation
provides networking capabilities. While the SUN Ethernet board
supports the 3 MBit/sec Ethernet-1, interfaces to the standard
10 MBit/sec Ethernet board are also available.
SUN Workstations with the Ethernet interface are typically connected
into a SUN Cluster with a SUN Fileserver providing a diskless
SUN UNIX operating system for each SUN Workstation.

A SUN Fileserver is a SUN Workstation with Ethernet and disk and optional backup,
providing mass storage for the network.
Separating file storage service from individual workstations
permits users to access their files from anywhere on the network and to share
them with other users on the network. Centralized file storage
also offers lower cost per megabyte than local storage and
permits better control of the backup function.
Optionally, a SUN Fileserver can provide gateways to
other networks or long-haul communications, as well as printer services.


---

#### Summary


The SUN Workstation architecture is based on the philosophy
of dedicating computer power to the productive use of an individual.
Each SUN Workstation contains a 32-bit processor with virtual memory,
typically one megabyte of main memory, a high-resolution bitmap display,
and an Ethernet local-area-network interface.

The SUN Workstation architecture achieves the economy
of timeshared computer systems by sharing those components of a computing
environment for which economies of scale apply: mass storage, printers,
special-purpose processors, and other peripherals.
Sharing is achieved through the local network, providing high-speed
communication between SUN Workstations and common resources.
A SUN network system consists of a cluster of SUN Workstations
and a SUN Fileserver that can also provide backup and printing services.

The SUN Workstation executes the Berkeley 4.2 version of the
Bell UNIX operating system and supports the ARPA IP/TCP network protocols.
Languages that run on the SUN Workstation include C, PASCAL, and FORTRAN.
A multi-window display system, capable of displaying proportional characters
as well as graphics, serves as a user interface.

Based on state-of-the-art technology, the SUN Workstation is an
economical replacement for mainframes and minicomputers.
SUN Workstations can be interconnected in SUN Clusters
that can grow from a small number of workstations
to a large number without the performance degradation
experienced in timeshared systems.
This makes the SUN Cluster an ideal environment
for interactive applications demanding constant response times.

The SUN Workstation with the Berkeley 4.2bsd UNIX software
provides a suitable base to support applications ranging from
computer aided design to typesetting and office automation.
By adopting multi-vendor software and hardware standards, the SUN Workstation
provides a solid foundation for a long-term software investment and
a system base that can grow with the evolution of technology.
SUN is developing a compatible family of workstations that covers
a range of capability, performance, and cost options.


`
UNIX is a trademark of Bell Laboratories.
Multibus is a trademark of Intel Corporation.
VAX and VT100 is a trademark of Digital Equipment Corporation.
SUN Workstation, SUN Cluster, SUN Fileserver, and SUN Microsystems
are trademarks of SUN Microsystems, Inc.

Important Notice:
Some of the products described in this document are under active development.
SUN Microsystems, Inc. reserves the right to make changes at any time in the
products described. SUN Microsystems, Inc. assumes no responsibility
for any errors that may appear in this document.
`
