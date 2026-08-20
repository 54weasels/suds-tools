## Gate Arrays


This section summarizes opportunities for gatearrays in the McSun.
For each gatearray, a possible pinout is given.

These gatearrays are concepts only at this point.
For each gatearray, we need detailled specifications,
select technology and packaging, and perform a cost-benefit analysis.

The following Gate arrays are listed in here:

Gate Array		Chip Savings
--------------------------------------------------
Video Buffer 		20
MMU Interface		20
SCSI Interface		30
Memory Controller 	14
Video Controller 	6
--------------------------------------------------

If all gatearrays were implemented, total chip
savings would be 90. The only other chips left
at this point are the 68010/68020 CPU, MMU RAMs,
256K RAMs, EPROMs, UARTs, Ethernet Interface,
and about 10 glue chips.

---

### Video Buffer


This gatearray replaces 20 ICs or 25 ICEQs.


```


(40)	Total PinCount

I(2)	VCC, GND
I(32)	Memory Data
I(2)	LD0, LD1
I(1)	LD SHIFTER
I(1)	ENABLE SHIFTER
I(1)	CLK SHIFTER
O(1)	SHIFT DATA


```


---

### MMU Interface


This gatearray replaces 20 ICs or 25 ICEQs.


```

(86)	PINS  TOTAL

I(2)  	VCC, GND

  (2)

IO(16)	Data Bus
I(1)	CS\
I(1)	R/W\
I(3)	AS\ UDS\, LDS\
I(3)	FC0, FC1, FC2
I(3)	A1,A2,A3
I(1)	CLK

  (28)

O(4)	CX
IO(8)	SMAP
IO(24)	PMAP
I(4)	ERROR BITS
O(8)	ENABLE BITS\

  (48)

O(1)	PROTERR\
O(1)	WR.SMAP<00:07>\
O(1)	WR.PMAP<00:07>\
O(1)	WR.PMAP<08:11>\
O(1)	WR.PMAP<20:23>\
O(1)	WR.PMAP<24:24>\
O(1)	RD.IDPROM\
O(1)	WR.DIAG\

  (8)

```


---

### SCSI Interface


This gatearray replaces about 30 to 40 ICs.
One way to save pins here is to adopt a multiplexed address/data path
similar to the AMD Ethernet chip.

Note that this gatearray also includes the timer functions and
two serial interfaces for keyboard and mouse.
Other features that could be added to this gatearray is a
real-time-clock interface and the interrupt encoder.


```


(64)	Total PinCount

G(2)	GND
V(2)	VCC

  (4)

IO(16)	Data Bus
O(8)	Address Bus <16:23>

  (24)

IO(1)	AS\
IO(1)	UDS\
IO(1)	LDS\
IO(1)	R/W\
I(1)	Ready\
O(1)	INTR\
O(1)	HOLD\
I(1)	HLDA\
I(1)	CS\
I(3)	A1:3
I(1)	CLOCK
I(1)	RESET\

  (14)

IO(9)	SCSI DATA
IO(9)	SCSI CONTROL

  (18)

O(1)	MOUSE OUT
I(1)	MOUSE IN
O(1)	KEYBD OUT
I(1)	KEYBD IN

  (4)

```


---

### Memory Controller


This gatearray replaces 14 ICs.
It requires high-speed logic (Clock-Output 10 nanoseconds)
and FAST output buffers.


```

(58)	PINS  TOTAL

I(4)  	VCC, GND

  (4)

I(21)	Address
I(2)	Display Resolution
I(3)	AS,UDS,LDS
I(1)	VREQ
I(1)	VCLR

  (28)

O(9)	Multiplexed Address
O(4)	RAS<0..3>
O(4)	CAS<0..3>
O(4)	WEL<0..1>,WEU<0..1>
O(1)	DTACK
O(1)	C100
O(1)	C5
O(2)	LD0,LD1

  (26)

```


---

### Video Controller


This gatearray replaces 6 ICs.


```

(8)	PINS  TOTAL

I(2)  	VCC, GND

  (2)

I(1)	Shift Load Pulse
I(2)	Display Resolution

  (3)

O(1)	Horizontal Sync
O(1)	Vertical Sync
O(1)	Display Enable

  (3)

```
