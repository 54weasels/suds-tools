---


---


# Sun-2 Color Graphics Board


# User Manual


Sun Microsystems Inc

November 1983

Company Confidential

Revision 1.1


>
The Sun-2 Color Graphics Board is a bitmap graphics subsystem
offering a 900-line 60 Hz non-interlaced display, 256 simultaneously
displayable colors, "RasterOp" hardware support, integer zoom (1x - 16x),
pixel pan, and ten separate addressing modes.

This document describes the architecture, programming,
and the installation of the Sun-2 Color Graphics Board.


>
Sun is a trademark of Sun Microsystems Inc.


---


---

# System Architecture


## Overview


The color Sun-2 is a member of the Sun-2 family of workstations. The color
Sun-2 offers the same resolution and display characteristics as the
monochrome Sun-2 but with eight bits per pixel. The color and monochrome
Sun-2 workstations are architecturally compatible to allow the same
applications programs to run transparently on either machine.

The Sun-1 cclor provides medium resolution graphics at low cost in an
RS170A compatible output. The Sun-2 color unit provides a state of the art
flicker-free color resolution compatible with the Sun-2 monochrome display.


## Features


Color workstation transparently executes software written for monochrome workstation

Screen resolution 900 by 1152 with 8 bits per pixel

Screen aspect ratio of 3:4 results in the generation of square pixels

Flicker-free 60 Hz non-interlaced operation

Integer Zoom of 0 to 15 via pixel replication in hardware

Pan in increments of a single pixel

Variable height non-zoomed region at bottom of display

Frame buffer addressable ten different ways for different types of applications

Frame buffer addressable as memory or with RasterOp support

Separate RasterOp unit for each bit plane

Translation and Raster Operations on up to 128 bits in parallel

Write accesses only incur no MC68010 wait states

Frame buffer cycle time of 690 nsec (215 nsec during video blanking)

Hardware protection of arbitrary bit planes for window applications

Color Map selects 256 colors from a palette of 16 million


---

## The Frame Buffer


### Addressing Modes


The Sun-2 color frame buffer has ten addressing modes. The first addressing
mode (Word-Mode Memory) is strictly compatible with the monochrome Sun-2 and
allows the rasterop chip on the Sun-2 processor to operate directly on the
Sun-2 color board. The third and fifth addressing modes (Word-Mode with
RasterOp and Word-Mode with RasterOp and Hidden Read) provide the same function
as the first addressing mode using the processor rasterop chip;
however, the third and fifth addressing modes execute much faster than if
the first addressing mode together with the processor rasterop chip were to
be used. In fact, when the processor rasterop chip is not used, writes to
the color frame buffer respond with an immediate transfer acknowledge such
that CPU and color board processing can be fully overlapped.

While word-mode accesses will be preferred for text-intensive and window
operations, pixel-mode accesses will be preferred for image processing
and other applications where only single pixels will be modified with
each access.

Accesses to the color frame buffer can be eight, sixteen or thirty-two
bit; however, all writes to the Rasterop units should be in sixteen bit
increments.

The ten addressing modes are:


```


	* Word-Mode Memory. Frame buffer appears as a stack of eight
		memory planes. Each memory plane is equivalent to 128KB
		of system memory. A word accesses addresses 16 adjacent
		bits within a bit plane.

	* Pixel-Mode Memory. Frame buffer appears as 1 Million 8-bit
		deep pixels. Memory planes masked by the per-plane mask
		register are read and write protected. 16/32 bit accesses
		transfer 2/4 pixels simultaneously, but the cycle time
		of these operations is 2/4 times longer than normal.

	* Word-Mode with RasterOp. Frame buffer reads load destination
		Register on each rasterop chip (ROPC). Write data written
		to ROPC source registers and ROPC output written to frame
		buffer.

	* Pixel-Mode with RasterOp. Frame buffer reads load ROPC destination.
		Writes load per-plane source registers with either all
		zeros or ones; for instance, writing 0xAA will load the
		Source on even bit-planes with zeros and odd bit-planes with
		ones. Memory planes masked by the per-plane mask register
		are read and write protected.

```


---


```


	* Word-Mode With RasterOp and Hidden Read. The rasterop chip on the
		Sun-2 CPU normally performs a read-modify-write cycle on memory
		where the read data is loaded into the ROPC destination
		register, the write data is loaded into the ROPC source
		register, and the ROPC output is written back to memory.
		On the Sun-2 color with the "Hidden Read" addressing
		modes, writing to the color board executes a read cycle
		followed by a write cycle. "Hidden Read" accesses perform
		the same function as the normal ROPC read-modify-write cycle,
		but unfortunately take double the normal frame buffer memory
		cycle time to complete. Read accesses using this addressing mode
		do not affect the rasterop chips and appear as normal word-mode
		reads.
	* Pixel-Mode With RasterOp and Hidden Read. Frame buffer reads do not
		load rasterop destination registers and act like normal pixel-mode
		reads. Frame buffer writes immediately load the ROPC source
		registers then initiate a frame buffer read cycle to load the
		rasterop destination registers. ROPC output then written to the
		frame buffer. Write accesses take double the normal frame buffer
		cycle time to complete.

 	* Parallel Word-Mode with RasterOp. Frame Buffer reads load ROPC
		*source* registers 128 bits in parallel. With frame buffer
		writes, the write data is ignored and the ROPC outputs are
		written to all memory planes enabled by the per-plane mask
		register. This addressing mode is useful for moving windows.

	* Parallel Pixel-Mode with RasterOp. Frame buffer reads load ROPC
		destination. Writes load per-plane source registers with
		either all zeros or ones; for instance, writing 0xAA will
		load the Source on even bit-planes with zeros and odd
		bit-planes with	ones. Memory planes masked by the per-plane
		mask register are read and write protected. ROPC output
		written to 16 adjacent pixels along word (16-pixel) boundaries,
		and ROPC *Mask1 and Mask2 registers* can be used to further
		protect specific pixels from update.

	* Parallel Word-Mode with RasterOp and Hidden Read. Frame buffer
		reads load ROPC *source* registers 128 bits in parallel.
		With frame buffer writes, the write data is ignored, a
		read cycle is performed to load the ROPC destination registers
		and then a write cycle is performed to write the ROPC outputs
		to all memory planes enabled by the per-plane mask register.
		Write accesses take two memory cycles to complete using this
		addressing mode.

	* Parallel Pixel-Mode With RasterOp and Hidden Read. Frame buffer
		reads do not load rasterop destination registers. Frame buffer
		writes cause a read cycle to load rasterop destination registers
		after the write data has been written to ROPC source registers.
		Write accesses take two	memory cycles to complete. ROPC output
		written to 16 adjacent pixels along word (16-pixel) boundaries.
		Write accesses take double the normal frame buffer cycle time
		to complete.


```


