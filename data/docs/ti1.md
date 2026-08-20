---


---


# Sun 1/4" Tape Interface


# User Manual


Sun Microsystems Inc.

December 1982


>
The Sun 1/4" Tape Controller Board consists of 256K bytes of multibus memory
and an interface between the Intel Multibus and Archive`s QIIC (Quarter Inch
Intelligent Control) bus. The board can be depopulated to remove either the
tape interface and/or 128K bytes of memory.

This document describes the architecture, programming,
and the installation of the Sun 1/4" Tape Interface Board.


>
Multibus is a trademark of Intel Corporation.


---


---

# System Architecture


## Features


128K or 256K bytes of multibus memory with parity.
Memory addressable as bytes or words.

QIIC (Quarter Inch Intelligent Control) Interface for driving 1/4" Streaming
Tape Drives offered by Archive and Cipher

90 inch per second, 8000 BPI Tape Operation.

Handles 20MB or 45MB streaming tapes transparently to both software and hardware.

Single board compatible with IEEE-796 Bus/Intel Multibus

5V only operation.


## Overview


The Sun 1/4" Streaming Tape Interface brings low-cost and high-speed system
backup capabilities to IEEE-796/Intel Multibus based systems.
In addition, the board can optionally contain upto 256K bytes of
parity-checking multibus memory for use by any devices on the system requiring
DMA.

The Sun 1/4" Tape Interface can be used for bootstrapping an operating
system, receiving Sun software distributions, and performing system backup.

---

## Introduction


This chapter provides an overview of the architecture of the Sun 1/4" tape
interface board and the Archive streaming tape drive.


## Memory Architecture


The memory portion of the PC card supports 128K or 256K bytes of parity
checking ram. For configuration information, look at the section titled
'Switch Settings' in chapter three.

Parity can be selectively enabled or disabled by writting to the appropriate
register in I/O address space. The value of the parity-enable bit can be read
or written. A programmable parity enable/disable is invaluable for diagnostics
attempting to pin-point faulty 64K rams. On power-up, parity is always enabled, so
the parity disable feature can ignored by all system software except diagnostics.

Parity is not a component of the IEEE-796 bus. For this reason, parity errors
are effected by inhibiting transfer acknowledge (Pin #23 on the bus),
thus causing a timeout.


---

## Archive Tape Drive Architecture


The Archive tape drives stream at 90 inches per second and pack 8000 bits
per inch to give a 90K byte per second data storage rate.
To acheive this storage rate, inter-record gaps are virtually eliminated
to allow constant tape motion. This tradeoff means that the ability to
start and stop between individual records is lost, and hence, the drive
can not backspace a record at a time.
However, the following commands can be performed:


```

	Tape drive select
	Read status
	Rewind tape
	Retense tape
	Erase tape
	Write
	Read
	Write file mark
	Read file mark

```


To minimize the host`s overhead interfacing to the drive and to ensure that
at least an entire 512-byte block of data is ready for transfer, the Archive
tape drive contains three 512-byte data buffers.
On read, the drive signals when a block is ready. At this point, the processor
can transparently read from the first buffer while the second and third buffers
are being filled.
On write, when a buffer has been filled, the drive begins to write that block,
and the processor can begin filling another buffer. If the next buffer is not
ready in time, the drive will rewrite the previous block to allow the tape
to continue streaming. If the next block is still not ready, the drive will
rewind ten blocks and will take a running start to write the next block.

The read status command is quite extensive, and the drive
goes to great lengths to
ensure data integrity. Each block is given a standard address and CRC field,
and on writes, one of the data buffers is reserved for reading the block from
tape immediately after it is written. At the end of a block transfer, if the
block read does not match the block written, the block is rewritten and the
previously written block is flagged as invalid.

