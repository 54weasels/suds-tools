---


---


# Sun-2 Color Video Board


# Engineering Manual


Sun Microsystems Inc.

November 1983

Revision 1.1


>
**Trade Secret Notice**

This document contains unpublished, proprietary information
and describes subject matter proprietary to Sun Microsystems Inc.
This document may not be disclosed to third parties or copied
or duplicated in any form without the prior written consent of
Sun Microsystems Inc.


>
Multibus is a trademark of Intel Corporation.


---


---

# Principles of Operation


## Introduction


This chapter describes the operation of the Sun-2 color video board
from a hardware perspective. This manual is intended for those people
who must debug the hardware and steps through the functional areas
of the board in the same order that a technician might.

This manual assumes the reader is loosely familiar with the architecture
and programming of the Sun-2 color board; if not, the reader should first
peruse the Sun-2 Color Graphics Board User Manual. This manual further
assumes that data sheets of all relevant components are available for
reference.

The Sun-2 color board combines both transistor-transistor-logic (TTL)
and emitter-coupled-logic (ECL). Anyone unfamiliar with ECL logic
should obtain an ECL data book to
familiarize themselves with ECL logic levels and the ECL components
used on this board. All ECL signals on the board are given a common prefix
to help highlight the borders between the TTL and ECL circuitry.

Chapter 4 is intended to aid step by step debugging of
faulty hardware. The first section of Chapter 4 provides some
information on schematic conventions and the succeeding sections
step through board in the same manner that a technician might.

Chapter 5 discusses the programmable logic on the card. Chapter 6 contains
the signal list, parts list, schematics, parts location diagrams and
artwork. Chapter 7 is the wirelist.


---

## Block Diagram


---

## Schematic Conventions


### Signal Names


When possible, the schematics were drawn to standard drafting conventions
with input signal entering from the left and output signals exiting to the
right.

Both active-high and active-low signals are used.
A signal name that is followed by a backslash ("\") indicates
that the signal is asserted active low.
Conversely, a signal without a backslash denotes a
signal that is asserted active high.

Signals with multiple meanings or synonyms,
the synonyms are listed separated by a slash "/".
For example, the signal name for a read-write signal
that is active low for write is "RD/WR\".

Clock nets are all of the form "C(xx.yy-zz)". The digits "xx" specify the
period of the clock in nanoseconds. The digits "yy" specify the leading edge
of the clock signal and the digits "zz" specify the trailing edge of the
clock signal. ECL clock nets are of the form "E.C(xx.yy-zz)".

Signals that are part of busses are indicated by a common prefix
followed by a number. For example, a 16 bit data bus might be labelled
"D0", "D1", "D2", and so on until "D15".

A group of signals that are part of a signal vector are denoted by
a common prefix separated by the suffix with ".".
For example, all P2-bus signals start with the prefix "P2." and all ECL
nets, are prefixed with "E.".


---

### Component Conventions


Components in the schematics are identified by component type
(also referred to as body name).
Components are named according to "generic" or industry standard names
such as "74F32".
Components drawn in the morgan equivalent of their normal form are denoted
with a backslash; for instance, a FAST "AND" gate with inverting
inputs and outputs is a "74F32\".

Each component carries a location label.
Sections of a logical function that carry the same location label are
physically packaged into the same part. All location codes consist of
a letter from the alphabet followed by a number. The hundreds digit
of a location label specifies the page in the schematics where the
part can be found.
The letter prefix on the location label identifies the component type
and is one of:


        Letter  Component Type
        --------------------------------
        C,K     Capacitor
        U       Standard IC DIP
        M       64K RAM
        R       Resistor
        Y       PC-to-BNC Connector
        V       Voltage Regulator


Location labels are cross-indexed in the wirelist into component types,
and component types are translated into Sun Microsystem and manufacturer
part numbers by the parts list found in Chapter 6.


### Programmable Logic


Programmable logic elements such as PALs and PROMs are described
in a high-level functional language from which they are translated
automatically into the bitpatterns for programming.

Programmable logic elements are identified by name (SC1 through SC18).
The source code for the programmable logic is included in chapter 5 of this manual.
Tables and timing diagrams explaining programmable logic elements
are included in the description of the particular
functional block whenever appropriate.

---

## Power


The Sun-2 color video board requires a worst-case 19.0 Amp at +5 Volt,
5.5 Amp at -5.2 Volt and 0.2 Amp at -12 Volt.  Each board is tested with
a power supply variance of ten percent and is specified to operate within
a five percent range in a fully configured system.  At worst-case current
levels, the Sun-2 color board consumes 126 watts. Typical current levels
are 15.3 Amp at +5 Volt, 4.7 Amp at -5.2 Volt and 0.1 Amp at -12 Volt.

After checking the Sun-2 color card for power-ground shorts, the card should
be inserted into a system with the Sun-2 single board and power should be
applied. The power supply may need adjustment.


## Initialization


During system reset, the signal P2.INIT clears the control
register U207. With the control register reset, video is disabled (EN.VIDEO),
interrupts are inhibited (INTEN), and the TTL shadow color map is made
available for access by the host software (UPCMAP).

After system reset, if any video pattern appears on the monitor,
then the status register is not being properly reset and the signal P2.INIT
should be investigated.


## Clock Timing

<a id="clocks"></a>

Most of the ECL circuitry on the color board is used for generating clocks
that vary with the value of zoom. The clock circuitry on the board is
independent of all other functional areas on the board and is probably the
biggest cause of bus timeouts for boards in initial testing.

For the purpose of the following discussion, let us assume that our video
clock is exactly 100 MHz. The 100 MHz crystal oscillator outputs a TTL
signal that is feed into a MC10H124 TTL-to-ECL converter. This
100 MHz clock is then buffered by MC10H102 ECL NOR gates
which sharpen the signal's rise and fall times.  One buffered clock line,
E.C(10.0-5).0, clocks the 10H176 pixel buffers and the other buffered clock
line, E.C(10.0-5).1, is delayed by a 2.0 nsec delay line and clocks the
Intech DAC.  One gate delay after E.C(10.0-5) are the clocks E.C(10.1-6).0
and E.C(10.1-6).1 which clock the MC10H141 video shift registers and the
MC10H136 hexadecimal counters which generate the video shifter load pulses,
the 40 nsec TTL clock, and the variable period zoom clock.

The ECL counter at U1706 counts down to
divide E.C(10.1-6).0 by a factor of four to produce the clock E.C(40.0-20).
The TTL version of E.C(40.0-20) drives the Prom and Pal state machines
on the board. The period of these state machines is roughly 40 nanoseconds.
A failure of this clock line would generate continuous timeouts when
accessing the frame buffer memory.

The other two ECL counters also count down to produce a clock that
varies with the zoom and which we use to advance the data in the video
output pipeline.
The counter at U1704 is loaded with the value of zoom, counts down
to zero, and is reloaded to repeat the cycle. The outputs of counter
U1704 are connected together in a Wire-Or; only when all binary outputs
of U1704 are zero will the signal E.ZERO be active. With zoom equal to
zero, E.ZERO will be constantly asserted; with zoom greater than zero,
the period of E.ZERO will vary.


```

        Period of control signal E.ZERO (zoom = 0) = 0
        Period of control signal E.ZERO (zoom > 0) = 10nsec * (zoom + 1)

```


When E.ZERO is asserted, the hexadecimal counter at U1705 will decrement
on the next clock edge. On output of the counter is the 40 nsec zoom clock.


```

        Period of zoom clock E.C(Z40.0-20Z) = 40nsec * (zoom + 1)

```


The system clock, E.C(40.0-20), and the zoom clock, E.C(40Z.0-20Z),
are syncronized during horizontal retrace by E.ZSYNC. When asserted,
E.ZSYNC forces E.C(40Z.0-20Z) low.  E.ZSYNC is then deasserted 30 nsec
(plus one 10H176 delay) after the system clock edge so the next transition
of E.C(10.1-6) will generate the simultaneous assertion of E.C(40.0-20)
and E.C(40Z.0-20Z).

The signals E.ZERO1 and E.LOAD are used to control the loading
and shifting of the 10H141 ECL shift registers. E.ZERO1 is a buffered
version of E.ZERO; E.LOAD is generated
from the logical-AND of E.ZERO, E.C(40Z.0-20Z) and E.C20Z.0-10Z).
For non-zero zoom, E.LOAD has four times the
period of E.ZERO. When E.ZERO1 is asserted and E.LOAD is deasserted, the
MC10H141 shifters will shift on the next edge of E.C(10.1-6).1. When both
E.ZERO1 and E.LOAD are asserted, the MC10H141 video shifters will load new
data from the parallel input port on the next clock edge.

The ECL clocks E.C(40.0-20) and E.C(40Z.0-20Z) are converted to TTL by
an MC10H125 level converter and are then bufferred by 74F244 line drivers.
Not all the TTL clock signals need to be buffered, but bufferring them all
helps minimize clock skew.

The diagrams on the next page illustrate the clock waveforms at the
and their interaction with the syncronization signal E.ZSYNC.
Diagrams are only given for zoom zero through three.

---

```


Clock Timing Diagrams
---------------------

E.C(10.0-5)    _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

E.C(20.0-10)   _--__--__--__--__--__ -__--__--__--__ -__--__--__--__--__--__--_

E.C(40.0-20)   _----____----____----____----____----____----____----____----___

E.C(40.30-10)  ---____----____----____----____----____----____----____----____-

ZSYNC40\       __________xx----------------------------------------------------

E.ZSYNC\       _______________-------------------------------------------------

At Zoom = 0,
-----------
E.C(40Z.0-20Z) _________________----____----____----____----____----____----___

E.ZERO\        ________________________________________________________________

E.LOAD\	       _________________------__------__------__------__------__------_

At Zoom = 1,
-----------
E.C(40Z.0-20Z) _________________--------________--------________--------_______

E.ZERO\        _________________--__--__--__--__--__--__--__--__--__--__--__--_

E.LOAD\	       _________________--------------__--------------__--------------_

At Zoom = 2,
-----------
E.C(40Z.0-20Z) _________________------------____________------------___________

E.ZERO\        _________________----__----__----__----__----__----__----__----_

E.LOAD\	       _________________----------------------__--------------------___

At Zoom = 3,
-----------
E.C(40Z.0-20Z) _________________----------------________________---------------

E.ZERO\        _________________------__------__------__------__------__------_

E.LOAD\	       ________________________________________________________________


```


---

## VME Interface


After the initialization and clock circuitry, the bus interface circuitry
is the next functional block to verify. The bus interface operates
asyncronously with the state machines and handles the functions of
latching the VME data and address, setting the control or frame
buffer request flip-flops, and issuing the VME data transfer acknowledge.
The VME interface circuitry consists of all the logic on page one of the
schematics and is controlled by pal SC1.

There are three basic VME cycles to which the sun-2 color board will
respond. These are read cycles, write cycles, and interrupt acknowledge
cycles.

On a VME read or write cycle, the 8 bit comparator at U107 is enabled by
the VME address strobe. If P1.DTACK has not yet been asserted, if P1.BERR
is not asserted, if P1.IACK does not signify an interrupt acknowledge cycle,
and if the VME address modifiers and P1.A23 and P1.A22 match the board's
location, BDSEL will be asserted.  If there are no frame buffer requests
pending (FB.REQ deasserted), the assertion of DS will cause pal SC1 to
assert A_LATCH and DTACK. A_LATCH clocks the 74F74 at U110-0 to set FB.REQ
and also latches the VME address and data lines in 74ALS373 buffers.

The signal DTACK does not directly generate P1.DTACK. DTACK only acts as
the output enable for a 74F244 buffer. While the VME address strobe is
idle, the 74F74 at U114-0 is set (RREQ asserted) to inhibit P1.DTACK.
On the rising edge of A_LATCH, U114-0 is clocked; if a VME read cycle is
in progress, the flip-flop will remain set and will not be cleared until
END_RMW is asserted and pal SC1, in turn, asserts RD.ACK. Once seeing
P1.DTACK, the VME master should deasserted DS. Pal SC1 will then assert
END_REQ and FB.REQ will be deasserted. End of transfer.

Unlike VME read cycles which wait for a on-board dtack (END_RMW), VME
write cycles are fully buffered and respond with an immediate DTACK.
On a VME write cycle, the rising edge of A_LATCH clears flip-flop U114-0
and RREQ. At the rising edge of A_LATCH, FB.REQ should also be deasserted
so WREQ, the output of U114-1, will also be deasserted and hence P1.DTACK
will be immediately asserted.  Once the VME master accepts the data
transfer acknowledge, DS will be deasserted and the flip-flop at U114-1
will be clocked to assert WREQ which will prevent further DTACKs until
the current frame buffer request (FB.REQ) completes. When the write cycle
completes, END_RMW will be asserted, pal SC1 will immediately assert END_REQ
and FB.REQ will be reset.  Buffered write cycles improve overall system
throughput by allowing the color board latency to overlap with CPU processing.

Internally, the sun-2 color board breaks FB.REQ cycles into several groups.
Timing for frame buffer cycles is synchronous and must interact with the
memory state machine. Timing for all register, rasterop chip and color
map updates are asyncronous and interact in a limited manner with most
of the board. On an asynchronous control cycle, pal SC5 decodes the high
order address bits and qualifies them with FB.REQ to assert the control
request signal, C.REQ.  All control timing relies exclusively on signals
A_LATCH100 and A_LATCH150 whose assertions are delayed 130 nsec and 195 nsec,
respectively, from A_LATCH.  When A_LATCH150 is asserted, pal SC4 asserts
END_RMW and the control cycle terminates as described previously. Note
that during control cycles, pal SC4 also asserts END_RINC which is delayed
two pal delays by SC6 and then inhibits RMW1 from being asserted by the
74F74 at U111.

Frame buffer update cycles take several forms, but all involve memory
ras/cas cycles.  Frame buffer update cycles can be normal memory read/write
cycles or the rasterop chips can be invoked. Some rasterop memory cycles
are actually parsed into two memory cycles and all rasterop memory addressing
modes effect different patterns of rasterop chip LD_DST and LD_SRC timing.
However, understanding the ROPC addressing modes is not pertinent to the
VME timing and will be described later.

On simple frame buffer update cycles, neither C.REQ or END_RINC is asserted.
The memory control state machine (prom SC11) asserts RMW_INC which clocks
the 74F74 at U111-0 to sample FB.REQ. The trailing edge of RMW_INC then
clocks the 74F74 at U111-1 to double-sample FB.REQ and assert RMW1.  When
RMW1 is asserted prom SC11 will step through a memory update cycle. The
most important part of this update cycle is the assertion of RDAT(0-120)
which gets delayed by two clocks and causes pal SC4 to assert END_RMW
which terminates the frame buffer request as just described.

NOTE: It may be difficult to trigger an oscilloscope on the memory controller
(SC11) outputs. The memory controller outputs vary with zoom and horizontal
blanking. TO GET CYCLICAL OUTPUTS FROM SC11, GROUND SIGNAL 'NZBOT\' AND LIFT
PIN 5 ON SC11 (FAST_CNT\) TO LET IT FLOAT HIGH.

There are four fundamental types of accesses to the Sun-2 color board:
control read cycles, control write cycles, frame buffer read cycles, and
frame buffer write cycles. The timing for these access types follows:

---

```

Control Read Cycle
------------------

P1.A23..P1.A0     XXXX-------VALID--------XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

P1.D15..P1.D0     XXXXXXXXXXXXXXXXXXXX-----VALID-------XXXXXXXXXXXXXXXXXXX

P1.AS\            ------______________________________--------------------

P1.DS\		  ----------__________________________--------------------

P1.DTACK\	  -----------------------______________-------------------

FB.REQ\		  -----------__________________________-------------------

C.REQ\            -----------__________________________-------------------

A_LATCH   	  __________---------------------------___________________

A_LATCH150        ______________________---------------___________________

END_RMW\	  -----------------------______________-------------------

RD.ACK\           -----------------------______________-------------------


```


---

```

Control Write Cycle
-------------------

P1.A23..P1.A0     XXXX--VALID--XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

P1.D15..P1.D0     XXXXXXXX-VALID-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

P1.AS\            ------______________________________--------------------

P1.DS\		  ----------__________________________--------------------

P1.DTACK\	  -----------__________________________-------------------

FB.REQ\		  -----------_____________--------------------------------

C.REQ\            -----------___________----------------------------------

A_LATCH   	  __________---------------------------___________________

A_LATCH150        ______________________---------------___________________

END_RMW\	  -----------------------______________-------------------

```


---

```


Frame Buffer Read Cycle
-----------------------

P1.A23..P2.A1     XXXX-------------------VALID--------------------XXXXXXXX

P1.D15..P1.D0     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX---VALID----XXXXXXXX

P1.AS\            ------____________________________________________------

P1.DS\		  ---------_______________________________________--------

P1.DTACK\	  --------------------------------------___________-------

A_LATCH           _________---------------------------------------________

FB.REQ\           ---------_______________________________________--------

RDAT(0-120)       _______________________---------________________________

RDAT(80-200)      _____________________________---------__________________

END_RMW\          --------------------------------------___________-------

END_REQ\          ------------------------------------------------_-------

RD.ACK\		  ---------------------------------------__________-------


Frame Buffer Write Cycle
------------------------

P1.A23..P2.A1     XXXX--VALID--XXXXXXXXXXXXXX-----VALID-----XXXXXXXXXXXXXX

P1.D15..P1.D0     XXXXXX-VALID-XXXXXXXXXXXXXXXXX---VALID---XXXXXXXXXXXXXXX

P1.AS\            ------________________-------__________________---------

P1.DS\		  ---------____________-----------_______________---------

P1.DTACK\	  ----------____________-----------------_________--------

A_LATCH           __________---------------------------__-----------------

FB.REQ\           ----------___________________________--_________________

RDAT(80-200)      ____________________________________---------___________

END_RMW\          ------------------------------------__------------------

END_REQ\	  ------------------------------------__------------------

```


---

## VME Interrupt Cycles


VME interrupt acknowledge cycles differ from normal VME read and write
cycles. During a VME interrupt acknowledge cycle, the master drives P1.A3
through P1.A1, asserts P1.IACK, deasserts P1.WRITE, and strobes P1.AS and
P1.DS0.  Starting with cardcage slot 0, each VME card determines if they
are the source of the interrupt at the level specified by P1.A3..P1.A1;
if so, the card drives an 8-bit vector address onto P1.D7..P1.D0 and asserts
P1.DTACK. If the card is not the source of the specified interrupt, it
passes P1.IACKOUT to the next cardcage slot which accepts the signal as
P1.IACKIN and continues the chain.

When P1.IACK is asserted, the color board address decoder is inhibited.
P1.IACKIN is also gated with a buffered P1.AS to form IACKIN and, if asserted,
clocks the 74F74 at U108-0 which samples the state of our interrupt request
flip-flop at U110-1.  IACKIN then feeds into pal SC1; when all pending
frame buffer requests are complete, pal SC1 will assert A_LATCH and the
version delayed 130 nsec, A_LATCH100, is used to qualify the output of the
flop at U108-0 which was our interrupt request synchronizer.

C1
If the color board is interrupting, pal SC1 asserts RD.WORD and RD.IACK
to drive the interrupt vector onto the VME data bus and then pal SC1
asserts DTACK and RD.ACK to cause the assertion of P1.DTACK.

If the color board is not interrupting, pal SC1 still waits for IACKIN and
A_LATCH100 and then asserts P1.IACKOUT to continue the interrupt acknowledge
daisy chain.


---

## Memory Timing


The memory control state machines generates the memory timing for
the color video board. This section describes all the circuitry necessary
for the frame buffer memory to operate correctly. While the memory timings
do depend on the zoom syncronization (Prom SC10), a failure in that logic
will not generate frame buffer memory errors. This section does not
attempt to explain the interaction of the rasterop chips with the memory;
it assumes that all memory operations treat the frame buffer as pixel-mode
memory or word-mode memory.

The memory control circuitry resides predominately on pages 3 through 5
of the schematics. The
heart of the memory control is prom SC11. This prom operates on
40 nsec boundaries and generates the next state for the memory timing.
There are sixteen possible memory control states
(ST3..ST0). The first eleven states of the memory control cycle generate
a nibble mode read cyle that buffers the next block of data for video output.
The last five states of the memory controller are reserved for read/write updates
to the frame buffer memory; if no request is pending, a Cas-Before-Ras
refresh cycle is run.

