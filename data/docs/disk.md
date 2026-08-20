# disk.mss

SUN SMD DISK CONTROLLER

Design Philosophy:

	Keep it as simple as possible to reduce design time and cost

	Make it as fast as possible: handle up to 3 Mbyte disk transfers
	and up to 4 MByte Multibus transfers

	Allow up to 2 disk drives via one 40 pin connector

	Make it failsafe: Handle Firecodes and Header CRC on board
	Be able to read raw data back

	Make operations at the single sector level

	Be able to chain sector operations without delay.

	If there is space, add a tape interface (to be defined)

****	Be compatible with variable levels of SMD interface

****	Have three queues: disk0, disk1, and tape

Design Constraints:

	Size: Multibus format, possibly VME bus format

	Chipcount: less than 100 chips

	Power: 5V only, allow space for -5V power converter.


Host Interface / Dual Port Buffer:

	Dual Port High Speed Buffer: 16 16k*1 RAMs (16 kWord/32 kByte)
	Allow 64k Byte highspeed RAM if PCB space allows.

	Buffer looks like normal memory to Multibus.
	Can be used by other DMAs. Allow Byte/Word accesses.

	Queues for IOPB blocks are maintained in buffer starting at 0

	Dual port buffer timesliced between controller and Multibus

	Controller can preempt host by requesting buffer access
	one cycle before doing access

	Status and Interrupt Register is in Dual Port Buffer at location 0.


Tape Interface

	Add provision for streamer tape parallel port interface.

---
Input/Output Parameter Block (IOPB):

	Command Code/Return Code	8 bit/8 bit
	Unit/Cylinder Select		4 bit/12 bit
	Head/Sector Select		8 bit/8 bit
	Word Pointer to Buffer		16 bit

IOPB Chaining:

	IOPBs are executed sequentially in a cyclical fashion.
	Consecutive IOPBs referring to consecutive sectors can be
	executed without skipping a disk sector (interleaving).
	Multisector transfers are accomplished by setting up multiple IOPBs.


Interrupt Mechanism

	The disk controller communicates with the host CPU via interrupt.
	Interrupt level is programmed in hardware with switch select.
	Alternatively, all interrupt sources can be polled in software.
	Interrupts are cleared by resetting the corresponding bits.
	The time from clearing the bits until the hardware interrupt
	actually goes away will be about 10 usec.

	Interrupt enable register (per unit)

		Enable controller
		Interrupt when Disk Status Byte 0 changes
		Interrupt when command completed with interrupt request.

	Interrupt register (per unit)

		Disk Status changed
		Command compeleted

Disk Status Block

	Starting at location 0 is disk status, including disk error status.

		Tag Byte 0, Tag Byte 1
		Tag Byte 2, Tag Byte 3
		Unit/Cyclinder Limit
		Head/Sector Limit


Controller Status

	The disk controller maintains a pointer to the head of the
	IOPB queue for each drive.

		Pointer to Head of IOPB queue

	Pointer can be reset by RESET Controller command.

---
Commands: (4 bits)

Housekeeping Commands

	Noop

	Reset (Drive Clear)

	Release (Dual Port Drive)

Positioning Commands

	Seek

	RTZ (Return to Zero)

Data Transfer Commands (All commands have implied Seek)

	Read Data	("Check Header")

	Write Data	("Check Header")

	Read Header	("Verify Format")

	Write Header	("Format")

	Read Sector	(Header, CRC, Data, and ECC)	("Diagnostic")

	Write Sector	(Header, CRC, Data, and ECC)	("Diagnostic")

	Read All	(0, Sync, Header, CRC, 0, Sync, Data, and ECC)

	Write All	(0, Sync, Header, CRC, 0, Sync, Data, and ECC)


The last two functions allow access to entire sectors, no matter what
the header, CRC, or ECC is. The write Sector command allows to write
all fields, including CRC and ECC, for diagnostic purposes.


Command Bits:

	Interrupt when done

Status associated with command/return code

	Go Bit		(Command block setup, committ to transaction)
	Active Bit	(Command in progress)
	Done Bit	(Command completed)
	Error Bit	(Command status)


---
Return Code / Error Codes

	Done

Error Bits:

	Correctable ECC error

	Uncorrectable ECC error

	Header CRC Error

	Disk Error (see next page)

	No Index Pulse (Timeout)

	No Sector Pulse (Timeout)

	No Header Field (Timeout)

	No Data Field (Timeout)

	Invalid Sync in Header Field

	Invalid Sync in Data Field


Bounds Checking (This could be left out)


	Invalid Command Code	Command Code > Command Code Limit

	Invalid Unit		Unit Select > Unit Select Limit

	Invalid Head		Head Select > Head Select Limit

	Invalid Track		Track Select > Track Select Limit

	Invalid Sector		Sector Select > Sector Select Limit

---
Errors: Disk Unit Status

Disk Unit Status is status or error information respective to a particular disk.
The status is checked before a read/write operation to see whether any
error bits are present. If an error is present, the operation requested
and any further operations are aborted via DONE DISK ERROR flag.
The device driver has to examine the cause of the disk error
and initiate corrective action.
Check the disk manufacturer manuals for further information on the error bits.