The Archive tape drives use a serpentine recording technique. In this method,
the drive writes a serial data stream from the start to the end of the tape,
and then turns around and writes a second serial data stream from the end
to start of the tape at position slightly higher or lower on the tape. This
technique reduces the amount of time required to rewind a tape, and it allows
the 20MB versions of the drive to be compatible with 45MB versions of the
drive. Tapes written with the 20MB drives can be read by the 45MB drives;
although tapes written with the 45MB drives can not be reliably read by the
20MB units.
The 20 MB drive uses four serpentine tracks; the 45MB drive uses nine
serpentine tracks.

---

## Hardware/Software Interface


The Sun 1/4" Tape Controller minimizes hardware complexity while attempting
to maximize tape throughput.

The tape controller board consists of three registers. There is a write control
register, a read control register, and a data register. All registers can be
read and written.

The control bits on the QIIC (Quarter Inch Intelligent Control) bus are:

```

	ONLINE
	REQUEST
	XFER
	RESET
	READY
	EXCEPTION
	ACKNOWLEDGE
	DIRECTION

```


The first four bits on the QIIC-bus are output to the tape drive
from the write control register, and the
second four bits are received from the drive and are part of the
read control register. Except during burst mode
data transfers, the above bits must be
explicitly twiddled by software drivers.

On command transfers between the host and the tape, the signals REQUEST and
READY are used for hand-shaking. Features such as the variability of the READY
signal and the requirement that REQUEST is asserted for at least 20 usec make
the transfer of commands more suitable for software rather than hardware.
Typically, commands are issued very infrequently.
For instance, a read or write
command must only be issued after reading or writting an EOF mark, so the
processor overhead in twiddling these control bits is minimal.

On data transfer commands, however, a data byte can be transfered upto every
560 nsec. Handshaking for data bytes uses the XFER and ACKNOWLEDGE bits, and
contol of the XFER bit is handled by the board in burst mode. Burst mode is
entered by setting the burst mode bit in the write control register. If that
bit is not set, the XFER bit in the write control register is output onto the
QIIC bus and data transfers can be controlled via software.
In normal use, however, a read or write command will be issued to the drive, the
burst mode bit will then be set, 512 consecutive data reads or writes
will be performed, and then the burst mode bit will be cleared.

During burst mode, or any other time for that matter, reads and writes from
the control
registers can interspersed with accesses to the data register. One problem with
with burst mode transfers, however,
is that the controller board has no way of telling
if the tape cable is accidentally unplugged during the middle of a data
transfer. If this happens, or if some catastrophic hardware failure in the
tape drive occurs, the tape subsection of the board may hang trying to transfer
the next data byte to or from the tape. If the board is waiting for an
ACKNOWLEDGE from the drive, all subsequent accesses to the control or data
registers will cause a multibus timeout. To clear this state, writing to the
soft reset address on the board will simulate a data transfer acknowledge.
The burst mode bit can now be cleared in the write control register, and the
software driver can now attempt a read status command to determine the cause
of the problem.


---


## References


```

Archive Corporation. Product Description and User's Manual.

Ciper Data Products Inc. "Series 400 Quarterback Cartridge Tape Drive
	Product Description". April 1982.

```


---

## Specification Summary


**Tape Controller**

```

	Occupies 8 bytes of I/O address space
	Controls QIIC interface (Archive and Cipher 1/4" Streaming Tapes)
	Handles 20MB or 45MB version of drive

```


**Tape Access Characteristics**

```

	One data byte every 560 to 1200 nsec.
	Access time less than 100 nsec once cycle time of 560-1200 nsec exceeded.

```


**Memory Subsection**

```

	Completely independent of tape
	Hardware refresh
	Four wait-state memory (Upto seven wait-states if refresh in progress)

```


**796-Bus Compatibility**

```

	D16 M20 VOL, 8 or 16-bit data to/from memory.
	D8  M20 VOL, to/from tape interface.

```


**Electrical Characteristics**

```

	+ 5V +- 10%.  Maximum current: 2 A.

```


**Physical Characteristics**

```

	Width: 12.00 in. (30.48 cm)
	Height: 6.75 in. (17.15 cm)
	Depth:  0.50 in. (1.27 cm)

```


**Environmental Characteristics**

```

	Operating Temperature: 0-55 C

```


---

