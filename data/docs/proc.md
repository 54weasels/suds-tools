# proc.mss

.bp
.NH
PROGRAMMING THE SUN PROCESSOR
.NH 2
Processor
.NH 3
Physical Address Space
.PP
The Sun processor is provided with a map so that you can map pages of 2K
bytes anywhere in your address space.
The structure of a virtual address
is described in the Memory Managsses are identical.
All segments, starting at segment 0, are fully mapped
to page map entries.
Segments are initialized for all contexts identically.
Segment
protection is set so that both Supervisor and User modes have Read, Write,
and Execute access to every segment.
The first 512 page map entries access sequential on-board memory addresses,
unless there is less than 1 Mbyte of memory, in which case all page map entries
corresponding to nonexistent memory are invalidated.
.PP
Two other physical address sp.
The first 64K bytes of MultiBus I/O space is mapped at the top of
the virtual address space, at addresses from 0x1F0000 to 0x1FFFFF.
Most commercially available Multibus I/O devices use this space.
.PP
The logical address space of 24-bit addresses used by the programmer
is divided into eight parts:
.IP "0x000000 - 0x1FFFFF" 20
Mapped address space, as described above.
There are 256K bytes of on-board RAM and up to
two memory expansion boards.  The first memory expansion board
adds 768K, bringing the totMultibus Memory space on a per-page basis (see section 5.2.5,
``Page Map'', below).
.IP "0x200000 - 0x3FFFFF" 20
On board PROM0.
See the discussion below on ``boot
state''.
.IP "0x400000 - 0x5FFFFF" 20
On board PROM1.
.IP "0x600000 - 0x7FFFFF" 20
The on-b 20
On board Timer chip. 800000 is the Data register, 800002 is
the Command register.
.IP "0xA00000 - 0xBFFFFF" 20
Page map.
The page map entry used to map some virtual address X is addressed
at virtual address X + 0xA00000\(dg.
.FS
\(dg Actually, the lowess X should be
set up before accessing the page map entries since the segment map
entries determine which page map entries are accessed.
.IP "0xC00000 - 0xDFFFFF" 20
Segment map.
The current value of the context register determines which group
of segment the low-order 15 bits are ignored, except that the MC68000
requires the low-order bit to be zero.
.FE
.IP "" 20
When read as a short-word, the high-order 4
bits of any segment map entry
give the current value of the context register.
.IP "0xE00000 - 0xFFthis input port for
the keyboard and mouse.
.PP
In ``boot state'', the state of the system after reset, read and execute
accesses to any location 0x0zzzzz in mapped addresss space are redirected to
come from the corresponding location 0x2zzzzz (in the PROe'' ones) are inhibited.
In this way it is possible to initialize RAM just after reset.
Boot state
is exited by writing to the PROM0 address space.
(Note that this enables or disables parity; see next section).
.NH 3
Exception Handling
.PP
When a processoyte address, five external conditions
can make it impossible to complete the current instruction or bus cycle.
These external conditions which raise a Bus Error
exception are: system space
errors, segment map errors, page map errors, timeout errors, and por supervisor state to address the on-board
system facilities.
A segment map error indicates that the protection bits in the segment map
did not allow the type of operation attempted.
A page map error is caused by accessing an invalid page.
Timeout errorsce has been addressed.
(There are no timeouts for on-board references because the on-board bus
is synchronous and all cycles are always acknowledged.  If a page is
mapped to a nonexistent on-board RAM address, writes are ignored and
reads return random dannot abort the cycle in which the error occured, but the next
cycle.
Parity checking can be enabled or disabled under software control.
When a write is done to PROM0 address space, the
low order bit of the data written controls whether parity checking
is r occurs the cause of the error can be determined by checking
whether the attempted access was to system space in user mode, whether
a mapped access violated the segment protection code, or whether the page
referenced was nonexistent.
If none of the above
The MC68000 has seven interrupt levels, numbered 1 through 7, with level 7
being the highest priority and level 1 the lowest priority.
Interrupts are recognized for all priority levels greater the the
current processor priority level contained in the MC6 that it is recognized even if the mask
in the MC68000's status register is set to 7, thus providing a
non-maskable interrupt capability.
A level 7 interrupt is acknowledged every time the interrupt request
changes from a lower level to level 7, that is,tandard recommends the interrupts be level triggered instead of
edge-triggered to allow multiple interrupt sources on each interrupt line.
.PP
To avoid confusion for MC68000 programmers, the numbering and the priorities
of the interrupt lines on the Multinted.
In addition, INT7 is non-maskable and edge-triggered, whereas all other
interrupts are maskable and level-triggered.
.PP
Three interrupt lines are assigned to on-board interrupt sources:
INT7 - Refresh Timer, INT6 - User Timer, INT5 - UART.
INT7, INly by the MC68000 and is not
supplied by the device.
Thus the INTA signal on the Multibus and the interrupt vector capabilities
of the Multibus are not used.
.NH 3
Initialization
.PP
After hardware reset, the MC68000 processor board comes up in a special
s
RAM starting at location 0, and is also accessible in its normal location.
Thus the initial program counter and stack pointer are fetched from PROM
at locations 0 to 3, whereas other bootstrap code can execute from
normal PROM addresses.
.IP 2)
Since teption and interrupt vectors in RAM.
.IP 3)
All interrupts, including the non-maskable interrupt, are disabled in hardware.
After leaving the boot state, non-maskable interrupts can occur at any time,
and maskable interrupts can occur as soon as the inter or disables parity checking;
see section ``Exception Handling'' above.
.NH 2
Memory Management
.NH 3
Overview
.PP
The Sun Memory Management Unit has been designed to support
a multi-tasking operating system, such as Bell Labs'
.UX
system.
It provides address translation, protection, sharing, and
memory allocation for multiple processes executing on the
MC68000.
All accesses of the MC68000 to on-board RAM memory,
Multibus memory, and Multibus I/O space are translated
and protected in an identical fashion.emory processor when it becomes available.
.PP
The memory management consists of a context register, a segment map,
and a page map.
Virtual addresses from the processor are translated into intermediate
addresses by the segment map and then into physical aently.
The maximum logical address space for a context is 1024 pages (2M bytes).
The maximum physical address space that can be mapped simultaneously is
2M bytes.
.PP
The organization of the memory management system is shown in figure MEMMAN
below.
The ad2i
.ce
Figure MEMMAN.  Memory Mapping on the Sun Processor.
.sp 2v
.DE
.KE
.KF
.DS L
.sp 3i
.sp
.sp
.sp 3i
.ce
Figure MMADDR.  Addressing Scheme for Segment and Page Map Entries.
.sp 2v
.DE
.KE
.NH 3
Context Register
.PP
In a multitask environment it is important to be able to switch between
processes quickly without having to reload all the translation state
information of a particular process.
The context register is a 4 bit register which can be set under supervisor
control to switch between 16 sectionsplacing
out-of-date contexts on a least-recently-used or other basis.
.PP
Each context has its own virtual address space.
Sharing and intercontext communication may be implemented
by writing the same values into the segment or page maps
of multiple contexts.
.PP
A simple implementation of multitasking will allocate one context
per process.
More complex schemes are possible in which a team of processes occupies
one context, or in which one process extends over more than one context
(with context changes managat the currently executing instruction stream at the time
of a write must be mapped into both the old and new
contexts at the same address (or must be in PROM).
The context register is read by reading any of the segment map
entries (starting at location 0ts.  This requires that valid
interrupt vectors must always be mapped in page 0 of each context, as
well as a valid Supervisor Stack.
.NH 3
Segment Map
.PP
The segment map has 1024 entries, indexed by the 6 most significant bits of
the virtual address andh-order bits of a pointer
into the page map
and a 4 bit protection code, defined below.
.PP
Only the 64 segments of the current context may be addressed at
any one time\(dg.
.FS
\(dg ROM routines, which run outside mappable memory, are provided for
readinich group
of segment map entries are addressed.
The segment map entry used to map some virtual address X is
addressed at virtual address X + 0xC00000.
.PP
Each virtual address space thus has 64 segments.
Each segment can be mapped to 16 pages (32K bytes) or can be
made inaccessible.
The 16 page map entries pointed to by the segment map entry
determine whether each 2K page exists and where it is located.
.NH 3
Protection
.PP
Protection is associated with the segment map; each segment has a
4-bit protection four bits, 16 of the most
useful combinations are provided.
The 16 protection codes are defined in the following table.
Full access is denoted "rwxrwx",
with the first "rwx" being Read-Write-eXecute for the supervisor
and the second for the user.
A "-" de--------      --------------
 0  ------  None           None           Unused segment
 1  --x---  Execute        None           System code
 2  r-----  Read           None           System fixed data
 3  r-x---  Read, execute  None           Mixed system           User fixed data
 7  rw-r--  Read, write    Read           System -> user transfer
 8  r--rw-  Read           Read, write    User variable data
 9  rw-rw-  Read, write    Read, write    System <-> user data
10  rw-r-x  Read, write    Read, executead, execute  System-generated, shared
14  rwx--x  Full           Execute        Proprietary code
15  rwxrwx  Full           Full           Unprotected
.DE
.NH 3
Page Map
.PP
The page map handles the paging and the allocation of physical memory.
A page marithms by maintaining
reference and modified bits for each page.
.PP
The 6 bits from the segment map entry concatenated with
the next 4 logical address bits from the MC68000
form an index into the page map.
Thus each segment accesses a block of 16 consecu form a 23-bit physical address.
In addition, a page can be declared to be in on-board memory space,
Multibus memory space, Multibus I/O space, or nonexistent, according
to the following values of the page type field:
.DS
0 - on-board memory
1 - nonexisted and can be used
by software.
.PP
Notice that each of the physical
address spaces is 23 address bits (8M bytes) large.
Since on-board memory is at most 2 megabytes with two memory
expansion boards, and the address space on the standard Multibus is at
mosare to provide correct table entries for
a particular system configuration.
.PP
The page map entry used to map some virtual address X is addressed
at virtual address X + 0xA00000.
Note that the context register and
segment map entries for virtual address ion to the page mapping information, each page entry has two
associated statistic bits, "accessed" and "modified", that are set whenever
that page has been accessed or written into, respectively.
These bits are updated automatically on all cycles for which access has
been granted by the protection mechanism.
Bit 14 of the page map entry is the "modified" bit and bit 15 is
the "accessed" bit.