At zoom zero, one memory cycle consists of one nibble-mode video read cycle
followed by one read/write cycle. At larger zooms, however, a memory cycle
consists of one nibble-mode video read cycle followed by multiple read/write
cycles; and, at non-zero zooms, state1 of the overall memory control cycle
is repeated upto four times to pad the total number of states in the cycle
to "16 times zoom+1". For example, at zoom one, the 64
pixels buffered during a video read
cycle will be output over 32 states instead of 16 states. At zoom one, we
perform one video read cycle followed by 4 read/write cycles and repeat
state1 one extra period. At zoom two, we perform one video read cycle,
7 read/write cycles, and repeat state1 2 extra times.


```


   States per memory control cycle = 16 * (zoom + 1)

   Nibble-mode video read cycles per memory control cycle = 1

   Read/write cycles per memory control cycle = (16 * (zoom + 1) - 11) DIV 5

   Times State1 repeated per memory control cycle = (16 * (zoom + 1) - 11) MOD 5


```


Each extended memory cycle (number of states = 16 + 16*zoom) consists of
one video refresh cycle, a variable number of read/write cycles and a
variable number of padding states. The number of read/write cycles performed
is controlled by prom SC8 and two 74ALS163 counters. Prom SC8 computes the
value 256 minus the number of read/write cycles; the ones complement of this
number is loaded into the 74ALS163 counters at STATE10 and these counters
are incremented whenever the control signal
RMW_INC is asserted. The terminal count output of
the 74ALS163 counters is resynchronized with the 40 nsec clock to form RMW_TC
and this signal is input to prom SC11 which controls the next memory controller
state. If RMW_TC is not asserted in state15, the next memory controller
state will be state11 and another frame buffer read/write cycle will be
executed.  If RMW_TC is asserted in state15 and the monitor is not in
horizontal retrace, the next memory controller state will be state0.

To pad the extended memory cycles to the correct number of states,
SPARE_TC is generated using prom SC9 which calculates the number of times to
repeat state1 in the memory cycle. SP_ST2..SP_ST0 are loaded into a
74ALS163 counter at STATE10 and the counter is allowed to increment between
memory control states zero and seven. The terminal count output of the 74ALS163
is resynchronized with the 40 nsec clock to form SPARE_TC which forces the
memory controller to state1 until SPARE_TC is asserted.

