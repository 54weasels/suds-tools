---


---


# Sun-2 Architecture Manual


Draft Version 0.5

Company Confidential

Sun Microsystems Inc.

[date]


>
This document describes the Sun-2 Architecture and its implementations.


>
This document contains unpublished, proprietary information
and describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied
or duplicated in any form without the prior written consent of
SUN MICROSYSTEMS INC.

Sun and DVMA are trademarks of Sun Microsystems Inc.
Multibus is a trademark of Intel Corporation.
UNIX is a trademark of Bell Laboratories.


---


---

# Introduction


This document is the specification of the Sun-2 Architecture.
It is intended as a reference for Sun-2 software, hardware,
and systems implementors.

The main part of this document is independent of a particular
implementations of the Sun-2 architecture.
Implementation specific data, as well as timing information,
is described in an appendix for each implementation.

An important goal of this document is correctness.
Please report any errors, omissions, or oversights
immediately so they can be corrected in future revisions.


## Definitions


In the subsequent description of the Sun-2 architecture the following
abbreviations are used:

**DVMA:** Direct Virtual Memory Access

**CPU:** Central Processing Unit

**MMU:** Memory Management Unit

**PMEG:** Page Map Entry Group

**RES:** Reserved

**POR:** Power-On-Reset


---

# Spaces


The Sun-2 architecture has three major sections:
CPU Space, MMU Space, and Device Space.
Each of these spaces is largely independent of the others.


## CPU Space


The CPU space comprises the 68010/68020 central processing unit (the "CPU")
together with coprocessors, such as the floating point coprocessor,
and DVMA masters, such as the Ethernet interface.


## MMU Space


The MMU space is the core of the Sun-2 architecture.
It includes the Sun-2 memory management unit (the "MMU")
as well as all other Sun-2 architecture extensions to the CPU,
such as the bus error register, the system enable register,
the diagnostic register, and the ID-PROM.
The ID-PROM contains a unique serial number and configuration
data for a particular implementation of the architecture.
All devices in MMU Space are accessed in CPU address space 3.


## Device Space


The Device space of the Sun-2 architecture are the devices
accessed by the CPU with data or program space instructions.
These devices include main memory, the system bus, I/O devices, and so on.
All elements of device space are accessed vi the MMU.
This allows all devices to be protected, shared, and managed
in a uniform manner in a multiprocess environment.


## Address Spaces


The following table describes how the different CPU address spaces
are mapped to the CPU, MMU, and Device space.
By using separate address spaces for MMU and CPU space,
the full virtual address space is retained for supervisor and user processes.


```

----------------------------------------
FC0..2	Address Space
----------------------------------------
0	Reserved
1	Device Space (User Data)
2	Device Space (User Program)
3	MMU Space
4	Reserved
5	Device Space (Supervisor Data)
6	Device Space (Supervisor Program)
7	CPU Space
-----------------------------------------

```


---

# CPU Space


## Reset


Three types of reset need to be distinguished:
Power-On Reset, Watchdog Reset, and CPU Reset.

*Power-On Reset*. Power-On Reset (POR) is active for 100 milliseconds
after the power supply voltage reaches 4.5V.
POR resets the CPU and clears the System Enable register
forcing boot state,
and it resets the diagnostic register, lighting all the LEDs.

*Watchdog Reset*. The Sun-2 architecture provides a
watchdog circuit which generates a signal equivalent to power-on reset (POR)
whenever the CPU halts with a double bus fault.
The result of a watchdog reset is identical to a POR,
as far as the CPU and the system is concerned.

*CPU Reset*. When the CPU executes a reset instruction,
it resets all on-board and off-board I/O devices that offer
an external reset function. No other devices are affected.
Specifically, MMU devices such as the system enable register
and the diagnostic register are not affected by CPU Reset.


---

## DVMA


Input/Output devices with direct memory access capability
are typically implemented in the Sun-2 Architecture
with "direct-virtual-memory-access", or DVMA.

DVMA means that masters use virtual addresses, rather than
physical addresses, to access their target device which is typically memory.
In addition, DVMA translates and protects all accesses in an
identical fashion. This avoids the dual-mapping problems associated
with physical address DMA in a virtual memory environment.

DVMA is implemented as follows:

*Address Space.*
DVMA accesses are performed as data read-write operations
in the supervisor function code.

*Protection*. Protection applies to DVMA the same way as to the CPU.
Thus the supervisor read or write capability in the page map has to be
enabled to allow the corresponding type of access.
If the respective capability is not set, the attempted DVMA cycle
is aborted.

*Parity Errors*.
DVMA read cycles that cause a parity error are aborted.

*Statistic Bits*. The update and modify bits are set on DVMA cycles
that execute sucessfully the same way as on CPU cycles.

*Deadlock*. For DVMA devices that can cause deadlock with the CPU, such
as a CPU access to the system bus conflicting with a DVMA access
from the system bus, deadlock is resolved by rerunning the CPU cycle.

*Self-Reference*. DVMA cycles that are self-referential,
such as a system bus DVMA transfer attempting to reference the system bus,
wiil be aborted.

*Error Handling*.
When a DVMA cycle is aborted, the error is signalled to the controlling master
for error handling. The master typically will stop transferring.