---

### Pixel-Mode Addressing


In pixel-mode, each pixel occupies a byte value.
Assuming Pan and Zoom are disabled, pixel number 0 is in the
upper left corner of the screen and successive pixels are displayed
horizontally towards the right. At each "MOD 1152" pixel address,
a new vertical line is started. Mapped as memory, the pixel data written
to the device will enter the frame buffer without modification. Mapped
through the RasterOp unit, the byte value written to the device will be
written to the RasterOp chip source registers and the ROPC output will
be written to sixteen adjacent pixels in the frame buffer. Both with
and without RasterOp support, an arbitrary selection of bit planes
can be masked from reads or writes by the Per-Plane Mask Register.
Addressing the frame buffer in pixel-mode with RasterOp support is
invaluable for performing rapid area fills.


![sc11.press](../svg/sc11.drw.O.svg)


*Figure: **Pixel-Mode Frame Buffer Addressing***

<a id="pixaddr"></a>


---

### Word-Mode Addressing

In word-mode, the frame buffer is configured as eight separate bit planes.
Each bit plane occupies a separate 128 Kbyte block of the system address
space, and each bit plane by itself is architecturally identical to the
black and white frame buffer. In this addressing mode, writing to the
device will alter 16 horizontally adjacent pixels. Word 0
is in the upper left corner of the display, and each scan line
is 72 words wide (1152/16 = 72). The most significant bit of a word
appears to the left of the least significant bit of a word. Data
written in word-mode can be written directly to the frame buffer or it
can be optionally combined via the RasterOp unit with the data currently
at that address. This set of addressing
modes, in conjunction with the RasterOp chips, is particularly suited for
painting character data. For example, a 15-bit wide character
starting at an arbitrary pixel location could
could be drawn in 30 CPU move instructions after the RasterOp chips were
properly initialized.


![sc12.press](../svg/sc12v.drw.O.svg)


*Figure: **Word-Mode Frame Buffer Addressing***

<a id="wordaddr"></a>


---

A word-mode access will only address one of the eight memory planes of the
frame buffer. However, there are two addressing modes which access all
eight memory planes in parallel. Using these modes is useful for such
operations as dragging a window on the display.

The color frame buffer memory is dual ported. One port connects to the
synchronous system bus and the second is dedicated to video refresh which has
priority over system bus accesses. A new datum can be read or
written to the Sun-2 color frame buffer every 640 nsec, and during blanking
and at large zoom factors the frame buffer cycle time drops to 200 nsec.

While a standard color configuration will consist of 8 bits per pixel,
Sun-2 color video boards can be stacked three deep to provide eight
bits each for red, green, and blue. In this configuration, each board
lies in a separate address space, but the timings of the boards are
synchronized to properly overlap the red, green, and blue images
generated by each board.

---

## A Virtual Frame Buffer


The Sun-2 color frame buffer was designed to implement some features of a
virtual frame buffer. While a single display may be driven from a single
physical frame buffer, a virtual frame buffer implements hardware protection
features preventing one process from overwriting the output of another
in a multi-window environment. In this manner, a single frame buffer
appears as several logical frame buffers. Each process accessing the
physical frame buffer is allocated a separate logical frame buffer
by the host operating system software.

