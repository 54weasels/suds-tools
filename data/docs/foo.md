# User Guide


## Programming


The 2050 Board implements the Sun-2 Architecture, Machine Type 2.
The full architecture is documented in the Sun-2 Architecture Manual
and no attempt is made to repeat this information here.
However, this section does describe the features specific
to this implementation of the architecture.


### MMU Implementation


The MMU of this machine type implements a page number field of 12 bits.
It thus supports a physical address of 23 bits, capable of addressing 8 MBytes.
The other physical address bits in the page map are not implemented.
On a read cycle, the not implemented bits read back as 0.


### Physical Address Assignments


```


Type	Address		Device				Wait States
------------------------------------------------------------------------------
0	23-bit		Memory Bus

	[0x000000]	Physical Memory	1..8 MBytes	0
------------------------------------------------------------------------------
1	23-bit		I/O Bus

	[0x000000]	BW-Frame Buffer			2 (Write), 4..8 (Read)
	[0x040000]	Video Control Register		2

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
			Accesses to the VME Bus incur an additional 2 wait states
			access time if the 2050 board is not currently bus master.

```


### Interrupt Assignments


The following table summarizes the interrupt level assignments
for the devices that have been described in this manual.
All these interrupts are autovectored.


```

-----------------------------------------------------
    7	TIMER1
    6	Serial Port
    5	TIMER2..5
    4	VIDEO
    3	Ethernet or system enable register EN.INT3
    2 	System enable register EN.INT2
    1 	System enable register EN.INT1
------------------------------------------------------

```


In addition, the VME-Bus can cause vectored interrupts on all levels.
Individual VME-Bus interrupt levels can be disabled with jumpers.


### DVMA Implementation


*Mapping*. DVMA maps one Megabyte from the VME-Bus to the
most-significant Megabyte of the system context virtual address space.
The mapped Megabyte is jumper selectable.


```


P1-Address			Virtual Address
---------------------------------------------------
[0x"i"00000..0x"i"FFFFE]	[0xF00000..0xFFFFFE]

where "i" is jumper-selectable from 0 to 0xF.


```


### Video Memory


Read accesses are unbuffered and will cause 4 to 8 wait states.
Write accesses to the video memory are buffered.
However, subsequent read or write accesses will have to wait
until the video memory has completed the requested operation.
Write accesses to the video memory via the copy mode will cause the
same behavior as direct write accesses.


### CPU Timing


CPU Timing is as follows:


```


CPU clock cycle:	101.7 nanoseconds (9.8304 MHz)
CPU basic cycle:	407 nanoseconds
Timeout period:		6.4 microseconds


```


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
