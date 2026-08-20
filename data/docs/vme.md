---


# Sun VME-Bus Boards


# Specifications


SUN MICROSYSTEMS INC.

[date]


>
**Trade Secret Notice**

This document contains unpublished, proprietary information
and describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied
or duplicated in any form without the prior written consent of
SUN MICROSYSTEMS INC.


---


---
VME-Bus Specifications:


System Controller Capabilities:

	Clock Option:		SYSCLK		16 MHz, jumperable

	Arbiter Option:		ONE		Bus Request 3 Only

Power Monitor Capabilities:

	ACFAIL Option:		ACFAIL		asserted when VCC < 4.5V

	SYSRESET Option:	SYSRESET	asserted during CPU Reset

	SYSFAIL Option:		SYSFAIL		asserted while CPU is in BOOT State

Master Capabilities:

	Data Bus Size:		D16 MASTER	16-bit/8-bit transfers

	Address Bus Size:	A24 MASTER	24-bit-only addresses

	Timeout Option:		TOUT = 5 USEC	timeout equal 5 microsecond

	Sequential Access:	None

	Interrupt Handler:	IH(1-7)		Level 1 through 7, jumperable

	Requestor Option:	ROR		Release on Request

Slave Capabilities:

	Data Bus Size:		D16 SLAVE	16-bit/8-bit transfers

	Address Bus Size:	A24 SLAVE	24-bit-only addresses

	Sequential Access:	None

	Interrupter Options:	None

Environmental Options:

	Operating Temperature:	10 - 55 C

	Humidity:		0 - 90 %, non-condensing

Power Requirements:

	10 Amp max at +5 Volt +- 5%

	0.5 Amp max at +12 Volt +- 5%

Physical Configuration:

	Height:			TRIPLE		366.67 mm (14.44")

	Width:			QUAD		400.00 mm (15.75")

	Depth:			DUAL		40.64 mm (1.6")
