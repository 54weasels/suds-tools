---


---


# Sun-2 (796-Bus) SCSI/IO Board


Preliminary Data Sheet

Draft Version 0.3

Company Confidential

Sun Microsystems Inc.

[date]


>
The Sun-2 (796-Bus) SCSI/IO Board combines a SCSI interface and
four serial lines with full modem control on a single board
compatible with the IEEE-796 Bus.


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


SCSI interface with DMA channel for data

16-bit data transfers

Four UARTs with full modem control


## Introduction


The SCSI/IO Board implements miscellaneous I/O capabilities for the Sun-2.

The SCSI interface is a single-initiator interface. Data is transferred
via DMA directly to the IEEE-796 Bus.
Data transfers may be done either 8 bits or 16 bits at a time.
Command and status transfers are done 8-bits at a time using programmed I/O.

Besides the SCSI interface, the board features four UARTs with full modem control
and synchronous communication capabilities.

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

    four identical channels
    Synchronous Communication Controller
    full modem control and external clock support

```


**796-Bus Compatibility**

```

    D16 M24 VOL.

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
