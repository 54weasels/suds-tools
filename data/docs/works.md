---


# The SUN Workstation Architecture


	   Andreas Bechtolsheim, Forest Baskett, Vaughan Pratt

		       Computer Systems Laboratory
			   Stanford University
			   Stanford, CA 94305

			Technical Report 229

			    March 1982


>
**Abstract**
The SUN workstation is a personal computer system that combines
graphics and networking capabilities with powerful local processing.
The workstation has been developed for research in VLSI design automation,
text processing, distributed operating systems and programming environments.
Clusters of SUN workstations are connected via a local network
sharing a network-based file system.

The SUN workstation is based on the Motorola 68000 processor,
has a 1024 by 800 pixel bitmap display, and uses Ethernet as its local network.
The hardware supports virtual memory management,
a "RasterOP" mechanism for high-speed display updates,
and data-link-control for the Ethernet.
The entire workstation electronics consists of 260 chips mounted on
three 6.75 by 12 inch PC boards compatible with the IEEE-796 Bus (Intel Multibus).
In addition to implementing a workstation, the boards
have been configured to serve as network nodes for
file servers, printer servers, network gateways,
and terminal concentrators.

This report discusses the architecture and implementation of the SUN
workstation, gives the background and the goals of the project, contemplates
future developments, and describes in detail its three main components: the
processor, graphics, and ethernet boards.


**Keywords:** Workstation, Personal Computer, Local Networks, Graphics

**CR Categories:** 6.21, 8.2


>
This work has been supported in part by the Defense Advanced Research
Projects Agency under order DARPA-MDA-903-C-0680 and in part by Stanford
University Computer Science Department.

UNIX is a trademark of Bell Laboratories and Multibus is a trademark of
Intel Corporation.


---


---

#### Introduction


The SUN workstation is a powerful modular network-based graphics workstation.
Its primary use is as a personal computer with high resolution high
performance graphics capabilities and substantial local processing power.
Its modularity permits it to be reconfigured for a variety of
applications, including support for networks of SUN workstations in the form
of printer servers, file servers, terminal concentrators, and gateways.
Such a system provides a suitable hardware base to support research in design
automation, advanced text processing, office automation, distributed systems,
computer aided manufacturing, robotics, and other
interactive graphical computing tasks.

The SUN workstation consists of a bitmap display,
keyboard, network connection, and processor.
A "mouse" pointing device may be connected to the keyboard.
The display has 1024 by 800 pixel resolution and
can show arbitrary raster images, thus permitting variable width fonts,
foreign alphabets, mathematical symbols, vectors, curves, shaded regions,
and even photographic pictures, on a full page display on either portrait
or landscape mode monitors.
The SUN workstation uses Ethernet as its local network.
The Ethernet connection allows many SUN workstations
to be tied together to exchange messages and electronic mail
and to share services such as file storage and printing.
The processor is based on the Motorola 68000 CPU, extended
with virtual memory management hardware. The design allows
a 10 MHz 68000 to operate at full speed without wait states.


![Placeholder: works1.press]()


*Figure: **The SUN Workstation***


The following sections describe the background and rationale of the project,
the network architecture, configurations of SUN workstations,
implementation goals and tradeoffs, and the three components
of the basic workstation: the processor, graphics, and ethernet boards.


---

#### Design Rationale


The architecture of the 70's is not well-matched to the hardware of the 80's.
Powerful large-memory processors suited to a broad spectrum of applications
are becoming too cheap to be worth the effort of timesharing.
High-speed local networks permit mass storage, printers, special-purpose
processors, communications interfaces, and other resources to be located and
shared for optimal cost and speed of access.  High resolution high
performance displays previously only available to specialized markets are
becoming available to the ordinary user, presenting new opportunities for
effective user interfaces in such areas as document preparation, software
development, computer-aided design, and information management.

