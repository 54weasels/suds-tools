SUN Microsystems, Inc.
2310 Walsh Avenue
Santa Clara, CA 95051

(408) 748-9900


Thank you very much for your interest in the SUN Workstation.
SUN Microsystems, Inc. was formed in February 1982 to manufacture,
sell, and support this high-performance, low-cost graphics workstation.

The SUN Workstation (TM) is a high-performance graphics workstation
aimed primarily at scientific/engineering and CAD/CAM applications.
It consists of a high-resolution bitmap display,
an Ethernet local network interface, and a powerful processor executing
the UNIX operating system (UNIX TM Bell Laboratories).
The System is packaged as a desk-top unit with a detachable keyboard.
A mouse pointing device may be optionally connected for graphical input.

SUN Workstations are interconnected via the Ethernet into clusters
forming a distributed computing system.
A typical SUN Cluster (TM) combines five to ten SUN Workstations with
a fileserver, printer server, backup server, etc.
This gives each user a high-quality display and a powerful local processor
while sharing the cost of the peripherals (disks, tapes, printers, etc.).
It also provides a quiet and cool office environment because
the peripherals can be located remotely.

SUN Microsystems is porting the Berkeley 4.2bsd UNIX to the SUN.
This allows a full UNIX system to be run on SUN Workstations
without local disks, accessing files and programs over the network.
4.2bsd supports very high-performance networking and file system.
In addition, it includes a large number of utilities as part of the system.
A FORTRAN and a PASCAL compiler is also available.
The system is scheduled for release in 1Q83 and
will be made available to betasites in 4Q82.

Currently available software for the SUN Workstation is a UNIX Version 7
distributed by Unisoft. To run this UNIX, a disk is required for each workstation.
This system inlcudes some of the Berkeley UNIX enhancements, such as vi.
An optional Pascal and Fortran compiler is available.
SUN Workstations shipped with UNIX V7 will be field upgradable to
the 4.2bsd UNIX system through a hardware/software upgrade package.

The workstation can also be used as a programmable graphics terminal.
A PROM-based DEC VT100 emulator and a Tektronix 4014 emulator is available,
as well as an implementation of the SIGGRAPH CORE standard of graphics routines.

The basic SUN Workstation, consisting of keyboard, display, and processor,
and graphics terminal software, has a list price of $8,900.
A SUN Workstation with a 12 MByte Winchester disk
(6 MByte fixed, 6 MByte removable), SMD Disk controller,
a 128K Multibus Memory Board, and V7 UNIX costs $19,900.
Lead time is 60 to 90 days.


---


---
(A SUN OVERVIEW FROM ANDY BECHTOLSHEIM)

The SUN Workstation is a high-performance graphics workstation
aimed primarily at scientific/engineering and CAD/CAM applications.
It consists of a high-resolution bitmap display,
a local network interface, and a powerful processor executing
the Bell UNIX operating system (UNIX TM Western Electric).
The System is contained as a desk-top unit with a detachable keyboard
and a separately packaged disk subsystem.
An optional mouse pointing device may be connected for graphical input.

The display is a 17" wide-format screen with 1024 by 800 points resolution.
It can display two pages of characters and graphics, including
proportionally spaced characters, foreign alphabets, and mathematical symbols,
as well as lines, curves, and shaded images.
High-speed "RasterOp" hardware assist can write a full screen of
variable-width characters in less than 100 milliseconds.

The processor is based on the Motorola 68000/68010 CPU, extended with
a powerful virtual memory management unit that allows demand paging
and rapid task switching between multiple processes.

The design allows the 68010 processor to operate
at 10 MHz at full speed without wait states. Main memory is based on
64K technology and starts from 256 kilobytes, expandable in 768 kilobyte
increments.

The SUN workstation uses Ethernet for its local network.
It is currently equipped with an interface to the Ethernet-1 3 MBit/sec
network. A 10 Mbit/sec Ethernet interface is planned for 3Q82.

A color display option extends the basic workstation with a high-speed
color capability, offering a 640 by 480 display area with 256 simultaneous
colors from a palette of over 16 Million.  The video output is RS-170
compatible.

An optional disk controller interfaces the workstation to high-performance
SMD disk drives. Two 8" Winchester drives are offered as a standard:
an 84 MByte, 20 msec drive and a 16 MByte (8 fixed, 8 removable) drive.