# Programming the SUN 1/4" Tape Controller


This section provides detailled programming information about the
Sun 1/4" tape controller board.


## Initialization


The multibus INIT\ signal causes the board to initialize itself. The signal
enables parity detection on the memory, disables interrupts, and clears
the burst mode data transfer request flip-flop.
The hardware INIT\ does not perform a complete reset of the board. To
effect a complete reset, certain software steps must be performed.

First, the entire memory array must be filled with dummy data to initialize
the parity information on each byte, and the system may also wish to disable
parity checking. Next, to initialize the tape, the write control
register must be cleared before *any* access is made to the data register;
clearing the write control register takes the board out of burst mode operation.
Finally, the software must permanently reenable interrupts by
asserting the bit CATCH_EDGE_OF_READY in the write control register.
The memory and tape interface are now initialized.


---

## Registers and Bit Assignments


A description of the registers on the tape controller and their
offset from the base address of the device are given herein.
Note that all bits on the contoller board are active high whereas all bits
described in the Archive and Cipher manuals are active low.
In the following table,
address offsets 0, 2, 4, and 6 are ignored on writes and return garbage on
reads. The most significant bit is bit 7; the least significant bit is bit 0.


```


Address   Function
-------   --------
0x0001	  8-Bit Data Port. Used for transferring commands and data to the
	  tape unit. Readable and Writeable.

0x0003    Write Control Register. Readable and Writeable.
		Bit 0  ONLINE. Output directly onto QIIC interface bus.
		Bit 1  REQUEST. Output directly onto QIIC interface bus.
		Bit 2  RESET. Output directly onto QIIC interface bus. Recalibrates
		       heads on tape drive, and rewinds tape.
		Bit 3  XFER. Output directly onto QIIC interface bus only if
		       'Burst' bit is deasserted.
		Bit 4  BURST. When true, controller board handles all `Xfer' and
		       'Acknowledge' handshaking with the tape drive.
		Bit 5  CATCH_EDGE_OF_READY. This bit serves two functions. First,
		       after a reset, deasserting then asserting this bit will
		       permanently reenable interrupts. Next, this bit is used
		       to set a flag when 'Ready' goes from deasserted to asserted.
		       When this bit is off, the bit 'Edge_Of_Ready' is also off.
		       When this bit is set, the next time the tape drive changes
		       'Ready' from deasserted to asserted, 'Edge_Of_Ready' will
		       be asserted and will stay asserted until cleared by resetting
		       'Catch_Edge_Of_Ready'.
		Bit 6  INTERRUPT_ON_EXCEPTION. Generate interrupt if 'Exception`
		       true.
		Bit 7  INTERRUPT_ON_READY. Interrupt if 'Edge_Of_Ready' asserted.

0x0005    Read Control Register. Only bit 'Parity_En' writable.
		Bit 0  READY. Input from QIIC interface bus.
		Bit 1  DIRECTION. Input from QIIC interface bus.
		Bit 2  EXCEPTION. Input from QIIC interface bus.
		Bit 3  ACKNOWLEDGE. Input from QIIC interface bus.
		Bit 4  EDGE_OF_READY. Asserted if 'Catch_Edge_Of_Ready' is asserted
		       and 'Ready' has gone from deasserted to asserted since we
		       asserted 'Catch_Edge_Of_Ready'.
		Bit 5  INTERRUPT. True if this device is currently interrupting.
		Bit 6  unused.
		Bit 7  PARITY_ENABLE. Readable and Writeable. Enables/Disables
		       parity checking on reads from the memory section of the
		       board. Parity is always generated on writes.

0x0007    On write, performs a phony burst mode data transfer acknowledge. If the
	  cable to the tape drive is removed during a burst mode data transfer,
	  or if software erroneously sets the burst mode bit and then accesses
	  the data register, the 1/4" tape interface will cause a bus timeout
	  on all accesses to it (The memory is not affected). To clear this
	  state any byte value must be written to this address, and the burst mode
	  bit must be deasserted before another access is made to the data register.
	  Reading from this address returns garbage and will cause a timeout if
	  the tape interface is hung.


