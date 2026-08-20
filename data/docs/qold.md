---


---


# Sun-2 Processor Board


User Manual

Draft Version 1.0

Company Confidential

Sun Microsystems Inc.

April 1, 1983


>
The Sun-2 Processor Board is a powerful single-board computer combining
a 10 MHz 68010, multiprocess virtual memory management,
direct virtual memory access (DVMA), two serial channels, five timers, and a
16-bit parallel input port on a single board compatible with the IEEE 796 Bus
(Intel Multibus). A floating point processor and a data ciphering processor
can optionally be added.
The memory management supports processes with up to 16 MByte virtual memory space
and physical memories up to 8 MByte of zero wait-state memory.


>
Multibus is a trademark of Intel Corporation.
Sun and DVMA are trademarks of Sun Microsystems Inc.


---


---

# Architecture Overview


## Features


10-MHz M68010 CPU

no wait states with Sun Memory Expansion Boards

addresses up to 8 MBytes of no-wait state main memory

two-level, multiprocess virtual memory management

16 Mbytes virtual address space per process

separate address spaces for supervisor and user

protection bits at page level

up to 64K bytes EPROM

two programmable high-speed serial I/O channels

five programmable 16-bit timers

16-bit parallel input port

8-bit parallel diagnostic output port

optional DES encryption processor

optional IEEE standard floating point processor

DVMA (direct virtual memory access) from Multibus

soft interrupts

bus error register

transparent hardware memory refresh

watchdog reset timer

P1-bus fully compatible with IEEE-796 Bus (Intel Multibus)

P2-bus implements high-speed synchronous memory bus

single 5 Volt power supply


---

# Sun-2 Memory Management Unit


## Summary


```

	page size:		2 KBytes
	segment size:		64 KBytes
	process size:		16 MBytes
	# of contexts:		8
	# of segments/context:	512
	# of pages/segment:	16
	# of pmegs:		256	(pmeg = page map entry group)
	# of pages total:	4096
	# of segments total:	4096

```


## Virtual Address


```

        24	       15      11                   1   0
	--------------------------------------------------
	|      (9)	|  (4)  |       (10)	     |(1)|
	--------------------------------------------------

	segment #	 page #      word #           byte #

```


## Context Register


```

	15             8 7             0
	---------------------------------
	| (res)	|  (3)  | (res)	|  (3)	|	(res): reserved (undefined)
	---------------------------------
	 System Context    User Context

```


## Segment Map


```

	7		0
	-----------------
	|     (8)	|
	-----------------
	     pmeg #

```


## Page Map


```

        31 30      25	22  20 19	     12		               0
	-----------------------------------------------------------------
	|1|  (6)     |  (3) |1|1|      (8)     |      (12)     		|
	-----------------------------------------------------------------

	 v protection  type  a m    (reserved)        page #
	   (rwxrwx)

	v: valid bit
	a: accessed bit
	m: modified bit

```


---

## MMU Overview


The Sun-2 Memory Management Unit
provides address translation, protection, sharing, and
memory allocation for multiple processes executing on the
68010 CPU. All CPU accesses to memory, I/O,
and Multibus devices are translated and protected in an identical fashion.

The memory management consists of a context register, a segment map,
and a page map.
Virtual addresses from the processor are translated into intermediate
addresses by the segment map and then into physical addresses by the page map.

The page size is 2048 bytes, the segment size is 32K bytes (giving
16 pages per segment), and up to 8 contexts can be mapped concurrently.
The maximum logical address space for a context is 16M bytes.
The maximum physical address space that can be mapped simultaneously is
8M bytes.


## Contexts


The Sun-2 MMU is divided into 8 distinct address spaces or "contexts".
The current context is selected by means of a 3-bit *context* register.
To allow different address spaces for the supervisor and user,
two alternate context values are provided.
The MMU automatically uses the system context register whenever the
68010 issues a supervisor function code.
The supervisor can address the user context via the 68010 MOVS instruction
using a non-supervisor function code,
by mapping the pages of interest into its own system context,
or by sharing address space with the user by setting the two context values equal.
The two context registers can be accessed as a word
or separately accessed as the odd or even byte within a word.


## Segment Map


The segment map has 4096 entries. It is indexed by the 8 most significant bits of
the virtual address and 4 bits of the current context register.
Thus, the segment map is divided into 8 sections of 512 entries each,
with one section per context.
Segment map entries are 8 bits wide, pointing to a page map entry group (*pmeg*).


## Page Map


