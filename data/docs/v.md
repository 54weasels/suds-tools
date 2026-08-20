---


---


# Sun-2 (796-Bus) Video Board


Data Sheet

Draft Version 0.3

Company Confidential

Sun Microsystems Inc.

[date]


>
The Sun-2 (MB) Video Board is a high-resolution, dual-ported frame buffer
for the Sun-2 (MB) Processor Board. It also features an audio interface
with sound generator and serial TTL-level interfaces for a keyboard and a mouse.


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


1152 by 900 pixel frame buffer

non-interlaced 70 Hz refresh

directly addressable by CPU as memory

Sun P2-Bus compatible for high-speed access

audio interface with sound generator

two serial interfaces for keyboard and mouse


## Introduction


The Sun-2 Video Board contains the video subsystem of the Sun-2 workstation.
This includes a high-resolution frame buffer, video controller, and P2-bus
interface. The video board is capable of displaying a 1152 by 900 pixel
image on a non-interlaced monitor in a flicker-free way.

The frame buffer is a dual-ported memory.
One port of the frame buffer memory is dedicated for video refresh,
displaying the frame buffer content on the high-resolution monitor.
The other port is available to the processor for updating the frame buffer.

The frame buffer memory appears to the processor like memory.
It is interfaced to the processor via the P2 bus,
allowing high-speed access from the CPU.

The Sun-2 Video Board also contains two serial interfaces with TTL levels
intended for a keyboard and a mouse pointing device.
A programmable sound generator provides audio output capabilities.

---

## Specification Summary


**Frame Buffer and Addressing**

```

    1152 by 900 pixels
    addressable as memory

```


**Frame Buffer Performance Characteristics**

```

    Cycle Time: 0.64 microseconds.

```


**Video Monitor and Video Interface**

```

    non-interlaced video monitor
    100 MHz video clock
    65 KHz horizontal
    70 Hz vertical

```


**Other Interfaces**

```

    audio interface with sound generator
    two TTL-level serial interfaces for keyboard and mouse

```


**796-Bus Compatibility**

```

    n.a. (Board only interfaces to Sun P2-Bus).

```


**Sound Generator**

```

    Three programmable oscillators, one noise source

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
