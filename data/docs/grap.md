# grap.mss

.NH 2
The Sun Graphics System
.NH 3
The Frame Buffer
.PP
The Sun graphics hardware consists of a bit mapped memory, coupled with
a Raster-function unit capable of performing bit manipulation functions
on the contnts of this memory.  The graphical memory is one meg
The term ``frame buffer'' as used in Sun documents refers either to
the graphics board or to its bit-mapped memory; where the meaning is
not clear from context, a more specific term is used.
.PP
Although there are 1024 by 1024 pixels in the frame buffer,un Graphics Screen.
.sp 2v
.DE
.KE
The pixels not displayed (1024 by 224) are still accessible, and may be
used as a cache to store bit maps which are not visible but which may
be moved (or copied) into the visible region by one of the
raster operations d displacement is to the right; positive Y
displacement is downward.
The frame buffer allows the access of up to sixteen
horizontally adjacent pixels
on one read or write cycle (one access to the graphical
memory).  This yields increased bandwidth when a cllustrates the concept of a raster operation or
``RasterOp'', as developed by Newman and Sproull [1].
.FS
[1] Newman, William M. and Sproull, Robert F.,
.I
Principles of Interactive Computer Graphics,
.R
Second Edition, McGraw-Hill, 1979.
.FE
.KF
.DS L
.sf three variables: its original
contents (Dt), a source rectangle (Src), and a repeating bit pattern
(Pat).
There are 256 possible functions mapping three boolean operands into a
boolean result.  The frame buffer's eight-bit FUNCTION register selects
onee
we want to set Destination equal to (Dst OR Src), ignoring the value of
the pattern.  Consider the application of this function to a
single pixel.  The function may be expressed in tabular form as shown
in figure RASTEREXAMPLE.
.KF
.TS
center;
| ci ci cction.
.sp 2v
.KE
.PP
The Pat, Src, and Dst columns in the table form an index running from
zero (000) through seven (111).  The eight bits of the result column
uniquely specify the desired boolean function, and these are precisely
the eight bits which ar (Src OR Dst) is represented by
the eight-bit value 11101110 (0xEE).
Examples of other function encodings are 0 (clear destination bits),
FF (set destination bits), and CC (copy source to destination).
.PP
The Sun graphics system allows all 256 possible Re.
To flash a certain window, the function
NOT Dst is performed on that window.
To write a character, the Src
function is used, while NOT Src writes the character inverted (black on
white), Dst OR Src overstrikes (paints) the character, and Src OR Pat writer, Source Register, and
Mask Register, respectively.
.NH 3
Frame Buffer Addressing
.PP
The frame buffer is a dual ported memory, providing storage for a 1024
by 1024 pixel bitmap image.  One port of the frame buffer connects
(thru the function unit) to ry microsecond for a 16-bit operation.
.PP
The frame buffer is addressed in a cartesian coordinate system, in which
<0,0> is the upper-left corner of the screen.  From one to 16 horizontal
pixels can be read or written in a single cycle, starting at the cill write the most
significant four data bits (D15 through D12) into locations <200,300> through
<203,300>.
.NH 3
Registers and Function Unit
.PP
Figure GRAPHBLOCK shows the major functional components
of the Sun graphics board.  There
are three data registers,
.I destination,
.I source,
and
.I mask,
feeding into the
function unit.  These registers can be loaded from the host processor on
a write cycle and from the frame buffer memory on a read cycle.
There are three registers controlling update operation:
rd Block Diagram.
.sp 2v
.DE
.KE
.NH 4
Destination Register
.PP
The destination register
holds the data that is being modified with a read-modify-write cycle on
update operations in the frame buffer.
.NH 4
Source Register
.PP
The source register
holds data to be combined with the destination data and the mask
(pattern) data to
compose new data for the frame buffer.  The source register can be loaded
from the frame buffer or from the processor.  The data in the source register
is bit-wise aligned with the bdestination register and the source register to compose new data
for the frame buffer.  Again, the mask register can be loaded either from
the frame buffer or from the Multibus.  The difference between the mask
register and the source register is that thehat
(x mod 16 = 0), and is treated as a repeating pattern.  The mask register
is intended for background coloring and stipple-pattern generation where
bit-alignment is undesirable.
.NH 4
Function Register
.PP
The function register specifies how the functi the 256
possible RasterOps for three boolean operands.  See section ``RasterOps''
above for details.
.NH 4
Width Register
.PP
The actual width of an update operation is set via the width register from
one to sixteen pixels.
.NH 4
Control Register
.PP
The control register controls video enable, interrupt enable, interrupt
level, and graphics board LED as follows, where bits are numbered
from D15 (most significant) to D0 (least significant):
.DS
.TS
box;
l l.
D15..D13	Interrupt Level
D12..D11	Reserved
D10	Lrrupt Enable bit enables interrupts
on the level selected.  When enabled, an interrupt is generated at
the beginning of every vertical retrace, allowing synchronization of
display updates with display refresh.  The Interrupt flag stays pending
until resetard LED off when set;
the LED lights when this bit is zero.
.PP
The control register is cleared (set to zeros) on INIT
to guarantee a blank screen, LED on, and disabled interrupts when
the graphics board is powered up.
.NH 4
X-Y Registers
.PP
The host prodress bus.  Only one (x) or (y)
register is updated at one time; the others do not change.
.NH 3
Graphics Board Multibus Interface
.PP
The Sun graphics board uses both the data and the address lines of the
Multibus to maximize the information that can be s via the address bus.  At the same time, the processor can
select which of the four sets of (x,y) registers to use, whether to
load a register from the data bus or from the frame buffer, whether to
load the source or the mask register, and whether to exe
.PP
On a write cycle, five things happen sequentially.
.IP (1)
One of the four sets of (x,y) cursor registers is selected.
.IP (2)
An x or y coordinate encoded in the address is loaded into
the (x) or (y) register of the selected pair.
.IP (3)
Data from
the Multibus is written into the selected register on the graphics board
(source, mask, function, width, or control), or the data is ignored if
no register is selected.
.IP (4)
The contents of the addressed (x,y) frame buffer location
are read into the destie preselected function and new data is written back into the addressed
frame buffer location.
.PP
On a read cycle, four things happen.  The first two are the same as
for the case of a write cycle.
.IP (1)
One of the four sets of (x,y) cursor registers is ) location in the frame buffer into the selec on the
graphics board.
.IP (4)
The data then stored in the source register
is returned to the Multibus, correctly bit-aligned with the bus data
lines.
.LP
The frame buffer is never updated on a reagraphics board and are subsequently
executed independently and in parallel with the processor.  This makes
the frame buffer a zero-access-time device as long as the request rate
does not exceed one request per microsecond.  Since normally streams
of data se of the pipelining, the data read back
corresponds to the previous read request.  Thus, to read a stream of
data, one additional word needs to be read before valid data is obtained.
.NH 3
Graphics Board Address Decoding
.PP
The graphics board decodes 20ecoding.
.sp 2v
.DE
.KE
By encoding these operation bits
in the address, repetitive operations like generalized RasterOps can be
done very quickly.
There is a patent pending on this design, which
was meant to be used efficiently with the MC68000
auto-incrboard occupies 128K bytes of Multibus address space.
By accident this also happens to be how much
physical memory there is on each graphics board.
.PP
The Update bit (bit 16) is on if the frame buffer is to be modified.
Usually several operations are perfe buffer.
.PP
Bits 14 and 15 select the operation.
If they are set to 0, then the
data on the data bus is not used (although an X or Y address must be loaded
in this cycle, as in all cycles).
If they are set to 1, then one of the four auxiliary
registers normal case for copy operations.
If they are set to 3, the
mask register will be loaded from the data bus.
If the Update bit is also set in any of these cases,
then the RasterOp will be performed and
the frame buffer modified after the specified register alue of 0 loads the function register fr eight
bits of the data bus.
The interpretation of the function register is explained above in
section ``RasterOps''.
A register number of 1 specifies the width register, which
determines the width oh-order bits of the data
in the source and mask registers will be
significant on RasterOps.
An auxiliary register number of 2 loads the control register bits from the data
bus.  See section ``Registers and Function Unit'' above for details.
Finally, regisr pairs of ten-bit address registers (called ``cursors''),
selected by bits 12 and 13.
Bit 11 selects either X or Y of
the pair, and bits 1 through 10 of the address are loaded into the selected
address register.
Note that
.B every
read or write referenceffer.
.PP
The low order bit (bit 0) of the address must always be zero.
.PP
Appendix A contains a simple example
(written in the programming language C)
which displays an 8 by 8 ``cursor'' at a given screen position.
The example also illustrates the use of
some mnemonic definitions for the frame buffer commands.
C language definitions for these names appear in Appendix B.
