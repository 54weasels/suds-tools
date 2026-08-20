---


---


# Sun-2 (796-Bus) Processor Board


Data Sheet

Draft Version 0.3

Company Confidential

Sun Microsystems Inc.

[date]


>
The Sun-2 Processor Board is a powerful single-board computer combining
a 10 MHz 68010, multiprocess virtual memory management,
direct virtual memory access (DVMA), two serial channels, five timers, and a
16-bit parallel input port on a single board compatible with the IEEE 796 Bus
(Intel Multibus). A floating point processor, a data ciphering processor,
and a raster operation processor can optionally be added.
The memory management supports processes with up to 16 MByte virtual memory space.
Up to 4 MBytes of zero wait-state main memory can be added via the P2-Bus.


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.

Sun and the combination of Sun with a numeric suffix are trademarks of
Sun Microsystems Inc.


---


---

# Architecture Overview


## Features


10-MHz M68010 CPU

no wait states with Sun Memory Expansion Boards

addresses up to 8 MBytes of no-wait state main memory

two-level, multiprocess virtual memory management

16 Mbytes virtual address space per process

separate address spaces for supervisor and user

up to 64 KBytes of EPROM

two programmable serial I/O channels with full modem control

five programmable 16-bit timers

time-of-day clock with battery backup

16-bit parallel input port

8-bit diagnostic display

optional IEEE standard floating point processor

optional DES encryption processor

optional Raster Operation processor

DVMA (direct virtual memory access) from IEEE-796 Bus

software interrupts

bus error register

transparent hardware memory refresh

watchdog reset timer

single 5 Volt power supply


---

## Introduction


The Sun-2 Processor Board is an implementation of the
Sun-2 architecture on a single board compatible with the IEEE 796-Bus.
The Sun-2 Processor Board was designed for high-performance workstation,
fileserver, and network server configurations.
It also was designed to allow direct upgrading from Sun-1 systems to Sun-2 systems.
Both boards feature identical I/O connectors for this purpose.

The Sun-2 Processor Board includes the 68010 32-bit VLSI CPU,
virtual memory management, and system facilities.
It also includes two serial lines with full modem control, a parallel port,
and a number of diagnostic capabilities.
An IEEE standard floating point processor, a NBS data encryption processor,
and a raster operation processor can optionally be added.

A main component of the Sun-2 Processor Board is the virtual memory management.
The Sun-2 virtual memory management was specifically designed to support the
demand paging requirements of the Berkeley 4.2bsd version of
the Unix (TM) operating system.
The MMU provides up to 16 MByte of virtual memory space per process,
with separate process spaces for the system and for the user.

The Sun-2 Processor is based on a dual-bus architecture.
Input/Output and peripheral controllers connect to the P1-Bus,
which is compatible with the IEEE-796 Bus.
A number of other Sun Boards are available for peripheral expansion on the P1 Bus,
in particular the Sun SCSI/IO Board and the Sun Ethernet Board.

Main memory is added to the Sun-2 Processor Board via the P2-Bus.
The P2-Bus is a high-speed synchronous memory bus that allows
memory access without wait states.
Since the CPU never has to wait for memory, all of main memory delivers
the same performance as a cache.
The Sun-2 processor board supports up to 4 MBytes of no-wait state memory
on the P2 Bus. P2 memory can be added in increments of 1 MByte.
Memory is refreshed by special hardware invisibly to the software
and it features byte parity error detection.

An important capability of the Sun-2 Processor Board is that
P2 Memory is directly addressable from devices on the P1 Bus (IEEE 796-Bus).
via direct-virtual-memory-access (DVMA TM).
This allows IEEE 796-Bus peripheral devices such as disk or tape controllers
to directly access data in main memory in a fully protected manner.

The Sun-2 Processor Board includes a number of features
to allow software and hardware diagnostics.
Among them are a bus-error register and a diagnostic display for
indicating error conditions. A hardware watchdog timer will reset
the CPU if it should ever halt.


---

## Specification Summary


**Processor**

```

    Central Processing Unit:	Motorola 68010, 10 Mhz
    Floating Point Proessor:	Intel 80287
    Data Ciphering Processor:	AMD 9518
    Raster Operation Proessor:	Proprietary

```


**Memory Management Unit**

```

    demand-paged virtual memory management
    two-level segment/page MMU
    up to 16 MBytes per process
    separate process spaces for supervisor and user
    hardware context switching support

```


**Memory**

```

    RAM:	up to 4 MByte of no-wait state memory via Sun P2 Bus
    PROM: 	two 28-pin sockets for 2764/27128/27256 EPROMs on-board

```


**DVMA**

```

    Direct Virtual Memory Access from IEEE-796 Bus to Sun P2 Bus Memory
    256K of IEEE-796 Bus Memory Space are mapped to system context space

```


**Input/Output**

```

    two programmable RS423 serial I/O channels with RS-232 pinout
    one 16-bit input port
    five programmable 16-bit Timers
    time-of-day clock with battery backup

```


**Diagnostic Features**

```

    Bus Error Register
    Diagnostic LED Display
    Processor Watchdog Timer
    Timeout Timer

```


**IEEE-796 Bus Compatibility**

```

    D16 M20 I20 VOL.

```


**Electrical Characteristics**

```

    VCC = +5V +-5%
    ICC = 6A max.

```


**Physical Characteristics**

```

    Width: 12.00 in. (30.48 cm)	    Height: 6.75 in. (17.15 cm)
    Depth:  0.50 in. (1.27 cm)	    Weight: 16 oz.   (447 g)

```


**Environmental Characteristics**

```

    Operating Temperature: 0-55 C

```