The qualitative in today's designs depends heavily on the quantitative.
A processor with a quarter of a megabyte of memory, segment-and-page
memory mapping, and a CPU close in performance to a VAX-11/780 for
a broad range of applications, can be built from $1000 worth
of integrated circuits.
It becomes difficult to justify buying a conventional mainframe,
allocating basement space for it, and pulling terminal cables
throughout the building, when for less money one can buy
50 computers and put them on the desks of their users.

The computer-per-desk model would of course be flawed if large, noisy,
and expensive peripherals had to go on the desk beside the computer.
This is where the network comes in. All the traditional peripheral
functions and services of a computing environment can be distributed
over the network, sharing resources for optimal cost,
replicating services where needed for performance and reliability reasons.

Thanks to the speed of today's networks, it has become
thinkable to interpose a network between the computer and its disk drive.
The speed of a 10 MBit/sec Ethernet matches the data rate of SMD disk drives
and permits mass storage to be shared among a local cluster of workstations.
A disk connected via a network to ten personal computers offers essentially
the same performance as a disk directly connected to a computer
timeshared by ten users, provided the network is not overloaded with
other non-disk tasks.

Another parameter that affects design qualitatively is the display.
A high-resolution, high-speed display, which can show a full page of text
and images virtually instantaneously,
opens up new applications and new alternatives for many tasks.
Consider the problem of having many more characters than keys on the keyboard.  If the image of a nonstandard
keyboard, say with Greek or mathematical symbols, can be superimposed
instantaneously on the screen, and removed just as instantaneously, the need
for keytops with many symbols per keytop disappears.

Although a display with 1024 by 800 pixel resolution is slightly more expensive
than traditional lower-resolution displays,
the tremendous human-factor advantage of high resolution more than
justifies any residual price difference between the two technologies as they
move into high volume production.


---

#### SUN: The Stanford University Network


In Fall 1979, the Computer Science Department at Stanford University
began installation of a campus-wide experimental Ethernet network.
The initial network connected 18 Xerox Altos,
Dover Laserprinter, and Fileserver, all donated by Xerox Corporation, along
with two VAX-11/780
computers located in Margaret Jacks Hall.  Since then the network has been
extended to the Computer Systems Laboratory and the Center for Integrated
Systems, and has been connected via a gateway to the Stanford University
Medical Center's Ethernet.  Besides the initial computers, these networks now
have connected to them 4 more VAX-11/780 computers, 5 Xerox Dolphins, the
SAIL KL-10, the SUMEX KI-10, DecSystem 2020, and PDP-11, and the SCORE
DecSystem 2060 computers.  Counting the 10 Sun workstations also on the net,
there are more than 40 computers presently connected.
Two gateways between the Ethernets and the ARPA network
allow users of the Stanford University Network to communicate
electronically with other researchers throughout the country
and even overseas.


![Placeholder: works2.press]()


*Figure: **The SUN Network***


---

#### The SUN Workstation Environment


The SUN workstation depends on the SUN network environment for
a variety of services, including communication, file storage,
printing, and bootstrapping.
These services are provided by dedicated network nodes that themselves
may be a particular configuration of a SUN workstation.
Server nodes can be replicated on a network when
appropriate to enhance performance, reliability, availability, or accessability.

For a distributed operating system the network file system is a
particularly important issue,
since the basic SUN workstation has no local secondary storage.
We are currently planning a network file system that combines
the logical simplicity of centralized file storage with the performance
of local file caches.  To this end, the network is organized as many subnets
each supporting a *cluster* of SUN workstations.


![Placeholder: works3.press]()


*Figure: **A SUN Workstation Cluster***

<a id="SUN Workstation Cluster"></a>