Further details and limitations of DVMA operation are described under
each particular DVMA device.

---

# MMU Space


MMU space includes the Sun-2 memory management unit and
all Sun-2 architectural extensions to the CPU.
These extensions include the bus error register, the system enable register,
the diagnostic register, and the ID-PROM.


## Access to Devices in MMU Space


MMU devices are selected by the low-order address bits.
For map accesses, the high-order virtual address bits determine
which map entry is being modified.
For accesses to the page map and segment map,
the content of the user context register determines
which context's map will be modified.
Thus, for user virtual address V, the map entries are accessed as follows:


```

-----------------------------------------------------
REGISTER/MAP	ADDRESS	SIZE		RELEVANT BITS
-----------------------------------------------------
PAGE MAP	0 + V	LONG/WORD/BYTE	V & 0xFFF800
SEGMENT MAP	4 + V	WORD/BYTE	V & 0xFF8000
CONTEXT REG.	6 + V	WORD/BYTE	V & 0x000000
ID PROM		8 + V	WORD		V & 0xFFF800
DIAGNOSTIC REG.	0xA	WORD
BUS ERROR REG.	0xC	WORD
SYSTEM ENABLE   0xE	WORD
-----------------------------------------------------

```


---

## Memory Management Unit Summary


## Summary


```

	page size:		2 KBytes
	segment size:		32 KBytes
	process size:		16 MBytes
	# of contexts:		8
	# of segments/context:	512
	# of pages/segment:	16
	# of pmegs:		256
	# of pages total:	4096
	# of segments total:	4096

```


### Virtual Address


```

        23	       15      11                   1   0
	--------------------------------------------------
	|      (9)	|  (4)  |       (10)	     |(1)|
	--------------------------------------------------
	segment #	 page #      word #           byte #

```


### Context Register


```

	15             8 7             0
	---------------------------------
	| (res)	|  (3)  | (res)	|  (3)	|	(res): reserved
	---------------------------------
	 System Context    User Context

```


### Segment Map


```

	7		0
	-----------------
	|     (8)	|
	-----------------
	     pmeg #

```


### Page Map


```

        31         25	  22  20                  	               0
	-----------------------------------------------------------------
	|1|  (6)     |  (3) |1|1|            (20)              		|
	-----------------------------------------------------------------
	 v protection  type  a m          physical page #
	   (rwxrwx)

	v: valid bit
	a: accessed bit
	m: modified bit

```


---

## MMU Overview


The Sun-2 Memory Management Unit
provides address translation, protection, sharing, and
memory allocation for a multiprocess environment.
All CPU accesses to memory, on-board I/O, and to the system
bus (P1-Bus) are translated and protected in an identical fashion.
In addition, DVMA accesses by I/O channels
also pass through the virtual memory management and thus
operate in a fully protected environment.

The memory management consists of a context register, a segment map,
and a page map.
Virtual addresses from the processor are translated into intermediate
addresses by the segment map and then into physical addresses by the page map.

The most important numbers for the memory management are a page size of
2048 bytes and a segment size of 32K bytes (giving 16 pages per segment).
Up to 8 contexts can be mapped concurrently.
The maximum virtual address space for each context is 16M bytes.


## Contexts


The Sun-2 MMU is divided into 8 distinct address spaces or "contexts".
The current context is selected by means of a 3-bit *context* register.
To allow different address spaces for the supervisor and user,
separate context values for each are provided.
The MMU automatically uses the system context register whenever the
CPU issues a supervisor function code.
The supervisor can address the user context via the CPU MOVS instruction
using a non-supervisor function code,
by mapping the pages of interest into its own system context,
or by sharing address space with the user by setting the two context values equal.
The two context registers can be accessed as a word
or separately accessed as the odd or even byte within a word.
When read, the reserved bits are not defined.


## Segment Map


The segment map has 4096 entries. It is indexed by the 9 most significant bits of
the virtual address and 3 bits of the current context register.
Thus, the segment map is divided into 8 sections of 512 entries each,
with one section per context.
Segment map entries are 8 bits wide, pointing to a page map entry group (*pmeg*).


## Page Map


The page map contains 4096 page entries each mapping a 2K byte page.
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


### Statistics Bits: Accessed and Modified


The accessed and modified bits are set, as the name implies,
whenever a page is accessed or modified (written into).
The statistics bits will not be updated
when the page is invalid or when the protection code
does not allow the attempted operation.
In addition, these bits will not be updated in a cycle that aborts
due to a parity error in the previous cycle.
However, the statistics bits will be updated on all other cycles,
including cycles that terminate due to timeout or cycles that cause parity errors.


### Physical Page Number


The page map contains a 20-bit physical page number field.
In conjunction with the 11-bit physical byte number,
the page map thus can generate physical addresses
of up to 31 bits.
However, the Sun-2 architecture does not define how many physical address bits
are actually stored in the map, or how many physical address bits are
decoded when accessing specific physical devices.
This specification depends on the implementation and is described
in the implementation section.


### PageType


The page type field provides for multiple physical address spaces,
each starting at a physical address of 0.
At the same time, the page type field can indicate what busses
and bus synchronization are used for a particular physical address space.
The assignment of the page type field is described in the implementation section.