The page map contains 4096 page entries each corresponding to a 2K byte page.
Page map entries are composed of a valid bit, protection field, type field,
accessed and modified bits, and a page number.

The page map is divided into 256 sections of 16 entries each.
Each section is pointed to by a segment map entry and is called
a page map entry group, or *pmeg*.


### Valid Bit


The valid bit determines whether a page map entry is valid or not.
A valid bit of 1 means that the page map entry is valid and that
the other fields of the page map entry determine how the reference
is to be translated and protected.
A valid bit of 0 means that an access to this page will be aborted,
while the rest of the page map entry is ignored.
In this case, the remaining bits of the page map entry may contain
arbitrary information.


### Protection Field


Access to pages can be controlled via the 6-bit protection field.
From left (MSB) to right (LSB), the six bits correspond to
"supervisor-read-write-execute" and "user-read-write-execute" privileges.
This provides all 64 combinations of supervisor and user "rwxrwx".
A "1" entry enables the corresponding capability, a "0" bit
means that the respective capability is disabled.


### PageType


The page type field provides for multiple physical address spaces,
each starting at a physical address of 0.
At the same time, the page type field decodes what busses and bus synchronization
is required for a particular physical address space.
The decoding of the page type field is described in a subsequent chapter.


### Accessed and Modified Bits


The accessed and modified bits are set, as the name implies,
whenever a page is accessed or modified (written into).
These bits will not be updated on accesses to a page that is invalid or protected.
The protection bits will be updated on all other cycles,
including cycles that terminate due to timeout or cycles that cause parity errors.


### Physical Address


The page map contains a 20-bit page number field. In conjunction with the
11-bit byte number, the page map thus generates a 31-bit physical address,
capable of addressing up to 2 GBytes.

The present Sun-2 Processor Board implements a subset of this addressing
capability in that its page number field only stores 12 bits. It thus
supports a physical address of 23 bits, capable of addressing 8 MBytes.
The other physical address bits in the page map are not implemented.
They may be written but will always read back as 0.


## Access to MMU


Entries in the Sun-2 MMU are accessed by the same address they
normally would translate, but using the reserved function code "3"
as the source or destination function of a `MOVS` instruction.
The content of the user context register selects
which context's map will be modified.
Byte, word and long-word accesses to the maps are supported.
For a given MMU address, address bits A1 and A2 select which
element of the MMU is to be modified:


```

 A2 A1	ENTRY
--------------------------------
  0  0	PAGE MAP <16..31>
  0  1	PAGE MAP <0..15>
  1  0  SEGMENT MAP <0..7>
  1  1	CONTEXT REGISTER <0..15>
--------------------------------

```


Thus, for user virtual address V, the map entries are accessed at location:

```

  MAP		ADDRESS	SIZE	RELEVANT BITS
--------------------------------------------
  PAGEMAP	0 + V	LONG	V & 0xFFF800
  SEGMENT MAP:	4 + V	BYTE	V & 0xFF0000
  CONTEXT REG:	6 + V	WORD	V & 0x000000
--------------------------------------------

```


---

# Page Types


This chapter discusses the characteristics of the different page types.
The following table gives the decoding of the page type field and
shows what busses and synchronization are used for each type.

```


TYPE	DEVICE		BUS	ACK
----------------------------------------
0	On-board RAM	P2-Bus	always
1	On-board I/O	--	always
2	Multibus Memory	P1-Bus	P1-XACK
3	Multibus I/O	P1-Bus	P1-XACK
4	RESERVED
5	RESERVED
6	RESERVED
7	RESERVED
----------------------------------------

```


Each page type offers a full physical address space of 31 bits
(of which 23 bits are implemented on the Sun-2 Processor Board).
In general, non-implemented addresses within each page type are
not further decoded and cause no error when set.
Exceptions to this are described below.
It is the responsibility of the system configuration software
to map only those addresses within each page type that are actually
present in a given system.


## On-board RAM


Page Type 0 selects local main memory.
Local main memory is provided by the Sun-2 Memory Expansion boards that
interface to the Sun-2 Processor Board via the P2 Bus.
Sun-2 memory expansion boards are refreshed in hardware on the Sun-2
processor board.


## On-board I/O


