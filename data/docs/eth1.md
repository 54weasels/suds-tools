---


---


# Sun-2 (MB) Ethernet Board


Data Sheet

Draft Version 1.1

Company Confidential

Sun Microsystems Inc.

May 11, 1983


>
The Sun-2 (MB) Ethernet Board is a high-performance Ethernet interface
compatible with the Intel Multibus.


>
Multibus is a trademark of Intel Corporation.
Sun, Sun-1, Sun-2, and DVMA are trademarks of Sun Microsystems Inc.


---


---

# Architecture Overview


## Features


VLSI Ethernet controller

integrated Encoder/Decoder

up to 512 KByte of on-board memory

memory management for efficient buffer handling

memory expandable via P-2 to 2.5 MBytes

byte parity error detection


## Introduction


The Sun-2 Ethernet Board was designed to support high-performance Ethernet
server applications, such as fileservers.
In such a system, the majority of the data is transferred between
the disk and the Ethernet. The Sun-2 Ethernet Board includes up to 512K Bytes
of on-board memory that can buffer data between the Ethernet controller
and the Multibus.
For very large server applications, the on-board memory can be expanded
up to 2.5 Mbytes with Sun-2 Memory Expansion boards.

The Ethernet controller features back-to-back packet capability,
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

    256K or 512K Bytes
    dual ported between Ethernet Controller and Multibus
    byte parity error detection

```


**Memory Management**

```

    One-level page map
    1K byte pages

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
