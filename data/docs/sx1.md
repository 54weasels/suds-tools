---


---


# Sun-2 Color Graphics Board


# User Manual


Sun Microsystems Inc

June 1983

Company Confidential

Revision 0.4


>
The Sun-2 Color Graphics Board is a bitmap graphics subsystem
offering a 900-line 70 Hz non-interlaced display, 256 simultaneously
displayable colors, "RasterOp" hardware support, integer zoom (1x - 16x),
pixel pan, and eight separate addressing modes.

This document describes the architecture, programming,
and the installation of the Sun-2 Color Graphics Board.


>
Sun is a trademark of Sun Microsystems Inc.


---


---

# System Architecture


## Overview


The Color Sun-2 is a member of the Sun-2 family of workstations. The Color
Sun-2 is architecturally compatible with the Sun-2 monochrome workstation
and will run all programs written for the monochrome display.
The product will be available with the same packaging as the Sun-2
monochrome unit.

Sun Microsystems currently markets a medium resolution color option
(480 x 640 x 8) that is well suited for many low-cost applications.
This product, however, does not adequately meet the needs of CAD/CAM Original
Equipment Manufacturers and users involved in state-of-the-art
image processing. The CAD marketplace requires 1000-line color monitors
in order to display respectable character fonts; it requires a display
without flicker; and, it requires a system that can interactively perform
such operations as zoom, scroll, and pan. Current color terminals that
meet these needs cost about $40,000. The Color Sun-2 is intended to address
this marketplace at a cost much lower than currently available systems.


## Features


Color Architecture a superset of Monochrome Architecture

Screen Resolution of 900 by 1152 (3:4 aspect ratio) with 8 bits per pixel

Screen Resolution expandable to 900 by 1152 by 32

70 Hz non-interlaced vertical frequency, 64 KHz horizontal frequency

Integer Zoom via pixel replication (Magnifications 1 to 16)

Pan in increments of a single pixel

Frame buffer addressable as pixels or as words within separate bit planes

Frame buffer addressable as memory or as memory with RasterOp support

Separate RasterOp unit with 256 functions for each bit plane

Translation and Raster Operations on upto 128 bits in parallel

Most accesses run without incurring MC68010 wait states

Frame buffer cycle time of 640 nsec (200 nsec 20% - 95% of time)

Hardware protection of arbitrary bit planes for window applications

Color Map selects 256 colors from a palette of 16 million


---

## The Frame Buffer


The Sun-2 color frame buffer has eight addressing modes. These are:


```


	* Word-Mode Memory. Frame buffer appears as a stack of eight
		memory planes. Each memory plane is equivalent to 128KB
		of system memory. A word accesses addresses 16 adjacent
		bits within a bit plane. Byte and/or word access.

	* Pixel-Mode Memory. Frame buffer appears as 1 Million 8-bit
		deep pixels. Memory planes masked by Per-Plane Mask Register
		are write and read protected. Byte access only.

	* Word-Mode with RasterOp. Frame buffer reads have side effect of
		loading Destination Register on each RasterOp Chip (ROPC).
		Write data written to ROPC Source Registers and ROPC output
		written to frame buffer. Byte and/or word access.

	* Pixel-Mode with RasterOp. Frame buffer reads load ROPC Destination.
		Writes load per-plane Source Registers with either all
		zeros or ones; for instance, writing 0xAA will load the
		Source on even bit-planes with zeros and odd bit-planes with
		ones. ROPC output written to sixteen adjacent pixels along
		word-mode word boundaries. Memory planes masked by Per-Plane
		Mask Register are write and read protected. Byte access only.

	* Word-Mode With RasterOp and Hidden Read. Identical to addressing
		mode "Word-Mode with RasterOp" except that writes have the
		side effect of loading the Destination Registers in each
		ROPC. Doubles frame buffer cycle time.

	* Pixel-Mode With RasterOp and Hidden Read. Identical to addressing
		mode "Pixel-Mode with RasterOp" except that writes have the
		side effect of loading the Destination Registers in each
		ROPC. Memory planes masked by Per-Plane Mask Register are
		write and read protected. Doubles frame buffer cycle time.

	* Parallel Word-Mode with RasterOp. Frame Buffer reads load ROPC
		Source Registers 128 bits in parallel. Writes cause ROPC
		outputs to be written to all memory planes enabled by
		Per-Plane Mask Register.

	* Parallel Word-Mode with RasterOp and Hidden Read. Identical to
		addressing mode "Parallel Word-Mode with RasterOp" except
		that writes have the side effect of loading the Destination
		Registers in each ROPC.


```


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

