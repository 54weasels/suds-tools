---


---


# SUN Color Graphic Board Specifications


---


#### SUN Microsystems Color Frame Buffer


**Frame Buffer:**


```

	640 by 512 by 8 bit frame buffer, 640 by 485 by 8 visible.
        Frame Buffer expandable to 24 bits deep by strapping three
           boards together.
	Addressed in (x,y) coordinates.
	Separate (x,y) registers for both read and write operations.
	Cartesian coordinate system with (0,0) in upper left corner.

```


**Color Map:**


```

        24-bit wide color map with 8-bits each for Red, Green, Blue.
	Color Map Readable and Writeable in Software.
	Can simultaneously display 256 different colors
	   out of a palette of over 16 Million possible colors.
        Four color maps are selectable via a status register.

```


**Video Interface:**


```

	RS-170 compatible. Separate cables for Red, Green, Blue, Sync.
        Video interface modifiable in firmware to support certain
           non-standard interfaces (e.g. Mitsubishi`s).
	Pixel Clock:	84 nsec		11.9 Mhz
	Horizontal:	64.8 usec	15.42 khz
	Vertical:	16.56 msec	60 Hz (interlaced)

```


**Update Characteristics:**


```

	One pixel can be read, written or modified every 0.84 usec.
        Cycle time during horizontal and vertical retrace is 0.42 usec.
        All accesses to the frame buffer are fully buffered so that
           each request is acknowledged in less than 40 nsec.
        A "Paint-Mode" is available that will write five consequtive
           horizontal pixels with the same value. This allows the
           screen to be set to a background value in 52 msec.

```


**Hardware Function Unit:**


```

        Updates operate via a function unit that combines the Color
        Register, the new pixel value, and the old pixel value to
        select a bit from the Function Register. The function unit can
        execute RasterOp operations in hardware using any one of 256
        possible bit-wise boolean functions. Thus the board can
        individually access and modify each bit-plane in hardware; and,
        the color map can be quickly altered to modify the visible
        characteristics of each bit-plane (for example, if text were
        assigned to one bit-plane) or to display an interaction between
        multiple bit-planes (for example, if two doping regions were to
        overlap in a CAD application).

```


**Physical Characteristics:**


```

        Multibus* compatible. Configurable with either Intel or MC68000
           byte-order.
        Design implemented on a single 6.5" by 12.0" board.
        Device occupies only 8K of system memory space.

```


**Electrical Requirements:**


```

	VCC: +5V +- 5%. ICC: 8.0 A (max), 5.0 A (typ)
	VEE: -5V +- 10%.IEE: 0.5 A (max), 0.3 A (typ)

```