The SUN Workstation uses the Intel Multibus (TM Intel Corp) as a system bus,
providing hardware expandibility with a wide number of board-level products
and allowing a user to configure a system to his particular needs.


---


---
(MESSAGE FROM BILL JOY ON USENET)

Some previous net.general news items surfaced which asked about SUN
workstations.  Since I will soon be joining SUN Microsystems I can
answer the questions posed and provide some information about current
and future plans for hardware and software at SUN.

SUN Microsystems is the holder of the license for the SUN workstation,
which was originally developed at Stanford University by Andy
Bechtolsheim and Forest Baskett.  Earlier versions of the basic SUN
design were manufactured by Andy's company VLSI Systems, which has been
superseded by SUN.  Andy is one of the founders of SUN.  A number of
other companies were licensed to manufacture the early SUN boards.  Two
of these companies are licensed to manufacture all three of the SUN
boards (processor, Ethernet and graphics card):  Forward Technology,
which is marketing a package based on the SUN boards as the ``SPICE''
workstation, and CADLINC, which is building a CAD/CAM product based on
the SUN boards.  A number of other companies are using SUN processor
cards in their products; notable among these is CODATA which has a
multi-user UNIX machine available based on the board.

SUN was launched in February, 1982 with a multi-million dollar venture
financing.  The company was founded with Andy Bechtolsheim the chief
technical person, Vinod Khosla (who was a founder of Daisy Systems, a
electronics CAD company) as president, and Scott McNealy, who was
director of operations at Onyx systems, in charge of manufacturing.
I agreed to join the company shortly thereafter, with my involvement
with SUN beginning in July, 1982, when I will begin working half-time.
I will be working full time for SUN after the 4.2bsd distribution is
complete.

The SUN is a powerful workstation computer especially suitable for use
in science and engineering and is a marvelous UNIX machine.  Each SUN
workstation contains a 1000*800 pixel 17'' monitor, with each point on
the monitor individually mapped to a bit of display memory.  (The
display currently being used in the workstation is that used in the
Xerox STAR office product which you may have seen.)  In the base of the
display are a power supply and a 6-slot MULTIBUS card cage.  The basic
workstation uses three of these slots for a CPU card, a frame buffer
(for the display) and an Ethernet interface:

* The CPU card contains a Motorola 68000, memory management hardware which
  gives access and referenced bits at the page level and virtual address
  translation with NO slowdown of processor access, 256Kb of parity memory,
  5 timers for use by the operating system, 2 UARTS capable of running RS232
  terminals or HDLC type interfaces, and an interface to the MULTIBUS.
  A 10Mhz 68000 is roughly comparable to a 11/750 in C code performance.
  The basic (old revision) SUN boards support up to 2 Megabytes of virtual
  memory per process.

* The frame buffer card contains a 1024*1024*1 bit memory.  It supports
  the ``rasterop'' operation first popularized in the ALTO microcode, and
  described in the article about SMALLTALK in a recent issue of BYTE magazine.
  Using the hardware support in the frame buffer it is possible to manipulate
  from 1-16 bits in the memory, do an arbitrary logical operation on this data
  and other data from display memory and then store the result into the
  frame buffer all in about 1 microsecond.  The entire screen can be repainted
  in about 64 milliseconds.

* The Ethernet card in the basic SUN workstation is currently a 3 Mbit
  interface designed by Andy.  You will be able to use a 10 Mbit Ethernet
  interface (e.g. the one manufactured by 3COM) as soon as they are
  available (early this summer?).  Other local networks (such as PRONET)
  also have MULTIBUS interfaces which can be used with SUNs.

The other component of the current basic workstation is a high-quality
detachable keyboard.

The concept of the SUN is to place clusters of terminals on an Ethernet
with other resources such as a file server and a printer.  This gives
each user a high-quality display and a powerful local processor on
which programs can be run at low cost while sharing the higher cost of
the servers resources (disks, tapes, printers, etc.) among a number of
users.  The high-resolution display allows applications with
user-interfaces like SMALLTALK, variable-width fonts, vector and raster
graphics, multi-window user interfaces (much like the Apollo or Perq),
etc.  Because the SUN processor will be running UNIX, it is also
possible to use it as a file server (by adding disks), as a timesharing
node (either by plugging in terminals or accessing it over the network)
or as a inter-network gateway (by plugging in several network
interfaces).