---

## ID PROM


The purpose of the ID PROM is to provide
basic information on the machine type and a unique serial number
for software licensing, distribution, and access. In addition, the ID PROM
stores the Ethernet address, the date of manufacturing, and a checksum.

The ID PROM is implemented as a 32-byte PROM mapped as follows:


```

REGISTER	ADDRESS	SIZE	TYPE
------------------------------------------
ID PROM 0	0x0008	BYTE	READ-ONLY
ID PROM 1	0x0808	BYTE	READ-ONLY
ID PROM 2	0x1008	BYTE	READ-ONLY
...		...	...	...
ID PROM 31	0xF808	BYTE	READ-ONLY
------------------------------------------

```


The content of the ID PROM is as follows:


```


Entry	Field
------------------------------------------------------------
(1) Format		1 Byte
(2) Machine Type	1 Byte
(3) Ethernet Address	6 Byte
(4) Date		4 Byte
(5) Serial Number	3 Byte
(6) Checksum		1 Byte
(7) Reserved		16 Byte
------------------------------------------------------------


```


In detail:

(1) *Format*. The format of the ID PROM. 1 for now.

(2) *Machine Type*. A number specifying an implementation of the architecture.

(3) *Ethernet Address*. This is the unique 48-bit Ethernet address
    assigned by Sun to this machine. The Ethernet address stored in the ID PROM
    is the primary Ethernet address of the CPU, replacing and additional
    Ethernet addresses that might be stored on peripheral boards.

(4) *Date*. The date the ID PROM was generated.
    It is in the form of a 32-bit long word
    which contains the number of seconds since January 1, 1970.

(5) *Serial Number*. This is a 3-byte serial number.

(6) *Checksum*. The checksum is defined such that the longitudinal XOR
    of the first 16 bytes of the PROM including the checksum yields 0.

(7) *Reserved*. This is reserved for future expansion.

---

## Diagnostic Register


The diagnostic register drives an 8-bit LED display for
displaying error messages. Although the diagnostic
register is a word device, only bits 0 through 7 are
actually displayed.
A "0" bit written will cause
the corresponding LED to light up, a "1" bit to be dark.
Upon power-on-reset, the diagnostic register is initialized to 0
causing all LEDs to light up.
The no-fault state is defined to be all ones, with no LEDs light up.


```

Initialization:	none
------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
DIAGNOSTIC LED	0xA	WORD	WRITE-ONLY
------------------------------------------

```


---

## Bus Error Register


When a bus error occurs, the bus error register latches its cause to
allow software to identify the source of the bus error.
The bus error register always latches the cause of the most recent
bus error. In case of multiple bus errors, the information relating
to the earlier bus errors is lost.

The bus error register is a read-only register.
It is not initialized or cleared upon reset.
Without a precending bus error, the content of the bus error register
is undefined.


```


------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
BUS ERROR	0xC	WORD	READ-ONLY
------------------------------------------

```


The fields of the bus error registers are defined as follows:


```

BIT	NAME		MEANING
----------------------------------------------------------
    D0	PARERRL		Parity Error Low Byte
    D1	PARERRU		Parity Error Upper Byte
    D2	TIMEOUT		Timeout Error
    D3	PROTERR		Protection Error
    D4	(reserved)
    D5	(reserved)
    D6	BUSERROR	System Bus Error
    D7	PAGEVALID	1 => Valid Page, 0 => invalid page
    D8	(reserved)
  ..D15	(reserved)
----------------------------------------------------------

```


In more detail, the bus error conditions are as follows:


Page invalid (PAGEVALID=0) means that the page referenced did not
have a valid bit set.

Protection error (PROTERR) means that the page protection bits
or the PAGEVALID bit did not allow the kind of operation attempted.

Parity errors (PARERRL and PARERRU) can occur only on read cycles from
on-board memory (page type 0).
Since parity errors are detected too late in the cycle to abort
the current cycle, they abort the following cycle instead.
If the following CPU cycle does not recognize bus errors
then the parity error will abort the next cycle that does recognize bus errors.
CPU cycles that do not recognize bus errors include
CPU accesses to the MMU, interrupt acknowledge cycles, trap cycles,
and supervisor program accesses in boot state.
In any event, the address at which the CPU receives the bus error
is unrelated to the address of the parity error, which is not available.

Timeout results from a non-completed reference.
This can occur when accessing non-existent devices on cycles that
utilize a positive handshaking mechanism.
The bus error address can be used to determine which device did not respond.

Bus Errors occur on system bus accesses that are
aborted via a positive error mechanism.


---

## System Enable Register


The System Enable Register enables system facilities,
provides soft interrupts, and controls booting.
The System Enable Register can be read and written under software control
and is cleared on power up (hardware reset) and watchdog reset,
but not upon CPU reset.
Bits are assigned as follows:


```

Interrupt:	level 1, 2, and 3, Autovctor
Initialization:	cleared on power-up-reset
------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
SYSTEM ENABLE	0xE	WORD	READ/WRITE
------------------------------------------

```


The fields of the system enable register are as follows:


