---


---


# Sun-2 (796-Bus) Ethernet Board


Data Sheet

Draft Version 0.3

Company Confidential

Sun Microsystems Inc.

[date]


>
The Sun-2 (MB) Ethernet Board is a high-performance Ethernet interface
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


VLSI Ethernet controller

integrated Encoder/Decoder

up to 1 MByte of on-board memory

memory management for efficient buffer handling

memory expandable via P-2 Bus to 2 MBytes

byte parity error detection


## Introduction


The Sun-2 Ethernet Board was designed to support high-performance Ethernet
server applications, such as fileservers.
In such a system, the majority of the data is transferred between
the disk and the Ethernet. The Sun-2 Ethernet Board includes up to 256 KBytes
(64K RAMs) or 1 MByte (256k RAMs) of on-board memory that buffers data
between the Ethernet controller and the IEEE 796-Bus.
For very large server applications, the on-board memory can be expanded
up to 2 Mbytes with Sun-2 Memory Expansion boards.
All local memory is protected with byte parity error detection.

The interface between the IEEE-796 Bus and the on-board memory
includes a paged memory management unit with 1024 1K page entries.
This MMU provides for buffer management in the local memory from
the IEEE-796 Bus.

The VLSI Ethernet controller features back-to-back packet capability,
a high degree of programmability, and extensive diagnostic features.
The encoder/decoder function is implemented with a digital phase-lock loop.

---

## Specification Summary


**Ethernet Controller**

```

    Intel 82586

```


**On-board Memory**

```

    256K (64K) or 1M Bytes (256K)
    memory expandable with Sun-2 Memory Boards
    dual ported between Ethernet Controller and 796-Bus.
    byte parity error detection

```


**Memory Management**

```

    One-level page map
    1K byte pages

```


**796-Bus Compatibility**

```

    D16 M20 VOL.

```


**Electrical Characteristics**

```

    VCC = +5V +-5%
    ICC = 5A max.

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