The basic workstation can be expanded by adding additional memory.
Early versions of the SUN (being sold by other companies) allow up to
1/2 Megabyte of memory local to the processor, 1/4 megabyte on the
processor card and 1/4 on another similar card.  This memory can be
accessed with no wait states, while other memory resides on the
multibus and can be accessed only more slowly.  SUN has redesigned the
boards and built new memory cards containing 3/4 megabytes of memory
which can be accessed directly from the CPU with no wait states.  Up to
two of these 3/4 Megabyte memory cards can be added to the basic
workstation to give up to 1.75 megabytes of local storage.

You can also add SMD (storage module interface) disks to the basic
workstation, e.g. by using an INTERPHASE disk controller.  Disks with
this interface are manufactured by all the major disk manufacturers:
CDC, Ampex, Fujitsu, etc.

Other devices are currently being integrated into the system:

*) Pointing devices: ``mice'' and tablets.  There are a number of different
   devices currently available differing widely in cost and desirability.
   The mice and tablets can be interfaced easily to ports on the processor
   card.

*) A color frame buffer: 640*480*8 bits which gives 256 different colors
   mapped into a 24 bit color map.  If more colors are desired, then up to
   three of these cards can be stacked to provide a 24-bit deep frame buffer.

*) Interfaces for standard peripherals such as 9 track tapes, cartridge
   tapes, and raster output devices such as Versatek printer-plotters
   or the newer laser printers (e.g. the Canon LPB-10).

Andy has modified the CPU card so that it will allow up to 8 Megabytes
of virtual memory per-process.  This is especially important since
Motorola will be releasing the 68010 chip in the fall which will
support virtual memory, and essentially all current VAX UNIX
applications will run in an 8 Megabyte virtual address space.  The
software group at SUN is porting the Berkeley UNIX kernel from the VAX
to the 68000 to get a paged system on the workstation.

Currently available software for the system is a UNIX version 7 system
distributed by UNISOFT.  To run this UNIX you need a disk on the
workstation.  It is also possible to use SUNs without disks either as a
programmable graphics terminal, as a multi-window vt100, or to download
programs compiled on another machine into the SUN through a serial port
or over an Ethernet.  The 4.2bsd system which is being ported to the
SUNs will allow a full UNIX system to be run on each workstation
without a local disk, accessing a file server over the network for
files and programs.  This style of operation is made possible by the
networking and inter-process communication support in 4.2bsd and made
feasible by the speed of the local network protocols, and a new
higher-performance file system implementation in 4.2.

Besides myself, other people at SUN who may be known to the UNIX
community are: Laura Tong, who was previously working at the Computer
Systems Research Group at Berkeley, administering the project and
coordinating the 3bsd and 4bsd distributions; Bill Shannon, who
previously worked in the UNIX Engineering Group at DEC and wrote many
of the VAX drivers; Tom Lyon, who was previously at AMDAHL and was one
of the principals in the AMDAHL UTS UNIX product.  Other software
people at SUN include John Gilmore (previously with Data General),
Marty Rattner (previously with National Semiconductor), and Mike Shantz
(previously with Deanza Graphics).

In addition to the port of the 4.2bsd system and development of
graphics support for vector and raster graphics on the workstation, SUN
will be developing a basic window system for the machine.  It is also
expected that a large number of languages and application packages will
become available for UNIX on the SUN.

SUN will be cooperating closely with the Computer Systems Research
Group at Berkeley in future developments of the 4.2bsd system, with
John Seamons, Bill Shannon and others at Lucasfilm who have done a good
deal of work on UNIX for the SUN, and with other groups.  Cooperative
arrangements with Universities, research labs and commercial outfits
will be of benefit to all users of UNIX and of the SUN.


SUN is currently accepting orders for the workstation, which has a list
price of $9,900, or $8,900 without the Ethernet.  Universities get a
discount price of $8,000 for the workstation, or $7,000 without the
Ethernet.  The systems being manufactured by SUN have a number of
improvements over other versions of the design currently being
manufactured.  In particular, the other versions of the workstation
operate at 8Mhz rather than 10Mhz and allow only a limited amount of
on-board memory.  SUN has also redesigned the boards to get higher
reliability and noise immunity, and is using only burned and tested
components.  If you want more information about prices, delivery or
anything else, you can contact:


	SUN Microsystems, Inc.
	2310 Walsh Avenue
	Santa Clara, CA
	408 748 9900


See you all at the USENIX meeting in Boston,


	Bill Joy


---
