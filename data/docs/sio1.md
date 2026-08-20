---


---


# Sun-2 (MB) SCSI/IO Board


Data Sheet

Draft Version 1.1

Company Confidential

Sun Microsystems Inc.

May 11, 1983


>
The Sun-2 (MB) SCSI/IO Board combines a SCSI interface,
two UARTs with full modem control, a pair of EPROM sockets,
and a real-time clock with battery backup on a single board
compatible with the Intel Multibus.


>
Multibus is a trademark of Intel Corporation.
Sun, Sun-1, Sun-2, and DVMA are trademarks of Sun Microsystems Inc.


---


---

# Architecture Overview


## Features


SCSI interface with DMA channel for data

16-bit data transfers

Two UARTs with full modem control

Real-Time Clock with battery backup

Two EPROM sockets for 2764/27128/27256 EPROMs or battery-backup RAM


## Introduction


The SCSI/IO Board implements miscellaneous I/O capabilities for the Sun-2.

The SCSI interface is a single-initiator interface. Data can be transferred
via DMA directly into Multibus or Sun-2 Processor memory. Data transfers
may be done either 8 bits or 16 bits at a time.
Command and status transfers are done 8-bits at a time using programmed I/O.

Besides the SCSI interface, the board features two UARTs with full modem control
and synchronous communication capabilities.
There is also a real-time clock with battery backup and two EPROM sockets.

---

## Specification Summary


**SCSI Interface**

```

    Single Initiator
    DMA transfers for data
    8-bit or 16-bit data transfers

```


**Serial Line Interface**

```

    two identical channels
    Synchronous Communication Controller
    full modem control and external clock support

```


**Real-Time Clock**

```

    provides time of day in milliseconds
    rechargeable battery backup

```


**PROM sockets**

```

    two 28-pin sockets for 2764/27128/27256 EPROMs or battery backup RAM

```


**Electrical Characteristics**

```

    VCC = +5V +-5%
    ICC = 4A max.

```


**Physical Characteristics**

```

    Width: 12.00 in. (30.48 cm)
    Height: 6.75 in. (17.15 cm)
    Depth:  0.50 in. (1.27 cm)
    Weight: 16 oz.   (447 g)

```


**Environmental Characteristics**

```

    Operating Temperature: 0-55 C

```