```

SYSTEM ENABLE REGISTER FIELDS
-----------------------------------------------------------
D0	EN.PAR		Enable Parity Generation
D1	EN.INT1		Autovector Interrupt on Level 1
D2	EN.INT2		Autovector Interrupt on Level 2
D3	EN.INT3		Autovector Interrupt on Level 3
D4	EN.PARERR	Enable Parity Error Checking
D5	EN.DVMA		Enable Direct Virtual Memory Access
D6	EN.INT		Enable all Interrupts
D7	BOOT* 		Boot State (0 => boot, 1 => normal)
D8..D15	Reserved
-----------------------------------------------------------

```


When cleared after power-up or watchdog reset, all bits are initialized to 0.
In this state, boot state is active, parity generation
and checking is disabled, DVMA, soft interrupts and all other
interrupts are disabled.

The EN.INT fields cause level interrupts.
That is, an interrupt request caused by an EN.INT bit
stays active until software clears the corresponding bit.

Upon Power-on Reset or Watchdog Reset, the system enable register is cleared,
forcing boot state active and disabling all interrupts and parity errors.
Boot state forces all supervisor program fetches to access the onboard
EPROM device independent of the setting of the memory management.
All other types of references are unaffected and will be mapped
as during normal operation of the processor.

---

# Device Space


Device space includes all the devices of the system
that are accessed through the memory management.

In the following, each device is described in terms of its
initialization, interrupts, exceptions, reference, and register mapping.

Not all devices are present in all implementations of the architecture.
Which devices are present and their physical addresses are
described in the implementation section for each machine type.

---

## Main Memory


The main memory device comprises the primary system memory.
Main memory is allocated at consecutive locations starting at 0.
Memory size ranges from a minimum of 1 Megabyte to a maximum of 8 Megabytes
in increments of 1 Megabyte.
Main memory is typically built with dynamic memories,
with memory refresh performed in hardware.


```

Exception:	Parity Error
Initialization:	Parity needs to be initialized in software
----------------------------------------------------------
REGISTER	ADDRESS		DATA		TYPE
----------------------------------------------------------
WORD 0x000000	0x000000	LWORD/WORD/BYTE	READ-WRITE
....
WORD 0x7FFFFE	0x7FFFFE	LWORD/WORD/BYTE	READ-WRITE
----------------------------------------------------------

```


Parity is initialized by setting the "parity generation" bit
in the system enable register and writing all of memory.
A Parity exception is caused if on a memory read cycle the
parity read is different from the parity written.


---

## Monochrome Video Memory


The monochrome video memory is a dual-ported memory.
One port performs video refresh, the second port provides processor access.


```

----------------------------------------------------------
REGISTER	ADDRESS		DATA		TYPE
----------------------------------------------------------
WORD 0x000000	0x000000	LWORD/WORD/BYTE	READ-WRITE
....
WORD 0x01FFFE	0x01FFFE	LWORD/WORD/BYTE	READ-WRITE
----------------------------------------------------------

```


This memory is mapped to the display screen as follows:

Data bit 15 of Word 0 is the first visible pixel in the upper left corner
of the display. Consecutive words are displayed along the horizontal scanline.
After <display-width> number of pixels have been displayed, the next word
is displayed at the beginning of the next horizontal line, up to <display-height>
number of lines. <display-width> and <display-height> are implementation constants.


```

 N = <display-width> / 16
 M = <display-height>

 15	       0 15	       0 15	      0	 15	       0
-----------------------------------------------------------------
| WORD 0	| WORD 1	|  ...		| WORD N-1	|
-----------------------------------------------------------------
| WORD N  	| WORD N+1	|  ...		| WORD 2*N-1	|
-----------------------------------------------------------------
| WORD 2*N  	| WORD 2*N+1	|  ...		| WORD 2*N-1	|
-----------------------------------------------------------------
|  ...	  	|   ...		|  ...		|    ...	|
-----------------------------------------------------------------
| WORD (M-1)*N	|   ...		|  ...		| WORD (M-1)*N-1|
-----------------------------------------------------------------

```


The frame buffer can be updated in two ways.
First, it can be read and written directly like memory.
As such, it is visible as a 128 KByte block of memory locations.
Second, the frame buffer can be written in copy mode
as a side-effect of writing into main memory.
This is achieved by selecting a base address and
setting the copy enable bit in the video control register.
The base address selects a 128K region of main memory.
Data written into this 128K region is also written into
the frame buffer at the same offset within the 128K region.

---

## Video Control Register


The video control register determines the operation of the video memory.
It has the following fields:


```

Initialization:	cleared on reset
Interrupt:	Level 4 Autovector
-----------------------------------------------------------
REGISTER		ADDRESS	DATA		TYPE
-----------------------------------------------------------
VIDEO CONTROL REGISTER	0	WORD/BYTE	READ-WRITE
-----------------------------------------------------------
BIT	NAME	MEANING
-----------------------------------------------------------
D0	RES	Reserved
D1..6	BASE	Copy memory base address A17..A22
D7	RES	Reserved
D8..11	CONFIG	Configuration Bits
D12	INT	Interrupt Pending (read-only)
D13	INTEN	Interrupt Enable
D14	COPYEN	Copy Enable
D15	DISPEN	Display Enable
-----------------------------------------------------------

```


