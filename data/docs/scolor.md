---


# SUN Graphics Board


---


# SUN 1024*1024 Graphics Board


#### Features


1024 by 1024 pixel frame buffer

800 by 1024 pixel visible display area

landscape mode or portrait mode

bit-map is organized by (x,y) coordinates

arbitrary 1 by 16 rectangles directly accessible

on-board "RasterOP" unit with 256 combination functions

Vector drawing speed: 1 pixel per microsecond

Character painting speed: 16 microseconds

Screen fill: 64 milliseconds

Single board compatible with IEEE-796 Bus/Intel Multibus

5V only operation.


#### Overview


The SUN 1024*1024 graphics board brings high-resolution and high-speed
graphics capabilities to IEEE-796/Intel Multibus based systems.

The SUN graphics board has been specifically designed for interactive applications
such as text processing, CAD, CAM, programming environments, and process control.
In particular, the SUN graphics board supports directly
composite images, combining text and graphics, multiple character sets,
variable width fonts, multi-window systems, and menus, ikons or other symbols.
In addition, the SUN graphics board is highly suited for
applications traditionally served with vector or storage tube displays.


---


---

#### Functional Description


The SUN graphics board combines a high-resolution display (1024 by 1024 pixel)
with a high-speed "RasterOp" update mechanism (screen fill in 64 milliseconds).

The displayed image is stored in a 1024 by 1024 pixel frame buffer of which
1024 by 800 pixels are visible in landscape mode and 800 by 1024 pixels
in portrait mode. The remaining 224 by 1024 invisible pixels can be used
to store characters, cursors, and other graphical symbols.

The frame buffer is a dual-port memory with one port dedicated for
video refresh and the other port available for processor updates.
In addition to the frame buffer memory, the SUN graphics board provides
the video refresh logic and special hardware to assist in frame buffer updates.
A complete graphics system requires a processor board such as the
SUN 68000 board to control the updating of the graphics board.


#### RasterOp Architecture


The SUN Graphics system incorporates the concept of "RasterOP" [Newman&Sproull].
RasterOp means that rectangular areas of display data ("raster")
are modified or combined according to a preselected operation ("Op").
RasterOp provides complete generality to paint characters, manipulate windows,
scroll screens, and to draw vectors. An example for RasterOp is shown
in Figure 1, in which a source character is copied to a destination
anded with a mask.

A highspeed RasterOp was implemented on the Xerox Alto computer [Thacker et al],
as a microcoded instruction called BitBlt (for Bit Boundary Block Transfer).
The Alto BitBlt instruction provides 8 pixel combination functions
between a destination and source raster. These functions are:
Bit-Copy, Bit-Or, Bit-Xor, Bit-And, and all of these with the source complemented.

The SUN graphics board offers a generalized version of RasterOp,
involving one, two, or three operands: destination, source, and mask.
Destination is the operand being changed in the frame buffer,
the source and mask operands can be loaded either from the frame buffer
or from main memory of the host processor.
The SUN RasterOP allows any of the possible 256 combination functions
to be selected dynamically.


![Placeholder: graph1.press]()


*Figure: **A RasterOp Operation***


---


#### Hardware/Software Interface


The SUN graphics system divides the task of executing RasterOPs between
hardware and software in such a way that maximum performance is maintained
while minimizing the hardware complexity.

In brief, the SUN graphics board is equipped with two special hardware mechanisms:
cartesian coordinate access to arbitrary 1 by 16 pixel rectangles,
and hardware execution of the raster operation.
The SUN graphics board itself does not store any control information,
such as algorithms for manipulating rectangles or drawing vectors.
All control resides in the program of the host processor.

The SUN graphics board design has been optimized for such an interface
by incorporating a number of registers to hold all state information
that relates to a particular raster operation.
This state information includes the data being manipulated,
the rasterOp function to be performed, and the (x,y) addresses of the operands.
Storing this state information locally on the graphics board extends
the register set of the host processor and allows raster operations
to proceed at full speed without having to reload critical state information.


#### Speed


A major problem with high-resolution bit-map graphics is the
time required for creating and modifying the frame buffer image.
The problem is rooted in the sheer number of bits being manipulated.
For example, if a 1024 by 1024 pixel frame buffer were updated at a rate
of 1 pixel per microsecond, it would take 1 second to fill the screen.

In comparision, the SUN graphics board, in conjunction
with a high-performance processor board such as the SUN 68000 Board,
can update 16 pixels per microsecond or fill the screen
in 64 milliseconds (excluding higher-level overhead).
Even better, the SUN graphics system achieves this speed without
a special-purpose graphics processor and is thus fully user programmable.
A high-performance microprocessor such as the 68000
or a DMA device can drive the frame buffer at its full speed.

Again, the frame buffer on the SUN graphics allows one update every microsecond.
A frame buffer update involves from one to 16 pixels.
Painting a 16 by 16 pixel character thus takes 16 microseconds,
drawing vectors takes 1 microsecond per pixel, excluding overhead.