```


---

## Tape Drive Commands


The following table defines the commands that the 1/4" tape drive will
accept. Use
of any command not listed in this table will cause the tape drive to assert
EXCEPTION and otherwise ignore the issued command.

**Command Set Summary**


                				BIT PATTERN
						-----------
						MSB     LSB
	COMMAND				HEX	 7654 3210
	-------				---	-----------
	SELECT DRIVE 0			 01	 0000 0001
	SELECT DRIVE 1			 02	 0000 0010
	SELECT DRIVE 2			 04      0000 0100
	SELECT DRIVE 3			 08      0000 1000

	SELECT DRIVE 0, LIGHT LED	 11	 0001 0001
	SELECT DRIVE 1, LIGHT LED	 12	 0001 0010
	SELECT DRIVE 2, LIGHT LED 	 14      0001 0100
	SELECT DRIVE 3, LIGHT LED	 18      0001 1000

	REWIND TAPE			 21      0010 0001
	ERASE TAPE			 22	 0010 0010
	RETENSE TAPE			 24      0010 0100

	WRITE DATA			 40 	 0100 0000
	WRITE FILEMARK			 60	 0110 0000

	READ DATA			 80	 1000 0000
	READ FILEMARK			 A0	 1010 0000

	READ STATUS			 C0	 1100 0000


---

## QIIC-Bus Timing Diagrams


This section contains the timing diagrams for all possible commands to the
Archive Streaming Tape Drives. These timing diagrams can also be found in the
Archive or Cipher product description manuals.

All of the protocol and timing requirements described here must be met by
software, except the handshaking of XFER and ACK during burst mode transfers.
The burst mode bit in the write control register should be cleared at all times
except when transferring a data block (i.e. times T9-T18 of the write data
diagram or times T10-T20 of the read data diagram).

**Reset Timing**


---
**Read Status Timing**


---
**Tape Select Timing**


---
**Positioning Command Timing**


---
**Write Data Timing**


---
**Read Data Timing**


---
**Write File Mark Timing**


---
**Read File Mark Timing**


---

## Tape Status Information


A read status command must always be performed after a reset command, a
read file mark command, or any other time EXCEPTION is asserted.
A Read Status command can also be issued whenever the tape is idle and READY
is asserted.

The read status command returns six bytes of status information.
Status bytes 0 and 1 contain the status bits shown below. Status bytes
2 and 3 form a 16-bit value which accumulates the number of data blocks
rewritten during write operations, and the number of read retries made during
a read operation.
Status bytes 4 and 5 form a 16-bit value that is incremented whenever the
tape stops streaming and must reposition itself.

Most tape drive exceptions are the result of normal tape operation or are
caused by the user. The bits described below are mostly independent of one
another and often occur in comination.


```


	 Byte 0      Byte 1    	Description
	--------    --------    -----------
	1XXXXXXX    XXXXXXXX    One or more bits set in status byte 0.
	X1XXXXXX    XXXXXXXX    Cartridge not in place.
	XX1XXXXX    XXXXXXXX    Unselected tape drive.
	XXX1XXXX    XXXXXXXX    Write Protected cartridge.
	XXXX1XXX    XXXXXXXX    End of Media.
	XXXXX1XX    XXXXXXXX    Unrecoverable data error.
	XXXXXX1X    XXXXXXXX    Bad block not located.
	XXXXXXX1    XXXXXXXX    File mark detected.

	XXXXXXXX    1XXXXXXX	One or more bits set in status byte 1.
	XXXXXXXX    X1XXXXXX	Illegal Command.
	XXXXXXXX    XX1XXXXX	No data detected.
	XXXXXXXX    XXX1XXXX	Greater than 7 retries reading/writting last block.
	XXXXXXXX    XXXX1XXX    Tape positioned at beginning of media.
	XXXXXXXX    XXXXX1XX    Reserved for future use.
	XXXXXXXX    XXXXXX1X    Reserved for future use.
	XXXXXXXX    XXXXXXX1    Power On reset occurred.