The Sun-2 color frame buffer allows processes to be mapped to a variable
number of bit planes. In this manner, a program having a 7-bit view
of the frame buffer can share the device with programs having, for
instance, 6-bit, 4-bit, or 1-bit views of the frame buffer.
The Sun-2 color board does not provide clipping hardware, but it can
prevent a process from writing to any set of bit planes.
When accessed in word-mode or parallel word-mode, the frame buffer is
protected by the main processor`s memory maps. In pixel-mode,
a *Per-Plane Mask Register* provides bit-plane protection by specifying which
bit planes can be updated. Likewise, during pixel-read, the
mask register determines which bit planes are read; all other bits
in the pixel are set to zero. In this manner, each window on the display
can be dynamically allocated a range of colors that appear to begin at zero.
This feature is useful because it obviates the need for a program sharing
the frame buffer to add a variable base to each pixel written
or to subtract the same variable base from each pixel value read.

In a typical scenario,
a CAD program may be running with three separate windows. Two of these
windows might wish to use 16 colors and the third may wish to use
64 colors. The window system could allocate colors 0 through 15 for the first
window, colors 16 through 31 for the second window, and colors 64 through 127
for the third window. Once the high-order frame buffer bits for each window
are initialized, the window system, using the per-plane mask register,
can protect the appropriate bit-planes
for each window. The processes running in the first two windows will both read
and write byte values 0 to 15 to the frame buffer, and the process running
in the third window will be able to read and write byte quantities from
0 to 63 to its window. In this way, the color values allocated to each
window can always start with zero and programs writing to the color frame
buffer do not have to worry about overwriting valid bits in other bit planes.

---

## RasterOp Architecture


The Sun Graphics system incorporates the concept of "rasterop".
Rasterop means that rectangular areas of display data ("Raster")
are modified or combined according to a preselected operation ("Op").
Rasterop provides complete generality to paint characters, manipulate windows,
scroll screens, and to draw vectors. Write accesses to the Sun-2 color
frame buffer can be routed through the rasterop Unit to operate on word or
pixel data. An example for
RasterOp is shown in Figure [Figure](#RasterOp), in which a source character
is copied to a destination anded with a pattern mask.


![sc13.press](../svg/sc13.drw.O.svg)


*Figure: **A Raster Operation***

<a id="RasterOp"></a>


During a rasterop, the pixels accessed in the frame buffer are modified
according to one of 256 possible bit functions operating on the source
data, the destination data, and the pattern mask data. The pattern mask
is loaded from the processor, the destination data is the frame buffer data
being modified, and the source data is the 16-bit quantity being written to
the color graphics board.
In addition, each rasterop unit consists of a left mask, a right mask, a barrel
shifter for the source data, and raster width information
which accelerate writing arbitrarily sized rasters into variable starting
pixel locations.

There is a separate rasterop unit for each memory plane in the frame buffer.
They can be operated individually or in parallel to update as many as 128
frame buffer bits simultaneously.

Parallel word-mode rasterops are conceptually identical to word-mode rasterops
on a single bit plane; parallel pixel-mode rasterops, however, are different.
With parallel pixel-mode rasterops, all pixels falling between modulo 16
pixel boundaries will be accessed. For instance, using rasterops on any pixel
numbered 16 through 31 will access all the pixels between 16 and 31. To mask
specifiec pixels from update when using rasterops, the masks internal to the
rasterop chips should be used. For more information on the rasterop chips,
please refer to section [Figure](#aropc).

---

## Speed


A major problem with high-resolution bit-map graphics is the
time required for creating and modifying the frame buffer image.
The problem is rooted in the sheer number of bits being manipulated.
For example, if a 900 by 1152 pixel frame buffer were updated at a rate
of 1 pixel per microsecond, it would take 1 second to fill the screen.

The Sun-2 color workstation operates without MC68010 wait states on
control register and frame buffer writes.
The color workstation operates with two wait states on control register
reads and frame
buffer reads take from three to ten wait states to complete.

As an example of the speed of a color system, writting a constant
to the entire display would take roughly 43 msec (32K long-word move
instructions on a 10 MHz processor).
Likewise, painting an  arbitrarily positioned
12 by 12 character would take approximately 30 usec (24 word move instructions
at 1200 nsec per instruction); this speed in displaying text translates
to 32K baud.

Applications packages always want faster graphics. Three hardware specific
actions can be taken to improve color performance. First,
read operations are much slower than write operations and should be minimized.
As a corallary, using the Rasterop chip on the CPU board rather than the
Rasterop chips on the color board will continually generate color frame buffer
reads and will degrade the system performance.

Secondly, sixteen bit accesses in pixel-mode incur a doubling of the frame
buffer cycle time compared to sixteen bit word-mode accesses. Sixteen and
thirty-two bit pixel-mode accesses should be replaced with word-mode accesses
whenever possible.

Lastly, the frame buffer cycle time drops from 690 nsec to 215 nsec during
horizontal retrace and at large values of zoom. Applications loading or
storing the entire contents of the frame buffer might consider disabling
video output and setting zoom to the maximum value before performing these
memory intensive operations.

A.  Bechtolsheim and F.  Baskett, "High-Performance Raster Graphics for
Microcomputer Systems", *Proceedings SIGGRAPH Conference*, Seattle, July 1980.

W. M. Newman and R. F. Sproull, *Principles of Interactive Computer Graphics*,
second edition,	McGraw Hill, 1979.

C. P. Thacker, E. M. McCreight, B. W. Lampson, R. F. Sproull, and D. R. Boggs,
"Alto: A personal Computer", in Siewiorek, Bell, and Newell, eds.,
*Computer Structures: Readings and Examples*, McGraw Hill, 1979.


---

## Specification Summary


**Frame Buffer and Update Characteristics**

```

	Pixel area of 900 by 1152 by 8
	Pixel depth expandable to 24 bits per pixel
	Frame buffer architecture compatible with monochrome architecture
	Frame buffer adressable as depth-wise or width-wise within bit planes
	One RasterOp unit per bit plane
	Updates on upto 128 bits in parallel
	Per-Plane Mask register protects bit-planes from update
	Frame buffer cycle time of 690 nsec
	Memory cycle time of 215 nsec during horizontal retrace and at large zoom
	Frame buffer writes buffered to overlap color board and MC68010 processing

```


**Color Map**

```

	Selects 256 colors from palette of 16 million
	Addressable even during video display

```


**Zoom and Pan**

```

	One to eleven times magnification with pixel replication
	Pan in increments of a single pixel horizontally or vertically
	Variable width non-zoomed region at bottom of display

```


**Video Monitor and Video Interface**

```

	60 Hz non-interlaced vertical, 61 kHz horizontal
	92.75 MHz video rate
	Separate horizontal and vertical sync (0-5 Vpp)
	Separate RGB analog inputs (0.7 Volts peak-to-peak)

```


**Electrical Characteristics**

```

	+ 5.0V +- 10%.  Maximum current: 20 A.
	- 5.2V +- 10%.  Maximum current:  6 A.

```


**Physical Characteristics**

```

	Triple-Height Eurocard form-factor
	Width:  400 mm
	Height: 360 mm
	Depth:  0.66 in. (1.66 cm)
	Weight: 48 oz.   (1400 g)

```


**Environmental Characteristics**

```

	Operating Temperature: 0-50 C
	Operating Humidity: 0-90% non-condensing