#### References


A.  Bechtolsheim and F.  Baskett, "High-Performance Raster Graphics for
Microcomputer Systems", *Proceedings SIGGRAPH Conference*, Seattle, July 1980.

W. M. Newman and R. F. Sproull, *Principles of Interactive Computer Graphics*,
second edition,	McGraw Hill, 1979.

C. P. Thacker, E. M. McCreight, B. W. Lampson, R. F. Sproull, and D. R. Boggs,
"Alto: A personal Computer", in Siewiorek, Bell, and Newell, eds.,
*Computer Structures: Readings and Examples*, McGraw Hill, 1979.


---


---

#### Frame Buffer and Addressing


The frame buffer is a dual ported memory, providing
storage for a 1024 by 1024 pixel bitmap image.
One port of the frame buffer connects to the host processor,
the other port is dedicated for video-refresh, with priority
given to the video refresh. The processor port can access
the frame buffer once every microsecond for a 16-bit operation.

The frame buffer is addressed in a cartesian coordinate system,
in which (0,0) is the upper-left corner of the screen.
From one to 16 horizontal pixels can be read or written in
a single cycle, starting at the current (x,y) position,
with the data bits within a word being left justified.
For example, a 4-bit update at location (200,300) will write
the most significant four data bits (D15 through D12)
into location (200,300) through (203,300).


#### Display Monitor


The SUN graphics is designed to drive a high-resolution
interlaced monitor, either in landscape or in portrait mode.
The nominal display area is 1024 by 800 pixel in landscape mode
or 800 by 1024 pixels in portrait mode.
Decomposite video, horizontal, and vertical synchronization is provided.
Display formats, refresh rates, and sync polarity is firmware programmable.

For white displays, flicker is reduced by using monitors
with the slower P40 phosphor, instead of the P4 phosphor normally used.
For green displays, P39 phosphor provides a pleasant looking display
with very little flicker.


![Placeholder: graph2.press]()


*Figure: **Video Monitor Display Area***


---


---

#### Registers and Function Unit


Figure 3 shows the registers of the SUN graphics board.
There are three data registers, destination, source, and data,
feeding into the function unit.
These registers can be loaded from the host processor on a
write cycle and from the frame buffer memory on a read cycle.
There are three registers controlling update operation:
function, width, and status.
There are four sets of (x,y) registers for addressing.


![Placeholder: graph3.press]()


*Figure: **SUN Graphics Board Block Diagram***


**Destination Register**

The destination register holds the data that is being
modified with a read-modify-write cycle on update operations
in the frame buffer.

**Source Register**

The source register holds data to be combined with the destination data
and the mask data to compose new data for the frame buffer.
The source register can be loaded from the frame buffer or from the processor.
The data in the source register is bit-wise aligned with
the bit-address of the destination in the frame buffer.

**Mask Register**

Similarly to the source register, the mask register
holds data to be combined with the destination register
and the source register to compose new data for the frame buffer.
Again, the mask register can be loaded either from the frame buffer
or from the IEEE-796 Bus.
The difference between the mask register and the source register is
that the mask register value is not bit-aligned with the (x) position
of the destination in the frame buffer.
Instead, the mask register is aligned with location (x MOD 16 = 0).
The mask register is intended for background coloring and stipple-pattern
generation where bit-alignment is undesirable.

**Function Register**

The function register specifies how the function unit
combines destination, source, and mask data when data is written
into the frame buffer memory.
There are 256 possible raster operations for three boolean operands.
The function register selects one of these at a time by acting as a function table
that is indexed by the value of (destination*2@+(0)+ source*2@+(1) + mask*2@+(2)).
For example, a bit-clear function is 0, bit-set is 0xFF, bit-OR is 0xFE,
and bit-AND is 0X80. A good way to find out what a function should be is
to write down its desired truth table.

**Width Register**

The actual width of an update operation is programmable via the `WIDTH` register
from 1 to 16 pixels.

**Control Registers**

The control register controls video enable, interrupt enable, and interrupt level
assigned as follows:


    D12..D15	Interrupt level
    D10..D11	Reserved
    D9		Video Enable
    D8		Interrupt Enable


The Video Enable bit turns on video to the monitor, the screen appears
blank when this bit is off. The Interrupt enable Bit enables interrupts
on the level selected. When enabled, an interrupt is generated
at the beginning of every vertical retrace, allowing synchronization
of display updates with display refresh. The Interrupt flag stays
pending until reset in software by accessing the Interrupt Acknowledge
location.

The control register is cleared (set to zero) on INIT to guarantee
a blank screen and disabled interrupts when the display board is powered up.

**X-Y Registers**

The host processor accesses graphical objects in the frame buffer via
(x-y) register pairs. Four sets of (x-y) registers are provided
that can be selected dynamically via the address bus.
Only one (x) or (y) register is updated at one time,
the other registers do not change.