*Base* selects the base address for the copy update mode.
The six bits of the base address correspond to physical address bits
A17 through A22. If the value of base matches the corresponding
physical address bits during a write operation and copy enable is active,
then a copy of the write data is stored in the frame buffer
at the physical address modulo 128 KByte.

*Configuration Bits* encode what display and what display resolution
is present in a given system. <THESE BITS NEED TO BE DEFINED>

*Interrupt Pending* indicates that a video interrupt has occured.
When enabled, it interrupts the CPU on level 4.
Video interrupt is set at the beginning of vertical retrace,
that is, when the scanning of a display field just completed.
The interrupt is cleared by momentarily turning off the interrupt enable bit.

*Interrupt Enable* allows video interrupts as described above.

*Copy Enable* enables the copy update mode to the frame buffer memory.

*Display Enable* turns on the video signal to the video monitor.


---

## EPROM


Device EPROM is a pair of 28-pin sockets for 64K, 128K, 256K, or 512K EPROMs.
Unlike all other devices, the EPROM is addressed directly
with the low-order non-translated (virtual) address bits from the CPU.
Thus, even though each 2K page must be enabled with its own entry
in the page map, the phyiscal page number in the page map is ignored
and the low-order bits of the virtual address are used instead.


```

Reference:	none
Interrupt:	none
Initialization:	none
-------------------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
-------------------------------------------------------
WORD 0		0	WORD	READ-ONLY
WORD 1		2	WORD	READ-ONLY
....
WORD 0x1FFF	0x3FFE	WORD	READ-ONLY	(2764s)
WORD 0x3FFF	0x7FFE	WORD	READ-ONLY	(27128s)
WORD 0x7FFF	0xFFFF	WORD	READ-ONLY	(27256s)
WORD 0xFFFF	0x1FFFF	WORD	READ-ONLY	(27512s)
-------------------------------------------------------

```


The EPROM device is also accessed in boot state.
In boot state, all supervisor program fetches are forced to fetch from
the EPROM device, independent of the setting of the memory management.

---

## Parallel Port


The parallel port is a non-latching 16-bit input port.
Since the input data is non-latched, the data may change
in the moment of being read. For best results, the data
should be reread until stable data is obtained.


```

Interrupt:	none
Initialization:	none
Reference:	none
------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
INPUT PORT	0	WORD	READ-ONLY
------------------------------------------

```


---

## Serial Port


Serial ports are implemented with the Zilog 8530 SCC
(serial communication controller).
The SCC features two high-speed, fully symmetrical and highly
programmable serial channels with built-in baud-rate generators.
The clock input to the SCC is a 4.9152 MHz clock, independent of the CPU clock.

The SCC is mapped as follows:


```

Interrupt:	Level 6 Autovector
Initialization:	Needs to be initialized in software
Reference:	Zilog 8530 SCC data sheet
Recovery Time:	1.6 microseconds
--------------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
--------------------------------------------------
CH B CONTROL	0	BYTE	READ/WRITE
CH B DATA	2	BYTE	READ/WRITE
CH A CONTROL	4	BYTE	READ/WRITE
CH A DATA	6	BYTE	READ/WRITE
--------------------------------------------------

```


---

## Keyboard/Mouse UART


These serial ports are implemented with the Zilog 8530 SCC
(serial communication controller).
The SCC features two high-speed, fully symmetrical and highly
programmable serial channels with built-in baud-rate generators.
The clock input to the SCCs is a 4.9152 MHz clock, independent of the CPU clock.
Control lines are not used.

The SCC is mapped as follows:


```

Interrupt:	Level 6 Autovector
Initialization:	Needs to be initialized in software
Reference:	Zilog 8530 SCC data sheet
Recovery Time:	1.6 microseconds
--------------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
--------------------------------------------------
CH B CONTROL	0	BYTE	READ/WRITE
CH B DATA	2	BYTE	READ/WRITE
CH A CONTROL	4	BYTE	READ/WRITE
CH A DATA	6	BYTE	READ/WRITE
--------------------------------------------------

```


---

## Timer


An AMD 9513 timer chip with five 16-bit timers is provided.
The clock input to the 9513 is a 4.9152 MHz clock, independent of the CPU clock.
The 9513 `GATE1` input is wired to the 9513 `FOUT` output.
The timer is mapped as follows:


```

Interrupt:	Level 7 for Timer 1, Level 5 for Timer 2 through 5, Autovector.
Initialization:	Internal Reset whenever power supply drops below 3.0V.
Reference:	AMD 9513 programming book
------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
TIMER DATA	0	WORD	READ/WRITE
TIMER COMMAND	2	WORD	READ/WRITE
------------------------------------------

```


Note the synchronization requirements of the 9513 timer.
Before writing into a counter, the counter's clock source must be
disabled first.

Initialization of the 9513 timer is special in that the chip
has an on-chip power-on reset that initializes the chip whenever
the power supply voltage is less than 3V. The chip is not affected
by power-on resets, watchdog resets, or CPU resets.

---

## Encryption Processor