```


---

# Programming the Sun-2 Color Graphics Board


This section provides detailed information about the functions
and the registers of the Sun-2 color graphics board. These include
the color map, zoom and pan registers, the status register, and the
per-plane RasterOp units.


## Coordinate System


The frame buffer memory is configured as a memory image; the frame
buffer is not addressed in cartesian coordinates.
In pixel-mode, the Sun-2 color frame buffer appears as one million
8-bit pixels.
In word-mode, the Sun-2 color frame buffer appears as a stack of
eight 128 KByte monochrome frame buffers.
Writes to the frame buffer can be optionally mapped through the RasterOp units.

In pixel-mode, pixel number 0 is in the upper-left corner of the
frame buffer pixel number 1151 is in the upper-right corner of the
corner. Scan line "n" in the frame buffer (0 <= n < 910) always begins
at pixel number "n*1152" and ends at pixel number "n*1152 + 1151".

In word-mode, each scan line in the frame buffer is 72 words wide
(1152 pixels/line divided by 16 pixels/word gives 72 words/line).
The MSB of word number zero for some bit plane is located in the
upper left corner of the frame buffer, and the LSB of word 71 for some
bit plane is located in the upper right corner of the frame buffer.
Each successive scan line in the frame buffer occupies another 72 words.

The use of hardware zoom and pan does not change the addressing of the
color frame buffer; it alters the region of the frame buffer that is
actually displayed. Because of zoom and pan, a frame buffer scan line
is not equivalent to a monitor scan line. For instance, let us pan until
pixel "n" is in the upper left corner of the CRT monitor. If the zoom
factor is 14 (magnification 15 times), then pixel "n + (1152 DIV 15)"
will be the last pixel on the monitor scan line. This monitor scan
line will now be redrawn 15 times and the next monitor scan line will
begin with pixel "n + 1152". Pan and Zoom are discussed further in
section [Figure](#zandp).

---

## Per-Plane Mask Register


The per-plane mask register is used for restricting frame buffer access to
some bit planes.

In pixel-mode, a '0' bit in the per-plane mask register will prevent
modification of
the corresponding bit plane during writes, and will cause a zero to be
returned from that bit plane during reads. Masking of bit planes
on read operations allows arithmetic to be performed on a subset
of the bit-planes while saving a per-pixel "and" instruction in software
and maintaining a consistent model of a variable depth frame buffer.

In word-mode, the per-plane mask register has no effect.
However, in parallel word-mode,
data is written from the RasterOp chips to all bit planes in parallel.
The per-plane mask register selectively enables/disables bit planes from update.
Hardware protection for word-mode accesses to bit planes zero through
seven is effected by using the processor memory maps.


```


	    Mask Register		     Protection
	    -------------		----------------------
	     0B XXXXXXX0		Bit Plane  0 Protected
	     0B XXXXXX0X	 	Bit Plane  1 Protected
	     0B XXXXX0XX	 	Bit Plane  2 Protected
	     0B XXXX0XXX	 	Bit Plane  3 Protected
	     0B XXX0XXXX	 	Bit Plane  4 Protected
	     0B XX0XXXXX	 	Bit Plane  5 Protected
	     0B X0XXXXXX  		Bit Plane  6 Protected
	     0B 0XXXXXXX		Bit Plane  7 Protected


```


---

## Zoom and Pan

<a id="zandp"></a>

The Sun-2 Color workstation supports pixel pan and zoom in integer
magnifications of zero to ten. Zoom magnifications of eleven to fifteen
can be used, but they impose some restrictions on panning which will
be detailed later.

The zoom register is a byte register. The least-significant nibble holds a
value specifying the size on the monitor to display a single frame buffer pixel.


```

	   Zoom 	Monitor Pixel Size
	   ----		------------------
	     0		      1 x  1
	     1	              2 x  2
	     2                3 x  3
	     3                4 x  4
             4	              5 x  5
	     5                6 x  6
	     6                7 x  7
	     7                8 x  8
	     8                9 x  9
	     9               10 x 10
	    10               11 x 11
	    11               12 x 12
	    12               13 x 13
	    13               14 x 14
	    14               15 x 15
	    15               16 x 16

```


Pan information is split across three separate registers. Primarily this
information is the 20-bit pixel address of the point to be the origin.

The Sun-2 color board additionally offers an added degree of granularity
when panning. In the vertical direction, a four-bit field called the
"line_offset" can be used to limit panning to one screen phosphor at a time.
A screen phosphor is the height of a pixel when zoom is disabled.
In the horizontal direction, a four-bit field called the "pixel_offset" can
be used to limit panning to between one and four screen phosphors at a time.

To understand the use of the line_offset and pixel_offset register fields,
assume that we are starting from a pixel address. From this pixel address,
we can compute the approximate (X,Y) coordinates of the origin. In this
case, "X" is in the range 0 to 1151, and "Y" is in the range 0 to 909.

Now let us rescale our coordinate system such that:


```

   The zoomed coordinate space consists of all (X',Y') pairs such that
                0 ≤ X' < 1152 * (zoom + 1)
		0 ≤ Y' <  910 * (zoom + 1)

   In the zoomed coordinate space, the origin is the point (X',Y') such that
		X' = (X * (zoom + 1)) + (pixel_offset * 4)
		Y' = (Y * (zoom + 1)) + (zoom - line_offset)

```


The above formulas assume that "line_offset" is not greater than "zoom", and
the above formulas do not account for the boundary condition where we
wrap to the next horizontal line. To be completely precise, the value "line_offset"
is the number of times we redraw the first line on the display.

In the above formulas, the value "pixel_offset * 4" *can be larger* than the
value "zoom". If we are careful to keep X' within its legal range, we can
use this quirk in the hardware to further smooth panning for even values
of zoom.

---

For zoom magnifications of zero to ten, all pan possibilities can be excercised.
Above zoom ten, some values of pan will result in the right-hand edge of the
monitor being improperly displayed. Above zoom ten, the following formula
should be satisfied:


```

   (zoom + 1) * ((pixel_addr_of_origin MOD 16) DIV 4) + pixel_offset ≤ 81

```


As a brief example of zoom and pan, assume that we wish to set the zoom register
to a value of two and assume that we
wish to smoothly pan our display origin horizontally towards the right
from the frame buffer origin. The following code
performs the operation while preventing wrap-around of the display:


```

#define MOD %
#define DIV /
#define zoom 2
#define zfactor (zoom+1)	/* Size of magnified pixels is 3 x 3 */
#define FB_width (1152*zfactor)	/* Width of frame buffer in new coord system */

short *zoom_reg  = (SC_control + sc_zoom_addr);
short *word_pan  = (SC_control + sc_wpan_addr);
short *pixel_pan = (SC_control + sc_ppan_addr);

procedure pan_at_zoom2();
{  int x,x1,x2;			/* Current X coord of origin */
   short pixoff;		/* Horizontal zoom for first pixel */

   *zoom_reg  = (zoom<<4)+zoom;	/* Set zoom and height of first line to 12 */
   *word_pan  = 0;		/* Set monitor origin to word 0 */
   *pixel_pan = 0;		/* Set monitor origin to MSB of word 0 */

   x2 = 0;
   while (x2 < (FB_width - FB_width/zfactor)) {
      Wait_for_Vertical_Retrace;
      x2 += 1;
      pixoff = x2 MOD zfactor;
      x = x2 DIV zfactor;

      x1 = x - pixoff;
      if (x1 == -2) {		/* Deal with initial boundary condition */
	 x1 = 0xFFFFE;		/* After 0xFFFFF the pixel addr wraps to 0 */
      } else if (x1 == -1) {
	 x1 = 0xFFFFF;
      }

      *pixel_pan = (short)(x << 4);	/* Low four bits of pixel address */
      *pixel_pan |= pixoff;		/* Add in pixel offset field */
      *word_pan  = (short)(x >> 4);     /* High four bits of pixel address */
   }
}

