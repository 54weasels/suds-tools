# sunmon.mss

In addition, the 68000 differs from the Multibus in that it transfers
even bytes on data lines D8 through D15 and odd bytes on D0 through D7,
whereas the Multibus transfer both odd and even bytes via D0 through D7.
Finally, the 68000 does not output address bit A0. This address bit needs
to be reconstructed from the 68000 data strobes. To achieve 68000 byte-order
on the Multibus, the A0 on the Multibus must be the inverse of 68000 A0
for byte transfers.

It is strongly recommended to use the Sun 68000 with 68000 byte order.
However, for systems that require Multibus byte order, the Sun 68000
board provides a pair of jumpers to switch from 68000 to Multibus byte order.
Note that Multibus byte order is inconsistent with 68000 byte order.

To keep 68000 byte order, install J801-1..2 and do not install J801-3::4.
For Multibus byte order, install J801-3::4 and do not install J801-1..2.


P2 Serial Port:			Prewired to be a DTE on Port 2.

    P2.RxD	J100-1::2	Connects P2.RxD as DTE
    P2.TxD	J100-3::4	Connects P2.TxD as DTE
    P2.RxD	J100-1..3	Connects P2.RxD as DCE
    P2.TxD	J100-2..4	Connects P2.TxD as DCE

PROM Type:		        Prewired for 2732/2764 EPROMs.

    2764/2732	J100-7::8	Connects U101..U104(23) to A12
    2716	J100-5..6	Connects U101..U104(23) to VCC

Byte-Order Select:		Prewired for 68000 Byte Order

    A0=LDS\	J801-1..2	Multibus Byte Order
    A0=UDS\	J801-3::4	68000 Byte Order
-------


Note: a special version of the Sun 68000 Board is available to support
24-bit Multibus systems. This board does not support the Sun 68000
Memory Expansion Board, however, because it uses the P2 connector
to drive the high-order Multibus addresses. Address bits
A20 through A22 are generated from the three highest order bits of
the physical address in the page map entry, whereas address bit A23
is terminated to be 0. Thus this special version of the Sun 68000 board
can address directly the low-order 8 MBytes of the expanded
16 MByte Multibus address space.

--------

On power-up, the monitor maps the first megabyte
of on-board RAM and memory expansion board RAM so that
its physical and virtual addresses are identical.
All segments, starting at segment 0, are fully mapped
to page map entries.
Segments are initialized for all contexts identically. Segment
protection is set so that both Supervisor and User modes have Read, Write,
and Execute access to every segment.
The first 512 page map entries access sequential on-board memory addresses,
unless there is less than 1 Mbyte of memory, in which case all page map entries
corresponding to nonexistent memory are invalidated.

Two other physical address spaces are mapped into the memory address
space.
Address from 0x100000 to 0x1EFFFF are mapped to Multibus
memory space addresses 0 to 0EFFFF, respectively.
The first 64K bytes of Multibus I/O space is mapped at the top of
the virtual address space, at addresses from 0x1F0000 to 0x1FFFFF.
Most commercially available Multibus I/O devices use this space.

---

## Interrupts


The 68000 has seven interrupt levels, numbered 1 through 7, with level 7 being
the highest priority and level 1 the least priority.  Interrupts are recognized
for all priority levels greater than the current processor priority contained
in the 68000 status register.  When an interrupt is acknowledged, the processor
priority is set to the level of the interrupt request.

A level 7 interrupt is special in that it is recognized even if the mask in the
68000's status register is set to 7, thus providing a non-maskable interrupt
capability.  A level 7 interrupt is acknowledged every time the interrupt
request changes from a lower level to level 7, that is, level 7 interrupts are
"edge-triggered".

The Sun 68000 board operates the 68000 in auto-vector mode,
that is interrupt vectors are generated internally to the 68000
and peripheral devices do not provide interrupt vectors.
The interrupt vector capabilities of the Multibus are not used.

The board has three on-board interrupt sources wired as follows:


	INT7	REFRESH TIMER (non-maskable interrupt)
	INT6	TIMER2	(user programmable timer)
	INT5	SERIAL I/O CHIP (UART).


These interrupt levels are normally disconnected from the Multibus.
Interrupt level 1 thru 4 are available on the Multibus.

Note: interrupt levels were labelled according to 68000 order.
Thus Interrupt level 7 is the highest priority (non-maskable) interrupt,
interrupt level 1 is the least priority.
This ordering is different from the standard Multibus order where
Level 0 is the highest priority and level 7 is the least.
Since the 68000 only has 7 interrupt levels versus 8 for the Multibus,
Interrupt level 0 on the Multibus is unused.

Interrupt level assignments can be modified via Jumper J904.
The default is the assignment described above
with on-board interrupts isolated from Multibus.

*Exceptions*.
In ``boot state'', the state of the system after reset, read and execute
accesses to any location 0x0XXXXX in mapped address space are redirected to
come from the corresponding location 0x2XXXXX (in the PROM0 address space),
but write accesses to the mapped address space go to on board RAM or Multibus
as usual.  Refer to the section on initialization for further information.
Write accesses to any location 0x2XXXXX (PROM0 address space)
set the state of parity enable (see section on exception handling).