Figure [Figure](#SUN Workstation Cluster) illustrates a typical workstation cluster.
From one to ten or more SUN workstations share a local Ethernet
and a local fileserver.  The local fileserver in turn is connected to other
Ethernets to access a logically central but physically network-wide
distributed file system.

The local file server functions as a gateway, a file cache, and a swapping device.
As a gateway it connects the local Ethernet to its neighbors.  As a cache it
maintains copies of active files, those currently in local use.
As a swapping device it provides swapping and paging services to the
workstations in the local cluster, isolating this traffic from the remote
Ethernet.


---

#### SUN Workstation Components


The SUN workstation is divided into three basic components:
the processor, the graphics, and the Ethernet subsystem.
Each one of these is implemented as a single board
electrically and mechanically compatible with the
IEEE-796 Bus or Intel Multibus. The choice of the
Intel Multibus makes the SUN workstation compatible
with the board products of over 100 board and system manufacturers.

A basic SUN workstation consists just of these three board types.
When an application demands, the basic workstation can be enhanced with
additional capabilities, such as color graphics, expanded memory,
or additional communication facilities.

We shall now describe the most salient features of these boards.
More detailed descriptions sufficient for programming the boards
can be found in the user manual of each board [VLSI Systems].


---

#### SUN Processor Board


The SUN Processor board is the main component of the SUN workstation.
It combines a 10 MHz 68000/68010, virtual memory management,
256k bytes of main memory, and input/output
on a single board compatible with the IEEE 796 Bus.
The processor can execute from on-board memory without wait states.
On-board memory is expandable from 256K bytes to 512K bytes
or 1M bytes with the SUN memory expansion board.  With offboard
(Multibus) memory a total of 2 megabytes of physical memory is directly
addressable at any one time.

On-board input/output includes two high-speed programmable serial channels,
a 16-bit input port for configuration control,
and five 16-bit timers.  One of the timers can be configured as watch-dog timer
for auto-reload in remote applications.

**SUN Memory Management**

The SUN Memory Management Unit has been designed to support
a multitasking operating system such as Bell Lab's UNIX.
It provides address translation, protection, sharing, and
memory allocation for a multiprocess environment.
All accesses of the processor to on-board RAM memory, 796-Bus memory, and
796-Bus I/O space are translated and protected in an identical fashion.
Further, the SUN memory management provides
all the necessary mechanism for demand paging and virtual memory, anticipating
the appearance of the 68010 virtual memory processor.

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
allowing read, write, and execute cycles in supervisor and user states.

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
If all page entries are in use, a page must be replaced.

Full virtual memory capability is possible with the 68010 processor,
the virtual-memory version of the 68000.
The original 68000 processor cannot fully
recover from page faults because it does not save
sufficient state information to continue an aborted instruction.
However, for a limited set of operations, such as load and store,
recovery from aborted instructions is straightforward.
With additional software assistance, recovery from more
complex addressing modes appears feasible.


---

#### SUN Graphics Board


The SUN Graphics Subsystem combines a high-resolution display
(up to 1024 by 1024 pixels) with a high-speed "RasterOp" update mechanism
(screen fill in 64 milliseconds).

The displayed image is stored in a 1024 by 1024 pixel frame buffer
that can be used either with a portrait or landscape mode monitor.
1024 by 800 pixels are actually displayed,
the remaining 224 by 1024 invisible pixels are available as a cache
to store characters, cursors, and other graphical symbols.

The frame buffer is implemented as a special dual-port memory.
One port is dedicated to video refresh, the other port permits the frame
buffer to be updated.  In addition to the frame buffer memory, the SUN
graphics board provides the video refresh logic and special hardware to
assist in frame buffer updates.  The actual updating is performed by the main
processor, which in combination with the graphics hardware can perform
updates at a rate of up to 32 MBit/sec (one read-modify-write cycle on a 16-bit
operand per microsecond).

**RasterOp Architecture**

The SUN Graphics system incorporates the concept of "RasterOp"
[Ingalls, Newman&Sproull].
RasterOp means that rectangular areas of display data ("raster")
are modified or combined according to a preselected operation ("Op").
The RasterOp function provides complete generality to paint characters,
manipulate windows, scroll screens, and to draw vectors.
An example for RasterOp is shown in Figure [Figure](#SUN RasterOP),
in which source characters are copied to a destination in the frame buffer.


![Placeholder: graph0.press]()


*Figure: **A RasterOp Operation***

<a id="SUN RasterOP"></a>


---


RasterOp grew out of an attempt to unify the treatment of text and
bitmap graphics in the early history of Smalltalk [Ingalls].
It was then implemented on the Xerox Alto computer
as a microcoded instruction called BitBlt,
for Bit Boundary Block Transfer [Thacker et al].
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
Vectors are drawn at a rate of about 1 pixel per microsecond,
using raster-vector algorithms.

---

#### SUN Ethernet Interface


The SUN Ethernet board is a high-performance interface to the experimental
3 MBit/sec Ethernet. It is capable of supporting workstations, gateways,
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


Although the main design goal of the SUN workstation
was to be a graphics workstation, a second and equally important goal
was to provide a set of modular hardware components configurable
for a variety of network nodes including terminal concentrators,
printer servers, file servers, gateways, and processor servers.
This goal was attained through the modular construction of the hardware.
Different network nodes can be assembled using the SUN processor board,
the Ethernet board, and other boards depending on the application.
Nodes that have been built with SUN boards are described below.

A terminal concentrator, or "Ethertip", connects RS-232 terminals or dial-up
modems to host computers on the Ethernet, or via the ARPA gateway, on the
ARPA net.  Acting like a crosspoint switch between terminals and host
computers, a concentrator allows any terminal to connect to any host computer
on the network.  The SUN Ethertip supports from 10 to 32 terminals at speeds of
9600 baud.

A printer server controls a hardcopy device such as a lineprinter or laser
printer.  A request to print a file can be directed to the nearest printer
server offering the appropriate level of service (ASCII text or graphics,
monochrome or color, low or high volume, etc.)
The Imagen printers in use at Stanford, based on the Canon LBP-10 laser
printer, use the SUN processor board [Imagen Corporation].

A file server provides mass storage for the network.
Separating file storage service from individual processors
permits users to access their files from anywhere on the network and to share
them with all users on the entire network.
Mass file storage also offers lower cost for storage of inactive files than
local file storage, permits better control of the backup function, and lends
itself to redundancy techniques for better availability and access times for
files requested from random locations.

A gateway interconnects independent or different networks,
isolating the traffic in each net and decoupling the networks.
Gateways are a necessity for the SUN network because of the physical
distance across the campus.

A processor server is a multiprocessor system, providing processors as a
network resource.  One such system, the LOTS workstation, is presently under
construction at Stanford for teaching computer programming.  In this system
each student's terminal is connected via a TIP on the Ethernet to one of a
bank of 16 processors.  Each processor is dedicated to that student for
the duration of the session.  In the expected use, a text editor and Pascal
interpreter or compiler will remain resident on the processor [Nielsen].

---

#### Implementation Strategy


The primary goal in implementing the SUN workstation
was to design a system with the maximum performance offered by
state-of-the art VLSI technology, using standard components
and interfaces, at a price permitting
each researcher to have a personal SUN workstation.
We accomplished this using the following implementation strategy.


The use of mass-produced state-of-the-art technology.  Today's integrated
circuit technology renders possible the design of a high-performance yet
affordable workstation.  The SUN workstation has a raw computing power
approaching 1 MIPS (million instructions per second), in a unit the size and
price of presently available personal computers having neither graphics nor
networking capabilities.

Maximum performance subject to the above technology constraint.
Particular attention was paid to achieving a system that allows
a 10 MHz 68000 processor to execute at full speed without wait states.
The computational power of this system operating at 8 MHz has been benchmarked
at more than 70% of a VAX 11/780 on a broad spectrum of
non-numerical compute-bound applications written in the C programming language.

Optimization of hardware/software tradeoffs.
Workstation functions were carefully analysed in terms of
hardware/software implementations.
Special-purpose hardware was added where needed to maximize performance,
for example in the graphics system and the Ethernet interface.
Functions were implemented in software where performance
was not impaired. Some functions traditionally implemented in
hardware, such as DMA and memory refresh, actually improved in performance by
being implemented in software, due to elimination of arbitration overheads.

Adherence to popular industry standards where appropriate.  Use of the
Motorola 68000 processor, the Intel Multibus backplane, and the Xerox
Ethernet greatly reduced design time and permitted attention to be focused
on the areas most critical to the success of the
workstation, namely the system level architecture and the graphics subsystem.
These industry standards are precise and well-understood, leading to an
effective partitioning of the design that justifies the term "modular."  The
popularity of these standards facilitates adaptation of the design to other
applications for which hardware using those standards already exists.


This implementation strategy led to a high-performance,
yet simple and economical design.
One measure for system complexity is the number of integrated circuits used.
The SUN workstation incorporates a total of 260 packages, whereas
comparable products on the market today have more than twice as many components.
The economy of the SUN design is due to careful system level design,
optimization of hardware/software tradeoffs,
and the use of large scale integration whenever practical.


---

#### Project History


The SUN workstations grew out of the desire to have
a display capability for the Stanford University Network [Baskett et al].
In May 1980, after a series of architectural discussions,
the detailed design of the SUN workstation was started.
By November 30, 1980, a first wirewrap prototype
of the workstation had been built.

During testing and debugging of this prototype a number of improvements
led to a revised design.  This "production" version of the design was
completely tested and demonstrated on July 3, 1981.  At this time, the
processor board
was already laid out as a printed circuit board, followed by
the graphics board and Ethernet board over the next two months.
On September 1, 1981, all layouts were completed and artwork
was sent out to several companies for manufacturing.  At the time of this
writing, a combined manufacturing experience of several hundred SUN boards
has been accumulated.

It is estimated that two man-years went into the design of the SUN workstation
up to its release for production.
About one third of this time was spent developing
design automation tools to support the design activity.
An existing Stanford design automation system, SUDS,
was used for schematic entry and printed circuit layout,
enhancing it with a new physical design subsystem
and interfacing it to the in-house typesetter machine
for generating PC artwork.
The time investment in CAD tools was a highly profitable one;
it was returned in terms of saved time the first time the tools were used.
All design errors that occurred in the design process
were collected and categorized to provide feedback for the development
of future design automation tools to prevent such errors.

At about the time the design of the SUN hardware was being finalized,
software support tools were developed, including diagnostics,
debuggers, device drivers, and run-time support.
All of these tools are written in the C language
and were developed on a VAX 11/780 computer under
the UC Berkeley version of the Bell UNIX operating system.
A detailed description of this software environment may be found in
the SUN software User's Guide [Nowicki].


#### Future Developments


The SUN workstation design is driven by technology.
As new chip components become available,
they will be incorporated into the workstation, and the
design has been formulated with an eye towards such enhancements,
some of which are briefly discussed here.

An important enhancement will be to full virtual memory.
The SUN workstation has been designed to use the virtual memory version
of the 68000, the 68010, without modifications.
All hardware needed for adequate support of demand paging is already in place.

The Ethernet interface will be upgraded to 10 MBit/sec
as soon as suitable components become available.
3 MBit/sec Ethernets will continue to stay in service,
connected to their 10 MBit/sec cousins via gateways.

A number of enhanced graphics capabilities are planned, including
color graphics and non-interlaced monochrome displays.
A high-speed floating point geometric processor to perform
matrix transformations, clipping and scaling is under development [Clark].

Finally, a file-server development is planned, including performance analysis
of distributed file systems and defining efficient network file protocols.

---

#### Acknowledgements


The authors' contributions to this development are as follows.
Forest Baskett conceived the idea of the Sun workstation and
designed the memory management architecture.
Andreas Bechtolsheim developed the graphics architecture and was responsible
for the bulk of the design of the three boards.
Vaughan Pratt has coordinated the project for the past year.
Mike Nielsen and John Seamons contributed to the design of the Ethernet interface.
Jeff Mogul and Bill Nowicki were indispensable assistants
in assembling the SUN software development environment.


#### Conclusions


The SUN workstation architecture is based on the recognition
that there is no economical advantage in attempting to share
a computer system comprised of $1000 worth of integrated circuits,
if that computer power can be put to productive use by an individual.

However, the SUN workstation architecture achieves the economy
of shared computer systems by sharing those components of a computing
environment for which economies of scale apply: mass storage, printers,
special-purpose computers, and other pheripherals.

Sharing is achieved through the local network, providing high-speed
communication between personal workstations and shared resources.
Thanks to the speed of today's networks, this communication path
does not pose a bottleneck.

The SUN workstation demonstrates that powerful local processing
with high-performance graphics and networking capabilities
can be attained in an economical system,
that high-speed bit-map graphics is feasible with standard processors,
and that the same base hardware can support a variety of network nodes
and applications through modular construction.

---

#### References


F. Baskett, "Pascal and Virtual Memory in a Z8000 or MC68000 Based
Design Station, *COMPCON* 1980.

F. Baskett, A. Bechtolsheim, W.Nowicki, and J.Seamons:
"The SUN Workstation: a Terminal System for the Stanford University Network,"
Stanford Computer Science Dep., Internal Report, March 1980.

A. Bechtolsheim and F. Baskett,
"High-performance Raster Graphics for Microcomputer Systems",
*Proceedings SIGGRAPH Conference*, Seattle, July 1980.

A. Bechtolsheim and D. J. Brown,
"The SUN RasterOP", submitted to *SIGGRAPH Conference*, Boston, July 1982.

J. H. Clark, "The Geometry Engine: A VLSI Geometry System for Graphics",
submitted to *SIGGRAPH Conference*, Boston, July 1982.

Digital Equipment Corporation, Intel Corporation, and Xerox Corporation,
*The Ethernet, A Local Area Network, Data Link Layer and Physical
Layer Specifications*, September 1980.

R. Boberg, "Proposed Microcomputer System 796 Bus Standard",
*Computer*, October 1980.

R. Greenblatt, "MIT's LISP Machine", *COMPCON*, 1980.

Motorola Inc., "MC68000 16-bit Microprocessor User's Manual, IMC68000UM, 1980.

Imagen Corporation, "Imprint-10 Printing System", 1981.

D. Ingalls, "The Smalltalk Graphics Kernel",
*Byte Magazine*, Volume 6, No. 8, August 1981.

R. Metcalfe and D. Boggs, "Ethernet: Distributed Packet Switching for
Local Computer Networks", *Communications of the ACM*, 19, 7, July 1976.

G. A. McDaniel: "The Dorado: A Compact, High-Performance Personal Computer
for Computer Scientists", *COMPCON* 1980.

W. M. Newman and R. F. Sproull, *Principles of Interactive Computer Graphics*,
second edition,	McGraw Hill, 1979.

A. Newell, S. E. Fahlman, R. F. Sproull, and H. D. Wactlar, "CMU Proposal for
Scientific Personal Computing", *COMPCON*, 1980.

M. Nielsen, "SUN Student Workstation System Overview",
Computer Science Department, Stanford University, 1981.

W. Nowicki, ed., SUN User's Guide, Stanford, 1981.

Brian Rosen, PERQ: "A Comercially Available Personal Scientific Computer",
*COMPCON*, 1980.

C. P. Thacker, E. M. McCreight, B. W. Lampson, R. F. Sproull, and D. R. Boggs,
"Alto: A personal Computer", in Siewiorek, Bell, and Newell, eds., *Computer
Structures: Readings and Examples*, McGraw Hill, 1979.

S. Ward and C. Terman, "An Approach to Personal Computing",
*COMPCON*, 1980.

VLSI Systems Inc., "SUN 68000 Board, SUN Graphics Board, and
SUN Ethernet Board User Manuals", 1981.