```


The addressable frame buffer memory of the Sun-2 color graphics board is
configured as 910 lines of 1152 pixels.
If the pan base starts too far to the right in a scan line, the start of the
next scan line will wrap onto the end of the current scan line. Likewise,
if the pan base starts too close to the bottom of the display, the top of the
screen will wrap to the bottom of the screen.

Any changes to the zoom and pan registers do not take effect until the
start of vertical retrace.
Note that there is a small chance that one register may be updated just
before the start of vertical retrace while another may be updated just
after the start of vertical retrace. In this case, the video output
will be invalid
for 1/60th of a second. By coding consecutive move intructions
to these registers, however, the likelihood of this occurrance is only
one in 10,000. If zoom and pan are updated by an interrupt routine serviced
within 16 msec of the interrupt, this event will never occur.

---


Lastly, one problem with zooming an image is that text overlaying the image
is also zoomed. With a menu-driven software package, steps must be taken
to ensure that the menu remains usable. With the Sun-2 color graphics
controller, a variable number of lines at the bottom of the display
may remain non-zoomed. The Variable Zoom Register specifies the line
number after which the zoom will return to zero. The granularity of the
variable zoom register is four lines; the two least-significant bits of
the line number are assumed zero. The origin of this
non-zoomed region of the display is always set to pixel zero. Handling
of the two separate origins, which may both be at the top of memory,
must be handled by software.

The bit assignments to the registers controlling zoom and pan are
as follows:


```

   Register Name       Bit	 Function
   -------------       ---       --------
   Word Pan Register   D15	 Origin. Pixel Address (Bit A19)
		       D14	 Origin. Pixel Address (Bit A18)
		       D13	 Origin. Pixel Address (Bit A17)
		       D12	 Origin. Pixel Address (Bit A16)
		       D11	 Origin. Pixel Address (Bit A15)
		       D10	 Origin. Pixel Address (Bit A14)
		       D09	 Origin. Pixel Address (Bit A13)
		       D08	 Origin. Pixel Address (Bit A12)
		       D07	 Origin. Pixel Address (Bit A11)
		       D06	 Origin. Pixel Address (Bit A10)
		       D05	 Origin. Pixel Address (Bit A09)
		       D04	 Origin. Pixel Address (Bit A08)
		       D03	 Origin. Pixel Address (Bit A07)
		       D02	 Origin. Pixel Address (Bit A06)
		       D01	 Origin. Pixel Address (Bit A05)
		       D00	 Origin. Pixel Address (Bit A04)

   Pixel Pan Register
		       D07	 Origin. Pixel Address (Bit A03)
		       D06	 Origin. Pixel Address (Bit A02)
		       D05	 Origin. Pixel Address (Bit A01)
		       D04	 Origin. Pixel Address (Bit A00)
		       D03	 Pixel Offset (Bit 3)
		       D02	 Pixel Offset (Bit 2)
		       D01	 Pixel Offset (Bit 1)
		       D00	 Pixel Offset (Bit 0)

   Zoom Register       D07       Line Offset (Bit 3)
		       D06   	 Line Offset (Bit 2)
		       D05   	 Line Offset (Bit 1)
		       D04   	 Line Offset (Bit 0)
	  	       D03	 Zoom (Bit 3)
		       D02	 Zoom (Bit 2)
		       D01	 Zoom (Bit 1)
		       D00	 Zoom (Bit 0)

   Variable Zoom Reg   D07	 Resets zoom after specified line (Bit 9)
		       D06	 Resets zoom after specified line (Bit 8)
		       D05	 Resets zoom after specified line (Bit 7)
		       D04	 Resets zoom after specified line (Bit 6)
		       D03	 Resets zoom after specified line (Bit 5)
		       D02	 Resets zoom after specified line (Bit 4)
		       D01	 Resets zoom after specified line (Bit 3)
		       D00	 Resets zoom after specified line (Bit 2)
				 Bits 1..0 of specified line are zero.

```


---

## RasterOp Units


There exists a separate rasterop unit for each memory plane in the frame
buffer, and the data paths
connecting and coordinating these per-plane rasterop units are a bit complex.
This section attempts to explain the interconnection of these per-plane
rasterop units. This section assumes a general familiarity with
the concepts and terminology of "rasterop". For a better understanding of
the operation of a single rasterop unit, please refer to section [Figure](#aROPC).

There are two classes of accesses to each rasterop unit. There are explicit
accesses and implicit accesses. All registers in the rasterop chips can be
explicitly read or written. In addition, the source and destination
registers may be implicitly loaded on some operations.

Explicit reads and writes to rasterop units are performed by addressing
the desired unit; in addition, a pseudo rasterop unit exists.
Writes to the pseudo rasterop unit will load in parallel the rasterop
units on bit-planes enabled by the *per-plane mask register*.

Implicit writes to the rasterop units only occur to the source and destination
registers. All implicit writes occur to all rasterop units in parallel.
While implicitly loading all source and all destination registers in parallel
may seem undesirable, it actually imposes no performance or programming
restrictions on the product.

The rules regarding implicit writes to the source and destination registers
depend on the addressing mode used. When the frame buffer is treated as
*word-mode memory* or *pixel-mode memory*, no implicit writes are
performed on the rasterop chips. With the addressing modes
*word-mode with rasterop* or *pixel-mode with rasterop*, frame buffer
reads will implicitly load the destination registers on all ROPC chips
and frame buffer writes will actually load the system bus data to the
ROPC source registers
and the ROPC output will be written to the frame buffer. With the
addressing modes *word-mode with rasterop and hidden read* or
*pixel-mode with rasterop and hidden read*, frame buffer reads have no
effect on the ROPC chips, but frame buffer writes will load the system bus
data to the ROPC source registers, a hidden read cycle will load the
destination registers in the rasterop chips, and the ROPC output will
be written to the frame buffer. The last two addressing modes write
in parallel all bit planes enabled by the *per-plane mask register*.
These addressing modes, *parallel word-mode with rasterop* and
*parallel word-mode with rasterop and hidden read*, perform implicit
writes to the rasterop chips in a manner analogous to their single-plane
counterparts.

When using the rasterop chips with pixel-mode accesses, source register bits
D15..D0 on bit plane "n" are loaded from data bit "Dn" on the system bus.
In this manner, the source register for each bit plane is loaded with all
zeros or all ones; this causes the data written to the device to be conceptually
loaded vertically into the rasterop source registers. Another feature of using
rasterop support on pixel-mode accesses is that write enables are generated
for the sixteen adjacent pixels within a word. Since rasterops on a single
pixel appear uninteresting, the use of the two *pixel-mode with rasterop*
addressing modes allow fast area-fill operations without an extensive setup
of the rasterop chips. In these modes, the *right mask* and *left mask*
in the rasterop chips can be used to properly clip the region to be filled.

---

## A Single RasterOp Unit

<a id="aropc"></a>

### RasterOp Concepts


The Sun-2 color graphics board supports a three operand RasterOp in hardware.

During a RasterOp, the pixels accessed in the frame buffer are modified
according to the function specified by the function register and as a result
of data present in the data registers: destination, source, and pattern
(see the description of these registers for details).

There are 256 possible functions mapping three boolean operands into a
boolean result.  The frame buffer's eight-bit FUNCTION register selects
one of these at a time by acting as a three-bits-in, one-bit-out
lookup table for corresponding bits of the Destination, Source,
and pattern.  For example, suppose
we want to set Destination equal to (Dst OR Src), ignoring the value of
the pattern.  Consider the application of this function to a
single pixel.  The function may be expressed in tabular form as follows:


```