The Encryption processor is an AMD 9518/8068
data ciphering processor providing high-speed NBS DES encryption.
To access an internal register in the 9518/8068, the address register
must be written first. Once the address register is setup,
the selected register can be accessed repeatedly.


```

Initialization:	none
Interrupts:	none
Reference:	AMD 9518/8068 data sheet.
Recovery Time:	1.6 microseconds
------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
DATA REGISTER	0	BYTE	READ/WRITE
ADDRESS REG.	2	BYTE	WRITE-ONLY
------------------------------------------

```


---

## Real Time Clock


The Real-Time Clock maintains time of day and a calendar.
A battery powers the clock when the main power is off.
The real-time clock is based on the National 58167 chip
which is addressed as 32 registers.


```

Initialization:	none
Interrupts:	none
Reference:	National Semiconductor 58167 data sheet.
------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
REGISTER 0	0	BYTE	READ/WRITE
REGISTER 1	2	BYTE	READ/WRITE
...
REGISTER 0x1F	0x3E	BYTE	READ/WRITE
------------------------------------------

```


---

## Ethernet Interface


The Ethernet Interface uses the Intel 82586 chip.
Configured in maximum mode, the 82586 can directly address
24-bits of virtual memory. When the 82586 becomes active,
it performs data read-write operations in supervisor mode.
82586 DVMA cycles must access main memory only.
If an error occurs during an 82586 DVMA operation,
the error bit in the Ethernet control register is set
and further activity is inhibited until the 82586 is reset.

The 82586 is connected to the system in a permanent byte-reversed mode,
i.e. 82586 bits 0 through 7 are connected to 68000 bits 8 through 15
and vice versa. This causes Ethernet data to be stored in memory
in CPU byte order, whereas 82586 control blocks in memory are byte swapped.

Overall operation of the Ethernet Interface is controlled
by the Ethernet control register that can be read or written in the
Ethernet page.


```

Initialization:	cleared on all resets
Interrupts:	Level 3, Autovector
Reference:	Intel 82586 data sheet.
------------------------------------------
REGISTER	ADDRESS	DATA	TYPE
------------------------------------------
CONTROL REG.	0	BYTE	READ/WRITE
------------------------------------------

```


The fields of the Ethernet control register are assigned as follows:


```


ETHERNET CONTROL REGISTER FIELDS
-----------------------------------------------------------
    D0	INT	Interrupt Pending (Read-Only)
    D1	ERR	Error Pending (Read-Only)
    D2	RES	Reserved
    D3	RES	Reserved
    D4	INTEN	Interrupt Enable
    D5	CA	Channel Attention
    D6	LOOPB*	0 => Loopback, 1 => Normal Operation
    D7	RESET*	0 => Ethernet Reset, 1 => Normal Operation
-----------------------------------------------------------

```


*INT* signals Interrupt from the 82586.
*ERR* indicates that a Bus Error occured during an 82586 channel operation,
inhibiting further channel activity. To reset the *ERR* condition, the
*RESET* bit in the Ethernet control register must be activated.
*INTEN* enables 82586 interrupts to the CPU.
*CA* signals channel attention to the 82586.
*LOOPB** controls whether the front-end encoder/decoder is configured
in loopback mode (LOOPB* = 0) or connected to the transceiver cable (LOOPB* = 1).
*RESET* initializes the 82586 when active (RESET* = 0) and allows
normal operation when inactive (RESET* = 1).
It also clears the *ERR* condition when active.

---

## Multibus Interface


The Multibus interface is dual-ported with a
Multibus Master Interface from the CPU to the Multibus
and a Multibus Slave Interface from the Multibus to the CPU.


### Multibus Master Interface


```

Initialization:	Processor Reset causes Multibus INIT
Interrupts:	Level 1 through 7, Autovector
Exceptions:	Timeout after 100 microseconds
Reference:	Intel Multibus Specificaton
--------------------------------------------------
LOCATION	ADDRESS	DATA		TYPE
--------------------------------------------------
MULTIBUS MEMORY
--------------------------------------------------
WORD 0		0	WORD/BYTE	READ/WRITE
WORD 2		2	WORD/BYTE	READ/WRITE
...
WORD 0xFFFFE	0xFFFFE	WORD/BYTE	READ/WRITE
--------------------------------------------------
MULTIBUS I/O SPACE
--------------------------------------------------
WORD 0		0	WORD/BYTE	READ/WRITE
WORD 2		2	WORD/BYTE	READ/WRITE
...
WORD 0xFFFFE	0xFFFFE	WORD/BYTE	READ/WRITE
--------------------------------------------------

```


Byte transfers to and from the Multibus are performed
in 680X0 Byte order. Word transfers are not affected.


### Multibus Slave Interface


The Multibus Slave Interface causes a range of Multibus memory addresses
to be treated as though they were a range of virtual addresses
generated by the processor.
Multibus addresses 0..256K bytes in memory space
are mapped to the low-order 256K bytes
of the top 1 MByte of the system context virtual address space.
Multibus DVMA is enabled under software control via
the DVMA enable bit in the system register.
Only transfers to main memory are allowed.


```


P1-Address		Virtual Address
----------------------------------------
[0x00000..0x3FFFE]	[0xF00000..0xF3FFFE]


```