Disk Unit Status is updated on every command, including NOOP.


   Byte 0 corresponds to TAG4=0 and TAG5=0 status word from disk

	0 - Unit ready
	1 - On Cylinder
	2 - Seek Error
	3 - Fault (see Read/Write Check below)
	4 - Write Protected
	5 - Address Mark Found
	6 - Index Pulse
	7 - Sector Pulse

   Byte 1 corresponds to TAG4=1 and TAG5=0 status word from disk

	0 - Sector 1
	1 - Sector 2
	2 - Sector 4
	3 - Sector 8
	4 - Sector 16
	5 - Sector 32
	6 - Sector 64
	7 - Sector 128

   Byte 2 corresponds to TAG4=0 and TAG5=1 status word from disk

	0 - Index Check
	1 - Control Check
	2 - Multi Head Check
	3 - Head Short Check
	4 - Write Current on Read Check
	5 - Write Transition Check
	6 - Delta I Write Check
	7 - Servo Off-Track

   Byte 3 corresponds to TAG4=1 and TAG5=1 status word from disk

	0 - DE Sequence Check
	1 - Access Timeout Check
	2 - Overshoot Check
	3 - Rezero Mode Latch
	4 - Servo Latch
	5 - Linear Mode Latch
	6 - Control Latch
	7 - Wait Latch


---
Disk Formatting

Make it DEC media compatible with RM02

   - Allows dual port disk structure to VAX
   - Allows media exchange between VAX and SUN
   - allows formatting, backup, and disk boot via VAX.

Issues:

   - Track efficiency of DEC format is only 81%.
   - Check byte order in DEC format.
   - Bad sector and bad track mapping can vary from drive to drive.
   - Make sure fields are plenty, in particular Cylinder Field


---
DEC Disk Format:

	Sector Gap				29 Byte	232 Bit

		All Zeros		14 Word	28 Byte	224 Bit
		Sync			0.5 W	1 Byte	8 Bit

	Header				3 Word	6 Byte	48 Bit

		Cyclinder Address	1 Word	2 Byte	16 Bit
		Sector/Track Address	1 Word	2 Byte	16 Bit
		CRC Word		1 Word  2 Byte	16 Bit

	Header Gap				18 Byte	144 Bit

		All Zeros			17 Byte	136 Bit
		Sync				1 Byte	8 Bit

	Data	256 Words at 16 Bit	256 W	512 Byt	4096 Bit

	ECC	32 Bit			2 Word	4 Byte	32 Bit

	Data Gap

		All Zeros		1 Word	2 Byte	16 Bit
		Undefined			59 Byte	472 Bit

	Total				315	630	5040

	Efficiency	(512/613)		81.26%


Description of Fields:

    Sync Byte

					0   0   0   1   1   0   0   1

    Cylinder Address

	MF  UF  0   FMT 0   0   CY9 CY8 CY7 CY6 CY5 CY4 CY3 CY2 CY1 CY0

    Sector/Track Format

	0   0   0   TA4 TA3 TA2 TA1 TA0 0   0   0   SA4 SA3 SA2 SA1 SA0


	FMT	sector format
		- 1 indicates 16 Bit format
		- 0 means 18 Bit

	UF	user bad sector indicator
		- 0 sector BAD
		- 1 sector GOOD

	UF	manufacturer bad sector indicator
		- 0 sector GOOD
		- 1 sector BAD

---
Two Drives

	Have "per drive" status

	Maintain independent queues per drive

	Maintain MPS (Multiple position sensing)

---
Multiport drives

	Would be nice to use VAX UNIX file system

	Allow access to same disks from two controllers for reliability

	Understand protocol and additional commands

---
Microcode Tasks

    INIT

	On power up, clear enable register, queue pointer, disk drive.

    Interrupt Watch (every 10 usec or so for both drives)

	Copy the bits from the interrupt register in the dual port buffer
	into the actual interrupt flipflop

    Index Pulse (every 16.6 msec or so for both drives)

	Update MPS. Reset Sector count to 0.

    Sector Pulse (every 500 usec or so for 32 sectors, both drives)

	Increment sector count.
	If not transferring, check for transfers to be done.

    Command Loop

	In Idle State, Wait for GO bit at head of queue.
	If GO bit then
	    update/check disk status.
	    decode command.
	    cause implied seek.
	Setup Data Transfer by
	    precomputing CRC for Header
	    Set state to transfer ready.

    Read Data Transfer

	Check Disk Status.
	Compare Sync, Head, and CRC with precomputed values.
	Wait for Data Sync.
	Read Data field.
	Check ECC. If ECC fails, goto ECC error correction.

    Write Data Transfer

	Check Disk Status.
	Compare Sync, Head, and CRC with precomputed values.
	Wait for Data Sync.
	Enable Write Gate.
	Write Data field.
	Append ECC.

    Read Header Transfer

    Write Header Transfer

    Read Sector Transfer

    Write Sector Transfer

---
Issues:

	Linked Queue structure for IOPBs
	Circular