Page Type 1 gives access to on-board I/O devices.
On-board I/O devices are mapped via individual pages.
The devices available and their features are further described
in chapter [Figure](#IOpages).


## Multibus Memory


Page Type 2 selects the Multibus memory address space.
The Sun-2 Processor Board supports the 20-bit or 1 MByte
physical address space on the P1 connector of the Multibus.
Accesses to non-existing devices on the Multibus will cause a timeout exception.


## Multibus I/O


Page Type 3 selects the Multibus I/O address space.
The Sun-2 Processor Board can generates a 20-bit or 1 MByte
physical address for I/O devices, though most I/O devices
only decode a 16-bit or 8-bit address. Accesses to non-existing
devices on the Multibus will cause a timeout exception.

---

# DVMA: Direct Virtual Memory Access


The Sun-2 Processor Board allows other Multibus masters to directly access onboard
memory and I/O devices via DVMA (Direct Virtual Memory Access).
Direct virtual memory access avoids the dual mapping problems of DMA
(direct memory access) in a virtual memory environment.
DVMA translates and protects all accesses within the system in an identical fashion.
DVMA can be enabled or disabled under software control via
the DVMA enable bit in the system register.

*Mapping*. DVMA maps the 1 MByte Multibus memory address space
into the top 1 MByte of the current system context virtual address space.

*Enabled Sections*. 256 KByte sections of the 1 Mbyte Multibus memory space
can be individually enabled for DVMA operation as a
hardware configuration option. The standard configuration is that the
Sun-2 processor board responds to the low order 256 KByte for DVMA operation.

*Protection*. Protection applies to DVMA the same way as to the 68010.
DVMA cycles use the "supervisor data" function code.
Thus the supervisor read or write capability in the page map has to be
enabled to allow the corresponding type of access.
If the respective capability is not set, the attempted DVMA cycle
is aborted (see section on error handling).

*Parity Errors*.
DVMA read cycles that cause a parity error are
aborted as described under error handling.

*Error Handling*.
DVMA cycles that abort due to protection or parity error
signal the abort to the controlling Multibus master
by inhibiting Multibus transfer acknowledge (XACK).
This is interpreted by the Multibus master as an access to a nonexistent
device and should cause a timeout exception.
To allow this error handling, DVMA masters must support a timeout mechanism.
It is recommended that the timeout period be as short as possible because
on-board operation cannot proceed until the DVMA master ends the bus cycle.
In order to guarantee real-time response, other Multibus masters should
provide timeouts in the range of tens of microseconds.

*Statistic Bits*. The update and modify bits are set on DVMA cycles
that execute sucessfully the same way as on 68010 cycles.
Cycles aborted due to protection error do not change these bits.

*Selfreference*. Two types of self-reference are possible:
from the Sun-2 Processor Board to Multibus back to itself, and from
Multibus through the memory management back to the Multibus.
Neither type of access will complete.
For Sun-2 Processor Board accesses, the timeout period is the standard
timeout period of 15 microseconds. For DVMA cycles, the timeout period is
determined by the Multibus master.

*Deadlock*. Since Multibus mastership is arbitrated independently
from the 68010 bus mastership, the possibility exists that the
68010 is attempting to access the Multibus while the Multibus is
attempting to access the on-board bus. If this condition occurs,
deadlock is avoided by suspending the 68010 bus cycle and yielding
the on-board bus to the Multibus DVMA cycle. The 68010 cycle will resume
when the Multibus DVMA cycle is completed.

---

# I/O Pages

<a id="IOpages"></a>

The Sun-2 Processor Board provides two high-speed serial channels,
five 16-bit timers, and a 16-bit input port as on-board devices.
The capabilities of these devices and the location of their connectors
allow direct upgrading to Sun-2 processors from Sun-1 processor boards.
In addition, the Sun-2 Processor Board features an 8-bit output or
diagnostic port, optional floating point and data encryption processors,
and software accessible bus error and system enable registers.


## Access to on-board Devices


All on-board devices are accessed through the memory management unit.
This allows on-board devices to be protected, shared, and managed
effectively in a multiprocess environment.
The only exceptions to the mapping is access to the memory management itself,
described under the memory management, and booting, described under booting.

I/O devices on the Sun-2 processor board are assigned the first 16 pages
in the I/O addressing space.  In general, devices decode only those address
bits described under the individual device. Other address bits are ignored.
All other I/O pages are reserved for future expansion.
Accesses to reserved pages are not checked by the Sun-2 Processor.


```

IO-PAGE	DEVICE
--------------------------
    0	EPROM0
    1	EPROM1
    2	IDPROM
    3	PARALLEL PORT
    4	SCC
    5	TIMER
    6	BUS ERROR REGISTER
    7	SYSTEM ENABLE REGISTER
    8	RESERVED
    9	RESERVED
    10	FLOATING POINT PROCESSOR
    11	DATA CIPHERING PROCESSOR
    12	RESERVED
    13	RESERVED
    14	RESERVED
    15	RESERVED
--------------------------

```


## EPROM0 and EPROM1


Four 28-pin sockets for 64K or 128K EPROMs are provided.
The EPROMs are accessed as two 16-bit wide pairs (EPROM0, EPROM1).
Since the EPROMs are larger than a single 2K page, they are
addressed directly with non-translated addresses from the 68010,
even though they are enabled through a sequence of pages in the page map.
Thus a group of pages with the same page map entry (e.g. EPROM0)
will map to different sections of the EPROM, based on address bits
11 through 13 of the virtual address.


## ID PROM


The ID PROM offers 512 Byte of PROM storage for items such as serial number,
Ethernet ID, and other permanent identifiers established at manufacturing time.
It is addressed at odd byte locations 1,3,5,...,1023 within the page.


```

REGISTER	ADDRESS	SIZE	TYPE
------------------------------------------
ID PROM 0	1	BYTE	READ-ONLY
ID PROM 1	3	BYTE	READ-ONLY
...		...	...	...
ID PROM 511	1023	BYTE	READ-ONLY
------------------------------------------

```


## Parallel Port


A Parallel port is provided that offers a non-latching 16-bit input port,
accessible via connector J2.
and a latching 8-bit output port, wired to connector J3.
The output port is intended to be used as a diagnostic register
driving an 8-bit LED display. The input port can be used for diagnostics as well.


```

REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
INPUT PORT	0	WORD	READ-ONLY
OUTPUT PORT	0	BYTE	WRITE-ONLY
------------------------------------------

```


## SCC Serial Communication Controller


Serial I/O is implemented with the Zilog 8530 SCC serial communication controller.
The SCC features two high-speed, fully symmetrical and highly
programmable serial channels with built-in baud-rate generators.
Both channels are configured as DTE (data-terminal-equipment),
implement full modem control, and offer synchronous clock capabilities.
Modem controls are terminated on the board
such that they are enabled when not actively driven by the connected device.
The DTE interfaces are provided on connector J1.
SCC Registers are mapped as follows:


```

REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
CH B CONTROL	0	BYTE	READ/WRITE
CH B DATA	2	BYTE	READ/WRITE
CH A CONTROL	4	BYTE	READ/WRITE
CH A DATA	6	BYTE	READ/WRITE
------------------------------------------

```


## Timer


An AMD 9513 timer chip with five 16-bit timers is provided.
Timer 1 OUT is connected to the non-maskable interrupt level 7
for purposes such as making profile statistics.
Timers 2 through 5 interrupt on level 6.
The gate inputs for timers 5, 4 and 3 are driven by supervisor state,
user state, and "CPU is not master" state, respectively.
The timer command/data port is mapped as follows:


```

REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
TIMER DATA	0	0..15	READ/WRITE
TIMER COMMAND	2	0..15	READ/WRITE
------------------------------------------

```


## Bus Error Register


The bus error register latches the cause of a bus error when a bus error occurs.
It can then be read by software to identify the source of the error.
If multiple bus errors occur, the register displays only the cause
of the most recent bus error event. The bus error register is a read-only
register. It is only written upon a bus error. It is not initialized
upon reset or power-up.


```

REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
BUS ERROR REG	0	WORD	READ-ONLY
------------------------------------------

BUS ERROR REGISTER FIELDS
----------------------------------------------------------
    D0	PARERRL		Parity Error Low Byte
    D1	PARERRU		Parity Error Upper Byte
    D2	TIMEOUT		Timeout Error
    D3	PROTERR		Protection Error
    D4	(reserved)
    D5	(reserved)
    D6	(reserved)
    D7	PAGEVALID	1 => Valid Page, 0 => invalid page
    D8..D15		Reserved
----------------------------------------------------------

```


See the section on bus errors for a meaning of these bits.


## System Enable Register


The System Enable Register enables system facilities,
provides soft interrupts, and controls booting.
The System Enable Register can be read and written under software control
and is cleared on power up (hardware reset) and watchdog reset,
but not upon 68010 reset.
Bits are assigned as follows:


```

REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
SYSTEM ENABLE REG. 0	WORD	READ/WRITE
------------------------------------------

SYSTEM ENABLE REGISTER FIELDS
-----------------------------------------------------------
    D0	EN.PAR		Enable Parity Generation
    D1	EN.INT1		Enable Soft Interrupt Level 1
    D2	EN.INT2		Enable Soft Interrupt Level 2
    D3	EN.INT3		Enable Soft Interrupt Level 3
    D4	EN.PARERR	Enable Parity Error Checking
    D5	EN.DVMA		Enable Direct Virtual Memory Access
    D6	EN.INT		Enable Interrupts
    D7	BOOT\ 		Boot State (0 => boot, 1 => normal)
    D8..D15		Reserved
-----------------------------------------------------------

```


When cleared after power-up or watchdog reset, all bits are 0
and Boot State is active. In this state, parity generation
and checking is disabled, soft interrupts, DVMA, and all other
interrupts are disabled.


## Floating Point Processor Option


This option is currently under development.


## Encryption Processor Option


The Encryption processor option is a socket for an AMD 9518
data ciphering processor providing high-speed NBS DES encryption.
To access an internal register in the 9518, the address register
must be written first. Once the address register is setup,
the selected register can be accessed repeatedly.


```

REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
DATA REGISTER	0	BYTE	READ/WRITE
ADDRESS REG.	2	BYTE	WRITE-ONLY
------------------------------------------

```


---

# Processor Operation


This chapter gives details of the 68010 processor
operation on the Sun-2 Processor Board.


## Reset


Four types of reset need to be distinguished:
Power-On Reset, Watchdog Reset, 68010 Reset, and Multibus reset.

*Power-On Reset*. Power-On Reset (POR) is active
after the power supply voltage reaches 4.5V.
POR resets the 68010, the floating point processor,
and clears the System Enable register, thereby forcing boot state.
The 9513 timer, the 8530 SCC, and the 9518 DCP
are not reset by POR and need to be initialized in software.
The 9513 timer is special in that is has an on-chip power-on reset
that initializes the chip whenever the power supply voltage is less than 3V.

*Watchdog Reset*.
A hardware watchdog timer is provided that generates a signal
equivalent to power-on reset (POR) whenever the case the 68010 halts
with a double bus fault. The result of a watchdog reset is identical to a POR,
except for the 9513 timer chip that is not affected by watchdog resets.
The 9513 timer chip can thus be used to distinguish POR from watchdog resets.

*68010 Reset*. When the 68010 executes a Reset Instruction,
it resets the floating point processor and it asserts the Multibus INIT line.
No other devices are affected. Specifically, the system enable register
is not cleared.

*Multibus Reset*. The Sun-2 Processor Board is a Multibus reset master, that is,
it drives INIT to the Multibus but is not affected by INIT from the Multibus.
Power-On Reset, Watchdog Reset, and 68010 Reset will all assert Multibus INIT.
Other Multibus devices may also assert Multibus INIT, but this will have
no affect on the Sun-2 Processor Board.


## Booting


Upon Power-on Reset or Watchdog Reset, the system enable register is cleared,
forcing boot state active and disabling all interrupts and parity errors.
Boot state forces all supervisor program fetches to access PROM0
independent of the setting of the memory management.
All other types of references are unaffected and will be mapped
as during normal operation of the processor.


## Bus Error


68010 Bus Error is caused by one of five conditions:
page invalid, protection error, parity error low byte, parity error high byte,
and timeout.
Bus error is inhibited during cycles that access the MMU, during
interrupt acknowledge cycles, and during supervisor program accesses
in boot state.

In more detail, the bus error conditions are as follows:


Page invalid (PAGEVALID=0) means that the page referenced did not
have a valid bit set.

Protection error (PROTERR) means that the page protection bits
or the PAGEVALID bit
did not allow the kind of operation attempted.

Parity errors (PARERRL and PARERRU) can occur only on read cycles from
local memory (page type 0).
Since parity errors are detected too late in the cycle to abort
the current cycle, they abort the following cycle instead.
If the following cycle does not recognize bus errors (see above)
then the parity error will abort the next cycle that does recognize bus errors.
In any event, the address in which the 68010 receives the bus error
is unrelated to the address of the parity error, which is not available.

TIMEOUT can result only from a reference to Multibus memory
or I/O space (page type 2 and 3).
Timeout is generated by a hardware timer whenever a Multibus cycle
exceeds 15 microseconds. The timeout period excludes the Multibus arbitration time.
Thus if the processor board is never granted access to the Multibus,
an attempted access to the Multibus results in permanent waiting.


The statistic bits (accessed and modified) will not be updated
when the page is invalid or when the protection code
does not allow the attempted operation.


## Hardware Interrupts


Interrupts are handled by the 68010 in autovector mode.
The default assignment of interrupt levels is as follows:


```

------------------------------------------------
    7	TIMER1
    6	TIMER2..5
    5	Serial I/O
    4	Multibus level 4
    3	Multibus level 3 or system enable register
    2 	Multibus level 2 or system enable register
    1 	Multibus level 1 or system enable register
------------------------------------------------

```


## Software Interrupts


The Sun-2 Processor Board can generate software or soft interrupts on
interrupt levels 1, 2, or 3, by setting the respective interrupt bits
in the system enable register.
These bits allow higher-priority interrupt routines to request a lower priority
interrupt to handle events after other high-priority interrupts have been
serviced. The soft interrupt lines also drive the Multibus.
This allows the Sun-2 Processor Board to interrupt other
Multibus devices.

---

# Timing


This chapter summarizes the timings for different parts of the Sun 68000
board.


## CPU


The 68010 CPU is driven by a 9.8304 MHz clock.
This means that the shortest possible CPU cycle will take 407 nanoseconds.
For devices that cannot respond in the shortest possible CPU cycle,
the Sun-2 Processor Board will insert wait states to extend the cycle time.
Each wait state will lengthen the CPU cycle by 102 nanoseconds.


## On-board Memory


On-board memory can be accessed by the CPU without wait states.
This means that a read, write, or execute cycle to on-board memory
will take 407 nanoseconds.


## On-board I/O


On-board input/output is accessed with one to five wait states, depending
on the access time of the particular I/O device.
As described before, each wait state extends the CPU cycle by 102 nanoseconds.
The following table gives the wait states for the different devices.


```

IO-PAGE	DEVICE		WAIT STATES
-----------------------------------
    0	EPROM0			1
    1	EPROM1			1
    2	IDPROM			1
    3	INPUT PORT		1
    4	SCC			1
    5	TIMER			1
    6	BUS ERROR REGISTER	1
    7	SYSTEM ENABLE REGISTER	1
    8	RESERVED
    9	RESERVED
    10	FLOATING POINT PROC.	[Note 1]
    11	DATA CIPHERING PROC.	3  [Note 2]
    12	RESERVED
    13	RESERVED
    14	RESERVED
    15	DIAGNOSTIC REGISTER	1
--------------------------
Note 1: Not known yet.
Note 2: Average number. Wait states can range from 1 to 5.

```


## Multibus Access


The timing of Multibus memory and I/O accesses depends on two factors:
first, the access time of the Multibus device and second whether
the Sun-2 Processor Board currently owns Multibus mastership or not.
In addition, some Multibus devices might have slower cycle times
than access times which can affect performance.

The total number of wait states for a Multibus access can be computed
by the following formula:

1 WS (overhead) + 3 WS (if board is currently not Multibus master) +
access time of Multibus device divided by 102 nanoseconds rounded up
to the nearest integer number.


## DVMA Access


DVMA cycles from the Multibus are serviced after the current CPU cycle
completes and after pending memory refresh cycles are executed.
Thus DVMA cycles exhibit a variable access time that ranges from
0.7 microseconds in the best case to 1.5 microseconds worst case
with an average of about 1.0 microseconds.

After a DVMA cycle has executed, typically a CPU cycle will start
before another DVMA cycle is granted. This means that the cycle time
for DVMA is one DVMA cycle plus at least one CPU cycle.
access time of a DVMA cycle. Thus the DVMA cycle time
will be in a range of 1.1 to 2.0 microseconds with an average
of 1.5 microseconds, as long as the DVMA device retains Multibus mastership
and as long as the DVMA master can generate transfers at this rate.
An additional 0.4 microseconds for DVMA access and cycle times
are caused every time the DVMA device arbitrates for Multibus mastership.


## Memory Refresh Timing


On-board memory is dynamic and thus needs to be refreshed to retain
its content. Memory refresh is accomplished in hardware that
executes one refresh cycle approximately every 13 microseconds.
Refresh cycles take 0.4 microseconds, thus the total refresh
overhead is about 3 %.

---

# Connectors


The Sun-2 Processor Board uses the following connectors:


J1 (50-pin) - Two Serial Channels

J2 (50-pin) - Parallel Input Port

J3 (16-pin) - Parallel Output Port

P1 (86-pin) - IEEE 796-Bus

P2 (60-pin) - Sun-2 Memory Bus