In word-mode, the frame buffer is configured as eight separate bit planes.
Each bit plane occupies a separate 128 Kbyte block of the system address
space, and each bit plane by itself is architecturally identical to the
black and white frame buffer. In this addressing mode, writing to the
device will alter upto 16 horizontally adjacent pixels. Word 0
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

Mapped as memory in word-mode, the color frame buffer will run without
recompilation the same applications programs
developed for the monochrome display. Likewise, in word-mode,
the device is highly tuned for DMA transfers of image data from disk or ethernet
to display. In word-mode, the Sun-2 color frame buffer could even be used
as a system I/O buffer space.


![sc12.press](../svg/sc12v.drw.O.svg)


*Figure: **Word-Mode Frame Buffer Addressing***

<a id="wordaddr"></a>


---

A word-mode access will only address one of the eight memory planes of the
frame buffer. However, there are two addressing modes which access all
eight memory planes in parallel. Using these modes is useful for such
operations as dragging a window on the display.

The color frame buffer memory is dual ported. One port connects to the
syncronous system bus and the second is dedicated to video refresh which has
priority over system bus accesses. A new datum can be read or
written to the Sun-2 color frame buffer every 640 nsec, and during blanking
and at large zoom factors the frame buffer cycle time drops to 200 nsec.

While a standard color configuration will consist of 8 bits per pixel,
Sun-2 color video boards can be stacked three deep to provide eight
bits each for red, green, and blue. In this configuration, each board
lies in a separate address space, but the timings of the boards are
syncronized to properly overlap the red, green, and blue images
generated by each board. A fourth video card can also be added to
provide 32 bits per pixel with the last eight bit planes being used
as an alpha buffer. If the RasterOp and mixed addressing capabilities
of the fourth card are not being used, then this board can be replaced
in function by a memory expansion card.

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
When accessed in word-mode, the frame buffer is protected by the
protection bits in the main processor`s page maps. In pixel-mode,
a *Per-Plane Mask Register* provides bit-plane protection by specifying which
bit planes can be updated. Likewise, during pixel-read, the
mask register determines which bit planes are read; all other bits
in the pixel are set to zero. In this manner, each window on the display
can be dynamically allocated a range of colors that appear to begin at zero.
This feature is useful because it obviates the need for a program sharing
the frame buffer to add a variable base to each pixel written
or to subtract the same variable base from each pixel value read.

In a typical scenario,
the user may wish to dynamically create an image allocating two bits
each for red, green, and blue; assume that the intensities for red, green,
and blue are computed separately. In this example, the user program would
request six bit planes from the operating system. The operating system
would then map the user`s address space and load the supplied 64 entries
into one quarter of the color map. Assuming a window had
already been created for this process, the system would also load
the most significant bit planes in this window with a zero or one.
Now the user program could set bits D1..D0 in the mask register and write
the red-pixel data for the image. Next the user could set bits D3..D2
in the mask register and write the green-pixel data for the
image. Finally, the user could set bits D5..D4 in the mask register
and complete the image.

---

## RasterOp Architecture