PAT 	SRC	DST	DST' = SRC OR DST
-------------------------------
0	0	0	0
0	0	1	1
0	1	0	1
0	1	1	1
1	0	0	0
1	0	1	1
1	1	0	1
1	1	1	1
-------------------------------

```


The `PAT`, `SRC`, and `DST` columns in the table form an index running from
zero (000) through seven (111).  The eight bits of the result column
uniquely specify the desired boolean function, and these are precisely
the eight bits which are to be loaded into the frame buffer's Function
register.  By convention, the least significant bit of the function
appears at the top
of the table, hence this function (Src OR Dst) is represented by
the eight-bit value 11101110 (0xEE).
Examples of other function encodings are 0x0 (clear destination bits),
0xFF (set destination bits), and 0xCC (copy source to destination).

The Sun-2 color graphics board allows all 256 possible RasterOp functions,
although only a few are used in practice.

For example, to clear the entire screen, the constant function `0` is
applied to the viewable rectangle.
To flash (invert) a window, the function `NOT Dst` is performed on that window.
To write a character, the `Src`
function is used, while `NOT Src` writes the character inverted (black on
white). `Dst OR Src` overstrikes (paints) the character,
and `Src OR Pat` writes the character with a background pattern.

---

### RasterOp Functional Overview


The simple rasterop unit described in the previous section has many limitations.
First, because Sun-2 frame buffers are organized as an image of normal
system memory, the simple rasterops described previously can not be aligned to
operate on arbitrary pixel boundaries. Second, let us assume that we are
using the pattern register to mask specific pixels from modification.
In this case, if the raster to be modified were less than 16-bits wide
or crossed a word boundary, it is conceivable that every
write to the frame buffer might be interleaved with a modification
of the pattern register.

To improve the performance and generality of rasterops, several
registers were added to each rasterop unit. Primarily, the source register
was extended to 32-bits and a source register barrel shifter
was added to facilitate alignment of rasters on arbitrary pixel boundaries.
Each rasterop unit consists of a destination register, 32-bit source
register, pattern register, mask1 register, mask2 register, shiftcount
register, function register, width register, opcount register, decoder
output latch, and an opcontrol register.


### RasterOp Masks


Since rasterops only operate on 16-bit words, often portions of words
must be masked from update. Performing this function with the pattern
register will usually be unacceptably slow. To accomplish this task,
each rasterop unit incorporates separate masks for the words containing
the left and right boundaries of the raster.

To use the masks, software must determine the width (in words) of the
raster. If the raster is entirely contained in one word, the width is zero.
If the raster is only three bits wide but spans a word
boundary, then the width of the raster is one. The raster width is
loaded into the width register.

The *opcounter* is a variable register. Before the start of a rasterop it
must be explicitly loaded with the same value as the width register.
Now, when the value of the opcounter equals the value of the width
register, the mask1 register is used to mask bits in the destination
from modification. When a bit in the mask1 register is asserted, the
corresponding bit in the destination will not be modified.
After every frame buffer write, the opcounter is decremented. When
the opcounter is zero, the mask1 register is used to mask destination
data bits from modification. When the opcounter is zero and a frame
buffer write occurs, the opcounter is loaded with the value of
the width register and the cycle repeats. This mechanism improves
graphics prrformance by negating the need to constantly reload the
pattern register; and by reloading the opcounter with the width
register after the opcounter has been decremented to zero,
there is need to explicitly load any rasterop unit registers
when moving from one scan line to the next in a raster operation.

When the width register is set to zero, both mask1 and mask2 are
simultaneously enabled.

---

### RasterOp Source Shifting


There is a need to align raster data in processor memory with
arbitrary pixels in the frame buffer memory. The 32-bit source
register, shiftcount register, and source_control bit control this
function.

Only 16-bit values are loaded into the source register.
The value of the source_control bit field specifies wether the
high-order source word, SRC2, or the low-order source word, SRC1, is loaded
by the main processor. The source register word not loaded directly by the
processor is always loaded from the source register word that is loaded
by the CPU. When SRC2 is loaded from the CPU, SRC1 is loaded with
the old contents of SRC2. When SRC1 is loaded from the CPU, SRC2 is loaded
with the old contents of SRC1. For example, when the source_control bit
is asserted, SRC1 is loaded directly by the CPU and SRC2 is
loaded with the old contents of SRC1. When the source_control bit is
deasserted, SRC2 is loaded directly by the CPU and SRC1 is loaded with
the old contents of SRC2.

From the 32-bit quantity formed by the concatenation of SRC2 and SRC1,
a 16-bit quantity is extracted. The shiftcount register specifies
the alignment of the extracted field with the 32-bit source register.
If the source-load bit is asserted, the shiftcount specifies a
left-shift of the extraction field from the LSB of the 32-bit SRC.
If the source-load bit is deasserted, the shiftcount must be set to
zero and the effective shift amount will 16. In the latter case, the
extracted source is just SRC2.

The source shifting mechanism is fully general and is extremely
efficient for drawing rasters on the screen. As an example, consider
the process of copying a 17-pixel by 17-pixel character onto the
display. For this example, the width of the operation is always one.
We set the width and opcount registers to one. Now assume that the
character font is stored in main memory as 32-bit left-justified
long integers; we have seventeen long integers. Further assume
that we wish to align the left-edge of our character with the
middle of a 16-bit word in the frame buffer. The left-mask (mask2)
will be 0xFF00; the right-mask (mask1) will be 0x007F; the
source_control bit will be asserted. We load the function register
with the "Copy" operation 0xCC, and we begin our Raster Operation.
Drawing our character from top-to-bottom starting at short-word "w", we
would perform seventeen long-word move instructions from our
font table to addresses "w", "w+72x1",...,"w+72x16". The 17x17
character has been copied to the frame buffer.

More information on the operation of a rasterop unit is available in
the rasterop datapath chip specification.

---

## Color Map


The color lookup tables for the Sun-2 color board consist of a high-speed
ECL lookup table used during video display, and a TTL shadow
color lookup table that can be accessed at any time by the host software.
The TTL shadow mask removes the software headaches associated with
allowing updates of the color map only during vertical blanking.

One control bit in the status register defines the coupling between the
host software and the color maps. When the bit "Update ECL Cmap" is
deasserted, the TTL color map can be read or written. When the status
bit "Update ECL Cmap" is asserted, the TTL color map *can not* be
read or written and instead is used to completely
update the ECL color map during vertical retrace. The ECL color map
can be loaded in half a vertical retrace period.

Although the status bit "Update ECL Cmap" can be toggled at any time,
changing it during a vertical retrace might cause
only a fraction of the ECL color map to be updated. This could cause
an undesirable glitch in the video display. Additionally, several processes
could be attempting to update the color map simultaneously and no
protections exist to keep a user process from updating color map entries not
allocated to it. For these reasons, updates to the color map in a
multi-window, multi-process environment should be made through system
calls which enable an interrupt routine to actually load the color maps.

All entries in the color maps are byte quantities stored consecutively
by entry number (0 to 255) and by color (red, green, blue).


## Status Register


The status register is cleared when a bus reset is issued. The status register
is a byte register and contains the following fields.


```

	Status Register
	Bit	Name and Function
	---	-----------------
	D0	Display_Enable: When asserted this bit enables the video DACs.
	D1	Update_Ecl_Cmap: When deasserted this bit allows the host
		 	software to read or write the TTL shadow color map.
			When this bit is asserted and the monitor is in
			vertical retrace, the TTL shadow color map will be
			loaded into the ECL color map.
	D2	Inten: When asserted, an interrupt is generated at the end
			of vertical retrace. Clearing bit resets interrupt.
			An interrupt once every screen frame is useful for
			effecting smooth panning and insuring that the color
			map is never only partially updated. Without interrupts,
			the user might experience glitches in the screen output.
	D3	Ropmod0. LSB of 3-bit field specifying current rasterop mode.
	D4	Ropmod1. Bit in 3-bit field specifying current rasterop mode.
	D5	Ropmod2. MSB of 3-bit field specifying current rasterop mode.
	D6	Interrupt_Pending: Read-only. Asserted if board interrupting.
	D7	Vertical_Retrace: Read-only. Asserted if monitor in vertical
			retrace.