```


Some of the above bits are not generated because of errors but are generated
during the normal operation of the tape drive. For instance, an exception is
always generated after reading a file mark, and bit 0 of status byte 0 will
be set. The end of media bit is another bit that the programmer must expect;
especially when the drive will be used for disk backup.

The illegal command bit has several meanings. It is asserted and an exception
is issued under the following circumstances:

```

	An undefined command is issued.
	An attempt is made to read, write, read a filemark, or write a filemark
		with ONLINE deasserted.
	An attempt is made to issue a command other than write or write filemark
		during a write command.
	An attempt is made to issue a command during a read command.

```


---

The following status byte error codes are very undesirable and are explained
herein:


```


	 Byte 0      Byte 1 	Description
	--------    --------    -----------
	100X0100    10001000	Read or write abort. Generated if the same block was
				rewritten 16 times during a write or write filemark
				command. The error is also generated if an
				unrecoverable repositioning error occurs during a
				write, write filemark, read, or read filemark
				command. In all cases, the tape is rewound.

	100x0100    00000000	CRC error on read. Block reread 16 times. Last
				block read from drive is the faulty block.

	100x0110    00000000    CRC error on read. Block reread 16 times. Block
				read from drive was so garbled that last block
				read from drive merely contained filler data
				to keep the total block count correct.

	100x0110    10100000    Read error. No data. Block reread 16 times. No
				data detected or file mark encountered. No data
				block transfered to host.

	100x1110    10100000    Read error. No data and logical end of tape
				detected. No data block transfered to host.