To further confuse matters, FAST_CNT is asserted by the 74F74 at U314-1 at
the start of the monitor's horizontal retrace. FAST_CNT is forces prom SC11 to
run back to back memory update cyles. FAST_CNT is deasserted by the zoom
synchronization signal ZSYNC. The main function of ZSYNC, however, is to
synchronize the memory state machine with C(Z40.0-20Z) which clocks the video
pixel buffers.  When signal ZSYNC is asserted, SC11 advances ST3..ST0 one
state at a time until state10. Prom SC11 then holds at state10 until ZSYNC
is deasserted. When SC11 resumes, the low-to-high transition of RAS.7
to RAS.0 marking the end of the nibble-mode video read cycle will
coincide with the rising edge of C(Z40.0-20Z). A malfunction
of signal ZSYNC can not cause frame buffer memory errors but will disrupt
video output. Further discussion of ZSYNC is reserved for section [Figure](#zandp).

Frame buffer read/write cycles are performed only if RMW is asserted during
memory control states 11 through 15. At states 8 and 13, prom SC11 generates
RMW_INC. This signal clocks 74F74 U117 section #0; if
a frame buffer request (FB.REQ) is pending, RMW.REQ is asserted and then
delayed two states to form RMW. RMW.REQ is clocked six states before the
falling edge of CAS on a read/write cycle because it takes 150 nsec after
FB.REQ to load the Rasterop source registers and it takes another 110 nsec
before the rasterop outputs are valid.

The selection/update of individual 64K rams is accomplished via the separate
encoding of the ras, cas and write-enable lines. Prom
SC11 generates RASX which is delayed 40 nsec to produce RAS.7..RAS.0.
RASX does not vary with the type of frame buffer access and depends only
on the values of ST3..ST0. Note that the 40 nsec delay of RASX was
introduced because prom SC11 could not drive the 8 TTL
loads of RASX quickly enough.

CAS is decoded by pals SC12 and SC13. During nibble-mode video read cycles,
CAS15..CAS0 are asserted simultaneously and are determined by ST3..ST0.
During the frame buffer update cycles, if RMW is asserted, some cas lines
will be deasserted at states 11 and 12 to cause the selection of those
bit locations in the subsequent memory cycle. If signal ONE_PIX is asserted,
pal SC4 has decoded a pixel-mode memory cycle and only the cas line selected
by A3..A0 will be strobed. If ONE_PIX is deasserted and A20 is asserted,
the memory cycle will be a word-mode access using rasterops and all
CAS15..CAS0 will be strobed. If ONE_PIX
and A20 are both deasserted, the memory cycle will be a word-mode access
and the cas lines are used to effect either 8 or 16-bit updates. In word-mode,
if LDS is asserted, then CAS7..CAS0 are strobed; independently, if UDS is
asserted, then CAS15..CAS8 are strobed.

At low values of zoom, refresh of the frame buffer 64K dynamic rams is
accomplished by the video refresh cycles. However, at larger values of
zoom the video refresh cycles are not enough to refresh the 64K dynamic rams.
The 64K nibble-mode rams, however, have a Cas-Before-Ras refresh mode
with an internal row address counter that we use to ensure dynamic
refresh. The Sun-2 color board runs a Cas-Before-Ras refresh cycle instead
of a memory read/write cycle when RMW is not asserted. During the
Cas-Before-Ras cycles, CAS15..CAS0 also remain asserted so that the ram
data outputs will remain driven to valid TTL logic levels.

Word-mode updates to a single bit plane and pixel-mode protection of
arbitrary bit planes are controlled by the frame buffer write-enable
lines WE.A..WE.H which are generated by pals SC14 and SC15.
For word-mode frame buffer updates, address bits A19..A17 select the
accessed plane and bit-plane protection is controlled by the main processor
page maps. For pixel-mode accesses, a zero bit in the per-plane mask register
will protect the corresponding frame buffer bit-plane from update.
The outputs of SC14 and SC15 are enabled by FB.WR1 and RDAT(0-120).

FB.WR1 is a re-clocked version of FB.WR.  For memory addressing modes, FB.WR
is equivalent to RD/WR\.  During RasterOp cycles that are broken into separate
read and write cycles, FB.WR is only asserted for the second memory cycle.
RasterOp write cycles with hidden read are discussed more fully in
section [Figure](#Hread).


---

Assuming that ZSYNC and FAST_CNT are deasserted, the following diagrams
show typical memory cycle at zoom zero and one.


```

Zoom = 0,
   State     00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF00

C(40.0-20)   -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

RAS\	     ----__________________----______----__________________----______--

CAS\	     __----____--__--__--______________----____--__--__--____----______

RDAT(0-120)  __________________________________________________________------__

A_DIS\	     __________________________________________________------------____

A_PIX\,A_WD\ --------------------------------------------------____________----

RMW_INC      ________________--________--____________________--________--______

RMW	     ____________________________________________________------------__

STATE10\     --------------------__------------------------------__------------

VIDEO_CK     ____________________--______--______________________--______--____

VID_CNT\     ----------------________------------------------________----------

RMW_TC       ------------------------------------------------------------------

SPARE_TC     ----____________________------------____________________----------


Zoom = 1,
   State     0011112233445566778899AABBCCDDEEFFBBCCDDEEFFBBCCDDEEFFBBCCDDEEFF00

C(40.0-20)   -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

RAS\	     ------__________________----______----______----______----______--

CAS\	     __------____--__--__--____----__________________________----______

RDAT(0-120)  ______________________________----________________________------__

A_DIS\       ____________________------------__________________------------____

A_PIX\,A_WD\ --------------------_____________-----------------____________----

RMW_INC\     __________________--________--________--________--________--______

RMW	     ______________________------------__________________------------__

STATE10\     ----------------------__------------------------------------------

VIDEO_CK     ______________________--______--________--________--________--____

VID_CNT\     ------------------________----------------------------------------

RMW_TC       ----------------------________________________________________----

SPARE_TC     ____--____________________________________________________________


```


---

## Frame Buffer Addresssing

<a id="memaddr"></a>

The frame buffer memory addressing logic can be found on page 3 of the
schematics.

The frame buffer ram addresses derive from two sources, the VME address
lines or the video refresh counters. During updates to the frame buffer
memory, the VME address lines are multiplexed to form the ras and cas
addresses. For word-mode accesses, address bit A0 is unused, A19..A17
select the bit plane accessed, and A16..A1 are multiplexed to form the Ras
and Cas addresses. For pixel-mode accesses, A3..A0 are used to selectively
enable the Cas lines and A19..A4 are multiplexed to form the Ras and Cas
addresses. Word-Mode multiplexing is performed by the 74F258s at U317 and
U318. Pixel-mode multiplexing is performed by the 74F258s at U319 and U320.

Video refresh memory cycles and inactive read/write cycles (RMW deasserted)
take their addresses from a pair of 16-bit counters and the Word-Pan Base
Address register. These addresses are multiplexed by the 74F258s at
U315 and U316 to the ram address drivers. The selection of the
video, word-mode or pixel-mode address multiplexors is performed by signals
A_DIS, A_WD and A_PIX which are generated by pal SC6.

For video memory cycle addressing,
the outputs of the Word-Pan Base Address register are connected to the
load inputs of the Scan-Line Base Address counter, and the outputs of the
Scan-Line Base Address counter
are connected to the load inputs of the Video Display Address
counter. During vertical retrace, the Scan-Line Base Address counter is loaded
from the Word-Pan Base Address register; and, during horizontal retrace,
the Video Display Address counter is loaded from the Scan-Line Base Address
counter.

The control signal, V_CNT, causes the Video Display Address to be
incremented during the horizontal display and reloaded during horizontal
retrace. The counters are clocked once per nibble-mode video read cycle and
once per memory read/write cycle. Incrementing the counters is inhibited
during video read cycles by VID_CNT, but clocking the counters at this time
ensures proper loading of these counters during horizontal retrace.

The control lines for the Scan-Line Base Address counters, BASE_I1..BASE_I0,
are generated by prom SC6. These controls increment the counters during
the horizontal display time of the monitor and when LINE_TC is asserted.
LINE_TC is used for non-zero values of zoom to repeat the display of
horizontal lines.

LINE_TC is generated by loading the ones complement of the
value of zoom into a hexadecimal counter. The hex counter is incremented
at the end of each scan line and LINE_TC is the terminal count output of
the counter. LINE_TC is forced true during vertical blanking and the no-zoom
region at the bottom of the monitor display. To do smooth panning in the
vertical direction, the LINE_TC counter is loaded with a variable,
LOFF3..LOFF0, for the first horizontal line of the display.


---

## Frame Buffer Input Data Paths

<a id="MemIDP"></a>

The input data to the frame buffer depends on the frame
buffer addressing mode. All told, there are ten frame buffer
addressing modes. Two of these modes, Word-Mode Memory and Pixel-Mode
Memory, do not use the rasterop chips and should be used to
debug the frame buffer input data paths. The eight remaining addressing
modes use the rasterop chips and are difficult to comprehend.
The data paths for the two memory-mapped addressing modes will be described
in this section.  The data paths for the rasterop addressing modes will be
discussed as part of the rasterop architecture in section [Figure](#ROParch).

Signals XMIT_WD, XMIT_DST, XMIT_PIX, OE.ROPC, RCV_WD and RD.PIX generated
by pal SC5 control the frame buffer data paths. On word-mode
memory write cycles, pal SC5 asserts XMIT_WD which enables the AM2949 buffers
that connect the data bus D15..D0 with the eight memory input data busses
MI15.H..MI0.H through MI15.A..MI0.A. The data bus D15..D0 is transmitted
identically to each frame buffer bit plane. On 16-bit writes to word mode
memory, Ras and Cas are asserted on all ram and the write enable lines
WE.H..WE.A determine which planes get updated. The AM2949 data buffers enabled
by XMIT_WD reside at U802, U803, U807, U808, U812, U813, U817, U818,
U902, U903, U907, U908, U912, U913, U917 and U918.

On word-mode memory read cycles, the ram data outputs,
MO15.H..MO0.H through MO15.A..MO0.A are latched by 74ALS373s at locations U800,
U801, U805, U806, U810, U811, U815, U816, U900, U901, U905, U906, U910,
U911, U915 and U916. Pal SC5 asserts XMIT_DST and the 74ALS373s transfer the
ram output data to the ram input data bus.  RDAT(80-160) is used to latch
the data in the 74ALS373s. Pal SC5 will also assert RCV_WD which enables the
74ALS138 decoder at U201 to generate one of RCV_WD.H to RCV_WD.A to multiplex
the ram data via the word-mode AM2949s onto D15..D0. Pal SC1 asserts RD.WORD
to drive D15..D0 to the VME bus.

On pixel-mode memory write cycles, Pal SC5 generates XMIT_PIX which transfers
D15..D0 to the pixel data bus P.D15..P.D0 and onwards to the ram input data
bus via the AM2949s at U700 to U715. Every odd/even pixel pair receives the
same input data as the next pixel pair. Ras and memory write enables are
applied uniformly to all pixel pairs and the Cas lines CAS15..CAS0 select
which pixels get updated.

On pixel-mode memory read cycles, the ram data outputs are latched
into the 74ALS373 destination registers as before. As with word-mode read
cycles, pal SC5 asserts XMIT_DST to transfer the ram output data
to the ram input data lines. Pal SC5 also asserts RD.PIX which enables one
of RD.PIX7..RD.PIX0 to multiplex an odd/even pixel pair via the pixel-mode
AM2949s onto P.D15..P.D0.  The odd/even pixel pair is then ANDed on a
per-plane basis with the per-plane mask register; The mask register forces
selected bit planes to zero to save an AND in software and the masked pixel
data is then output to D15..D0 through the three-state buffers at U724 and U725.
From D15..D0 the data heads to the VME.


---

## Frame Buffer Output Data Paths

<a id="vodata"></a>

This section describes the data paths between the frame buffer memory
and the analog RGB signals.

The frame buffer memory consists of 128 64K ram chips and is organized
as eight memory planes with 16 ram per plane. During video refresh cycles, all
frame buffer ram are accessed in parallel and the ram output is strobed by
CBUF into the 4-byte AM29520 register files; one nibble-mode read cycle
extracts 4 bits from each ram and buffers a total of 64 pixels in the
AM29520 video data buffers.

The video buffer output control circuitry on page 4 of the schematics
controls the multiplexed outputs of the AM29520 buffers. The AM29520
buffers are multiplexed four ways by signals OE3..OE0. The output
enable signals always cycle from OE0 to OE3 using the zoom clock C(40Z.0-20Z)
to advance the output enables. The AM29520s output a nibble at a time
for each bit plane.

The register selection for the four register AM29520s is performed by the
same circuitry on page 4 of the schematics. When the AM29520s are not
being clocked with new data, the 74ALS163 counter at U401 is clocked by
C(40Z.0-20Z) and selects a new AM29520 register on every fourth clock
using YBUF.S1 and YBUF.S0.
When the AM29520s are being strobed by CBUF, however, the valid data
remaining in these parts is being advanced from register to register on
80 nsec boundaries and YBUF.S1 and YBUF.S0 are not valid. In this case,
the AM29520 register selection is performed by prom SC7 which calculates
XBUF.S1 and XBUF.S0 on the basis of the current zoom and multiplexes these
signals with YBUF.S1 and YBUF.S0 to generate BUF.S1 and BUF.S0 which
drive the register select inputs (S1 and S0) of the AM29520s.

For each bit plane, the four bit outputs of the AM29520s are clocked into
two levels of 74F374 buffers by C(40Z.0-20Z) to provide eight consequetive
bits on a horizontal scan line. Seven of these eight bits are then feed
into a barrel shifter controlled by the two LSBs of the pixel pan origin.
Panning to a resolution of four pixels is accomplished by other mechanisms
and the barrel shifters allow pan to be controlled to the resolution of
a single pixel. The implementation of pan is discussed further in the
following section.

The four bit output of the per-plane 74F350 barrel shifters is connected
to a 10H124 TTL-to-ECL converter and the level shifted signals connect to
the load inputs of a 10H141 ECL shift register. The select lines to the
shift registers, E.ZERO1 and E.LOAD, are generated by the card's ECL
circuitry and are described in section [Figure](#clocks). The shift registers are
constantly clocked at a 100 Mhz rate.

The 100 MHz shift register data output, E.MA.A..E.MA.H, is wire-ORed with
the addresses used to update the digital-to-analog converter's internal
color map and are re-clocked by the 10H176 hex registers at U1610 and U1613.
The resynchronized data is labeled E.A7..E.A0 and feeds the address inputs
to the DAC. Internally to the hybrid, the DAC address inputs are connected to
a 256 entry color map which translates the address to a 24-bit
data value. The 24-bit translated address is registered and then split
to drive three eight-bit video DACs whose outputs are directly connected to
Red, Green, and Blue coax connectors on the Sun-2 color card.


---

## Zoom Synchronization and Pan

<a id="zandp"></a>

"Zoom Synchronization" should probably be called "Zoom Clock Synchronization".
The zoom synchronization logic performs the very important task of
synchronizing the zoom clock C(40Z.0-20Z) to state10 of the memory state
machine and synchronizing the memory state machine to the horizontal state
machine which generates horizontal sync and display enable.

Understanding of zoom syncronization requires a detailed knowledge of the
implementation of zoom and pan.  Zoom is easy and has been described in
section [Figure](#memaddr) on memory addressing and in section [Figure](#clocks) on
clock timing. To summarize, zoom in the vertical direction is controlled by
inhibiting the increment of the Scan-Line Base Address counter which causes
scan lines to be merely repeated; and, zoom in the horizontal direction is
performed by stretching the zoom clock C(40Z.0-20Z) and running a variable
number of video read/write cycles after each video refresh cycle.  As described
earlier, pixel replication also requires games with the output enables of the
AM29520 video buffers and with the ECL shifter control signals E.ZERO and
E.LOAD.

The pan logic on the Sun-2 color card has not yet been adequately described
and is a bit difficult to understand. Pan is actually controlled with several
different mechanisms and each mechanism increases the pan resolution just a
bit more.

First, the most coarse means of controlling pan is to load a new value in
the Word-Pan Base Address. This address controls the upper-left corner of
the display to a grain-size of 64 pixels.

To pan horizontally within the 64 pixel boundary, three more mechanisms are
employed. The first may or may not reduce the pan resolution to 16 pixels.
For zoom values of four or more, 16 pixels will take a minimum of 16 40nsec
states to be output. During this time we could run at least one memory
read/write cycle and one nibble-mode video refresh cycle. If zoom exceeds
or equals four, ZCRAMP is asserted by prom SC7 and the AM29520 buffer
select signals, BUF.S1 and BUF.S0, select one of the four AM29520 registers
to drop our horizontal pan resolution to 16 pixels. The different
values of BUF.S1 and BUF.S0 are computed with the mulitiplexor at U400 and
the counter at U401.  The number of read/write cycles performed after the
first video refresh cycle on a scan line also changes. ZSYNC80 is fed into
proms SC8 and SC9 to modify RMW_TC and SPARE_TC (see memory control timing)
for the first set of memory read/write cycles after the start of the horizontal
scan line.  For zoom values of zero to three, this mechanism is not used and
the pan resolution will have remained at 64 pixels.

The most clever mechanism to perform horizontal pan is the use of the
zoom syncronization signal, ZSYNC, to slide state10 of the memory state
machine in relation to the horizontal state machine.
The zoom syncronization prom SC10 controls pan down to a resolution of
four pixels. The inputs to prom SC10 are the value of zoom and the
low-order bits specifying horizontal pan. Prom SC10 then computes a
variable starting point for the memory control cycle against the horizontal
state. The output of prom SC10, ZH9..ZH2, is compared with the
horizontal state, H9..H2, by the AM25LS2521 at U414. On a match, the
hex counter at U415 is reset and counts back to 15 where it holds. The
terminal count output of U415 is registered and forms ZSYNC. While ZSYNC
is asserted, the memory control prom SC11 advances to state10 and holds.
At the the trailing edge of ZSYNC the memory control state machine resumes
and continues to state11. Likewise, the assertion of ZSYNC disables
C(40Z.0-20Z) and the trailing edge of ZSYNC causes the assertion of
C(40Z.0-20Z) at a fixed point relative to the memory state machine.

The last mechanism to control horizontal pan achieves a pan resolution of
a single pixel. This mechanism was described as part of the
video output data paths in section [Figure](#vodata). The outputs of the AM29520
video buffers change with C(40Z.0-20Z) and are resynchronized with a 74F374.
The four bits of data from each memory plane are then pipelined one more
stage and seven of the bits from each memory plane are run through a four-bit
74F350 barrel-shifter. This mechanism allows the user to specify any unique
pixel as the origin of the display; for clarification, I define a "pixel"
as having a duration of: 10nsec * (zoom+1).

Pan resolutions of partial pixels may now be desired. Moving the screen in
the vertical direction is easy.  To move the screen vertically, we merely
specify the vertical width, in pixels, of the top line of the display. This
value is the "Line-Offset" and occupies bits D7..D4 of the zoom register. No
more pan resolution in the vertical direction is required.

Pan resolutions of partial pixels in the horizontal direction is difficult,
but may be done with software tricks for certain values of zoom. A 16 value
variable POFF3..POFF0 is used to delay the leading edge of ZSYNC 40 nsec at
at a time so that we can readily pan to any 40 nsec boundary within a pixel.
Likewise, if the duration of individual pixels is relatively prime to 40 nsec,
we can use simple algebra to pick a starting pixel and a value of POFF3..POFF1
that will move the origin to any arbitrary 10 nsec boundary within the image.


---

## Horizontal State Machine


The horizontal state machine increments by fours on 40 nanosecond boundaries
and consists of three 74F163 counters (U1700, U1701, U1702), prom SC17
(U1703) and half a 74F374 register (U1704). The horizontal state machine
generates the signals HSYNC, H1152, HRESET and DISPON.

The horizontal sync, HSYNC, is ORed with vertical sync, VSYNC, and is
connected directly to a coax connector on the color card. HSYNC is asserted
every 16 usec and operates independently of vertical sync.

HRESET clears the horizontal state machine to state zero.

DISPON enables the video DACs. With DISPON inactive, the video DAC outputs
are forced to the video blanking level. Prom SC17 internally gates DISPON
with VBLANK to keep DISPON deasserted during video blanking.

Signal H1152 is asserted before HSYNC but after DISPON. H1152 is used
by the 74F74 section #1 at U314 to deassert V_CNT as quickly as possible
after DISPON. V_CNT, which controls the increment and load functions of
the Video Display Address counter, is reasserted by ZSYNC which can be
asserted very early in the horizontal retrace for certain values of zoom
and pan. The duration of V_CNT at a logic zero must be as long as possible
to ensure that the Video Display Address counter is properly loaded from
the Scan Line Base Address counter before the display of the next scan line.
A secondary use of signal H1152 is to enable the AM25LS2521 comparator at
U1710. This comparator generates the signal NZBOT to disable zoom after a
specified horizontal scan line. The timing below is shown for the
1152x900 display.


```

 State  00000000000000.....1111111111111111111111.....1111111111111.....11111
        00000000000000.....1112222222222222222222.....3333333333333.....44445
        00011222334445.....8990001122233444556667.....3344455666778.....88990
        04826048260482.....8260482604826048260482.....2604826048260.....48260

HSYNC\  --------------------------__________________________-----------------

H1152   _______________________-------------_________________________________

HRESET  ___________________________________________________________________-_

DISPON  ___________----------________________________________________________

```


---

## Vertical State Machine


The vertical state machine increments at the end of every horizontal
state machine cycle. The vertical state machine consists of three 74F163
counters (U1705, U1706, U1707), prom  SC18 (U1708), half a 74F374 register
(U1704), the No-Zoom Register (U1709), and an eight-bit comparator (U1710).
The vertical state machine generates the signals VSYNC, VRESET, VBLANK,
and NZBOT.

The vertical sync, VSYNC, is connected directly to a coax connector
on the color card. VSYNC is asserted every 15.16 msec and operates
independently of horizontal sync.

VRESET clears the vertical state machine to state zero.

VBLANK primarily forces the video DACs to the video blanking level. VBLANK
also enables some MC10124 TTL-to-ECL converters and is used by pal SC16 to
control the loading of the ECL color map with the TTL shadow color map.
VBLANK clocks the syncronized versions of the zoom and pan registers used
by the color board logic and clocks the interrupt
flip-flop to generate an interrupt if INTEN is asserted. Lastly, the
well-used signal VBLANK enables loading the frame buffer Scan
Line Base Address counter from the Word Pan Base Address register.

The signal NZBOT clears the zoom and pan registers and resets the Scan Line
Base Address to zero. NZBOT is used to create a menu region at the bottom of
the CRT where zoom and pan are disabled. The No-Zoom register at U1709
can be read and written by user software and its outputs are feed into a
comparator and compared with the high-order bits of the vertical line number.
On a match, NZBOT is asserted as soon as the display of the current line
has completed and all subsequent lines on the display will be shown unzoomed
and unpanned. The origin of the non-zoomed region will always be
frame buffer address zero. The timing below is shown for the 1152x900 display.


```

 State  00000000000000000......8888888889999999999999999999999999999999999999
	00000000000000000......9999999990000000000111111111112222222222333333
        01234567890123456......1234567890123456789012345678901234567890123456

VSYNC\  ----------------------------------____-------------------------------

VBLANK\ --------------------------------_____________________________________

VRESET\ --------------------------------------------------------------------_

```


---

## Color Maps and D-to-A Converters


The color map video translation tables and the video DACs are combined into
an ECL hybrid measuring two inches on a side. Because of the real-time
constraints in updating the ECL color map, a TTL shadow color map is used
for software read/write accesses and a status register bit controls loading
of the ECL color map from the TTL shadow color map during vertical retrace.

When status register bit UPCMAP (from 74ALS273 at U207) is deasserted, read
and write updates to the shadow color map can occur.
The color map is part of the control register
address space and accesses to it are acknowledged as with any control
register access by the bus-interface pal SC1.
Note how UPCMAP is syncronized once by CK.UPCM to the low-order horizontal
state machine bits H2 and H3; the syncronized signal is called UPCMAP1 and
is used as the select line to the 74ALS257 multiplexors at U1600, U1601, and
U1602. With UPCMAP1 deasserted, the multiplexors select the shadow
color map address lines T.A10..T.A1 from the on-board address bus
A10..A1 and the AM2949 buffer at U1605 is enabled to
connect the data bus D7..D0 to the shadow color map data lines
T.D7..T.D0. The shadow color map itself consists of the two 1Kx4 static
ram at U1603 and U1604 and all control signals necessary to access the
shadow color map are generated by pal SC16 at U1606.

When status register bit UPCMAP is asserted, all software accesses to the
shadow color map will be inhibited but will be properly acknowledged.
As before, UPCMAP is reclocked by CK.UPCM to form UPCMAP1 which will
now select the shadow color map address lines from a combination of
bits V3..V0 and H9..H4 in the vertical and horizontal state machines.
The rising edge of CK.UPCM is generated when <H3,H2> changes from <1,1>
to <0,0> and prevents the color map addresses from changing during a write to
the ECL color map. As implied, UPCMAP can be asserted or deasserted at
any time without corrupting the ECL or TTL color maps.

With UPCMAP asserted, vertical blanking
enables the TTL-to-ECL converters at U1608, U1611, U1614 and U1615.
The address inputs E.A7..E.A0 to the hybrid DAC are now equivalent to
address bits T.A8..T.A1 on the shadow color map and the data inputs
E.D7..E.D0 to the hybrid DAC are driven by the data outputs of the TTL
shadow color map. The vertical state machine bits V2 and V3 drive the
two high-order address inputs T.A9 and T.A8 on the shadow color maps,
and they are used by pal SC16 to select one of the red, green or blue
ECL color maps (signals CS.RED, CS.GRN and CS.BLU). With V3..V2 in the
range of 0-2 and <H3,H2> equal to <1,0>, pal SC16 asserts WE.ECL which is
connected through some level translators to the hybrid DAC. During
vertical blanking with UPCMAP asserted, one byte is transferred from the
shadow color map to the ECL color map every 160 nsec and the ECL color map
is completely loaded in 16 vertical scan lines.

The red, green and blue digital-to-analog converters (DACs) are included
with their color maps in the single hybrid. Testing of the
ECL color maps and the DACs, however, poses a bit of a problem.
Testing of both the ECL color maps and the DACs can be
performed by drawing separate red, green and blue ramps on the CRT
display. These ramps of color can be visually inspected for non-linearities
and glitches.


---

## RasterOp Architecture

<a id="ROParch"></a>


### RasterOp Overview


A simple understanding of the rasterop architecture is necessary
to debug problems with the frame buffer memory. However, rasterops need
only be understood well enough to disable them before frame buffer
debugging begins. All told, there are ten frame buffer addressing
modes. Two of these modes, Word-Mode Memory and Pixel-Mode Memory, do
not use the rasterop chips; the other eight do.

The ten addressing modes access a variable number of planes or pixels.
The eight RasterOp modes load the ROPC destination registers from the frame
buffer on either reads or writes. The RasterOp addressing modes also load
the ROPC source registers from either the frame buffer or the VME data bus;
the source registers are loaded sometimes on read, sometimes on write
The ten addressing modes are described more fully in the user's manual and
are:


```

   A21 A20 ROPMOD  SIZE       LD.SRC        LD.DST       Description
   ----------------------------------------------------------------------
    0   0    X    1 Plane      NONE   	     NONE      Word-mode memory
    0   1    X  1-2 Pixel      NONE   	     NONE      Pixel-mode memory
    1   0    0  All Plane   Fr VME on Wr  Fr FB on Rd  ROP Normal Word-mode
    1   0    1  1-2 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Normal Pixel-mode
    1   0    2  All Plane   Fr VME on Wr  Fr FB on Wr  ROP Normal Wd-mode HRead
    1   0    3  1-2 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Normal Pix-mode HRead
    1   0    4  All Plane   Fr  FB on Rd  Fr FB on Rd  ROP Scroll Word-mode
    1   0    5   16 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Fill Pixel-mode
    1   0    6  All Plane   Fr  FB on Rd  Fr FB on Wr  ROP Scroll Wd-mode HRead
    1   0    7   16 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Fill Pixel-mode HRead
    1   1    X                  NONE   	     NONE      Control Registers
   ----------------------------------------------------------------------

```


There are three basic ideas with the rasterop addressing modes. First,
Rasterops can operate on word-mode or pixel-mode data. Since rasterops are
traditionally used to speed the combination of text with graphics,
word-mode rasterops are well defined and understood. Rasterops on pixel
data seem fairly useless, however, if another mechanism exists for masking
updates to specific bit planes. To make pixel-mode rasterops more useful,
he implementation actually operates on all 16 pixels lying within a
particular word boundary. Using pixel-mode rasterops, for instance, a
general-purpose area fill subroutine could be written that requires
less rasterop set-up time than if any word-mode addressing mode were used.

Another idea with the rasterop decoding is that word-mode rasterops can
operate on all frame buffer bit planes in parallel. Using these Parallel
Word-Mode addressing modes, data can be read 128 bits in parallel into
the source registers of the per-plane rasterop chips and can be combined
with 128 bits of data from the destination address. Using 128-bit BitBlt
operations is extremely useful for fast copy or scroll operations.

The third major feature with Sun-2 color rasterops is that the destination
data need not always be read before the rasterop proceeds. With the Sun-2
monochrome implementation, the ROPC destination data is always loaded on
a raster operation. With the Sun-2 color, however, loading the destination
registers takes an extra 640 nsec. The keyword 'Hidden Read' describes
addressing modes that take the extra time to implicitly load the ROPC
destination registers.

One extension of the concept that rasterops can operate on all bit planes
in parallel is that the rasterop chips can also be written to in parallel
to speed rasterop set-up. Rasterop write decoding is performed by the
pals SC2 and SC3 at locations U204 and U205. If a ninth
psuedo rasterop chip is accessed for write, all rasterop chips will
have the same register loaded with the same data.


### Normal Rasterops without Hidden Read Cycles


RasterOp modes zero, one and five perform normal rasterop cycles without hidden
read. These addressing modes are nearly identical to the memory-mapped
addressing modes 'Word-Mode Memory' and 'Pixel-Mode Memory' which are described
fully in section [Figure](#MemIDP) on the frame buffer input data paths.

RasterOp mode zero uses word-mode addresses and updates all bit planes enabled
by the per-plane mask register. RasterOp mode one operates on a single pixel
or an 16-bit odd/even pixel pair. RasterOp mode five operates on upto 16
adjacent pixels at a time as determined by the rasterop mask registers.

On write cycles, the signals XMIT_WD and XMIT_PIX
are gated with the input A_LATCH150 to pal SC5 such that these signals
are only asserted for 150 nsec after FB.REQ. As you should recall from section
[Figure](#MemIDP), these control signals enable the data buffers between the
internal data bus D15..D0 and the 64K ram data inputs.

In rasterop modes where the ROPC source registers are loaded from the VME
on write, pal SC4 asserts LD_SRC for 100 nsec to strobe the rasterop chip
source registers with the input data MI15.H..MI0.H through MI15.A..MI0.A.
Fifty nanoseconds later, pal SC5 deasserts XMIT_WD or
XMIT_PIX and simultaneously asserts OE.ROPC to drive the 64K ram data
inputs with the outputs of the per-plane rasterop chips. During the time
LD_SRC is asserted, pal SC4 also asserts END_RINC which delays the earliest
possible assertion of RMW; this scheme allows us to meet the worst-case
set-up of LD_SRC to rasterop output data valid.  Note also that
pixel-mode and word-mode accesses load the rasterop chip source registers
with different data. On word-mode accesses, the rasterop source registers
are written in parallel with the data on D15..D0. With pixel-mode accesses,
the source register for memory plane A is loaded with <D8,D0,D8,D0...,D8,D0>,
memory plane B is loaded with <D9,D1,D9,D1..,D9,D1>, and so on.

Read cycles with rasterop support are only slightly different from read cycles
without rasterop support. These read cycles proceed exactly
as described in section [Figure](#MemIDP), but when the read data is valid
on the memory input data bus (MI15.H..MI0.H through MI15.A..MI0.A),
pal SC4 may generate either a LD_SRC or LD_DST pulse; otherwise, read cycles
with and without rasterops are identical.

The following diagrams show a read cycle followed by a write cycle, followed
by another read cycle. The addressing mode is a normal Word-Mode cycle with
ROP support; the source registers are loaded on write, the destination registers
are loaded on read.  Diagrams showing pixel-mode read and write cycles would be
identical except that XMIT_PIX would be asserted in place of XMIT_WD.
Signals FB.REQ, RD/WR, LD_SRC, XMIT_WD and OE.ROPC are asyncronous and the
rest are syncronous. The memory cycle shown assumes a zoom of zero.


```

Memory State 00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF00

FB.REQ\	     ------------__________________---------------_________________----

RD/WR\	     xxxxxxxxxxx___________________xxxxxxxxxxxxxxx-----------------xxxx

LD_SRC\      ------------_____-------------------------------------------------

XMIT_WD\     ------------_______-----------------------------------------------

OE.ROPC\     -------------------___________------------------------------------

C(40.0-20)   -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

RAS\	     ----__________________----______----__________________----______--

CAS\	     __----____--__--__--____----______----____--__--__--____----______

RMW	     ____________________------------____________________------------__

RDAT(0-120)  ____________________________------__________________________------

LD_DST\      ____------------------------------------------------------------__

```


### Normal Rasterops with Hidden Read Cycles

<a id="Hread"></a>

RasterOp addressing modes two, three and seven perform normal rasterop
cycles with hidden read. With these addressing modes, read accesses are
identical to memory-mapped read cycles and the rasterop chips are not affected.
On write accesses, these addressing modes perform a read cycle to load the ROPC
destination registers and then perform a write cycle to write the ROPC output
data to the frame buffer.

RasterOp mode two uses word-mode addresses and updates all bit planes enabled
by the per-plane mask register. RasterOp mode three operates on a single pixel
or an 16-bit odd/even pixel pair. RasterOp mode seven operates on upto 16
adjacent pixels at a time as determined by the rasterop mask registers.

On a write, D15..D0 is transferred to the ram input data bus by
XMIT_WD or XMIT_PIX which is asserted for the first 150 nsec
after the assertion of FB.REQ.

During hidden read cycles, the 74F74 flip-flops at U210 come into use.
On the first memory update cycle, both HR.TOG and HR.TOG1 will be
deasserted. Pal SC4 uses these inputs in conjuction with A22..A19 to
deassert FB.WR. The deassertion of FB.WR causes pal SC5 to assert XMIT_DST
and generate LD_DST after the first memory update cycle; the deassertion
of FB.WR also inhibits the write enables to frame buffer memory.

At memory control state 14 in the first memory update cycle, HR.TOG
will be asserted. If we next proceed to run a video refresh cycle, STATE4_10
will become asserted and HR.TOG1 will be set; otherwise, HR.TOG1 will be set
at state 14 in the second memory update cycle which will perform a dummy read
cycle.  When HR.TOG1 is asserted, FB.WR will be asserted and
pal SC5 will subsequently assert OE.ROPC to prepare for the final memory
write cycle. Because FB.WR can be asserted during the middle of a dummy
read cycle, it is re-clocked by U509-1 before it used by pals SC14 and SC15
to generate the per-plane write strobes to the frame buffer memory.

On frame buffer accesses that perform no hidden read cycle, pal SC4 generates
END_RMW as soon as RDAT(80-200) is asserted. With accesses that perform a
hidden read, pal SC4 gates END_RMW with HR.TOG and HR.TOG1 so that END_RMW
is not asserted until both a read and write cycle have been performed.

The following diagram depicts a memory write cycle using hidden read.
The following diagram assumes a large value of zoom.


```


   State     0011112233445566778899AABBCCDDEEFFBBCCDDEEFFBBCCDDEEFFBBCCDDEEFF00

FB.REQ\	     ----------__________________________________________--------------

LD_SRC\	     ----------_____---------------------------------------------------

XMIT_WD\     ----------_______-------------------------------------------------

C(40.0-20)   -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

RAS\	     ------__________________----______----______----______----______--

CAS\	     __------____--__--__--____----______----______----________________

RMW_INC      __________________--________--________--________--________--______

RMW	     ______________________--------------------------------____________

   State     0011112233445566778899AABBCCDDEEFFBBCCDDEEFFBBCCDDEEFFBBCCDDEEFF00

RDAT(0-120)  ____________________________------____------____------____________

HR.TOG	     ______________________________-----------------------_____________

HR.TOG1	     ________________________________________-------------_____________

FB.WR\	     ----------------------------------------____________--------------

XMIT_DST\    _________________-------________________-------------_____________

LD_DST\      --------------------------------______----------------------------

OE.ROPC\     ----------------------------------------__________________________

END_RMW\     ----------------------------------------------------__------------

```


### Windowing Word-Mode Rasterops


The remaining two addressing modes are rasterop modes four and six. Both
modes operate on word-mode addresses and update all planes enabled by the
per plane mask register.  Both rasterop modes load the source registers
with frame buffer data on read cycles.  Both rasterop modes also load the
destination data from the frame buffer; mode four loads the destination
registers on read cycles and  mode six loads the destination registers with
a hidden read cycle.

These two addressing modes are extremely useful for rapid frame buffer to
frame buffer copy operations. With these addressing modes, for instance,
the inner loop of a window moving routine could move 16 pixels at a time with
a 16-bit read followed by a 16-bit write.

The following diagram shows a read cycle followed by a write cycle for rasterop
mode six. The diagram assumes a large value of zoom.


```


   State     5566778899AABBCCDDEEFFBB...CDDEEFFBBCCDDEEFFBBCCDDEEFFBBCCDDEEFFBB

FB.REQ\	     -----_______________-------___________________________________----

RD/WR\       --------------------------________________________________________

FB_RD\       -----_______________-------_______________________----------------

XMIT_WD\     ---------------------------_______--------------------------------

C(40.0-20)   -_-_-_-_-_-_-_-_-_-_-_-_..._-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

RAS\	     ____________----______--...-______----______----______----______--

CAS\	     --__--__--____----__________________----______----______----______

RMW_INC      ______--________--______..._--________--________--________--______

RMW	     __________------------__________--------------------------------__

   State     5566778899AABBCCDDEEFFBB...CDDEEFFBBCCDDEEFFBBCCDDEEFFBBCCDDEEFFBB

RDAT(0-120)  ________________------________________------____------____------__

HR.TOG	     __________________---___________________-----------------------___

HR.TOG1	     __________________________________________________-------------___

XMIT_DST\    _____-------_______________-----------------------________________

LD_SRC\	     --------------------______----------------------------------------

LD_DST\      ------------------------------------------______------------------

OE.ROPC\     --------------------------------------------------________________

WE.A\..WE.H\ ----------------------------------------------------------______--

END_RMW\     --------------------__----------------------------------------__--

```


---

# Programmable Logic


This chapter contains the source files for programmable logic elements such
as PALs and PROMs. These source files are written using macros and
procedure calls in the programming language C.


## Definition of Proms


Without attempting to give a full definition of the prom macros
used, the following explanation should prove sufficient to explain the
programs. The prom macros are included in a file named "prom.c".

*#define INPUT1 (a0)* (or a statement in the same format) maps input
signals to the address lines on the prom.

*#define state (cvb(IN3)*d3 + cvb(IN2)*d2 + cvb(IN1)*d1 + cvb(IN0)*d0)*
decodes the potential inputs IN3..IN0 into a value in the range of zero
to fifteen. The same format can be used to decode data busses of any width.
The macro "cvb" is a mnuemonic meaning ConVert-to-Binary and the macros
of the form "dn" return a value of 2 to the power n.

*prom1024x4*, or a statement with the same form, sets the number of
addressable locations in the prom (in this case 1024). The width of
the prom (in this case 4) is irrelevant.

*prombegin* tells the program to evaluate the following statements until
*promend* for each addressable location in the prom.

*prom(#1,#2,expression) means to put the value of *expression* into
Prom *#1* bit position *#2*.  A single prom program can define the
contents of multiple proms with the same address inputs by using different
values for prom number *#1*.

*promend* terminates the evaluation of statements.

*writeprom("file",#1)* writes the object code of prom *#1* into file
*file*. The object code of each prom must be written to a separate
file. The object code generated at Sun Microsystems uses the Intel
Hexadecimal format. Compiling and executing the prom source code is
done using the standard C compiler.


---

## Definition of Pals


The definition of pals is somewhat different than the definition of
proms.

*Palytpe <paltype>* specifies the pal type.

*Palname <name>* specifies the file name of the pal.

*Palid SCCS %I% %E%* is used by the Source Code Control System to maintain
a revision history of the pal.

*PALBEGIN* tells the program to begin evaluation of the pal code.

*% <comment>* is a comment. The comment continues until the end-of-line.

*<Pin #> INPUT <pin name>* binds a symbolic name to an input pin number.
All inputs must be explicitly declared for test vector generation as some
output pins can be used as inputs.

*<Pin #> OUTPUT <pin name>* binds an symbolic name to an output pin.

*<Pin #> GND* defines the ground pin on the pal.

*<Pin #> VCC* defines the ground pin on the pal.

*<Pin #> OUTPUT-ENABLE <pin name>* binds a symbolic name to a input pin
used only as an output enable for a set of outputs. The sun-2 color card
uses only Pal16L8As which do not have common output enables.

*<Pin #> CLOCK <pin name>* binds a symbolic name to a clock input for
registered pals.

*: <function_name> <function text> ;* defines an intermediate function term.

*ASSERT <output name>* begins the definition of a new output term.

*ENABLE <term> [term]+* is required for outputs with output enables and
lists the terms that should be ANDed together to enable the output.

*OR <term> [term]+* specifies the AND terms that should connect to a single
OR input. An output can has as many OR terms as the pal physically supports.
The next *ASSERT <output name>* will begin the next output term. Carraige
returns and blank lines are not relevent.

*PALEND* terminates the evaluation of pal source code.


---

## PAL SC1


% ======================================================================
%  Pal Name: SC1
%  Pal Type: 16L8-A
%  Speed: 25 nsec. 35 nsec works but slows board access.
%  Purpose: Control VME-Bus data transfers and interrupt acknowledge
%  Notes:
%    1*	The trailing edge of A.LATCH occurs at the same time as the leading
%	edge of END.REQ, but the leading edge of A.LATCH is delayed from the
% 	trailing edge of END.REQ to insure that the clear input to the FB.REQ
%	flip-flop is deasserted before the flip-flop can be re-clocked.
%    2) The output A.LATCH is inverted. The product terms for A.LATCH define
%	when to deassert A.LATCH.
%    3) On interrupt acknowledge handshaking, we assume we interrupt at
%	level 4. Secondly, to meet the setup time from data to DTACK,
%	we first assert RD.IACK,- then RD.WORD- after one pal delay, and
%	finally IDTACK- after another pal delay.
%  ======================================================================

paltype pal16l8
palname SC1
palid 1.15 84/08/19

PALBEGIN

% Inputs

1  INPUT fb.req-
2  INPUT rd/wr\
3  INPUT bdsel-
4  INPUT end_rmw-
5  INPUT rdat(80-200)
6  INPUT ds-
7  INPUT a1_or_a2
8  INPUT a_latch100
9  INPUT ireq1
11 INPUT iackin

10 GND
20 VCC

% Outputs

19 OUTPUT wr.word-
18 OUTPUT rd.word-
17 OUTPUT a_latch
16 OUTPUT end_req-
15 OUTPUT rd.ack-
14 OUTPUT dtack-
13 OUTPUT rd.iack-
12 OUTPUT p1.iackout-

% Define intermediates

: wr / rd/wr\ ;
: read rd/wr\ ;

% Program Pal Outputs. A.LATCH active high; all other outputs active LOW.

ASSERT a_latch
ENABLE ALWAYS
OR	end_rmw & wr & / dtack			% Deassert at end of Write
OR	end_rmw & read & / rdat(80-200) & / ds 	% Deassert at end of Rd
OR	/ fb.req & / ds & / iackin		% Deassert til next strobe
OR	/ fb.req & / bdsel & / iackin & / dtack % Deassert til next strobe
OR	end_rmw & / a_latch			% Hold for a few pal delays
OR	end_req					% Wait till clear gone

ASSERT rd.word-
ENABLE ALWAYS
OR	fb.req & read
OR	rd.iack

ASSERT wr.word-
ENABLE ALWAYS
OR	fb.req & wr

ASSERT end_req-
ENABLE ALWAYS
OR	fb.req & end_rmw & / a_latch & wr
OR	fb.req & end_rmw & / a_latch & read & / rdat(80-200) & / ds

ASSERT rd.ack-
ENABLE ALWAYS
OR	fb.req & read & end_rmw & / rdat(80-200)
OR	rd.iack & dtack
OR	dtack & wr & a_latch & / a_latch100	% Prevent dtack reassertion

ASSERT dtack-
ENABLE ALWAYS
OR	ds & bdsel & / a_latch100 & / rd.ack
OR	rd.iack & a_latch100
OR	dtack & ds

ASSERT rd.iack-
ENABLE ALWAYS
OR	ds & / fb.req & ireq1 & iackin & / a1_or_a2

ASSERT p1.iackout-
ENABLE ALWAYS
OR	ds & / fb.req & iackin & / ireq1 & a_latch100
OR	ds & / fb.req & iackin & a1_or_a2 & a_latch100


TIMING: NO-CLOCK
%		12345678901234567890123456789012345678901234567890
fb.req-		---________-_______----________-------------------
wr.word-	---________-_______-------------------------------
rd.word-	-----------------------________--_____------------
rd/wr\		_____________________-----------------------------
a_latch		___-------_-------_____-------__------___------___
a_latch100	____-------__------_____-------__-----____-----___
ds-		---____---______--___--_______--______---______---
bdsel-		---____---______-------_______--______---______---

dtack-		---____----_____-------_______--______---______---
rdat(80-200)    -_________--______--______--______________________
end_req-	----------_-------_-----------_-------------------
end_rmw-	_---------_-------_--------____-------------------
rd.ack-		---_-------__---------------___--_____------------

a1_or_a2	_________________________________________---------
ireq1		_________________________________--------_________
iackin		________________________________------___------___
rd.iack-	---------------------------------_____------------
p1.iackout-	------------------------------------------_____---

PALEND


---

## PAL SC2


% ======================================================================
%  Pal Name: SC2
%  Pal Type: 16L8
%  Speed: 25 nsec.
%  Purpose: Generate Write Strobes for ROPC planes A..D
%  ======================================================================

paltype pal16l8
palname SC2
palid 1.4 84/07/23

PALBEGIN

% Inputs

1  INPUT a12
2  INPUT a13
3  INPUT a14
4  INPUT a15
5  INPUT a16
6  INPUT c.req-
7  INPUT msk.a
8  INPUT msk.b
9  INPUT msk.c
11 INPUT msk.d
18 INPUT rd/wr\
17 INPUT a_latch100

% Outputs

19 OUTPUT rd.regs1-
16 OUTPUT wr.regs1-
15 OUTPUT w.rop.a-
14 OUTPUT w.rop.b-
13 OUTPUT w.rop.c-
12 OUTPUT w.rop.d-

% Define intermediates

: wr		/ rd/wr\ ;
: read		  rd/wr\ ;
: plane0	/ a16 & / a15 & / a14 & / a13 & / a12 ;
: plane1	/ a16 & / a15 & / a14 & / a13 &   a12 ;
: plane2	/ a16 & / a15 & / a14 &   a13 & / a12 ;
: plane3	/ a16 & / a15 & / a14 &   a13 &   a12 ;
: plane_all	/ a16 &   a15 & / a14 & / a13 & / a12 ;

% Program Pal Outputs. All outputs Active LOW.

ASSERT rd.regs1-
ENABLE ALWAYS
OR	c.req & read & / a16 & a15

ASSERT wr.regs1-
ENABLE ALWAYS
OR	c.req & wr & / a_latch100 & / a16 & a15

ASSERT w.rop.a-
ENABLE ALWAYS
OR	c.req & wr & / a_latch100 & plane0
OR	c.req & wr & / a_latch100 & plane_all & msk.a

ASSERT w.rop.b-
ENABLE ALWAYS
OR	c.req & wr & / a_latch100 & plane1
OR	c.req & wr & / a_latch100 & plane_all & msk.b

ASSERT w.rop.c-
ENABLE ALWAYS
OR	c.req & wr & / a_latch100 & plane2
OR	c.req & wr & / a_latch100 & plane_all & msk.c

ASSERT w.rop.d-
ENABLE ALWAYS
OR	c.req & wr & / a_latch100 & plane3
OR	c.req & wr & / a_latch100 & plane_all & msk.d

TIMING: NO-CLOCK
%		12345678901234567890123456789012345678901234567890
c.req-		________________________________------------------
a_latch100	________________________________------------------
a12		_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
a13		__--__--__--__--__--__--__--__--__--__--__--__--__
a14		____----____----____----____----____----____----__
a15		________--------________--------________--------__
a16		________________----------------________________--
msk.a		--------------------------------__________________
msk.b		--------------------------------__________________
msk.c		--------------------------------__________________
msk.d		--------------------------------__________________
read		____________----__________________________________

rd.regs1-	------------____----------------------------------
wr.regs1-	--------____--------------------------------------
w.rop.a-	_-------_-----------------------------------------
w.rop.b-	-_------_-----------------------------------------
w.rop.c-	--_-----_-----------------------------------------
w.rop.d-	---_----_-----------------------------------------

PALEND


---

## PAL SC3


% ======================================================================
%  Pal Name: SC3
%  Pal Type: 16L8
%  Speed: 25 nsec.
%  Purpose: Generate Write Strobes for ROPC planes E..H
%  ======================================================================

paltype pal16l8
palname SC3
palid 1.6 84/07/24

PALBEGIN

% Inputs

1  INPUT a12
2  INPUT a13
3  INPUT a14
4  INPUT a15
5  INPUT a16
6  INPUT c.req-
7  INPUT msk.e
8  INPUT msk.f
9  INPUT msk.g
11 INPUT msk.h
17 INPUT a_latch100
18 INPUT rd/wr\

10 GND
20 VCC

% Outputs

19 OUTPUT rd.regs0-
16 OUTPUT pin16
15 OUTPUT w.rop.e-
14 OUTPUT w.rop.f-
13 OUTPUT w.rop.g-
12 OUTPUT w.rop.h-

% Define intermediates

: wr		/ rd/wr\ ;
: read		  rd/wr\ ;
: plane4	/ a16 & / a15 &   a14 & / a13 & / a12 ;
: plane5	/ a16 & / a15 &   a14 & / a13 &   a12 ;
: plane6	/ a16 & / a15 &   a14 &   a13 & / a12 ;
: plane7	/ a16 & / a15 &   a14 &   a13 &   a12 ;
: plane_all	/ a16 &   a15 & / a14 & / a13 & / a12 ;

% Program Pal Outputs. All outputs Active LOW.

ASSERT w.rop.e-
ENABLE ALWAYS
OR	c.req & wr & / a_latch100 & plane4
OR	c.req & wr & / a_latch100 & plane_all & msk.e

ASSERT w.rop.f-
ENABLE ALWAYS
OR	c.req & wr & / a_latch100 & plane5
OR	c.req & wr & / a_latch100 & plane_all & msk.f

ASSERT w.rop.g-
ENABLE ALWAYS
OR	c.req & wr & / a_latch100 & plane6
OR	c.req & wr & / a_latch100 & plane_all & msk.g

ASSERT w.rop.h-
ENABLE ALWAYS
OR	c.req & wr & / a_latch100 & plane7
OR	c.req & wr & / a_latch100 & plane_all & msk.h

ASSERT rd.regs0-
ENABLE ALWAYS
OR	c.req & read & / a16 & / a15
OR	c.req & read & / a16 & a15 & / a14 & / a13 & / a12

TIMING: NO-CLOCK
%		12345678901234567890123456789012345678901234567890
c.req-		________________________________------------------
a_latch100	________________________________------------------
a12		_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
a13		__--__--__--__--__--__--__--__--__--__--__--__--__
a14		____----____----____----____----____----____----__
a15		________--------________--------________--------__
a16		________________----------------________________--
msk.e		--------------------------------__________________
msk.f		--------------------------------__________________
msk.g		--------------------------------__________________
msk.h		--------------------------------__________________
read		----______________________________________________

rd.regs0-	____----------------------------------------------
w.rop.e-	----_---_-----------------------------------------
w.rop.f-	-----_--_-----------------------------------------
w.rop.g-	------_-_-----------------------------------------
w.rop.h-	-------__-----------------------------------------

pin16		??????????????????????????????????????????????????

PALEND


---

## PAL SC4


% ======================================================================
%  Pal Name: SC4
%  Pal Type: 16L8
%  Speed: 25 nsec.
%  Purpose: Decode Frame buffer access mode and implications for strobes
%	on ROPC chips. This Pal handles the hidden read cycles to load
%	the destination data into the ROPC.
%  Decoding:
%  A21 A20 ROPMOD ACCESS      LD.SRC        LD.DST       Description
%  ----------------------------------------------------------------------
%   0   0    X    1 Plane      NONE   	     NONE      Word-mode memory
%   0   1    X    1 Pixel      NONE   	     NONE      Pixel-mode memory
%   1   0    0  0-7 Plane   Fr VME on Wr  Fr FB on Rd  ROP Normal Word-mode
%   1   0    1    1 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Normal Pixel-mode
%   1   0    2  0-7 Plane   Fr VME on Wr  Fr FB on Wr  ROP Normal Wd-mode HRead
%   1   0    3    1 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Normal Pix-mode HRead
%   1   0    4  0-7 Plane   Fr  FB on Rd  Fr FB on Rd  ROP Scroll Word-mode
%   1   0    5   16 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Fill Pixel-mode
%   1   0    6  0-7 Plane   Fr  FB on Rd  Fr FB on Wr  ROP Scroll Wd-mode HRead
%   1   0    7   16 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Fill Pixel-mode HRead
%   1   1    X                  NONE   	     NONE      Control Registers
%
%  ======================================================================

paltype pal16l8
palname SC4
palid 1.7 84/07/24

PALBEGIN

% Inputs

1  INPUT a20
2  INPUT a21
3  INPUT ropmod0
4  INPUT ropmod1
5  INPUT ropmod2
6  INPUT hr.tog
7  INPUT hr.tog1
8  INPUT fb.req-
9  INPUT rd/wr\
11 INPUT rdat(80-200)
17 INPUT a_latch150
18 INPUT a_latch100

10 GND
20 VCC

% Outputs

19 OUTPUT end_rinc-
16 OUTPUT end_rmw-
15 OUTPUT ld_src-
14 OUTPUT ld_dst-
13 OUTPUT fb.wr-
12 OUTPUT pin12-

% Define intermediates

: wr		/ rd/wr\ ;
: read		  rd/wr\ ;

: cycle1	  hr.tog & / hr.tog1 ;		% After one rmw cycle
: cycle2 	  hr.tog &   hr.tog1 ;		% After two fast rmw cycle
: cycle3	/ hr.tog &  hr.tog1 ;		% After three fast rmw cycle

: after_cycle1	  rdat(80-200) & hr.tog ;
: after_cycle2	  rdat(80-200) & hr.tog1 ;
: after_cycle3	  rdat(80-200) & hr.tog1 & / hr.tog ;

: mode_wd	/ a21 & / a20 ;
: mode_pix	/ a21 &   a20 ;
: mode_wdpix	/ a21 ;
: mode_1357	  a21 & / a20 &   ropmod0 ;
: mode_0145	  a21 & / a20 & / ropmod1 ;
: mode_2367	  a21 & / a20 &   ropmod1 ;
: mode_0123	  a21 & / a20 & / ropmod2 ;
: mode_46	  a21 & / a20 &   ropmod2 & / ropmod0 ;
: mode_57	  a21 & / a20 &   ropmod2 &   ropmod0 ;
: ctrl	  	  a21 &   a20 ;

% Program Pal Outputs. All outputs Active LOW.

ASSERT end_rmw-
ENABLE ALWAYS
OR	fb.req & mode_wd   & after_cycle1	% Set
OR	fb.req & mode_pix  & after_cycle1	% Set
OR	fb.req & mode_0145 & after_cycle1	% Set
OR	fb.req & mode_2367 & after_cycle3	% Set
OR	fb.req & ctrl   & a_latch150		% Set
OR	fb.req & end_rmw 			% Hold

ASSERT end_rinc-
ENABLE ALWAYS
OR	fb.req & ld_src    & wr			% t + 120 nsec
OR	fb.req & mode_wd   & after_cycle1	% Set
OR	fb.req & mode_pix  & after_cycle1	% Set
OR	fb.req & mode_0145 & after_cycle1	% Set
OR	fb.req & mode_2367 & after_cycle3	% Set
OR	fb.req & ctrl				% Set
OR	fb.req & end_rmw 			% Hold

ASSERT fb.wr-
ENABLE ALWAYS
OR	fb.req & / end_rmw & mode_wdpix & wr
OR	fb.req & / end_rmw & mode_0145  & wr
OR	fb.req & / end_rmw & mode_2367  & wr & hr.tog1  % Hidden Read Cycle

ASSERT ld_src-
ENABLE ALWAYS
OR	fb.req & wr & mode_0123 & / a_latch100
OR	fb.req & wr & mode_57   & / a_latch100
OR	fb.req & read  & mode_46   & cycle1 & rdat(80-200)

ASSERT ld_dst-
ENABLE ALWAYS
OR	fb.req & read  & mode_0145 & cycle1 & rdat(80-200)
OR	fb.req & wr & mode_2367 & cycle1 & rdat(80-200)


TIMING: NO-CLOCK
%		1234567890123456789012345678901234567890123456789
a20		-------__________________________________________
a21		-------_______-----------------------------------
ropmod0		_________________________________________________
ropmod1		______________----------------___________________
ropmod2		_________________________________________________
hr.tog		___________--______--------_________--________--_
hr.tog1		_______________________-----_____________________
rd/wr\		_____________________________----------__________
a_latch100	___---___----____-----------_____-----____------_
a_latch150	____--____---_____----------______----_____-----_
rdat(80-200)	____________--_____--__--__--________--________--
fb.req-		--____--_____---____________----______---_______-

end_rmw-	----__------_--------------_---------_---------_-
end_rinc-	--____------_---_----------_---------_---_-----_-
fb.wr-		--------____-----------____--------------______--
ld_src-		----------------_------------------------_-------
ld_dst-		-------------------__----------------_-----------
pin12		?????????????????????????????????????????????????

PALEND


---

## PAL SC5


% ======================================================================
%  Pal Name: SC5
%  Pal Type: 16L8A
%  Speed: 25 nsec.
%  Purpose: In conjunction with Pal SC4, this IC controls the strobes and
%	buffer enables for the RasterOp Chips.
%  Decoding:
%  A21 A20 ROPMOD ACCESS      LD.SRC        LD.DST       Description
%  ----------------------------------------------------------------------
%   0   0    X    1 Plane      NONE   	     NONE      Word-mode memory
%   0   1    X    1 Pixel      NONE   	     NONE      Pixel-mode memory
%   1   0    0  0-7 Plane   Fr VME on Wr  Fr FB on Rd  ROP Normal Word-mode
%   1   0    1    1 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Normal Pixel-mode
%   1   0    2  0-7 Plane   Fr VME on Wr  Fr FB on Wr  ROP Normal Wd-mode HRead
%   1   0    3    1 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Normal Pix-mode HRead
%   1   0    4  0-7 Plane   Fr  FB on Rd  Fr FB on Rd  ROP Scroll Word-mode
%   1   0    5   16 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Fill Pixel-mode
%   1   0    6  0-7 Plane   Fr  FB on Rd  Fr FB on Wr  ROP Scroll Wd-mode HRead
%   1   0    7   16 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Fill Pixel-mode HRead
%   1   1    X                  NONE   	     NONE      Control Registers
%
%  ======================================================================

paltype pal16l8
palname SC5
palid 1.5 84/08/24

% Inputs

1  INPUT a20
2  INPUT a21
3  INPUT ropmod0
4  INPUT fb.req-
5  INPUT rd/wr\
6  INPUT fb.wr-
7  INPUT a_latch150
8  INPUT a11
9  INPUT ropmod2
11 INPUT end_rmw-

10 GND
20 VCC

% Outputs

19 OUTPUT xmit_wd-
18 OUTPUT xmit_pix-
17 OUTPUT oe.ropc-
16 OUTPUT xmit_dst-
15 OUTPUT rcv_wd-
14 OUTPUT rd.pix-
13 OUTPUT c.req-
12 OUTPUT rd.ropc-

% Define intermediates

: wr		/ rd/wr\ ;
: read		  rd/wr\ ;
: mem_word	/ a21 & / a20 ;
: mem_pix	/ a21 &   a20 ;
: rop_word	  a21 & / a20 & / ropmod0 ;
: rop_pix	  a21 & / a20 &   ropmod0 ;
: ropc		  a21 & / a20 ;
: ctrl	  	  a21 &   a20 ;
: mode_02  	  a21 & / a20 & / ropmod2 & / ropmod0 ;
: mode_46  	  a21 & / a20 &   ropmod2 & / ropmod0 ;

% Program Pal Outputs. All outputs Active LOW.

ASSERT xmit_wd-
ENABLE ALWAYS
OR	fb.req & mem_word & wr
OR	fb.req & mode_02 & wr & / a_latch150
OR	fb.req & ctrl  & wr & / a11

ASSERT xmit_pix-
ENABLE ALWAYS
OR	fb.req & mem_pix & wr
OR	fb.req & rop_pix & wr & / a_latch150
OR	fb.req & ctrl & wr & a11		% Load ROPC sideways

ASSERT oe.ropc-
ENABLE ALWAYS
OR	fb.req & ropc & fb.wr & a_latch150
OR	fb.req & mode_46 & fb.wr

ASSERT xmit_dst-
ENABLE ALWAYS
OR	fb.req & read & / a21
OR	fb.req & read & / a20
OR	fb.req & ropc & / fb.wr & wr & a_latch150
OR	fb.req-					% Don't let memory inputs float

ASSERT rcv_wd-
ENABLE ALWAYS
OR	fb.req & mem_word & read
OR	fb.req & rop_word & read
OR	fb.req & ctrl  & read

ASSERT rd.pix-
ENABLE ALWAYS
OR	fb.req & mem_pix & read
OR	fb.req & rop_pix & read

ASSERT c.req-
ENABLE ALWAYS
OR	fb.req & ctrl & wr & / a_latch150 & / end_rmw
OR	fb.req & ctrl & read

ASSERT rd.ropc-
ENABLE ALWAYS
OR	fb.req & ctrl & read


TIMING: NO-CLOCK
%		12345678901234567890123456789012345678901234567890
a11		_____________________________________-------------
a20		------------______________________________________
a21		------------____________--------------------------
ropmod0        	___----__--__________________________-------------
ropmod2        	_________________________-________________________
a_latch150	___--___---___---___---____---___---___----___---_
end_rmw-	--_-------_---------------------------------------

c.req-		-_-----____---------------------------------------
fb.req-		-____--____--____--____--_____--____--_____--____-

xmit_wd-	-____--------____---------_-----------------------
xmit_pix-	--------------------------------------_-----------
xmit_dst-	_----__----__----________--_--________-_---_______

rd/wr\		______------______------_______------_______------
fb.wr-		-------------____---___--_--__----------___-------
oe.ropc-	-------------------------_--__----------___-------

rcv_wd-		-------____--------____---------____--------------
rd.pix-		---------------------------------------------____-
rd.ropc-	-------____---------------------------------------

PALEND


---

## PAL SC6


% ======================================================================
%  Pal Name: SC6
%  Pal Type: 16L8A
%  Speed: 25 nsec.
%  Purpose: Controls output enable multiplexing of addresses to 64K rams
%	and instruction type to address counters.
%  ======================================================================

paltype pal16l8
palname SC6
palid 1.7 84/07/24

PALBEGIN

% Inputs

1  INPUT pix-
2  INPUT vblank
3  INPUT dispon
4  INPUT state11_15-
5  INPUT rmw1
6  INPUT nzbot-
7  INPUT v0
8  INPUT end_rinc-
9  INPUT h1152
11 INPUT v1

10 GND
20 VCC

% Outputs

19 OUTPUT end_rinc2-
18 OUTPUT end_rinc1-
17 OUTPUT base_i0-
16 OUTPUT base_i1-
15 OUTPUT nz.en-
14 OUTPUT a_wd-
13 OUTPUT a_pix-
12 OUTPUT a_dis-

% Define intermediates

: word 	/ pix ;

% Program Pal Outputs. All outputs Active LOW.

% 74LS461 I0__I1 codes_ LL = Clear_ LH = Load_ HL = Hold_ HH = Incr_
% For scan line base address:
%	If (vblank) { Load(LH) }
%	else if (nzbot) { Clear(LL) }
%	else if (dispon) { Incr(HH) }
%	else { Hold(HL) }

ASSERT base_i1-
ENABLE ALWAYS
OR	/ vblank & / dispon

ASSERT base_i0-
ENABLE ALWAYS
OR	vblank
OR	nzbot

ASSERT a_wd-
ENABLE ALWAYS
OR	word & state11_15 & rmw1

ASSERT a_pix-
ENABLE ALWAYS
OR	pix & state11_15 & rmw1

ASSERT a_dis-
ENABLE ALWAYS
OR	/ state11_15
OR	/ rmw1

ASSERT nz.en-
ENABLE ALWAYS
OR	/ vblank & v0 & v1 & h1152

ASSERT end_rinc1-
ENABLE ALWAYS
OR	end_rinc

ASSERT end_rinc2-
ENABLE ALWAYS
OR	end_rinc
OR	end_rinc1


TIMING: NO-CLOCK
%		1234567890123456
dispon		_-_-_-_-_-_-_-_-
nzbot-		__--__--__--__--
vblank		____----____----
base_i0-	__--______--____
base_i1-	_-_-----_-_-----

rmw1		_-_-_-_-_-_-_-_-
pix-		__--__--__--__--
state11_15-	____----____----
a_wd-		---_-------_----
a_pix-		-_-------_------
a_dis-		_-_-_____-_-____

h1152		_-_-_-_-_-_-_-_-
v0		__--__--__--__--
v1		____--------____
nz.en-		-----------_----

end_rinc-	____----____----
end_rinc1-	____----____----
end_rinc2-	____----____----

PALEND


---

## PROM SC7


static char* sccs_id = "1.1 84/04/23";

/* ======================================================================
   Prom Name: SC7
   Prom Type: 512 x 8.
   Speed: 35 nsec.
   Purpose: This cosmopolitan prom generates signals for the video output
	buffers, the memory address counters, and the memory state machine.
   Note: The AM29520 buffer select controls (BUF.S0..1) will not change
	quickly enough when the 74F257 select line STATE4_10 is changing.
	This problem was circumvented by defining the period of STATE4_10
	such that both sets of inputs to the 74F257 are identical whenever
	STATE4_10 changes.
   ====================================================================== */

#include "/usr/local/pl/prom.c"

#define range(low,x,high) ((low<=x)&&(x<=high))

/* Define Inputs */
#define st0   	 (a0)
#define st2	 (a1)
#define zoom0	 (a2)
#define zoom2 	 (a3)
#define pu	 (a4)
#define zoom3	 (a5)
#define zoom1	 (a6)
#define st3_     (a7)
#define st1	 (a8)


/* Define Intermediates and Outputs from Prom */

#define state (cvb(st0)*d0+cvb(st1)*d1+cvb(st2)*d2+cvb(!st3_)*d3)
#define zoom  (cvb(zoom0)*d0+cvb(zoom1)*d1+cvb(zoom2)*d2+cvb(zoom3)*d3+1)

#define RegB2 0			/* Register Assignments in AM29520 */
#define RegB1 1
#define RegA2 2
#define RegA1 3

/* Define next register to output from AM29520. */
#define buf buffer()
buffer()
{  short buff;
   if (range(0,state,2) || range(11,state,15)) {
       buff = 0;		/* Don't Care */
   } else {
       if (zoom==1) {
          if (range(3,state,4)) {
	     buff = RegA2;
          } else if (range(5,state,8)) {
	     buff = RegB1;
          } else if (range(9,state,10)) {
	     buff = RegB2;
	  }
       } else if (zoom==2) {
          if (range(3,state,4)) {
	     buff = RegA1;
          } else if (range(5,state,6)) {
	     buff = RegA2;
          } else if (range(7,state,8)) {
	     buff = RegB1;
          } else if (range(9,state,10)) {
	     buff = RegB2;
	  }
       } else if (zoom==3) {
          if (range(3,state,4)) {
	     buff = RegA1;
          } else if (range(5,state,7)) {
	     buff = RegB1;
          } else if (range(8,state,10)) {
	     buff = RegB2;
	  }
       } else if (zoom==4) {
          if (range(3,state,4)) {
	     buff = RegA1;
          } else if (range(5,state,6)) {
	     buff = RegA2;
          } else if (range(7,state,10)) {
	     buff = RegB2;
	  }
       } else if (zoom==5) {
          if (range(3,state,4)) {
	     buff = RegA1;
          } else if (range(5,state,5)) {
	     buff = RegA2;
          } else if (range(6,state,10)) {
	     buff = RegB2;
	  }
       } else {
          if (range(3,state,4)) {
	     buff = RegA1;
	  } else {
	     buff = RegB2;
	  }
       }
   }
   return(buff);
}

#define state10      (state==10)
#define zcramp       (zoom < 4)
#define state4_10    range(4,state,10)
#define video_cnt    range(4,state,11)
#define video_ck     ((state==10)||(state==14))
#define state11_15   range(11,state,14)

main()
{
prom512x8;

prombegin
prom(0,d0,(buf & d0))
prom(0,d1,(buf & d1))
prom(0,d2,!state10)
prom(0,d3,!zcramp)
prom(0,d4,!state4_10)
prom(0,d5,!video_cnt)
prom(0,d6,!video_ck)
prom(0,d7,!state11_15)
promend;

writeprom("sc7",0);
}


---

## PROM SC8


static char* sccs_id = "1.2 84/04/23";

/* ======================================================================
   Prom Name: SC8
   Prom Type: 512 x 8.
   Speed: Any.
   Purpose: With zoom disabled, a memory cycle consists of one nibble-mode
	read cycle for the video display and one optional read/write cycle
	for accesses to the frame buffer. With the zoom register non-zero,
	a memory cycle consists of one nibble-mode read cycle for the video
	display, a number of optional read/write cycles, and a few spare
	states.

	This prom computes the number of frame buffer read/write cycles
	to perform after loading the video data buffers so that the total
	length of the video cycle, the spare states, and the rmw cycles
	equals 16 times the zoom factor.

	When the zoom register is set to three or greater, the total length
	of the extended memory cycle (nibble mode read plus multiple
	read/write cycles) at the start of each scan line may vary because
	less than four words from the video buffers may actually be displayed.
	The reason we don't always display all four words at the start of
	each scan line: At the largest possible zoom, one "extended" memory
	cycle would last longer than the time available for horizontal retrace.
   Note: The inputs to this prom change at the start of vertical blanking.
	However, at the start of vertical blanking, the signal RMW_TC is
	not used until memory control state15 which occurs about 600 nsec
	down the road.
   ====================================================================== */

#include "/usr/local/pl/prom.c"
#define DIV /
#define MOD %
#define range(low,x,high) ((low<=x)&&(x<=high))

/* Define Inputs to 512 x 8 Prom. */
#define zoom0  (a0)
#define zoom2  (a1)
#define za4    (a2)
#define zsync_ (a3)
#define nused1 (a4)
#define nused2 (a5)
#define za5    (a6)
#define zoom3  (a7)
#define zoom1  (a8)

/* Define Intermediates */

#define zoom zooom()
zooom()
{  int i;
   i = (cvb(zoom0)*d0+cvb(zoom1)*d1+cvb(zoom2)*d2+cvb(zoom3)*d3)+1;
   return(i);
}

#define zsync (! zsync_)
#define za (cvb(za4)*d0 + cvb(za5)*d1)

#define st_cycle    16		/* 16 states in a memory cycle (720 nsec) */
#define st_word      4		/* 4 states to output one word (16-bits) */

#define zcramp (zoom < 4)

/* Compute number of 46nsec states required to output the first
   one, two, three, or four words at the start of a scan line. */
#define rmwcnt rmwct()
rmwct()
{ short i;
  if (zsync && (!zcramp)) {
     i = (st_cycle*zoom - za*st_word*zoom - 11) DIV 5;
  } else {
     i = (st_cycle*zoom - 11) DIV 5;
  }
  i = (i-1)*2;			/* RMW_INC valid for 2 states */
  i = 255 - i;
  return(i);
}

#define spares spare()
spare()
{ short i;
  if (zsync && (!zcramp)) {
     i = (st_cycle*zoom - za*st_word*zoom - 11) MOD 5;
  } else {
     i = (st_cycle*zoom - 11) MOD 5;
  }
  return(i);
}

main()
{
prom512x8;

prombegin
prom(0,d0,(rmwcnt & d0))
prom(0,d1,(rmwcnt & d1))
prom(0,d2,(rmwcnt & d2))
prom(0,d3,(rmwcnt & d3))
prom(0,d4,(rmwcnt & d4))
prom(0,d5,(rmwcnt & d5))
prom(0,d6,(rmwcnt & d6))
prom(0,d7,(rmwcnt & d7))
promend;

writeprom("sc8",0);
}


---

## PROM SC9


static char* sccs_id = "1.2 84/04/23";

/* ======================================================================
   Author: Peter Costello
   Date :  July 15, 1983
   Prom Name: SC9
   Prom Type: 512 x 8.
   Speed: Any.
   Purpose: With zoom disabled, a memory cycle consists of one nibble-mode
	read cycle for the video display and one optional read/write cycle
	for accesses to the frame buffer. With the zoom register non-zero,
	a memory cycle consists of one nibble-mode read cycle for the video
	display, a number of optional read/write cycles, and a few spare
	states.

	This prom computes the number of spare states on which the memory
	controller should just hold so that the total length of the video
	cycle, the spare states, and the rmw cycles equals 16 times the
	zoom factor.

	When the zoom register is set to three or greater, the total length
	of the extended memory cycle (nibble mode read plus multiple
	read/write cycles) at the start of each scan line may vary because
	less than four words from the video buffers may actually be displayed.
	The reason we don't always display all four words at the start of
	each scan line: At the largest possible zoom, one "extended" memory
	cycle would last longer than the time available for horizontal retrace.
   Note: The inputs to this prom change at the start of vertical blanking.
	However, at the start of vertical blanking, the signal RMW_TC is
	not used until memory control state15 which occurs about 600 nsec
	down the road.
   ====================================================================== */

#include "/usr/local/pl/prom.c"
#define DIV /
#define MOD %
#define range(low,x,high) ((low<=x)&&(x<=high))

/* Define Inputs to 512 x 8 Prom. */
#define zoom0  (a0)
#define zoom2  (a1)
#define za4    (a2)
#define zsync_ (a3)
#define nused1 (a4)
#define nused2 (a5)
#define za5    (a6)
#define zoom3  (a7)
#define zoom1  (a8)

/* Define Intermediates */

#define zoom zooom()
zooom()
{  int i;
   i = (cvb(zoom0)*d0+cvb(zoom1)*d1+cvb(zoom2)*d2+cvb(zoom3)*d3)+1;
   return(i);
}

#define zsync (! zsync_)
#define za (cvb(za4)*d0 + cvb(za5)*d1)

#define st_cycle    16		/* 16 states in a memory cycle (720 nsec) */
#define st_word      4		/* 4 states to output one word (16-bits) */

#define zcramp (zoom < 4)

/* Compute number of 46nsec states required to output the first
   one, two, three, or four words at the start of a scan line. */
#define rmwcnt rmwct()
rmwct()
{ short i;
  if (zsync && (!zcramp)) {
     i = (st_cycle*zoom - za*st_word*zoom - 11) DIV 5;
  } else {
     i = (st_cycle*zoom - 11) DIV 5;
  }
  i = 256 - i;
  return(i);
}

#define spares spare()
spare()
{ short i;
  if (zsync && (!zcramp)) {
     i = (st_cycle*zoom - za*st_word*zoom - 11) MOD 5;
  } else {
     i = (st_cycle*zoom - 11) MOD 5;
  }
  return(i);
}

main()
{
prom512x8;

prombegin
prom(0,d0,!(spares & d0))
prom(0,d1,!(spares & d1))
prom(0,d2,!(spares & d2))
prom(0,d3,1)
prom(0,d4,1)
prom(0,d5,1)
prom(0,d6,1)
prom(0,d7,1)
promend;

writeprom("sc9",0);
}


---

## PROM SC10


static char* sccs_id = "1.5 84/07/17";

/* ======================================================================
   Author: Peter Costello
   Date :  July 15, 1983
   Prom Name: SC10
   Prom Type: 8K x 8.
   Speed: Any.
   Purpose:
	Prom SC10 generates the horizontal state (H2-H10) at which the
	signal ZSYNC is generated. ZSYNC is asserted for 15 clock periods,
	and the trailing edge is used to syncronize the memory controller
	to the start of the next video scan line.
   Zoom and Pan Timing:
	Pan is accomplished by four separate mechanisms. We can pan a
	pixel at a time in the vertical direction, but only four pixels
	at a time in the horizontal direction. Hopefully this will not
	be noticeable.

	The origin of the display is controlled to a resolution of
	four words (64 frame-buffer pixels) by the Pan Base Address.
	These high-order bits (Z.A19..Z.A6) are loaded into a counter
	which is incremented after each video memory cycle.

	Increasing the pan resolution from four words to one word horizontally
	is effected by loading the word number to start displaying into Video
	Buffer Output Control Unit.

	Prom SC10 generates signal ZSYNC which forces the memory cycles
	to start on the four pixel boundary specified.

	Pan to one pixel units is performed by a barrel shifter just before
	the parallel-in serial-out shift registers (74F194) for each
	memory plane.
   Notes:
     1) When zoom is disabled, state 0 of the memory control timing
	coincides with horizontal state 0.
     2) When zoom syncronization (ZSYNC) is released, the memory control
	state machine will be holding at state 10, and will proceed from
	that point.
     3) The inputs to SC10 can be cleared by NZBOT\ or clocked by VBLANK.
	During these periods, the output of the address comparator is forced
	inactive by the signals NZBOT\ or H10.
   ====================================================================== */

#include "/usr/local/pl/prom.c"
#define DIV /
#define MOD %
#define range(low,x,high) ((low<=x)&&(x<=high))

/* Define Inputs to 8K x 8 Prom. */
#define za5      (a0)		/* Word of four */
#define za4      (a1)
#define zoom3    (a2)		/* Zoom */
#define zoom2    (a3)
#define zoom1    (a4)
#define zoom0    (a5)
#define pix2     (a6)		/* Pixel Div 4 */
#define pix3     (a7)
#define poff0    (a8)		/* Pixel Offset Fudge-Factor */
#define poff1    (a9)
#define poff3    (a10)
#define poff2    (a11)
#define input12  (a12)


/* Define intermediate terms */

#define pixoff poff()
poff()
{ short i;
  i = (cvb(poff0)*d0 + cvb(poff1)*d1 + cvb(poff2)*d2 + cvb(poff3)*d3);
  return(i);
}

#define pixel pix()
pix()
{ short i;
  i = (cvb(pix2)*d2 + cvb(pix3)*d3);
  return(i);
}

#define zoom zom()
zom()
{ short i;
  i = (cvb(zoom0)*d0 + cvb(zoom1)*d1 + cvb(zoom2)*d2 + cvb(zoom3)*d3) + 1;
  return(i);
}

#define total_states (1504>>2)

#define za   (cvb(za4)*d0 + cvb(za5)*d1)

#define st_cycle    16		/* 16 states in a memory cycle (64 pixels) */
#define st_word      4		/* 4 states to output one word (16 pixels) */

#define zsync_off    9		/* At the trailing edge of ZSYNC\, we are
				   holding at the start of state10. However,
				   there is a one state pipeline between the
				   outputs of prom SC11 and the registered
				   versions of these outputs. */
#define zsync_phase 17		/* One state after the address match, a
				   74LS163 is cleared, another state later,
				   ZSYNC is asserted. Fifteen states later,
				   ZSYNC is deasserted. */

/* Compute number of 46nsec states required to output the first
   one, two, three, or four words at the start of a scan line. */

#define states (st_cycle*zoom - za*st_word*zoom)
#define zcramp (zoom < 4)

/* Compute starting state for zoom syncronization. */
zstrt()
{  short i;
   /* Compute starting state assuming 'pixel=0' and 'poff=0'. */
   if (zcramp) {
      i = total_states + zsync_off - zsync_phase - za*st_word*zoom;
   } else {
      i = total_states + zsync_off - zsync_phase;
   }

   /* Compute offset for given pixel and pixel offset */
   /* i -= (pixel DIV 4)*zoom + ((pixoff MOD zoom) DIV 4); CHANGED: 10/7/83. */
   i -= (pixel DIV 4)*zoom + pixoff;

   /* Sub out piece for pixel pipeline */
   i -= 3 * (zoom-1);

   if (i < (1152>>2)) i = (1152>>2);
   return(i);
}

/* Convert unit of measure to horizontal pixels. */
#define zstart (zstrt()<<2)

main()
{
prom8192x8;

prombegin
prom(0,d0,(zstart & d3))
prom(0,d1,(zstart & d5))
prom(0,d2,(zstart & d7))
prom(0,d3,(zstart & d9))
prom(0,d4,(zstart & d8))
prom(0,d5,(zstart & d6))
prom(0,d6,(zstart & d4))
prom(0,d7,(zstart & d2))
promend;

writeprom("sc10",0);
}


---

## PROM SC11


static char* sccs_id = "1.2 84/04/23";

/* ======================================================================
   Author: Peter Costello
   Date :  July 15, 1983
   Prom Name: SC11
   Prom Type: 512 x 8.
   Speed: 35 nsec.
   Purpose: This file contains the source code for prom SC11 on the Sun-2
	color board. This prom controls the memory cycles on the frame
	buffer memory.

	The frame buffer memory cycle starts with a video refresh cycle.
	The state machine then performs read/write cycles (states 11..15)
	until the signal RMW_TC is asserted. If RMW_TC is asserted in
	state 15, then the memory controller advances to state 0. At
	state 1, the state machine pauses until the signal SPARE_TC is
	asserted.

	When the signal ZSYNC\ is asserted, the memory controller has
	15 clock periods to finish the operation in progress and
	pause at state 10. When signal ZSYNC\ is deasserted, the
	memory controller simply continues.

	During horizontal retrace, the signal FAST_CNT\ is asserted. When
	this signal is asserted, no video read cycles are required, and
	the memory controller simply runs back-to-back read/write cycles.
   ====================================================================== */

#include "/usr/local/pl/prom.c"

#define DIV /
#define MOD %
#define range(low,x,high) ((low<=x)&&(x<=high))

/* Define Inputs to 512 x 8 Prom. */
#define st0   	  (a0)
#define st2  	  (a1)
#define rmw       (a2)
#define spare_tc  (a3)
#define fast_cnt_ (a4)
#define rmw_tc	  (a5)
#define zsync_	  (a6)
#define st3_      (a7)
#define st1       (a8)

/* Define Intermediates and Outputs from Prom */

#define zsync    (!zsync_)
#define go_fast  ((!fast_cnt_)&&(zsync_))

#define state sstate()
sstate()
{  short st;
   st = (cvb(st0)*d0+cvb(st1)*d1+cvb(st2)*d2+cvb(!st3_)*d3);
   return(st);
}

/* Define next state. */
#define nstate nnstate()
nnstate()
{  short nst;
   if (zsync) {
      if (state==10) {
	 nst = 10;			/* Wait Here */
      } else {
	 nst = (state + 1) MOD 16;
      }
   } else if ((state==15)&&((!rmw_tc)||go_fast)) {
      nst = 11;
   } else if ((state==1)&&(!spare_tc)) {
      nst = 1;
   } else {
      nst = (state + 1) MOD 16;
   }
   return(nst);
}

/* RAS delayed 40 nsec before output to 64K ram. */
#define ras raas()
raas()
{ short i;
  i = range(1,state,9) || range(12,state,14);
  return(i);
}

#define rmw_inc rmwi()
rmwi()
{ short i;
   i = range(8,state,9) || range(13,state,14);
   return(i);
}

#define rdat0_120 (rmw && range(13,state,15))

#define cbuf ((state==3)||(state==5)||(state==7)||(state==9))

main()
{
prom512x8;

prombegin
prom(0,d0, (nstate & d0))
prom(0,d1, (nstate & d2))
prom(0,d2, rdat0_120)
prom(0,d3,!ras)
prom(0,d4,!cbuf)
prom(0,d5, rmw_inc)
prom(0,d6,!(nstate & d3))
prom(0,d7, (nstate & d1))
promend;

writeprom("sc11",0);
}


---

## PAL SC12


%  ======================================================================
%  Pal Name: SC12
%  Pal Type: 16L8-A
%  Speed: 25 nsec
%  Purpose: Controls CAS7..CAS0 for all frame buffer accessing modes.
%	CAS7 corresponds to the bit D7 in a word-mode access, CAS6
%	corresponds to bit D6, and so on.
%  Note: Signals Cas7..Cas0 are held low during unused memory read/write
%	cycles. This prevents the outputs of the 64K ram from floating and
%	potentially causing problems for the AM29520 buffers. This does not
%	increase 64K ram power consumption since power consumption is
%	determined by the Ras timing.
%  ======================================================================

paltype pal16l8
palname SC12
palid 1.6 84/07/24

PALBEGIN

% Inputs

1  INPUT st0
2  INPUT st1
3  INPUT st2
4  INPUT st3-
5  INPUT rmw_lds-
6  INPUT a1
7  INPUT a2
8  INPUT a3
9  INPUT one_pix-
11 INPUT rmw_uds-

10 GND
20 VCC

% Outputs

19 OUTPUT cass0
18 OUTPUT cass1
17 OUTPUT cass2
16 OUTPUT cass3
15 OUTPUT cass4
14 OUTPUT cass5
13 OUTPUT cass6
12 OUTPUT cass7

% Define intermediates

: state0	/ st3 & / st2 & / st1 & / st0 ;
: state1	/ st3 & / st2 & / st1 &   st0 ;
: state2	/ st3 & / st2 &   st1 & / st0 ;
: state3	/ st3 & / st2 &   st1 &   st0 ;
: state4	/ st3 &   st2 & / st1 & / st0 ;
: state5	/ st3 &   st2 & / st1 &   st0 ;
: state6	/ st3 &   st2 &   st1 & / st0 ;
: state7	/ st3 &   st2 &   st1 &   st0 ;
: state8	  st3 & / st2 & / st1 & / st0 ;
: state9	  st3 & / st2 & / st1 &   st0 ;
: state10	  st3 & / st2 &   st1 & / st0 ;
: state11	  st3 & / st2 &   st1 &   st0 ;
: state12	  st3 &   st2 & / st1 & / st0 ;
: state13	  st3 &   st2 & / st1 &   st0 ;
: state14	  st3 &   st2 &   st1 & / st0 ;
: state15	  st3 &   st2 &   st1 &   st0 ;

: state12_13	  st3 &   st2 & / st1 ;

: pix8		   a3 & /  a2 & /  a1 & rmw_uds ;
: pix9		   a3 & /  a2 & /  a1 & rmw_lds ;
: pix10		   a3 & /  a2 &    a1 & rmw_uds ;
: pix11		   a3 & /  a2 &    a1 & rmw_lds ;
: pix12		   a3 &    a2 & /  a1 & rmw_uds ;
: pix13		   a3 &    a2 & /  a1 & rmw_lds ;
: pix14		   a3 &    a2 &    a1 & rmw_uds ;
: pix15		   a3 &    a2 &    a1 & rmw_lds ;

% Program Pal Outputs. All outputs Active LOW.

ASSERT cass0
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix15
OR	state12_13 & / one_pix & rmw_lds

ASSERT cass1
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix14
OR	state12_13 & / one_pix & rmw_lds

ASSERT cass2
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix13
OR	state12_13 & / one_pix & rmw_lds

ASSERT cass3
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix12
OR	state12_13 & / one_pix & rmw_lds

ASSERT cass4
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix11
OR	state12_13 & / one_pix & rmw_lds

ASSERT cass5
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix10
OR	state12_13 & / one_pix & rmw_lds

ASSERT cass6
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix9
OR	state12_13 & / one_pix & rmw_lds

ASSERT cass7
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix8
OR	state12_13 & / one_pix & rmw_lds

TIMING: NO-CLOCK
%		123456789012345678901234567890123456789012345678
st0		_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
st1		__--__--__--__--________________________________
st2		____----____------------------------------------
st3-		--------________________________________________
rmw_uds-	----------------_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
rmw_lds-	-----------------_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
one_pix-	--------------------------------________________
a1		__________________--__--__--__--__--__--__--__--
a2		____________________----____----____----____----
a3		________________________--------________--------

cass0		-__--_-_-_-------_-_-_-_-_-_-_-_---------------_
cass1		-__--_-_-_-------_-_-_-_-_-_-_-_--------------_-
cass2		-__--_-_-_-------_-_-_-_-_-_-_-_-------------_--
cass3		-__--_-_-_-------_-_-_-_-_-_-_-_------------_---
cass4		-__--_-_-_-------_-_-_-_-_-_-_-_-----------_----
cass5		-__--_-_-_-------_-_-_-_-_-_-_-_----------_-----
cass6		-__--_-_-_-------_-_-_-_-_-_-_-_---------_------
cass7		-__--_-_-_-------_-_-_-_-_-_-_-_--------_-------

PALEND


---

## PAL SC13


%  ======================================================================
%  Pal Name: SC13
%  Pal Type: 16L8-A
%  Speed: 25 nsec
%  Purpose: Controls CAS15..CAS8 for all frame buffer accessing modes.
%	CAS15 corresponds to the bit D15 (the MSB) in a word-mode access,
%	CAS14 corresponds to bit D14, and so on.
%  Note: Signals Cas15..Cas8 are held low during unused memory read/write
%	cycles. This prevents the outputs of the 64K ram from floating and
%	potentially causing problems for the AM29520 buffers. This does not
%	increase 64K ram power consumption since power consumption is
%	determined by the Ras timing.
%  ======================================================================

paltype pal16l8
palname SC13
palid 1.7 84/07/24

PALBEGIN

% Inputs

1  INPUT st0
2  INPUT st1
3  INPUT st2
4  INPUT st3-
5  INPUT rmw_lds-
6  INPUT a1
7  INPUT a2
8  INPUT a3
9  INPUT one_pix-
11 INPUT rmw_uds-

% Outputs

19 OUTPUT cass8
18 OUTPUT cass9
17 OUTPUT cass10
16 OUTPUT cass11
15 OUTPUT cass12
14 OUTPUT cass13
13 OUTPUT cass14
12 OUTPUT cass15

% Define intermediates

: state0	/ st3 & / st2 & / st1 & / st0 ;
: state1	/ st3 & / st2 & / st1 &   st0 ;
: state2	/ st3 & / st2 &   st1 & / st0 ;
: state3	/ st3 & / st2 &   st1 &   st0 ;
: state4	/ st3 &   st2 & / st1 & / st0 ;
: state5	/ st3 &   st2 & / st1 &   st0 ;
: state6	/ st3 &   st2 &   st1 & / st0 ;
: state7	/ st3 &   st2 &   st1 &   st0 ;
: state8	  st3 & / st2 & / st1 & / st0 ;
: state9	  st3 & / st2 & / st1 &   st0 ;
: state10	  st3 & / st2 &   st1 & / st0 ;
: state11	  st3 & / st2 &   st1 &   st0 ;
: state12	  st3 &   st2 & / st1 & / st0 ;
: state13	  st3 &   st2 & / st1 &   st0 ;
: state14	  st3 &   st2 &   st1 & / st0 ;
: state15	  st3 &   st2 &   st1 &   st0 ;

: state12_13	  st3 &   st2 & / st1 ;

: pix0		/  a3 & /  a2 & /  a1 & rmw_uds ;
: pix1		/  a3 & /  a2 & /  a1 & rmw_lds ;
: pix2		/  a3 & /  a2 &    a1 & rmw_uds ;
: pix3		/  a3 & /  a2 &    a1 & rmw_lds ;
: pix4		/  a3 &    a2 & /  a1 & rmw_uds ;
: pix5		/  a3 &    a2 & /  a1 & rmw_lds ;
: pix6		/  a3 &    a2 &    a1 & rmw_uds ;
: pix7		/  a3 &    a2 &    a1 & rmw_lds ;

% Program Pal Outputs. All outputs Active LOW.

ASSERT cass8
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix7
OR	state12_13 & / one_pix & rmw_uds

ASSERT cass9
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix6
OR	state12_13 & / one_pix & rmw_uds

ASSERT cass10
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix5
OR	state12_13 & / one_pix & rmw_uds

ASSERT cass11
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix4
OR	state12_13 & / one_pix & rmw_uds

ASSERT cass12
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix3
OR	state12_13 & / one_pix & rmw_uds

ASSERT cass13
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix2
OR	state12_13 & / one_pix & rmw_uds

ASSERT cass14
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix1
OR	state12_13 & / one_pix & rmw_uds

ASSERT cass15
ENABLE ALWAYS
OR	state1
OR	state2
OR	state5
OR	state7
OR	state9
OR	state12_13 &   one_pix & pix0
OR	state12_13 & / one_pix & rmw_uds

TIMING: NO-CLOCK
%		123456789012345678901234567890123456789012345678
st0		_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
st1		__--__--__--__--________________________________
st2		____----____------------------------------------
st3-		--------________________________________________
rmw_uds-	----------------_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
rmw_lds-	-----------------_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
one_pix-	--------------------------------________________
a1		__________________--__--__--__--__--__--__--__--
a2		____________________----____----____----____----
a3		________________________--------________--------

cass8		-__--_-_-_------_-_-_-_-_-_-_-_--------_--------
cass9		-__--_-_-_------_-_-_-_-_-_-_-_-------_---------
cass10		-__--_-_-_------_-_-_-_-_-_-_-_------_----------
cass11		-__--_-_-_------_-_-_-_-_-_-_-_-----_-----------
cass12		-__--_-_-_------_-_-_-_-_-_-_-_----_------------
cass13		-__--_-_-_------_-_-_-_-_-_-_-_---_-------------
cass14		-__--_-_-_------_-_-_-_-_-_-_-_--_--------------
cass15		-__--_-_-_------_-_-_-_-_-_-_-_-_---------------

PALEND


---

## PAL SC14


% ======================================================================
%  Pal Name: SC14
%  Pal Type: 16L8-A
%  Speed: 25 nsec
%  Purpose: Generates WE lines to frame buffer planes A..D
%  Purpose: Decode Frame buffer access mode and implications for strobes
%	on ROPC chips. This Pal handles the hidden read cycles to load
%	the destination data into the ROPC.
%  Decoding:
%  A21 A20 ROPMOD ACCESS      LD.SRC        LD.DST       Description
%  ----------------------------------------------------------------------
%   0   0    X    1 Plane      NONE   	     NONE      Word-mode memory
%   0   1    X    1 Pixel      NONE   	     NONE      Pixel-mode memory
%   1   0    0  0-7 Plane   Fr VME on Wr  Fr FB on Rd  ROP Normal Word-mode
%   1   0    1    1 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Normal Pixel-mode
%   1   0    2  0-7 Plane   Fr VME on Wr  Fr FB on Wr  ROP Normal Wd-mode HRead
%   1   0    3    1 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Normal Pix-mode HRead
%   1   0    4  0-7 Plane   Fr  FB on Rd  Fr FB on Rd  ROP Scroll Word-mode
%   1   0    5   16 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Fill Pixel-mode
%   1   0    6  0-7 Plane   Fr  FB on Rd  Fr FB on Wr  ROP Scroll Wd-mode HRead
%   1   0    7   16 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Fill Pixel-mode HRead
%   1   1    X                  NONE   	     NONE      Control Registers
%
%  ======================================================================

paltype pal16l8
palname SC14
palid 1.5 84/07/24

PALBEGIN

% Inputs

1  INPUT a17
2  INPUT a18
3  INPUT a19
4  INPUT a20
5  INPUT a21
6  INPUT ropmod2
7  INPUT msk.a
8  INPUT msk.b
9  INPUT msk.c
11 INPUT msk.d
16 INPUT ropmod0
17 INPUT fb.wr1-
18 INPUT rdat(0-120)

10 GND
20 VCC

% Outputs

19 OUTPUT one_pix-
15 OUTPUT we_a-
14 OUTPUT we_b-
13 OUTPUT we_c-
12 OUTPUT we_d-

% Define intermediates

: we		  rdat(0-120) & fb.wr1 ;

: plane_a	/ a19 & / a18 & / a17 ;
: plane_b	/ a19 & / a18 &   a17 ;
: plane_c	/ a19 &   a18 & / a17 ;
: plane_d	/ a19 &   a18 &   a17 ;

: mode_wd	/ a21 & / a20 ;
: mode_pix	/ a21 &   a20 ;
: mode_ropc       a21 & / a20 ;
: mode_13	  a21 & / a20 & / ropmod2 & ropmod0 ;

% Program Pal Outputs. All outputs Active LOW.

ASSERT one_pix-
ENABLE ALWAYS
OR	mode_pix
OR	mode_13

ASSERT we_a-
ENABLE ALWAYS
OR	mode_wd   & plane_a & we
OR	mode_pix  &   msk.a & we
OR	mode_ropc &   msk.a & we

ASSERT we_b-
ENABLE ALWAYS
OR	mode_wd   & plane_b & we
OR	mode_pix  &   msk.b & we
OR	mode_ropc &   msk.b & we

ASSERT we_c-
ENABLE ALWAYS
OR	mode_wd   & plane_c & we
OR	mode_pix  &   msk.c & we
OR	mode_ropc &   msk.c & we

ASSERT we_d-
ENABLE ALWAYS
OR	mode_wd   & plane_d & we
OR	mode_pix  &   msk.d & we
OR	mode_ropc &   msk.d & we

TIMING: NO-CLOCK
%		12345678901234567890123456789012345678901234567890
a17		_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
a18		__--__--__--__--__--__--__--__--__--__--__--__--__
a19		____----____----____----____----____----____----__
a20		________--------________--------________--------__
a21		________________----------------________________--
msk.a		_-_-_-_-___---_-__--__------------___---------___-
msk.b		----____----___---____------------_______---------
msk.c		__----____----______------------------------------
msk.d		_-_---__----__------_________---------------______
fb.wr1-		________________________________------------------
rdat(0-120)	------------------------________________----------

we_a-		_----------___-_--__--__--------------------------
we_b-		-_------____---___----__--------------------------
we_c-		--_-------____------____--------------------------
we_d-		---_----____--______------------------------------

ropmod0		__--__--__--__--__--__--__--__--__--__--__--__--__
ropmod2		____----____----____----____----____----____----__
one_pix-	--------________--__--------------------________--

PALEND


---

## PAL SC15


% ======================================================================
%  Pal Name: SC15
%  Pal Type: 16L8-A
%  Speed: 25 nsec
%  Purpose: Generates WE lines to frame buffer planes E..H
%  Purpose: Decode Frame buffer access mode and implications for strobes
%	on ROPC chips. This Pal handles the hidden read cycles to load
%	the destination data into the ROPC.
%  Decoding:
%  A21 A20 ROPMOD ACCESS      LD.SRC        LD.DST       Description
%  ----------------------------------------------------------------------
%   0   0    X    1 Plane      NONE   	     NONE      Word-mode memory
%   0   1    X    1 Pixel      NONE   	     NONE      Pixel-mode memory
%   1   0    0  0-7 Plane   Fr VME on Wr  Fr FB on Rd  ROP Normal Word-mode
%   1   0    1    1 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Normal Pixel-mode
%   1   0    2  0-7 Plane   Fr VME on Wr  Fr FB on Wr  ROP Normal Wd-mode HRead
%   1   0    3    1 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Normal Pix-mode HRead
%   1   0    4  0-7 Plane   Fr  FB on Rd  Fr FB on Rd  ROP Scroll Word-mode
%   1   0    5   16 Pixel   Fr VME on Wr  Fr FB on Rd  ROP Fill Pixel-mode
%   1   0    6  0-7 Plane   Fr  FB on Rd  Fr FB on Wr  ROP Scroll Wd-mode HRead
%   1   0    7   16 Pixel   Fr VME on Wr  Fr FB on Wr  ROP Fill Pixel-mode HRead
%   1   1    X                  NONE   	     NONE      Control Registers
%
%  ======================================================================

paltype pal16l8
palname SC15
palid 1.7 84/07/24

PALBEGIN

% Inputs

1  INPUT a17
2  INPUT a18
3  INPUT a19
4  INPUT a20
5  INPUT a21
6  INPUT ropmod2
7  INPUT msk.e
8  INPUT msk.f
9  INPUT msk.g
11 INPUT msk.h
16 INPUT ropmod0
17 INPUT fb.wr1-
18 INPUT rdat(0-120)

10 GND
20 VCC

% Outputs

19 OUTPUT pix-
15 OUTPUT we_e-
14 OUTPUT we_f-
13 OUTPUT we_g-
12 OUTPUT we_h-

% Define intermediates

: we		  rdat(0-120) & fb.wr1 ;

: plane_e	  a19 & / a18 & / a17 ;
: plane_f	  a19 & / a18 &   a17 ;
: plane_g	  a19 &   a18 & / a17 ;
: plane_h	  a19 &   a18 &   a17 ;

: mode_wd	/ a21 & / a20 ;
: mode_pix	/ a21 &   a20 ;
: mode_ropc       a21 & / a20 ;
: mode_1357       a21 & / a20 & ropmod0 ;

% Program Pal Outputs. All outputs Active LOW.

ASSERT pix-
ENABLE ALWAYS
OR	mode_pix
OR	mode_1357

ASSERT we_e-
ENABLE ALWAYS
OR	mode_wd   & plane_e & we
OR	mode_pix  &   msk.e & we
OR	mode_ropc &   msk.e & we

ASSERT we_f-
ENABLE ALWAYS
OR	mode_wd   & plane_f & we
OR	mode_pix  &   msk.f & we
OR	mode_ropc &   msk.f & we

ASSERT we_g-
ENABLE ALWAYS
OR	mode_wd   & plane_g & we
OR	mode_pix  &   msk.g & we
OR	mode_ropc &   msk.g & we

ASSERT we_h-
ENABLE ALWAYS
OR	mode_wd   & plane_h & we
OR	mode_pix  &   msk.h & we
OR	mode_ropc &   msk.h & we

TIMING: NO-CLOCK
%		12345678901234567890123456789012345678901234567890
a17		_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
a18		__--__--__--__--__--__--__--__--__--__--__--__--__
a19		----____----____----____----____----____----____--
a20		________--------________--------________--------__
a21		________________----------------________________--
msk.e		_-_-_-_-___---_-__--__------------___---------___-
msk.f		----____----___---____------------_______---------
msk.g		__----____----______------------------------------
msk.h		_-_---__----__------_________---------------______
fb.wr1-		________________________________------------------
rdat(0-120)	------------------------________________----------

we_e-		_----------___-_--__--__--------------------------
we_f-		-_------____---___----__--------------------------
we_g-		--_-------____------____--------------------------
we_h-		---_----____--______------------------------------

ropmod0		__--__--__--__--__--__--__--__--__--__--__--__--__
ropmod2		____----____----____----____----____----____----__
pix-		--------________--__--__----------------________--

PALEND


---

## PAL SC16


% ======================================================================
%  Pal Name: SC16
%  Pal Type: 16L8
%  Speed: 25 nsec
%  Purpose: Controls buffer and write enables for TTL and ECL color maps.
%  Bugs:
%  ======================================================================

paltype pal16l8
palname SC16
palid 1.8 84/07/24

PALBEGIN

% Inputs

1  INPUT a16
2  INPUT c.req-
3  INPUT rd/wr\
4  INPUT a_latch100
5  INPUT upcmap1
6  INPUT vblank
7  INPUT v2
8  INPUT v3
9  INPUT h2
11 INPUT h3
13 INPUT a_latch150

10 GND
20 VCC

% Outputs
19 OUTPUT wr.cmap-
18 OUTPUT rd.cmap-
17 OUTPUT cs.red-
16 OUTPUT cs.grn-
15 OUTPUT cs.blu-
14 OUTPUT we.ecl-
12 OUTPUT ck.upcm-

% Program pal outputs. All outputs active LOW.

: read rd/wr\ ;
: wr / rd/wr\ ;

ASSERT wr.cmap-
ENABLE ALWAYS
OR	c.req & a16 & wr & / upcmap1 & a_latch100 & / a_latch150

ASSERT rd.cmap-
ENABLE ALWAYS
OR	c.req & a16 & read & / upcmap1

ASSERT cs.red-
ENABLE ALWAYS
OR	/ vblank
OR	  vblank & upcmap1 & / v2 & / v3

ASSERT cs.grn-
ENABLE ALWAYS
OR	/ vblank
OR	  vblank & upcmap1 & / v2 &   v3

ASSERT cs.blu-
ENABLE ALWAYS
OR	/ vblank
OR	  vblank & upcmap1 &   v2 & / v3

ASSERT we.ecl-
ENABLE ALWAYS
OR	vblank & upcmap1 & / v2 & / v3 & h3 & / h2
OR	vblank & upcmap1 & / v2 &   v3 & h3 & / h2
OR	vblank & upcmap1 &   v2 & / v3 & h3 & / h2

ASSERT ck.upcm-
ENABLE ALWAYS
OR	h3 & h2

TIMING: NO-CLOCK
%		12345678901234567890123456789012345678901234567890
h2		_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
h3		__--__--__--__--__--__--__--__--__--__--__--__--__
v2		____----____----____----____----____----____----__
v3		________--------________--------________--------__
upcmap1		----------------________________________________--
vblank		----------------________________----------------__
we.ecl-		--_---_---_---------------------------------------
ck.upcm-	---_---_---_---_---_---_---_---_---_---_---_---_--
cs.red-		____------------________________----------------__
cs.blu-		----____--------________________----------------__
cs.grn-		--------____----________________----------------__

a_latch100	_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
a_latch150	__--__--__--__--__--__--__--__--__--__--__--__--__
a16		____----____----____----____----____----____----__
rd/wr\		________--------________--------________--------__
c.req-		________________----------------________________--
wr.cmap-	-------------------------------------_------------
rd.cmap-	--------------------------------------------____--

PALEND


---

## PROM SC17


static char* sccs_id = "1.11 84/07/19";

/* ======================================================================
   Author: Peter Costello
   Date :  July 15, 1983
   Prom Name: SC17
   Prom Type: 1024 x 4.
   Speed: 35 nsec.
   Purpose: Control horizontal sync timing
   Timing Computation:
	Choose 92.9405 MHz crystal for 62.5 KHz and 60.0000 Hz operation
	in case we ever have 60 Hz interference problems. This translates
	to 1488 horizontal states and 1041 vertical lines. However, as
   	there is no known problem, we will run it at 65 Hz.

          STATES            TIME 	DESCRIPTION (1152x900 Display)
	----------	-----------	------------------------------
	   0..1151	12.395 usec	Display Enable
	1152..1163	 0.129 usec	Front Porch
	1164..1303	 1.506 usec	Horizontal Sync
	1304..1503	 2.152 usec	Back Porch
	   0..1503	16.181 usec	Horizontal Period (61.80 KHz)
	1152..1503	 3.786 usec	Horizontal Retrace

          STATES            TIME 	DESCRIPTION (1024x1024 Display)
	----------	-----------	-------------------------------
	   0..1023	12.395 usec	Display Enable
	1024..1100	 0.818 usec	Front Porch
	1100..1239	 1.506 usec	Horizontal Sync
	1240..1503	 2.840 usec	Back Porch
	   0..1503	16.181 usec	Horizontal Period (61.80 KHz)
	1024..1503	 5.164 usec	Horizontal Retrace

   ====================================================================== */

#include "/usr/local/pl/prom.c"
#define range(low,x,high) ((low<=x)&&(x<=high))

int res_1152x900;

/* Define Inputs to 1K x 4 Prom. */
#define h9	(a0)
#define h10	(a1)
#define vblank_	(a2)
#define h8	(a3)
#define h6	(a4)
#define h4	(a5)
#define h2	(a6)
#define h3	(a7)
#define h5	(a8)
#define h7	(a9)


#define h (cvb(h2)*d2 + cvb(h3)*d3 + cvb(h4)*d4 + cvb(h5)*d5 + 	\
	   cvb(h6)*d6 + cvb(h7)*d7 + cvb(h8)*d8 + cvb(h9)*d9 +	\
	   cvb(h10)*d10 )

#define vblank (!vblank_)
#define phase 13		/* Number of states from hreset
				   that video is enabled */
#define p (phase<<2)		/* Each 'state' is 4 pixels */


/* Define Outputs from Prom */

hsync()
{   int hsync;
    if (res_1152x900) {
       hsync = range(1164+p,h,1303+p);
    } else {
       hsync = range(1100+p,h,1239+p);
    }
    return(hsync);
}

h1152()
{   int h1152;
    h1152 = range(1152+p,h,1152+(25<<2));	/* Assert for clock by H5 */
    return(h1152);
}

hreset()
{   int hreset;
    hreset = range(1496,h,1499);		/* Make 0 <= H < 1504 */
    return(hreset);
}

dispen()
{   int dispen;
    if (res_1152x900) {
       dispen = (range(0+p-8,h,1151+p-8) && (!vblank));
    } else {
       dispen = (range(0+p-8,h,1023+p-8) && (!vblank));
    }
    return(dispen);
}

main()
{
prom1024x4;

res_1152x900 = 1;
prombegin
prom(0,d0,!hsync())
prom(0,d1, h1152())
prom(0,d2, hreset())
prom(0,d3, dispen())
promend;

res_1152x900 = 0;
prombegin
prom(1,d0,!hsync())
prom(1,d1, h1152())
prom(1,d2, hreset())
prom(1,d3, dispen())
promend;

writeprom("sc17",0);
writeprom("sc17_1024",1);
}


---

## PROM SC18


static char* sccs_id = "1.5 84/06/20";

/* ======================================================================
   Author: Peter Costello
   Date :  July 15, 1983
   Prom Name: SC18
   Prom Type: 1024 x 4.
   Speed: 35 nsec.
   Purpose: Controls the vertical sync timing.
   Timing Calculation:
	Horizontal Line Time: 16.181 usec with 1152x900 display

	   STATE	   TIME		DESCRIPTION (1152x900 Display)
	----------	-----------	------------------------------
 	   0.. 899	 14563 usec	Display Enable
	 900.. 901	    32 usec	Front Porch
	 902.. 905	    64 usec	Vertical Sync
	 906.. 936	   502 usec	Back Porch
	   0.. 936	 15162 usec	Vertical Period (65.96 Hz)

	   STATE	   TIME		DESCRIPTION (1024x1024 Display)
	----------	-----------	-------------------------------
	   0..1023	 16569 usec	Display Enable
	1024..1025	    32 usec	Front Porch
	1026..1029	    64 usec	Vertical Sync
	1030..1060	   502 usec	Back Porch
	   0..1060	 17168 usec	Vertical Period (58.25 Hz)

   ====================================================================== */

#include "/usr/local/pl/prom.c"
#define range(low,x,high) ((low<=x)&&(x<=high))

int res_1152x900;

/* Define Inputs to 1K x 4 Prom. */
#define v7  (a0)
#define v8  (a1)
#define v9  (a2)
#define v5  (a3)
#define v3  (a4)
#define v1  (a5)
#define v10 (a6)
#define v2  (a7)
#define v4  (a8)
#define v6  (a9)

#define v (cvb(v1)*d1 + cvb(v2)*d2 + cvb(v3)*d3 + cvb(v4)*d4 + \
	   cvb(v5)*d5 + cvb(v6)*d6 + cvb(v7)*d7 + cvb(v8)*d8 + \
	   cvb(v9)*d9 + cvb(v10)*d10)

/* Define Outputs from Prom */
vblank()
{  int vblank;
   if (res_1152x900) {
      vblank = (v >= 900);
   } else {
      vblank = (v >= 1024);
   }
   return(vblank);
}

vsync()
{  int vsync;
   if (res_1152x900) {
      vsync = range(902,v,905);
   } else {
      vsync = range(1026,v,1029);
   }
   return(vsync);
}

vreset()
{  int vreset;
   if (res_1152x900) {
      vreset = (v >= 936);
   } else {
      vreset = (v >= 1060);
   }
   return(vreset);
}

main()
{
prom1024x4;

res_1152x900 = 1;
prombegin
prom(0,d0,!vreset())
prom(0,d1,!vblank())
prom(0,d2,!vsync())
prom(0,d3, 1)
promend;

res_1152x900 = 0;
prombegin
prom(1,d0,!vreset())
prom(1,d1,!vblank())
prom(1,d2,!vsync())
prom(1,d3, 1)
promend;

writeprom("sc18",0);
writeprom("sc18_1024",1);
}


---

# Schematics


This chapter contains the signal summary, the parts list and the schematics
of the Sun-2 color video board. Traditionally this chapter has
contained the parts location diagram and printed-circuit board artwork as
well. However, the printed-circuit board has an outside dimension of
14.44" by 15.75" so blue-line copies of the artwork and part locations will
be included only as an appendix to the Engineering Manual.


## Signal Summary


------------------------------------------------------------------------------
Mnuemonic	Description
------------------------------------------------------------------------------

A_BLU   	Analog blue output from DAC. Output to color monitor
A_DIS		Address Display. FBuf addr taken from video refresh addr counter
A_GRN		Analog green output from DAC. Output to color monitor
A_LATCH		Address latch. Clocks request flip flops to start operation
A_LATCH50	Address latch delayed 65 nsec
A_LATCH100	Address latch delayed 130 nsec
A_LATCH150	Address latch delayed 195 nsec
A_PIX		Address pixel. FBuf addr taken from pixel-mode addr multiplexors
A_RED		Analog red output from DAC. Output to color monitor
A_WD		Address word. FBuf addr taken from word-mode addr multiplexors
A1_OR_2		OR of A1 and A2.
A21..A1		On-board address bus. Latched from VME.
BASE_I1..0	Instruction select lines for scan line base address counter
BS7..BS0	Buffer select lines for AM29520 before damping resistors.
BDSEL		Base address of board selected
BLURET		Blue DAC analog ground return
BUF.S1..BUF.S0  Buffer select lines for AM29520 after damping resistors.
C(40.0-20)	TTL clock. 40 nanosecond period.
C(40.20-40)	TTL clock. 40 nanosecond period.
C(40Z.0-20Z)	TTL zoom clock. Period equals 40 nsec * zoom.
C.REQ		Control register read/write request
CA15..CA0	Cas lines before series termination resistors
CAS15..CAS0	Cas lines to frame buffer
CASS15..0	Cas lines to frame buffer before 74F534 registers
CBUF		Clock to AM29520 video data buffers
CK.UPCM		Clock to syncronize status bit UPCMAP
CLR_RMW		Clears syncronized frame buffer request
CSYNC		Composite Sync. OR of HSYNC and VSYNC.
CSYNC1		Bufferred Composite Sync. Drives connector.
CS.BLU		Chip select blue color map
CS.GRN		Chip select green color map
CS.RED		Chip select red color map
D15..D0		On-board data bus
DISPEN		Display Enable. Resynchronized DISPEN1.
DISPEN1		Display Enable. DISPON gated by EN.VIDEO
DISPON		Display On
DS   		Data strobe
DTACK		Data transfer acknowledge
E.A7..E.A0	ECL address inputs to DAC
E.CSB		ECL chip select blue color map
E.CSG		ECL chip select green color map
E.CSR		ECL chip select red color map
E.C(10.0-5)	ECL 10 nsec clock
E.C(10.1-6)	ECL 10 nsec clock
E.C(10.3-8)	ECL 10 nsec clock
E.C(10.4-9)	ECL 10 nsec clock
E.C(20Z.0-10Z)	ECL zoom clock. Period = 20nsec * zoom.
E.C(40.0-20)	ECL 40 nsec clock
E.C(40.30-10)	ECL 40 nsec clock
E.C(40Z.0-20Z)	ECL zoom clock. Period = 40nsec * zoom.
E.D7..E.D0	ECL data inputs to DAC
E.DISP		ECL display enable
E.DISP1		ECL. E.DISP syncronized with E.C(40.30-10).
E.DISP2		ECL. E.DISP1 delayed 10 nsec
E.DISP3		ECL. E.DISP1 delayed 20 nsec
E.DISP4		ECL. E.DISP1 delayed 30 nsec
E.DISP34	ECL NOR of E.DISP3 and E.DISP3. Enables DAC clock.
E.LOAD		ECL load pulse to ECL video shifters
E.MA7..E.MA0	ECL address bus after translation from TTL signal levels
E.MS15..12.A	ECL inputs to video shifter. Plane 0.
E.MS15..12.B	ECL inputs to video shifter. Plane 1.
E.MS15..12.C	ECL inputs to video shifter. Plane 2.
E.MS15..12.D	ECL inputs to video shifter. Plane 3.
E.MS15..12.E	ECL inputs to video shifter. Plane 4.
E.MS15..12.F	ECL inputs to video shifter. Plane 5.
E.MS15..12.G	ECL inputs to video shifter. Plane 6.
E.MS15..12.H	ECL inputs to video shifter. Plane 7.
E.PU		ECL pull-up. Logical true.
E.S1		ECL generated select line for 74F194 shifters
E.WE 		ECL write enable line to DAC
E.X(10.0-5)	ECL 10 nsec clock.
E.Z3..E.Z0	ECL version of ZOOM3..ZOOM0
E.ZERO		ECL signal used to help generate zoom clock
E.ZERO1		ECL signal. Bufferred E.ZERO
E.ZOOM3..0	ECL version of ZOOM3..ZOOM0
E.ZSYNC		ECL zoom syncronization. Syncronizes zoom and normal clocks
E.ZS		ECL signal. Unregistered version of E.ZSYNC
END_REQ		End Request. Clear FB.REQ.
END_RINC	End Read-modify-write or inhibit RMW until LD_SRC deasserted.
END_RINC1	END_RINC plus one pal delay
END_RINC2	END_RINC plus two pal delays
END_RMW		End Read-modify-write. Clear RMW.
EN.VIDEO	Status bit to enable video
FAST_CNT	Enables back-to-back memory update cycles during retrace
FB.REQ		Frame buffer request
FB.WR		Frame buffer write. Used to implement ROPC hidden read cycles
FB.WR1		Re-clocked version of FB.WR.
GND		Signal and Power ground
GRNRET		Green DAC analog ground return
H10..H2		Horizontal state
H1152		Asserted around horizontal state 1152
HR.TOG		Hidden read state bit
HR.TOG1		Hidden read state bit
HRESET		Horizontal state machine reset
HSYNC		Horizontal sync. Output to color monitor
IACKIN		Interrupt acknowledge in. Gated with AS.
INTEN   	Status register bit that enables interrupts
IREQ    	Interrupt request pending
IREQ1		IREQ synchronized with IACKIN
L.DISPON	Unlatched version of DISPON
L.H1152 	Unlatched version of H1152
L.HRESET	Unlatched version of HRESET
L.HSYNC		Unlatched version of HSYNC
L.LOFF3..0	Unlatched version of LOFF3..LOFF0
L.NZBOT		Unlatched version of NZBOT
L.PIX3..L.PIX0	Unlatched version of PIX3..PIX0
L.POFF3..0	Unlatched version of POFF3..POFF0
L.RMW_TC	Unlatched version of RMW_TC
L.SPARE_TC	Unlatched version of SPARE_TC
L.VBLANK	Unlatched version of VBLANK
L.VRESET1	Unlatched version of VRESET1
L.VSYNC		Unlatched version of VSYNC
L.ZA5..L.ZA4	Unlatched version of ZA5 and ZA4
L.ZOOM3..0	Unlatched version of ZOOM3..ZOOM0
L.ZSYNC		Unlatched version of ZSYNC
LDS		Lower data strobe
LD_DST		Load destination register strobe to rasterop chips
LD_SRC		Load source register strobe to rasterop chips
LINE_TC		Line terminal count. Controls vertical zoom
LOFF3..0	Sets zoom on first line of display
M11.A..M0.A	Pipelined pixel data before 74F350 barrel shifters
M11.B..M0.B	Pipelined pixel data before 74F350 barrel shifters
M11.C..M0.C	Pipelined pixel data before 74F350 barrel shifters
M11.D..M0.D	Pipelined pixel data before 74F350 barrel shifters
M11.E..M0.E	Pipelined pixel data before 74F350 barrel shifters
M11.F..M0.F	Pipelined pixel data before 74F350 barrel shifters
M11.G..M0.G	Pipelined pixel data before 74F350 barrel shifters
M11.H..M0.H	Pipelined pixel data before 74F350 barrel shifters
MA7..MA0	Frame buffer memory address lines before drivers
MA7_A..MA0_A    Memory address lines before series terminators. Plane 0
MA7_B..MA0_B    Memory address lines before series terminators. Plane 1
MA7_C..MA0_C    Memory address lines before series terminators. Plane 2
MA7_D..MA0_D    Memory address lines before series terminators. Plane 3
MA7_E..MA0_E    Memory address lines before series terminators. Plane 4
MA7_F..MA0_F    Memory address lines before series terminators. Plane 5
MA7_G..MA0_G    Memory address lines before series terminators. Plane 6
MA7_H..MA0_H    Memory address lines before series terminators. Plane 7
MA7.A..MA0.A    Memory address lines after series terminators. Plane 0
MA7.B..MA0.B    Memory address lines after series terminators. Plane 1
MA7.C..MA0.C    Memory address lines after series terminators. Plane 2
MA7.D..MA0.D    Memory address lines after series terminators. Plane 3
MA7.E..MA0.E    Memory address lines after series terminators. Plane 4
MA7.F..MA0.F    Memory address lines after series terminators. Plane 5
MA7.G..MA0.G    Memory address lines after series terminators. Plane 6
MA7.H..MA0.H    Memory address lines after series terminators. Plane 7
MI15_A..MI0_A	Memory input data before series terminators. Plane 0
MI15_B..MI0_B	Memory input data before series terminators. Plane 1
MI15_C..MI0_C	Memory input data before series terminators. Plane 2
MI15_D..MI0_D	Memory input data before series terminators. Plane 3
MI15_E..MI0_E	Memory input data before series terminators. Plane 4
MI15_F..MI0_F	Memory input data before series terminators. Plane 5
MI15_G..MI0_G	Memory input data before series terminators. Plane 6
MI15_H..MI0_H	Memory input data before series terminators. Plane 7
MI15.A..MI0.A	Memory input data after series terminators. Plane 0
MI15.B..MI0.B	Memory input data after series terminators. Plane 1
MI15.C..MI0.C	Memory input data after series terminators. Plane 2
MI15.D..MI0.D	Memory input data after series terminators. Plane 3
MI15.E..MI0.E	Memory input data after series terminators. Plane 4
MI15.F..MI0.F	Memory input data after series terminators. Plane 5
MI15.G..MI0.G	Memory input data after series terminators. Plane 6
MI15.H..MI0.H	Memory input data after series terminators. Plane 7
MO15.A..MO0.A	Memory output data. Plane 0
MO15.B..MO0.B	Memory output data. Plane 1
MO15.C..MO0.C	Memory output data. Plane 2
MO15.D..MO0.D	Memory output data. Plane 3
MO15.E..MO0.E	Memory output data. Plane 4
MO15.F..MO0.F	Memory output data. Plane 5
MO15.G..MO0.G	Memory output data. Plane 6
MO15.H..MO0.H	Memory output data. Plane 7
MS15.A..MS12.A	Memory shift data. Output of 74F350. Plane 0.
MS15.B..MS12.B	Memory shift data. Output of 74F350. Plane 1.
MS15.C..MS12.C	Memory shift data. Output of 74F350. Plane 2.
MS15.D..MS12.D	Memory shift data. Output of 74F350. Plane 3.
MS15.E..MS12.E	Memory shift data. Output of 74F350. Plane 4.
MS15.F..MS12.F	Memory shift data. Output of 74F350. Plane 5.
MS15.G..MS12.G	Memory shift data. Output of 74F350. Plane 6.
MS15.H..MS12.H	Memory shift data. Output of 74F350. Plane 7.
MSK.H..MSK.A 	Per-plane mask register bits
NZBOT		No Zoom Bottom of display
NZ.EN		No Zoom Enable. Enable No-zoom comparator.
NZ.RST		No Zoom Reset. Reset Vertical zoom after NZBOT.
OE.ROPC		Output enable rasterop chip
OE3..OE0	Output enable multiplexors for AM29520 video buffers
ONE_PIX		Asserted on pixel mode memory frame buffer accesses
P.D7..P.D0	Pixel data bus
P1.A23..P1.A1	VME address bus
P1.AM5..P1.AM0	VME address modifiers
P1.BERR		VME bus error
P1.D15..P1.D0	VME data bus
P1.DS0		VME lower data strobe
P1.DS1		VME upper data strobe
P1.DTACK	VME data transfer acknowledge
P1.SYSRESET	VME initialization signal
P1.IACK		VME interrupt acknowledge cycle
P1.IACKIN	VME interrupt acknowledge daisy chain input
P1.IRQ4		VME interrupt level 4
P1.SYSRESET	VME initialization signal
P1.WRITE	VME read/write line
PIX3..PIX0	Value of pixel pan register
PIX1A..PIX0A	Same as PIX1..PIX0, but added drive current needed
POFF3..POFF0	Value of pixel offset register used for pan
PR.D7..PR.D0	Pixel read data bus
PU		Pull up.
PU.A22		Pull up for address decoding jumper
PU.A23		Pull up for address decoding jumper
RAS_7..RAS_0	Frame buffer Ras before series terminators
RAS.7..RAS.0	Frame buffer Ras after series terminators
RASX		Output by prom SC11. 40 nsec before RAS_7..RAS_0
RASY		RASX delayed 40 nsec
RASY20		RASY delayed 20 nsec. Turns around Ras/Cas addresses
RCV_WD		Receive word read data from frame buffer or rasterop chip
RCV_WD.H..A	RCV_WD decoded to one of eight memory planes
RD.CMAP		Read TTL color map
RD.MSK		Read from per-plane mask register
RD.PIX		Read pixel data
RD.PIX15..0	RD.PIX decoded to one of 16 pixels per word
RD.REGS1	Read one of second eight control registers
RD.ROPC		Read from rasterop chip
RD.STAT		Read from status register
RD.VZOOM	Read from register that sets base line number of no-zoom region
RD.WORD		Read 16 bits of un-swapped data to P2 bus
RD.WPAN		Read word pan register
RD.ZOOM		Read zoom register
RD/WR\		Buffered read/write select line from P2-bus
RDAT(0-120)	Control signal asserted during memory read/write cycles
RDAT(40-160)	RDAT(0-120) delayed 40 nsec.
RDAT(80-200)	RDAT(0-120) delayed 80 nsec.
RDAT(80-160)	RDAT(0-120) delayed 80 nsec.
REDRET		Red DAC analog ground return.
RMW     	Read-modify-write request pending. RMW.REQ delayed 80 nsec
RMW1		RMW.REQ delayed 40 nsec
RMW_CNT5..0	Controls # of FB read/write cycles between FB video cycles
RMW_INC		Clocks FB.REQ to set syncronized RMW.REQ
RMW_LDS		Read-modify-write and LDS asserted
RMW_TC		Read-modify-write terminal count. Time for a FB video cycle
RMW_UDS		Read-modify-write and UDS asserted
RMW.REQ 	FB.REQ syncronized to memory controller read/write cycle
ROPC		Memory access mode uses rasterop chips
S.WD		Performs decoding function when reading from rasterop chips
SA19..SA6	Scan line address counter base
SFT.S1..SFT.S0	Control load/shift functions on 74F194 video data shifters
SP_ST2..SP_ST0  Control number of times state1 repeated in memory control cycle
ST3..ST0	Memory control state
STATE10		State10 in memory control cycle
STATE11_15	State11 through State15 in memory control cycle
STATE4_10	State4 through State10 in memory control cycle
T.A9..T.A0	Address to TTL shadow color map
T.D7..T.D0	Buffered Data to TTL shadow color map
TBUF.S1..0	Used to generate select lines to AM29520 video data buffers
UDS		Upper data strobe
UPCMAP  	Status register bit enabling loading of ECL cmap from TTL cmap
UPCMAP1 	Syncronized version of UPCMAP
V_CNT		Controls load/count/clear function of video address counter
V9..V0		Vertical state
VA19..VA6	Output of video display address counter
VBB		-2 volts. Used for ECL termination
VBLANK  	Vertical blanking
VCC		+5 volts
VEE		-5.2 volts
VID_CNT		Carry input to video address counter
VIDEO_CK	Clock input to video address counter
VREF.M5		Precision -5.2 Volt for DAC.
VRESET		Vertical state machine reset
VRESET1		Gated with HRESET to generate VRESET
VSYNC		Vertical Sync. Output to color monitor
VZ9..VZ2	Variable zoom register. Sets base for not zooming bottom of CRT
W.ROP.H..A	Write lines to per-plane rasterop chips
WE_H..WE_A	Per-plane write enables to frame buffer memory
WE.H..WE.A	WE_H..WE_A after series terminators
WE.ECL		Write enable line to ECL color maps on DAC
WR.CMAP		Write enable to TTL color maps
WR.HBYTE	Enables byte-swapping on data written from P2 bus
WR.MSK		Write per-plane mask register
WR.POFF		Write pixel offset register
WR.R.ALL	Signal not used
WR.REGS1	Enable write on second set of control registers (8 total)
WR.ROP.H..A	Write lines to rasterop chips after series terminators
WR.STAT		Write status register
WR.VZOOM	Write variable zoom base register
WR.WORD		Enable un-swapped transfer of P2 write data to D15..D0
WR.WPAN		Write word pan register
WR.ZOOM		Write zoom register
X14..X12	Used to decode RCV_WD.H..RCV_WD.A on both ROPC and FB read
XBUF.S1..0	Used to generate select lines for AM29520 video data buffers
XMIT_DST	Transmit destination data from 64K data outputs to 64K inputs
XMIT_PIX	Transmit pixel data to 64K ram data inputs
XMIT_WD		Transmit word data to 64K ram data inputs
YBUF.S1..0	Used to generate select lines for AM29520 video data buffers
ZA19..ZA4	Output of word pan base address counter
ZCRAMP		Zoom cramped. Zoom less than four
ZH9..ZH2	Output of SC10. Horizontal state where ZSYNC asserted
ZO3..ZO0	Used to repeat variable number of horizontal lines for zoom
ZOOM3..ZOOM0	Output of zoom register
ZSYNC		Zoom syncronization signal
ZSYNC40		ZSYNC delayed 40 nsec
ZSYNC80		ZSYNC delayed 80 nsec


---

## Parts List


As an aid in specifying and ordering components, this parts list
translates diptypes into manufacturer names and manufacturer codes.
Only one manufacturer code is given, alternative sources
may be substituted. A manufacturer code of "ANY" is used
for generic parts with a large number of second sources.


--------------------------------------------------------------------------------
GENERIC PINS SMIPART    QTY   MFC     MFPART     DESCRIPTION
--------------------------------------------------------------------------------

10H102  16  100-1097     1    MOTOR   MC10H102   QUAD 2-INPUT ECL NOR
10H105  16  100-1208     2    MOTOR   MC10H105   TRIPLE 3-INPUT ECL NOR
10H124  16  100-1171    15    FAIR    10124Q     TTL TO ECL CONVERTER
10H125  16  100-1172     1    MOTOR   MC10125    ECL TO TTL CONVERTER
10H136  16  100-1101     3    MOTOR   MC10H136   4-BIT ECL COUNTER
10H176  16  100-1103     3    MOTOR   MC10H176   HEX ECL D-FLIPFLOP
2148    18  100-0002     2    INTEL   D2148H-3   1K-BY-4 STATIC RAM 45 NSEC
2600    16  100-1096   128    INMOS   IMS2600    NIBBLE MODE 64K RAM. 120 NSEC.
2764    24  100-0005     1    INTEL   D2764      8K-BY-8 EPROM. ANY SPEED
27S29A  18  100-1109     4    AMD     AM27S29A   512 BY 8 PROM. 35 NSEC.
27S33A  18  100-1108     2    AMD     AM27S33A   1K BY 4 PROM. 35 NSEC.
2952    24  100-0601     6    AMD     AM2952DC   8-BIT NON INVERTING I/O PORT
29520   24  100-1083    16    AMD     AM29520DC  PIPELINE REGISTER
7438    14  100-1007     1    TI      SN7438     QUAD NAND OPEN COLLECTOR
74F02   14  100-1009     1    FAST    74F02N     QUAD 2-INPUT NOR GATES
74F04   14  100-1010     2    FAST    74F04N     HEX INVERTERS
74F08   14  100-1011     5    FAST    74F08N     QUAD 2-INPUT AND GATES
74F163  16  100-1038     7    FAST    74F163N    BINARY 4-BIT COUNTER
74F240  20  100-1017     2    FAST    74F240N    OCTAL INVERTING BUFFER
74F244  20  100-1018     9    FAST    74F244N    OCTAL NONINVERTED BUFFERS
74F257  16  100-1037     2    FAST    74F257N    QUAD DATA SELECTOR
74F32   14  100-1020     2    FAST    74F32N     QUAD 2-INPUT OR GATES
74F350   8  100-0074	 8    FAST    74F350N    4 BIT BARREL SHIFTER
74F373  20  100-1074     1    FAST    74F373N    OCTAL LATCH
74F374  20  100-1021    15    FAST    74F374N    OCTAL REGISTER
74F74   14  100-1022     8    FAST    74F74N     DUAL D-TYPE FLIPFLOP
74LS461 24  100-1067     4    MMI     74LS461    8-BIT COUNTER/PAL
ALS138  16  100-1151     4    TI      74ALS138N  3-to-8 DECODER
ALS157  16  100-1173     6    TI      74ALS157N  3-to-8 DECODER
ALS163  16  100-1158     5    TI      74ALS163N  BINARY 4-BIT COUNTER
ALS258  16  100-____     5    TI      74ALS258N  BINARY 4-BIT COUNTER
ALS2441 20  100-1154     2    TI      74ALS244N  OCTAL NONINVERTED BUFFERS
ALS273  20  100-1150     4    TI      74ALS273N  OCTAL D-TYPE FLIPFLOP
ALS374  20  100-1152     1    TI      74ALS374N  OCTAL REGISTER
85000   28  100-1030     8    SCI     85000      ROPC
AM2949  20  100-1033    33    AMD     AM8308N    OCTAL BUS TRANSCEIVER
LS2521  20  100-0096     3    AMD     AM25LS2521 EIGHT-BIT EQUAL TO COMPARATOR
P16L8A  20  100-1164    11    MMI     PAL16L8-A  PAL. 25 NSEC
DAC8EH  42  100-1163     1    INTECH  DAC8EH     8-BIT DAC WITH COLOR MAP.
LM337H   3  100-1229     1    NAT     LM337H     TO-220 ADJUSTABLE VOLT REG
MC7902   3  100-1232     2    MOT     MC7902C    TO-220 VOLTAGE REGULATOR
C        2  110-0040   417    ANY     CAPACITOR  CAPACITOR GENERIC. 0.1 UFD.
K        2  110-0047    56    AVX     CAPACITOR  CAPACITOR TANTALUM 10 UF
R9.SIP  10  120-0078     1    BURNS   RESISTOR   RESISTOR SIP, 1K 5%
R9.SIP  10  120-1568     1    BURNS   RESISTOR   RESISTOR SIP, 33 OHM 5%
R9.SIP  10  120-1417     1    BURNS   RESISTOR   RESISTOR SIP, 56 OHM 5%
R8.DIP   9  120-1024    19    BECKMAN RESISTOR   RESISTOR DIP, 68 OHM 5%
R8.DIP   9  120-1416     8    BECKMAN RESISTOR   RESISTOR DIP, 47 OHM 5%
R8.DIP   9  120-1025     5    BECKMAN RESISTOR   RESISTOR DIP, 33 OHM 5%
R        2  120-1433     1    ANY     RESISTOR   1/8 Watt. 442 OHM 1%
R        2  120-1019     1    ANY     RESISTOR   1/8 Watt. 470 OHM 1%
R        2  120-1027     1    ANY     RESISTOR   1/8 Watt. 180 OHM 1%
R        2  120-1434     1    ANY     RESISTOR   1/8 Watt. 121 OHM 1%
R        2  120-1064    22    ANY     RESISTOR   1/8 Watt. 56 OHM 5%
R        2  120-1300     1    ANY     RESISTOR   1 Watt. 15 OHM 5%
R.VAR	 6  120-1435     1    BOURNS  VAR RES    VAR. RESISTOR 1K FIXED 9K VAR
J.2      8  130-0273     1    BERG    BERGSTICK  2 PIN
J.4      8  130-1096     2    BERG    BERGSTICK  4 PIN
J.8      8  130-1089     1    BERG    BERGSTICK  8 PIN
HEADER   2  130-0272	 3    BERG    HEADER	 2 PIN JUMPER
COAX_BNC 5  130-1098     5    KINGS   79-237M06  PC BOARD TO BNC COAX CONNECTOR
DIN     32  130-1062     3    AMP                RIGHT-ANGLE DIN EUROCONNECTOR
K1114A   4  150-1077     1    MOTOR   K1114A     OSCILLATOR. 92.9405 MHZ
MTTLDL  14  150-1087     1    ECC     MTTLDL-65  DELAY LINE 65 NSEC
DIODE	 2  150-0367     3    ANY     1N4148	 DIODE
TRANSIST 3  150-1089     1    ANY     2N2905	 TRANSISTOR
HEATSINK 1  150-1105     3    AVID    HEAT SINK  HEAT SINK
PAD      1  150-1046     3    ANY     		 THERMAL PAD FOR HEAT SINK
SOCKET   18 190-1000    18    ANY                18-PIN SOCKET
SOCKET   20 190-1052    20    ANY                20-PIN SOCKET
SOCKET   28 190-1054    28    ANY                28-PIN SOCKET
PC BOARD 1  270-1014	 1    ANY		 PRINTED CIRCUIT BOARD
STIFFNER 1  340-1129	 1    ANY     		 STIFFER
STIFFNER 1  340-1130	 1    ANY     		 STIFFER
PANEL    1  340-1131	 1    ANY     		 PC FRONT PANEL


---

## Schematic SC1 (Page 1 of 21)


---

## Schematic SC2 (Page 2 of 21)


---

## Schematic SC3 (Page 3 of 21)


---

## Schematic SC4 (Page 4 of 21)


---

## Schematic SC5 (Page 5 of 21)


---

## Schematic SC6 (Page 6 of 21)


---

## Schematic SC7 (Page 7 of 21)


---

## Schematic SC8 (Page 8 of 21)


---

## Schematic SC9 (Page 9 of 21)


---

## Schematic SC10 (Page 10 of 21)


---

## Schematic SC11 (Page 11 of 21)


---

## Schematic SC12 (Page 12 of 21)


---

## Schematic SC13 (Page 13 of 21)


---

## Schematic SC14 (Page 14 of 21)


---

## Schematic SC15 (Page 15 of 21)


---

## Schematic SC16 (Page 16 of 21)


---

## Schematic SC17 (Page 17 of 21)


---

## Schematic SC18 (Page 18 of 21)


---

## Schematic SC19 (Page 19 of 21)


---

## Schematic SC20 (Page 20 of 21)


---

## Schematic SC21 (Page 21 of 21)


---

# Wirelist


This chapter contains the wirelist for the Rev A Sun color video board.
The wirelist is comprised of the following sections which are
distinguished by the header lines on each page.


#### Schematics List


The schematics list summarizes all schematics files with titles and pages.
It starts with the following header:


```


FILNAM  P,PN            DATE       TIME MODULE(DWG NUM) REV     AUTHOR
        TITLE 1                         PROJECT         BOARD TYPE


```


#### Location List


The location list translates all location labels
into diptype and component names and locations on the schematics.
The location list start with the following header:


```


LOC     DIPTYPE BODY    FILE    POS


```


#### Signal List


The signal list describes all signals and synonyms in alphabetical order.
Signals that have no explicit name are automatically assigned a
computer-generated name that consists of the percent symbol ("%")
followed by the alphabetically lowest location and pin name connected to
this particular signal run. The signal list pages carry the following header:


```


SIGNAL NAME
        LOC(PIN#) TYPE  LOW     HI      USE     DIPTYPE BODY    FILE    POS


```


For each signal, the connected component locations are listed together
with the pin number, type (input, output, tri-state, open-collector),
low and high currents, usage on component, the component diptype and bodyname,
and a crossreference to the schematic file where this location is used.
Each signal is followed by a calculation of static current loading.


#### Unused Pin List


The last section of the wirelist displays all unused pin locations in a format
similar to the signal list. The header for this section is:


```


UNUSED PINS
        LOC(PIN#) TYPE  LOW     HI      USE     DIPTYPE BODY    FILE    POS


```