Multibus DVMA cycles can fail for two reasons:
protection error and parity error (on read cycles).
The error is signalled to the controlling Multibus master
by inhibiting the data transfer acknowledge (DTACK)
forcing a timeout exception.
It is recommended that the timeout period of DVMA masters
be as short as possible because on-board operation cannot proceed
until the DVMA master ends the bus cycle.
In order to guarantee real-time response, DVMA masters should
provide timeout periods in the range of tens of microseconds.


---

## VME Bus Interface


The VME-Bus interface is dual-ported with a
VME-Bus Master Interface from the CPU to the VME-Bus
and a VME-Bus Slave Interface from the VME-Bus to the CPU.


### VME-Bus Master Interface


```

Initialization:	Processor Reset causes VME-Bus INIT
Interrupts:	Level 1 through 7, Vectored
Exceptions:	Timeout after 200 microseconds
Reference:	Motorola VME-Bus Specificaton
----------------------------------------------------------
LOCATION	ADDRESS		DATA		TYPE
----------------------------------------------------------
VME-Bus 24-bit Address Space
----------------------------------------------------------
WORD 0		0		WORD/BYTE	READ/WRITE
WORD 2		2		WORD/BYTE	READ/WRITE
...
WORD 0xFEFFFE	0xFFFFE		WORD/BYTE	READ/WRITE
----------------------------------------------------------
VME-Bus 16-bit Address Space
----------------------------------------------------------
WORD 0		0xFF0000	WORD/BYTE	READ/WRITE
WORD 2		0xFF0002	WORD/BYTE	READ/WRITE
...
WORD 0xFFFE	0xFFFFFE	WORD/BYTE	READ/WRITE
----------------------------------------------------------

```


### VME-Bus Slave Interface


The VME-Bus Slave Interface causes a range of VME-Bus memory addresses
to be treated as though they were a range of virtual addresses
generated by the processor.
VME DVMA responds to the most significant 1 MByte of the VME-Bus
24-bit physical address space. This space is mapped to the most-significant
1 MBytes of the system context virtual address space.
VME-Bus DVMA is enabled under software control via
the DVMA enable bit in the system register.
Only transfers to main memory are allowed.


```


P1-Address		Virtual Address
----------------------------------------
[0xF00000..0xFFFFFE]	[0xF00000..0xFFFFFE]


```


VME-Bus DVMA cycles can fail for two reasons:
protection error and parity error (on read cycles).
The error is signalled to the controlling VME-Bus master
by asserting VME Bus Error.

---

# Implementation Information for Machine Type 1


Machine Type 1 is the Multibus or IEEE-796 Bus implementation of the architecture.


## MMU Implementation


The Version-1 Architecture implements a page number field that stores 12 bits.
It thus supports a physical address of 23 bits, capable of addressing 8 MBytes.
The other physical address bits in the page map are not implemented.
When read, the not implemented bits are not defined.


## Device Space Physical Addresses


The decoding of the page type field is described in the table below,
together with the number of address bits the page types use or decode.


```


Type	Address		Device				Wait States
------------------------------------------------------------------------------
0	23-bit		On-Board RAM

	[0x000000]	Physical Memory	1..4 MBytes	0
	[0x700000]	BW-Frame Buffer			0 (Write), 4..8 (Read)
	[0x780000]	Keyboard/Mouse UART		0 (Write), 4..8 (Read)
	[0x780800]	Sound Generator			0 (Write)
	[0x781800]	Video Control Register		0 (Write), 4..8 (Read)

------------------------------------------------------------------------------
1	14-bit		On-board I/O

	[0x000000]	EPROM				1
	[0x000800]	RESERVED			1
	[0x001000]	ENCRYPTION PROCESSOR		1..5
	[0x001800]	PARALLEL PORT			1
	[0x002000]	SERIAL PORT			1
	[0x002800]	TIMER				1
	[0x003000]	RASTEROP PROCESSOR		1
	[0x003800]	REAL-TIME CLOCK			4..8
------------------------------------------------------------------------------
2	20-bit		P1-Bus Memory

	[0x000000]	0..1 MByte 796-Bus Memory Space	2 + device access time
------------------------------------------------------------------------------
3	20-bit		P1-Bus I/O

	[0x000000]	0..1 MByte 796-Bus Memory Space	2 + device access time
------------------------------------------------------------------------------
			Accesses to the Multibus incur an additional 2 wait states
			access time if the bus mastership must be acquired.

```


---

## Performance Data


### CPU Speed


```


CPU clock cycle:	101.72 nsec (9.8304 MHz)
CPU basic cycle:	406.90 nsec


```


### Video Memory Access Time


Write accesses to the video memory are buffered.
Thus a single write will complete without wait states.
A subsequent operation, whether read or write, will have to wait
until the frame buffer has completed the requested operation.
Write accesses to the video memory via the copy mode will cause the
same behavior as direct write accesses.
Read accesses to the video memory are not buffered and must wait
until the cycle completes.


### Multibus Access Times


This section describes the access times of the Multibus.
Multibus I/O devices are identical to Multibus Memory
except that they are located in a separate address space.