```


---

## Interrupt Handling


Interrupts can be generated at the end of vertical retrace.
Interrupts are useful for effecting smooth scrolling and ensuring
the color map is never allowed to be only partially updated during
vertical retrace. If not controlled, random updates to the zoom and
pan registers and the color map can cause 16.7 milli second glitches
in the monitor display.

Interrupts are enabled by setting bit "Inten" in the status register.
At the end of a vertical retrace period, an interrupt will be
generated at interrupt level 4. This interrupt level is shared by
the monochrome and color video controllers residing on the system P2-Bus.
The color and monochrome controllers must be polled to determine the
source of the interrupt. If the source is the color controller, the
interrupt line can be reset by clearing the bit "Inten" in the status
register.


## Address Space Assignment


The frame buffer occupies 8 MByte of address space. This address space
must be aligned on an 8 MByte boundary. Jumpering the frame buffer base
address is discussed in Chapter 3. Addressing of the Sun-2 color board is
as follows:


```

			FRAME BUFFER ADDRESSING

 Offset from Base	Accessed Entity
-------------------	---------------
0x000000 - 0x0FFFFF	Word-Mode Memory. Frame buffer appears as a stack of eight
			memory planes. Each memory plane is equivalent to 128KB
			of system memory. A word accesses addresses 16 adjacent
			bits within a bit plane. Byte and/or word access.
0x100000 - 0x1FFFFF	Pixel-Mode Memory. Frame buffer appears as 1 Million 8-bit
			deep pixels. Memory planes masked by Per-Plane Mask Reg
			are write and read protected. Byte access only.
0x200000 - 0x2FFFFF 	RasterOp Memory. The eight rasterop addressing modes are
			specified by the bit field ROPMOD2..ROPMOD0 in the status
			register. Rasterop Modes:
				Mode 0: Word-Mode with RasterOp
				Mode 1: Pixel-Mode with RasterOp
				Mode 2: Word-Mode with RasterOp and Hidden Read
				Mode 3: Pixel-Mode with RasterOp and Hidden Read
				Mode 4: Parallel Word-Mode with RasterOp
				Mode 5: Parallel Pixel-Mode with RasterOp
				Mode 6: Parallel Word-Mode with RasterOp and HRead
				Mode 7: Parallel Pixel-Mode with RasterOp and HRead
0x300000 - 0x3::FFF	Control Registers and Color Maps.

```


---


All addressing modes specified as "Word-Mode" can be further delineated
by the address range corresponding to each bit plane. The breakdown of
address offsets to bit planes follows:


```


		FRAME BUFFER ADDRESSING IN WORD-MODE

	Offset from Word-Mode Base		Accessed Entity
	--------------------------		---------------
	   0x000000 - 0x01FFFE	    		Word-mode bit plane 0.
	   0x020000 - 0x03FFFE	    		Word-mode bit plane 1.
	   0x040000 - 0x05FFFE	    		Word-mode bit plane 2.
	   0x060000 - 0x07FFFE	    		Word-mode bit plane 3.
	   0x080000 - 0x09FFFE	    		Word-mode bit plane 4.
	   0x0A0000 - 0x0BFFFE	    		Word-mode bit plane 5.
	   0x0C0000 - 0x0DFFFE	    		Word-mode bit plane 6.
	   0x0D0000 - 0x0FFFFF	    		Word-mode bit plane 7.