**Operation Selection**

In addition to the (x-y) address, additional information is sent
as part of the address to the SUN graphics board
further specifying the desired operation.


---


#### IEEE-796 Bus Interface


The SUN graphics board uses both the data and the address lines of the IEEE-796 Bus
to maximize the information that can be sent to the graphics in one bus cycle.
In a single cycle, the controlling processor can transfer a new 16-bit data item
via the data bus and a new (x) or (y) address via the address bus.
At the same time, the processor can select which of the four
set of (x,y) registers to use, whether to load a register
from the data bus or from the frame buffer, whether to load the source
or the mask register, and whether to execute a frame buffer update or not.
Refer to the technical reference summary as to how this information
is encoded on the IEEE-796 Bus.

On a Write cycle, three things happen sequentially.
First, data from the IEEE-796 Bus is written into
the selected register on the graphics board (or no register).
Second, the addressed (x,y) location is read into the destination register.
Third, if and only if an update is requested, the data stored in the destination,
source, and mask registers is combined according to the preselected function
and new data is written back into the addressed frame buffer location.

On a Read cycle, two things happen.
First, data is read from the addressed (x,y) location in the frame buffer
into the selected register on the graphics board.
Second, the data then stored in the source register is returned
to the IEEE-796 Bus, correctly bit-aligned with the bus data lines.
The frame buffer is never updated on a read cycle
and the update bit is ignored for read cycles.

A one-deep FIFO decouples the graphics board from the controlling processor.
Processor requests are latched on the graphics board and are subsequently executed
independently and in parallel with the processor.
This makes the frame buffer a zero-access time device
as long as the request rate does not exceed one request per microsecond.
Since normally streams of data are being transferred,
the pipelining maximizes throughput.

On write cycles, the FIFO operation is fully transparent, that is, invisible.
On read cycles, however, because of the pipelining the data read back
corresponds to the previous read request. Thus, to read a stream of data,
one additional word needs to be read before valid data is obtained.


---


---

#### Specifications


**Frame Buffer and Addressing**

```

	1024 by 1024 by 1, addressable in (x,y) coordinates.
	Cartesian coordinate system with (0,0) in upper left corner.
	Four sets of (x,y) registers are provided.
	Each (x,y) registers pair points to a 1 by 16 pixel element.
	(x,y) registers are updated by accessing the respective register.

```


**Video Monitor Compatibility**

```

	Compatible with high-resolution interlaced monitors, e.g.:
	Ball HD-Series, ITOH QFD-1530V, Motorola M4408

```


**Video Interface**

```

	Decomposite synchronization and video signals.
	TTL-levels, positive logic, negative logic available as option
	ECL-levels available as option

	Portrait: Nominal display area: 800 pixel by 1024 pixel.
	Nominal pixel clock: 31.25 MHz.
	Nominal horizontal frequency: 30.5 kHz.
	Nominal vertical frequency: 60 Hz.

	Landscape: Nominal display area: 1024 pixel by 800 pixel.
	Nominal pixel clock: 32 MHz.
	Nominal horizontal frequency: 25 kHz.
	Nominal vertical frequency: 60 Hz.

	Other formats and frequencies optionally available.

```


**Update Characteristics**

```

	One frame buffer update every microsecond.
	Update width is selectable from 1 to 16 bits.
	Raster operation modifies destination data in frame buffer
	in conjunction with source and mask data previously loaded.
	Any one of the 256 possible raster operations can be selected.
	Source and mask data can be loaded from frame buffer
	or from the data bus.

```


**796-Bus Compatibility**

```

	D16 M20 VOL, 16-bit data only.

```


**Electrical Characteristics**

```

	+ 5V +- 5%.  Maximum current: 5 A.

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

	Operating Temparature: 0-50 C

```


---


---

#### Appendix: IEEE 796 Bus Interface


```


	D0..D15	New 16-bit data, read or write

	A1..10	New X or Y address

	A11	0 -> X,  1 -> Y

	A12..13	Selects one of the four sets of (x,y) registers

	A14..15	Select data register to be updated
		On *read cycles*, data is supplied from frame buffer
		On *write cycles*, data is supplied from processor

			0 -> No Register
			1 -> Control Registers
			2 -> Source Register
			3 -> Mask Register

		Control register are further decoded with A1..A2 as follows:

			0 -> Function Register
			1 -> Width Register
			2 -> Control Registers
			3 -> Interrupt Acknowledge

	A16	Enable raster operation on frame buffer

			0 -> no update operation
			1 -> execute update operation

	A17..19	Module Select

	MEMR	IEEE-796 Read Strobe

	MEMW	IEEE-796 Write Strobe

	XACK	IEEE-796 Acknowledge

	INT0..7	Interrupt request. Priority level selectable in software.

	INIT	Initialization, clears control register.

```