The timing of Multibus accesses depends on two factors:
the access time of the Multibus device and the cost of Multibus acquisition
if the Sun-2 Processor currently does not own Multibus mastership.
Once Multibus mastership is acquired it is retained
and given up only on demand if another master requests it.

The total number of wait states for a Multibus access can be computed
by the following formula:

2 WS (overhead) + 3 WS (if board is currently not Multibus master) +
access time of Multibus device divided by the clock period of the CPU
rounded up to the nearest integer number.

Another limitation on Multibus access time is cycle time.
Some Multibus devices have slower cycle times
than access times which will increase effective access time
in cycle-time limited transfers.


### Multibus DVMA Access Time


DVMA cycles from the Multibus are serviced after the current CPU cycle
completes and after pending memory refresh cycles are executed.
Thus DVMA cycles exhibit a variable access time that ranges from
0.7 microseconds in the best case to 1.5 microseconds worst case
with an average of about 1.0 microseconds.

After a DVMA cycle has executed, a CPU cycle will start
before another DVMA cycle is granted. This means that the cycle time
for DVMA is one DVMA cycle plus at least one CPU cycle.
Thus the DVMA cycle time will be in a range of 1.1 to 1.9 microseconds
with an average of 1.4 microseconds,
as long as the DVMA master can generate transfers at this rate.

---

# Implementation Information for Machine Type 2


Machine Type 2 is the VME-Bus implementation of the architecture.


## MMU Implementation


The MMU of this machine type implements a page number field of 12 bits.
It thus supports a physical address of 23 bits, capable of addressing 8 MBytes.
The other physical address bits in the page map are not implemented.
When read, the not implemented bits are not defined.


## Physical Address Assignments


```


Type	Address		Device				Wait States
------------------------------------------------------------------------------
0	23-bit		Memory Bus

	[0x000000]	Physical Memory	1..8 MBytes	0
------------------------------------------------------------------------------
1	23-bit		I/O Bus

	[0x000000]	BW-Frame Buffer			1 (Write), 4..8 (Read)
	[0x020000]	Video Control Register		2

	[0x7F0000]	EPROM				2
	[0x7F0800]	Ethernet Interface		2
	[0x7F1000]	Encryption Processor		2..8
	[0x7F1800]	Keyboard/Mouse Interface	2
	[0x7F2000]	Serial Port			2
	[0x7F2800]	Timer				2
	[0x7F3000]	Reserved			2
	[0x7F3800]	Reserved			2
------------------------------------------------------------------------------
2	23-bit		P1-Bus or System Bus

	[0x000000]	0..8 MByte VME 24-bit address	1 + device access time
------------------------------------------------------------------------------
3	23-bit		P1-Bus or System Bus

	[0x000000]	8..16 MByte VME 24-bit address	1 + device access time
	[0x7F0000]	64 KByte VME 16-bit address	1 + device access time
------------------------------------------------------------------------------
			Accesses to the VME-Bus incur an additional 2 wait states
			access time if the bus mastership must be acquired.

```


---

## Performance Data


### CPU Speed


```


CPU clock cycle:	101.72 nsec (9.8304 MHz)
CPU basic cycle:	406.90 nsec


```


### Video Memory Access Time


Read accesses are unbuffered and will cause 4 to 8 wait states.
Write accesses to the video memory are buffered.
However, subsequent read or write accesses will have to wait
until the video memory has completed the requested operation.
Write accesses to the video memory via the copy mode will cause the
same behavior as direct write accesses.


### P1-Bus Access Times


This section describes the access times of the P1-Bus.
The time to complete a P1-Bus access consists of three elements:
overhead, the cost of P1-Bus acquisition if the 2050 Board
is not currently P1-Bus master,
and the actual access time of the P1-Bus device.

The total number of wait states for a P1-Bus access can be computed
by the following formula:

1 WS (overhead)
+ 2 WS (bus acquisition time if board does not have bus mastership and bus is idle)
+ access time of P1-Bus device divided by the clock period of the CPU
rounded up to the nearest integer number.


### DVMA Access Time


DVMA cycles from the P1-Bus are serviced after the current CPU cycle
completes and after pending memory refresh cycles are executed.
Thus DVMA cycles exhibit a variable access time that ranges from
0.7 microseconds in the best case to 1.5 microseconds worst case
with an average of about 1.0 microseconds.

After a DVMA cycle has executed, a CPU cycle will start
before another DVMA cycle is granted. This means that the cycle time
for DVMA is one DVMA cycle plus at least one CPU cycle.
Thus the DVMA cycle time will be in the range of 1.1 to 1.9 microseconds
with an average of 1.4 microseconds,
as long as the DVMA master can generate transfers at this rate.


### P1-Bus Reset


The 2050 Board can be configured either as a P1-Bus Reset Master or Slave.

As a P1-Bus Reset Master, the 2050 Board issues Reset to the VME Bus.
Power-On Reset, Watchdog Reset, and 68010 Reset will all assert P1-Bus Reset.
Other P1-Bus devices may also assert P1-Bus Reset, but this will have
no effect on the on-board CPU and devices.

As a P1-Bus Reset Slave, the 2050 Board receives Reset from the VME Bus,
but does not drive Reset to the VME Bus. The VME Bus Reset
has the same effect as an on-board power-on-reset.