The Sun Graphics system incorporates the concept of "RasterOP".
RasterOp means that rectangular areas of display data ("Raster")
are modified or combined according to a preselected operation ("Op").
RasterOp provides complete generality to paint characters, manipulate windows,
scroll screens, and to draw vectors. All write-accesses to the Sun-2 color
frame buffer are routed through the RasterOp Unit and operate on word or
pixel data. An example for
RasterOp is shown in Figure [Figure](#RasterOp), in which a source character
is copied to a destination anded with a pattern mask.


![sc13.press](../svg/sc13.drw.O.svg)


*Figure: **A RasterOp Operation***

<a id="RasterOp"></a>


During a RasterOp, the pixels accessed in the frame buffer are modified
according to one of 256 possible bit functions operating on the source
data, the destination data, and the pattern mask data. The pattern mask
is loaded from the processor, the destination data is the frame buffer data
being modified, and the source data is the 16-bit quantity being written to
the color graphics board.
In addition, each RasterOp unit consists of a left mask, a right mask, a barrel
shifter for the source data, and raster width information
which accelerate writing arbitrarily sized rasters into variable starting
pixel locations.

There is a separate RasterOp unit for each memory plane in the frame buffer,
and writing to an additional psuedo RasterOp unit will cause all RasterOp
units selected by the mask register to written in parallel.

RasterOps will operate on both word-mode and pixel-mode frame buffer accesses.

---

## Hardware/Software Interface


The Sun-2 color graphics board maximizes graphics performance without
using a cumbersome command-based interface. A command-based interface
with an inadequate scope of comands can become a headache to circumvent,
and a complete set of microcoded routines quickly becomes too costly to
both develop and place on the desk of every engineer. By providing a
fully general RasterOp mechanism coupled with hardware zoom and pan,
the Sun-2 color graphics board offers an extremely fast
low-level interface to software that will not permanently lock applications
software to this particular product.

The Sun-2 color frame buffer can be accessed as pixels in the traditional
manner, or the the frame buffer memory can be mapped as a stack of eight
bit planes where each access addresses 16 adjacent bits within a bit plane.
In this second mode (word-mode),
the Sun-2 color graphics board is architecturally
identical to the Sun-2 black and white video board, so most Sun-2
software packages will run transparently on either the color or
monochrome video boards. In addition, the color graphics board provides
hardware support for mapping user processes to different sets of bit planes,
allowing multiple processes to run simultaneously using a variable number
of bit planes while maintaining separate color lookup maps.


## Speed


A major problem with high-resolution bit-map graphics is the
time required for creating and modifying the frame buffer image.
The problem is rooted in the sheer number of bits being manipulated.
For example, if a 900 by 1152 pixel frame buffer were updated at a rate
of 1 pixel per microsecond, it would take 1 second to fill the screen.

In comparision, the Sun-2 color graphics board, in conjuction with
the Sun-2 processor board, can update 16 pixels (128 bits) every 640 nsec
or fill the screen in 41 milliseconds (excluding higher-level overhead).
Painting a 12 by 12 character takes approximately 16 microseconds, and
altering zoom or pan can be performed with three move instructions.


## References


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
	Pixel area expandable to 900 by 1152 by 32
	Frame buffer architecture a superset of monochrome architecture
	Frame buffer radressable as pixels or words within bit planes
	One RasterOp unit per bit plane
	Updates on upto 128 bits in parallel
	Per-Plane Mask register protects bit-planes from update
	Frame buffer cycle time of 640 nsec
	Frame buffer cycle time of 200 nsec during horizontal retrace
	Frame buffer writes buffered to operate without MC68010 wait states

```


**Color Map**

```

	Selects 256 colors from palette of 16 million
	Addressable even during video display

```


**Zoom and Pan**

```

	One to sixteen times magnification with pixel replication
	Pan in increments of a single pixel horizontally or vertically

```


**Video Monitor and Video Interface**

```

	70 Hz non-interlaced vertical, 64 kHz horizontal
	100 MHz video rate
	Separate horizontal and vertical sync (0-5 Vpp)
	Separate RGB analog inputs (0.7 Volts peak-to-peak)

```


**Electrical Characteristics**

```

	+ 5.0V +- 10%.  Maximum current: 15 A.
	- 5.2V +- 15%.  Maximum current:  3 A.

```


**Physical Characteristics**

```

	Triple-Height Eurocard form-factor
	Width:  400 cm
	Height: 280 cm
	Depth:  0.50 in. (1.27 cm)
	Weight: 32 oz.   (894 g)

```


**Environmental Characteristics**

```

	Operating Temperature: 0-50 C

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

## Mask Register


The mask register is used for restricting frame buffer access to some bit planes.

In pixel-mode, a '0' bit in the mask register will prevent modification of
the corresponding bit plane during writes, and will cause a zero to be
returned from that bit plane during reads. Masking of bit planes
on read operations allows arithmetic to be performed on a subset
of the bit-planes while saving a per-pixel "and" instruction in software
and maintaining a consistent model of a variable depth frame buffer.

In word-mode, the mask register has no effect. However, in parallel word-mode,
data is written from the RasterOp chips to all bit planes in parallel.
The Per-Plane Mask register should be used to selectively enable
or disable bit planes from update.
Hardware protection for word-mode accesses to bit planes zero through
seven is effected by asserting the proper protection bits in the
processor page maps.


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

The Sun-2 Color workstation supports zoom in integer magnifications of
1 to 16. Associated with the zoom, the display can also be panned. Pan
can occur in increments of a single screen phosphor in the vertical direction,
and, horizontally, pan can occur in an increment equal to the lesser of
four screen phosphors or the size of a magnified pixel.

The zoom register is a byte register. The least-significant nibble holds a
value specifying the size on the
monitor to display a single frame buffer pixel.


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
information is the pixel address of the point at the origin. This 20-bit
address (22-bit address when using 256K rams) is stored in the Word-Pan
and Pixel-Pan registers.

The Sun-2 color board additionally offers an added degree of granularity
when panning. In the vertical direction, Pan can be controlled down to
the size of one screen phosphor (The height of a pixel when zoom is
disabled). In the horizontal direction, the smallest pan increment is
the lesser of the size of a magnified pixel or four screen phosphors.
Panning horizontally in increments of four screen phosphors is
unnecessary if our zoom factor is less than four; however, this feature
becomes useful at larger zooms.

When the zoom factor exceeds four, the width of the pixels on the
leftmost edge can be set to a non-negative number of screen phosphors
such that:

```


  Width of Leftmost Pixels (in Phosphors) = (Zoom + 1) - (4 * Pix_Offset)


```

The variable "Pixel_Offset" is a two bit value packed into the Pixel Pan
Register.

The height of the pixels on the first line of the display is stored in the
most-significant nibble (Bits D7..D4) of the zoom register.


```

   Register Name       Bit	 Function
   -------------       ---       --------
   Word Pan Register   D15	 Origin. Pixel Address Bit A21
		       D14	 Origin. Pixel Address Bit A20
		       D13	 Origin. Pixel Address Bit A19
		       D12	 Origin. Pixel Address Bit A18
		       D11	 Origin. Pixel Address Bit A17
		       D10	 Origin. Pixel Address Bit A16
		       D09	 Origin. Pixel Address Bit A15
		       D08	 Origin. Pixel Address Bit A14
		       D07	 Origin. Pixel Address Bit A13
		       D06	 Origin. Pixel Address Bit A12
		       D05	 Origin. Pixel Address Bit A11
		       D04	 Origin. Pixel Address Bit A10
		       D03	 Origin. Pixel Address Bit A09
		       D02	 Origin. Pixel Address Bit A08
		       D01	 Origin. Pixel Address Bit A07
		       D00	 Origin. Pixel Address Bit A06

   Pixel Pan Register
		       D07	 Origin. Pixel Address Bit A05
		       D06	 Origin. Pixel Address Bit A04
		       D05	 Origin. Pixel Address Bit A03
		       D04	 Origin. Pixel Address Bit A02
		       D03	 Origin. Pixel Address Bit A01
		       D02	 Origin. Pixel Address Bit A00
		       D01	 Pixel Offset of leftmost pixels (Bit 1)
		       D00	 Pixel Offset of leftmost pixels (Bit 0)

   Zoom Register       D07       Height of pixels on first line (Bit 3)
		       D06   	 Height of pixels on first line (Bit 2)
		       D05   	 Height of pixels on first line (Bit 1)
		       D04   	 Height of pixels on first line (Bit 0)
	  	       D03	 Zoom Factor (Bit 3)
		       D02	 Zoom Factor (Bit 2)
		       D01	 Zoom Factor (Bit 1)
		       D00	 Zoom Factor (Bit 0)


```


---

As a brief example, assume that we wish to zoom our display by a factor of
twelve and wish to move our display origin horizontally towards the right
from the frame buffer origin. The following code
performs the operation while preventing wrap-around of the display:


```

#define zoom 11			/* Zoom Factor equals 12 */
#define zfactor (zoom+1)
#define zf_div_4 (zfactor / 4)
#define FB_width 1152		/* Width of frame buffer in pixels */
short *zoom_reg  = (SC_control + sc_zoom_addr);
short *word_pan  = (SC_control + sc_wpan_addr);
short *pixel_pan = (SC_control + sc_ppan_addr);

procedure example;
{  short x;			/* Current X coord of origin */
   short pixoff;		/* Horizontal zoom for first pixel */

   *zoom_reg  = (zoom<<4)+zoom;	/* Set zoom and height of first line to 12 */
   *word_pan  = 0;		/* Set monitor origin to word 0 */
   *pixel_pan = 0;		/* Set monitor origin to MSB of word 0 */

   x = 0;
   while (x < (FB_width - FB_width/zfactor)) {
      for (pixoff = zf_div_4; pixoff >= 0; pixoff--) {
         Wait_for_Vretrace_Interrupt;	/* Update regs once every 1/60 sec */
         *pixel_pan = (x<<2) + pixoff;
      }
      *pixel_pan = (x << 2);		/* Low six bits of origin address */
      *word_pan  = (x << 6);		/* Word at origin of screen */
   }
}

```


The addressable frame buffer memory of the Sun-2 color graphics board is
configured as 910 lines of 1152 pixels.
If the pan base starts too far to the right in a scan line, the start of the
next scan line will wrap onto the end of the current scan line. Likewise,
if the pan base starts too close to the bottom of the display, the top of the
screen will wrap to the bottom of the screen.

The zoom and pan registers are syncronized with the start of vertical
retrace; any zoom and pan changes do not take effect until this time.
Note that there is a small chance that one register may be updated just
before the start of vertical retrace, and one may be updated just
after the start of vertical retrace. In this case, the screen will "glitch"
for 1/60th of a second. However, by coding four consecutive move intructions
to these registers, the likelihood of this occurrance is only
one in 10,000 and disappears if panning is controlled by an interrupt
routine that is serviced within 16 msec of the interrupt.

Lastly, one problem with zooming an image is that text overlaying the image
is also zoomed. With a menu-driven software package, steps must be taken
to ensure that the menu remains usable. With the Sun-2 color graphics
controller, a variable number of lines at the bottom of the display
may remain non-zoomed. The Variable Zoom Register specifies the line
number after which the zoom will return to zero. The origin of this
non-zoomed region of the display is always set to the base address of the
frame buffer.


```

   Register Name       Bit	 Function
   -------------       ---       --------
   Variable Zoom Reg   D07	 Resets zoom after specified line (Bit 10)
		       D06	 Resets zoom after specified line (Bit 9)
		       D05	 Resets zoom after specified line (Bit 8)
		       D04	 Resets zoom after specified line (Bit 7)
		       D03	 Resets zoom after specified line (Bit 6)
		       D02	 Resets zoom after specified line (Bit 5)
		       D01	 Resets zoom after specified line (Bit 4)
		       D00	 Resets zoom after specified line (Bit 3)
				 Bits 2..0 of specified line assumed zero.

```


---

## RasterOp Units


There exists a separate RasterOp unit for each memory plane in the frame
buffer, and the data paths
connecting and coordinating these per-plane RasterOp units are a bit complex.
This section attempts to explain the interconnection of these per-plane
RasterOp units. This section assumes a general familiarity with
the concepts and terminology of "RasterOp". For a better understanding of
the operation of a single RasterOp unit, please refer to section [Figure](#aropc).

There are two classes of accesses to each RasterOp unit. There are explicit
accesses and implicit accesses. All registers in the RasterOp chips can be
explicitly read or written. In addition, the source and destination
registers may be implicitly loaded on some operations.

Explicit reads and writes to RasterOp units are performed by addressing
the desired unit; in addition, a psuedo RasterOp unit exists.
Writes to the psuedo RasterOp unit will load in parallel the RasterOp
units on bit-planes enabled by the *Per-Plane Mask Register*.

Implicit writes to the RasterOp units only occur to the source and destination
registers. All implicit writes occur to all RasterOp units in parallel.
While implicitly loading all source and all destination registers in parallel
may seem undesirable, it actually imposes no performance or programming
restrictions on the product.

The rules regarding implicit writes to the source and destination registers
depend on the addressing mode used. When the frame buffer is treated as
*Word-Mode Memory* or *Pixel-Mode Memory*, no implicit writes are
performed on the RasterOp chips. With the addressing modes
*Word-Mode with RasterOp* or *Pixel-Mode with RasterOp*, frame buffer
reads will implicitly load the destination registers on all ROPC chips
and frame buffer writes will actually load the system bus data to the
ROPC source registers
and the ROPC output will be written to the frame buffer. With the
addressing modes *Word-Mode with RasterOp and Hidden Read* or
*Pixel-Mode with RasterOp and Hidden Read*, frame buffer reads have no
effect on the ROPC chips, but frame buffer writes will load the system bus
data to the ROPC source registers, a hidden read cycle will load the
destination registers in the RasterOp chips, and the ROPC output will
be written to the frame buffer. The last two addressing modes write
in parallel all bit planes enabled by the *Per-Plane Mask Register*.
These addressing modes, *Parallel Word-Mode with RasterOp* and
*Parallel Word-Mode with RasterOp and Hidden Read*, perform implicit
writes to the RasterOp chips in a manner analogous to their single-plane
counterparts.

When using the RasterOp chips with pixel-mode accesses, source register bits
D15..D0 on bit plane "n" are loaded from data bit "Dn" on the system bus.
In this manner, the source register for each bit plane is loaded with all
zeros or all ones; this causes the data written to the device to be conceptually
loaded vertically into the RasterOp source registers. Another feature of using
RasterOp support on pixel-mode accesses is that write enables are generated
for the sixteen adjacent pixels within a word. Since RasterOps on a single
pixel appear uninteresting, the use of the two *Pixel-Mode with RasterOp*
addressing modes allow fast area-fill operations without an extensive setup
of the RasterOp chips. In these modes, the *Right Mask* and *Left Mask*
in the RasterOp chips can be used to properly clip the region to be filled.

---

## A Single RasterOp Unit

<a id="aropc"></a>

### Function Unit Concepts


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

### RasterOp Unit Functional Overview


The function unit described in the previous section has some limitations.
First, because Sun-2 frame buffers are organized as an image of normal
system memory, the RasterOps described previously can not be aligned to
operate on arbitrary pixel boundaries. Second, let us assume that we are
using the pattern register to mask specific pixels from modification.
In this case, if the raster to be modified was less than 16-bits wide
or crossed a word boundary, it is conceivable that every
write to the frame buffer might have to be interleaved with a modification
of the Pattern register.

To improve the performance and generality of the RasterOp unit, several
registers were added to each RasterOp unit. In addition the source register
was extended to a 32-bit quantity and a source register barrel shifter
was added to facilitate alignment of rasters on arbitrary pixel boundaries.
Each RasterOp unit consists of a destination register, 32-bit source
register, pattern register, mask1 register, mask2 register, shiftcount
register, function register, width register, opcount register, decoder
output latch, and an opcontrol register.


### Masking


Since rasters only operate on 16-bit words, often portions of words
must be masked from update. Performing this function with the pattern
register will usually be unacceptably slow. To accomplish this task,
each RasterOp unit incorporates separate masks for the words containing
the left and right boundaries of the raster.

To use the masks, software must determine the width (in words) of the
raster. If a raster is only three bits wide but spans a word
boundary, then the width of the raster is one. The raster width is
loaded into the width register.

The Opcounter is a variable register. Before the start of a RasterOp it
must be explicitly loaded with the same value as the width register.
Now, when the value of the Opcounter equals the value of the width
register, the Mask1 register is used to mask bits in the destination
from modification. When a bit in the Mask1 register is asserted, the
corresponding bit in the destination will not be modified.
After every frame buffer write, the Opcounter is decremented. When
the Opcounter is zero, the Mask1 register is used to mask destination
data bits from modification. When the Opcounter is zero and a frame
buffer write occurs, the Opcounter is loaded with the value of
the width register and the cycle repeats. This mechanism improves
graphics prrformance by negating the need to constantly reload the
pattern register; and by reloading the Opcounter with the width
register after the Opcounter has been decremented to zero,
there is need to explicitly load any RasterOp unit registers
when moving from one scan line to the next in a raster operation.

When the width register is set to zero, both Mask1 and Mask2 are
simultaneously enabled.

---

### Source Shifting


There is a need to align raster data in processor memory with
arbitrary pixels in the frame buffer memory. The 32-bit source
register, shiftcount register, and source_control bit control this
function.

Only 16-bits are loaded into the source register at a time.
The value of the source_control bit specifies wether the
high-order (SRC2) or low-order (SRC1) word is loaded from
the external world. When SRC2 is loaded, SRC1 is loaded with
the old contents of SRC2. When SRC1 is loaded, SRC2 is loaded
with the old contents of SRC1. When the source_control bit
is asserted, SRC1 is loaded from the external world and SRC2 is
loaded with the old contents of SRC1.

From the 32-bit quantity formed by the concatenation of SRC2 and SRC1,
a 16-bit quantity is extracted. The shiftcount register specifies
the alignment of the extracted field with the 32-bit source register.
If the source-load bit is asserted, the shiftcount specifies a
left-shift of the extraction field from the LSB of the 32-bit SRC.
If the source-load bit is deasserted, the shiftcount specifies a
right-shift of the extraction field from the MSB of the 32-bit SRC.
The extracted field is supplied as the source data to the function
unit performing the bit-wise combination of the source, mask, and
pattern data. The shiftcount value must be in the range of zero to
fifteen.

The source shifting mechanism is fully general and is extremely
efficient for drawing rasters on the screen. As an example, consider
the process of copying a 17-pixel by 17-pixel character onto the
display. For this example, the width of the operation is always one.
We set the width and opcount registers to one. Now assume that the
character font is stored in main memory as 32-bit left-justified
long integers; we have seventeen long integers. Further assume
that we wish to align the left-edge of our character with the
middle of a 16-bit word in the frame buffer. The left-mask (Mask2)
will be 0xFF00; the right-mask (Mask1) will be 0x007F; the
source_control bit will be asserted. We load the function register
with the "Copy" operation 0xCC, and we begin our Raster Operation.
Drawing our character from top-to-bottom starting at short-word "w", we
would perform seventeen long-word move instructions from our
font table to addresses "w", "w+72x1",...,"w+72x16". The 17x17
character has been copied to the frame buffer.

The above example assumes left-justified raster information stored in
main memory. If our font information were right-justified, the same
example would work if the source_control bit were deasserted and
each of our long-word move instructions were broken into two short-word
move instructions with pre-decrement and a starting word address of
"w+4".

More information on the operation of a RasterOp unit is available in
the RasterOp Datapath Chip Specification.

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

---

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
	D3	Flag1. For software use.
	D4	Flag2. For software use.
	D5	Flag3. For software use.
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
pan registers and the color map can cause 16.7 milli-second glitches
in the monitor display.

Interrupts are enabled by setting bit "Inten" in the status register.
At the end of a vertical retrace period, an interrupt will be
generated at interrupt level 4. This interrupt level is shared by
the monochrome and color video controllers residing on the system P2-Bus.
The color and monochrome controllers must be polled to determine the
source of the interrupt. If the source is the color controller, the
interrupt line can be reset by clearing the bit "Inten" in the status
register.

---

## Address Space Assignment


The frame buffer occupies 8 MByte of address space. This address space
must be aligned on an 8 MByte boundary. Jumpering the frame buffer base
address is discussed in Chapter 3. Addressing of the Sun-2 color board is
as follows.


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
0x200000 - 0x2FFFFF 	Word-Mode with RasterOp. Frame buffer reads have side
			of loading Destination Register on each RasterOp Chip.
			Write data written to ROPC Source Registers and ROPC output
			written to frame buffer. Byte and/or word access.
0x300000 - 0x3FFFFF	Pixel-Mode with RasterOp. Frame buffer reads load ROPC
			Destination. Writes load per-plane Source Registers with
			either all zeros or ones; for instance, writing 0xAA will
			load the Source on even bit-planes with zeros and odd
			bit-planes with	ones. ROPC output written to sixteen
			adjacent pixels along word-mode word boundaries. Memory
			planes masked by Per-Plane Mask Register are write
			and read protected. Byte access only.
0x400000 - 0x4FFFFF	Word-Mode With RasterOp and Hidden Read. Identical to
			addressing mode "Word-Mode with RasterOp" except that
			writes have the	side effect of loading the Destination
			Registers in each ROPC. Doubles frame buffer cycle time.
0x500000 - 0x5FFFFF	Pixel-Mode With RasterOp and Hidden Read. Identical to
			addressing mode "Pixel-Mode with RasterOp" except that
			writes have the	side effect of loading the Destination
			Registers in each ROPC. Memory planes masked by Per-Plane
			Mask Register are write and read protected. Doubles
			frame buffer cycle time.
0x600000 - 0x61FFFF	Parallel Word-Mode with RasterOp. Frame Buffer reads
			load ROPC Source Registers 128 bits in parallel.
			Writes cause ROPC outputs to be written to all memory
			planes enabled by Per-Plane Mask Register.
0x680000 - 0x69FFFF	Parallel Word-Mode with RasterOp and Hidden Read.
			Identical to addressing mode "Parallel Word-Mode with
			RasterOp" except that writes have the side effect of
			loading the Destination	Registers in each ROPC.
0x700000 - 0x71FFFF	Control Registers and Color Maps.


```


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


---


The board`s color maps and registers occupy 128 KByte of address space.


```


		COLOR MAP AND CONTROL REGISTER ADDRESSING

	 Offset from Base	Accessed Entity
	-------------------	---------------
	 0x00000 - 0x0001E	RasterOp unit. Bit Plane  0.
	 0x01000 - 0x0101E	RasterOp unit. Bit Plane  1.
	 0x02000 - 0x0201E	RasterOp unit. Bit Plane  2.
	 0x03000 - 0x0301E	RasterOp unit. Bit Plane  3.
	 0x04000 - 0x0401E	RasterOp unit. Bit Plane  4.
	 0x05000 - 0x0501E	RasterOp unit. Bit Plane  5.
	 0x06000 - 0x0601E	RasterOp unit. Bit Plane  6.
	 0x07000 - 0x0701E	RasterOp unit. Bit Plane  7.
	 0x08000 - 0x0801E	On write, Psudeo RasterOp unit. Will
				write to all ROPC enabled by Per-Plane
				Mask register.
	 	   0x09000 	Status Register.
	 	   0x0A000 	Per-Plane Mask Register.
	 	   0x0B000 	Word Pan Register.
	 	   0x0C000 	Zoom and Line Offset Register.
	 	   0x0D000 	Pixel Pan Register.
	 	   0x0E000 	Variable Zoom Register.
	 0x10000 - 0x100FF	Red Shadow Color Map. Entries 0 to 256.
	 0x10100 - 0x101FF	Green Shadow Color Map. Entries 0 to 256.
	 0x10200 - 0x102FF	Blue Shadow Color Map. Entries 0 to 256.

```


---


There are twelve RasterOp units on the Sun-2 color board.
Each RasterOp unit has twelve 16-bit registers with the following
address offsets from the base address of the unit.


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
	      0x0C	     D15..D4	 Write as zeros, Read as Don`t Care.
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
	      0x1E	     D15..D8	 Flag register for applications software.
			     D7 ..D1	 Write as zeros, Read as Don`t Care.
				  D0	 Sourceload Bit. If zero, SRC2 loaded
					 from system data bus, SC1 loaded from
					 SRC2. If asserted, SRC1 loaded from
					 system data bus, SC2 loaded from SRC1.

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


The Sun-2 color graphics board draws 22A at 5V and 10A at -5V. Heat dissipation
can be a problem if the system is operated in an environment with a hot
ambient temperature. For better product reliability and increased MTBF
(Mean Time Before Failure), the product should be operated in an environment
with a comfortable ambient temperature.

The Sun-2 color graphics board
is designed for operation with the Sun-2 single board processor and
the Sun-2 packages. Outside this operating environment, FCC EMI and ESD levels
may be exceeded.


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