```


---

# Preparation for Use


## Introduction


This chapter provides information on installing the Sun 1/4" tape interface.
Included are instructions for unpacking, inspection, switch and jumper setting,
and interfacing the Sun 1/4" tape interface board with other IEEE 796-bus boards.


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


The board is designed for installation into a IEEE 796-bus or Intel multibus
cardcage.

`POWER`: The Sun 1/4" tape interace board requires a 5V power supply and draws
2 Amps.

`COOLING`: When installing the board
in an enclosed environment or under restricted airflow conditions,
ensure that the internal operating temperature does not exceed 130 degrees
F (55 degrees C).

`CAUTION`: To prevent possible equipment damage,
do not install board in a cardcage while power is on.
Also, to prevent damage due to static voltages,
avoid exposing the board to plastic materials.


## Repair Information


To return a Sun 1/4" tape interface board for repair,
obtain a return (RMA) authorization number from the address below
and send the board with the RMA number and a detailled description
of the problem to the following address:


	Sun Microsystems Inc
	Att: Service Department
	2310 Walsh Avenue
	Santa Clara, CA 95051
	408-748-9900


---

## Switch Settings


There are four 8-position DIP switches on the tape controller board. They are
used to select the interrupt level at which the tape controller will interrupt
the processor, to select the base address for the multibus memory on the board,
and to select the base address for the multibus I/O registers which communicate
commands and data between the 1/4" tape drive and the central processor.

With the multibus connectors facing you, the switches are all in the lower
left hand corner of the board at component locations U52, U50, U53, and U56.
U52 is closest to the left hand corner of the board; U50 is directly above
U52; U53 is to the immediate right of U50; and U56 is to the immediate right
of U53.For each package, switch #1 is on the right, and switch #8 is on the
left.


---

U52 selects the interrupt level; switch #1 selects interrupt level 0, switch #2
selects interrupt level 1, and so on. The desired switch should be closed
(ON); all others should be left open (OFF). The table below shows the switch
settings.


		Interrupt Level	    Close Switch Number
		---------------     -------------------
		       0		     1
		       1		     2
		       2		     3
		       3		     4
		       4		     5
		       5		     6
	               6		     7
		       7		     8


U50 selects the base address for the multibus memory. Memory on the tape
controller board comes in 128K byte chunks, and there may be one or two of
these chunks. For boards with 256K bytes of memory, two adjacent switches
should be closed. The following table defines the memory address selection
for boards with 256K bytes of multibus memory.


	For Tape Interface Boards with 256K bytes of Memory
	Closed Switches		Address Selected	Address(Hex)
	---------------		----------------	------------
	    7 and 8		    0K - 256K	     0x000000 - 0x040000
	    6 and 7		  128K - 384K        0x020000 - 0x060000
	    5 and 6		  256K - 512K        0x040000 - 0x080000
	    4 and 5       	  384K - 640K	     0x060000 - 0x0A0000
	    3 and 4		  512K - 768K	     0x080000 - 0x0C0000
	    2 and 3		  640K - 896K	     0x0A0000 - 0x0E0000
	    1 and 2		  768K -   1M	     0x0C0000 - 0x100000


For Rev A tape controller boards with 128K bytes of memory,
the memory must lie on a 256K byte boundary.
Only one switch should be closed, and the address selection is as follows:


	For Rev A Tape Interface Boards with 128K bytes of Memory
	Closed Switch		Address Selected	Address(Hex)
        -------------  		----------------	------------
	      8			    0K - 128K	     0x000000 - 0x020000
	      6			  256K - 384K	     0x040000 - 0x060000
	      4			  512K - 640K	     0x080000 - 0x0A0000
	      2			  768K - 896K	     0x0C0000 - 0x0E0000


---

For Rev B and later tape controller boards with 128K bytes of memory,
the memory can lie on any 128K byte boundary. There is a four pole jumper,
however, that must have either the top two pins shorted or the rightmost
two pins shorted. This jumper can be in either orientation for boards with
256K bytes of memory. This four pole jumper is located next to the multibus
memory address select DIP switch. The revision level of the board is stamped
in the upper right hand corner of the board.


	For Rev B Tape Interface Boards with 128K bytes of Memory
		     Orientation
			 of
	Closed Switch  Jumper	Address Selected	Address(Hex)
        -------------  ------	----------------	------------
	      8	     Horizontal	    0K - 128K	     0x000000 - 0x020000
	      7	      Vertical	  128K - 256K	     0x020000 - 0x040000
	      6	     Horizontal	  256K - 384K	     0x040000 - 0x060000
	      5       Vertical	  384K - 512K	     0x060000 - 0x080000
	      4	     Horizontal	  512K - 640K	     0x080000 - 0x0A0000
	      3       Vertical    640K - 768K	     0x0A0000 - 0x0C0000
	      2	     Horizontal	  768K - 896K	     0x0C0000 - 0x0E0000
	      1       Vertical 	  896K -   1M	     0x0E0000 - 0x100000


U53 and U56 select the base address of the I/O registers that the tape controller
uses in multibus I/O address space. The tape controller uses eight consecutive
bytes of multibu I/O space, and this block must be located on an eight-byte
boundary. DIP switch packages U53 and U56 decode address lines A15 through A3.
Switch #8 on U53 corresponds to
A15. Switch #1 on U53 corresponds to A8. Switch #8 on U56 corresponds to
to A7; and switch #4 on U56 corresponds to A3.
Address lines A0 through A2 are not decoded through the switches.

Switch #1 on U56 is used to enable/disable the tape section of the board. Switches
#2 and #3 on U56 are not used and their settings are irrelevant.

The table below illustrates the switch settings in a diagrammatic form. A logical
'0' in the address corresponds to an open (or OFF) switch, and a logical '1' in
the address corresponds to a closed (or ON) switch.


		Required 	   Switch Settings
		Address		   U53	      U56
		--------         --------   --------
		 0x0000		 00000000   00000XX0
		 0XF000		 11110000   00000XX0
		 0X02F8		 00000010   11111XX0

		Disable Tape     XXXXXXXX   XXXXXXX1


## Tape Drive Connector


The Sun 1/4" Tape Interface connects to the 1/4" tape drive through
the J1 connector.
This connector requires a 50-pin flat cable. Pin 1 on the tape drive
connects to pin 1 on the controller board, and so on through pin 50.
Since the QIIC interface uses TTL-level signals, this 50-pin flat cable
should be no more than six feet in length.
