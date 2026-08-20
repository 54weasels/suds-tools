# x.mss

---
What are the objectives:

	Time to Market
	Personal Communications
	UNIX

Product Definition and Cost: 3 Directions

    1) Lowest Cost Single User

	Material cost:	$800 ($500 ICs, $100 package, $50 p.s., $150 xvr) + $400 VTU
	End User cost:	$4000 (Mat. Cost*4 + VTU*2)

    2) Lowest Cost Multi User

	Material Cost:	$800 from above + $100/user (128k RAM) + $400 VTU/user
	End User Cost:	$4000/1, $5200/2, $6400/3, $7600/4, 23200/16
	Per User +VTU:	$3200/1, $2600/2, $2133/3, $1950/8, $1450/16.
	Without VTUs:	$3200/1, $3600/2, $4000/3, $6400/8, $9600/16
	Per User -VTU:	$3200/1, $1800/2, $1333/3, $800/8, 600/16.

    3) SUN Graphics Workstation

	Material Cost: $1600 (SUN-2)
	End User Cost: $6400/1.

Capabilities

    1)	should integrate terminal and voice to offer a novel, low-cost capability.

    2)	same as 1), but no voice, lower cost.

    3)	Novel graphics capabilities, but lacking software

---
Product Proposal:

	10 MHz 68000, no wait states
	virtual memory management
	128k - 768k RAM
	10 MHz Ethernet interface
	8-16 UARTs, 9600 Baud.
	dual-height Multibus (12"*13")

Same Board will function as:

	Shared UNIX workstation
	Shared Fileserver Processor
	Terminal Concentrator

Packaging:

	1) Modular a la Apple or IBM: Personal Computer expandibility

	2) Single Board: lower cost, slim package


Implementation Plan:

	Keep design as close as possible to current SUN 68000
	to reduce risk, time to market, development cost and production cost

	Key: Overlap Software, Hardware, and Package development

Schedule:

	Start software development (68000 UNIX, Filserver, UNET)	FEB 82
	immediately with SUN 68000 Board and Multibus Ethernet board

	Wirewrap Multibus UART board and Ethernet board for
	hardware/software testing.					MAR 82

	Start plastic tooling for package with design finalized.	MAR 82

	Layout final production board. Merge current SUN layout
	into double height Multibus board. Keep 2 layers for low cost.	MAY 82