```


All registers and the color map on the Sun-2 color video card begin
at an offset of 0x700000 from the base address of the board. The
control register and color map addresses are allocated as follows:


```


		CONTROL REGISTER AND COLOR MAP ADDRESSING

	 Offset from Base	Accessed Entity
	-------------------	---------------
	0x700000 - 0x70001E	RasterOp unit. Bit Plane  0.
	0x701000 - 0x70101E	RasterOp unit. Bit Plane  1.
	0x702000 - 0x70201E	RasterOp unit. Bit Plane  2.
	0x703000 - 0x70301E	RasterOp unit. Bit Plane  3.
	0x704000 - 0x70401E	RasterOp unit. Bit Plane  4.
	0x705000 - 0x70501E	RasterOp unit. Bit Plane  5.
	0x706000 - 0x70601E	RasterOp unit. Bit Plane  6.
	0x707000 - 0x70701E	RasterOp unit. Bit Plane  7.
	0x708000 - 0x70801E	On write, Psudeo RasterOp unit. Will
				write to all ROPC enabled by Per-Plane
				Mask register.
	 	   0x709000 	Status Register.
	 	   0x70A000 	Per-Plane Mask Register.
	 	   0x70B000 	Word Pan Register.
	 	   0x70C000 	Zoom and Line Offset Register.
	 	   0x70D000 	Pixel Pan Register.
	 	   0x70E000 	Variable Zoom Register.
	0x710000 - 0x7100FF	Red Shadow Color Map. Entries 0 to 256.
	0x710100 - 0x7101FF	Green Shadow Color Map. Entries 0 to 256.
	0x710200 - 0x7102FF	Blue Shadow Color Map. Entries 0 to 256.

```


---


There are eight RasterOp units on the Sun-2 color board.
Each rasterop chip has fourteen 16-bit registers with the following
address offsets from the base address of the rasterop chip:


```


		RASTEROP UNIT REGISTER ADDRESSING

	ROPC Base Offset    Data Bits    Accessed Entity
	----------------    ---------    ---------------
	      0x00	     D15..D0	 Destination Register.
	      0x02	     D15..D0     Source Register 1.
					 Least-significant word of SRC.
	      0x04	     D15..D0	 Source Register 2.
					 Most-significant word of SRC.
	      0x06	     D15..D0	 Pattern Register.
	      0x08	     D15..D0	 Mask1 Register.
					 Enabled when "Opcount" equal to zero.
	      0x0A	     D15..D0	 Mask2 Register.
					 Enabled when "Opcount" equals "Width".
	      0x0C	     D15..D9	 Write as zeros, Read as Don`t Care.
				  D8	 Sourceload Bit. If zero, SRC2 loaded
					 from system data bus, SC1 loaded from
					 SRC2. If asserted, SRC1 loaded from
					 system data bus, SC2 loaded from SRC1.
			     D7 ..D4
			     D3 ..D0	 SRC Shift Amount. SRC data bits output
					 to function unit are bits "Shift Amount"
					 through "Shift Amount + 15".
	      0x0E	     D15..D8	 Write as zeros, Read as Don`t Care.
			     D7 ..D0	 Function Register.
	      0x10	     D15..D0	 Width Register. Specifies width of
					 Raster in words.
	      0x12	     D15..D0	 Opcounter. Loaded from Width Register
					 when Opcounter equal to zero.
					 Decremented every frame buffer write.
 					 Controls enabling of mask registers.
	      0x14	     D15..D0	 Decoder output latch. Read-Only.
					 For diagnostic purposes. Gives output
					 of RasterOp unit based on current
					 register values.
	      0x16	     D15..D0	 Manual load destination. Loads destination
					 and strobes LD.DST pin. For diagnostic
					 purposes.
	      0x18	     D15..D0	 Manual load source. Loads source register
					 and strobes LD.SRC pin. For diagnostic
					 purposes.
	      0x1E	     D15..D8	 Write as zeros. Read as Don`t Care.
			     D7.. D0	 Flag register for applications software.

```


---

# Preparation for Use


## Introduction


This chapter provides information on installing the Sun-2 color graphics board.
Included are instructions for unpacking, inspection, switch and jumper setting,
and interfacing the Sun-2 color graphics board with the Sun-2 single board
processor and other Sun-2 color graphics boards.


## Unpacking Instructions


Inspect the shipping carton immediately upon receipt for evidence of damage.
If the shipping carton is severely damaged, request that the carrier's agent
be present when the carton is opened.
If the carrier's agent is not present when the carton is opened
and the contents are damaged, keep the content and carton for the
agent's inspection.

It is suggested that salvageable shipping cartons and packing material
be saved for future use in the event the product must be reshipped.


## Installation Considerations


The Sun-2 color graphics board draws a worst-case 20A at 5V and 6A at -5.2V.
Given that the Sun-2 color graphics board is designed for use with the Sun-2
single board computer which draws 20A at 5V, a minimum system will draw a
worst-case 45A at 5V and 6A at -5V. After installing a Sun-2 color board,
the power supply output voltages should be checked and readjusted if necessary.


## Base Address Jumper


The Sun-2 single board can is designed to support upto 8 MBytes worth of devices
on the single board P2-bus. The Sun-2 color board occupies 4 MBytes of address
space and jumper J100 selects between a base address of 0x000000 or 0x400000.
Connecting pins 3 and 4 of J100 selects a base address of 0x400000 for the
Sun-2 color board. Connecting pins 2 and 3 of J100 selects a base address of
0x000000 for the Sun-2 color board.a


---

## Repair Information


To return a Sun-2 color graphics board for repair,
obtain a return material authorization number (RMA) from the address below
and send the board with the RMA number and a detailed description
of the problem to the following address:


```

Sun Microsystems Inc
Att: Service Department
2550 Garcia Avenue
Mountain View, CA 94043
U.S.A.

415-960-1300

```
