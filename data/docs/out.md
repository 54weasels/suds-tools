**To:** Bill Joy, Tony West, Vinod Khosla

**From:** Andy Bechtolsheim

**Date:** February 8, 1983

**Subj:** I/O Connectors for Sun-2

This memo discusses the I/O connector requirements for the single board Sun-2.
This is an important topic because the number of connectors is constrained
by the size of the printd circuit board.

Below is a table of the connector width dimensions including clearance:


```

------------------------------
Purpose	Connector Type	Width
------------------------------
SASI	50-pin Flat:	4"
RS232	25-pin SubD:	2.25"
ETHER	15-pin SubD:	1.75"
VIDEO	9-pin SubD:	1.25"
KEYBD	RT11-J		0.5"
------------------------------

```


The PC board is 14.44" wide on the connector side. Retaining 0.44" for
clearance the available connector space is 14".
Thus the PC Board leaves space for the following connectors:


```

--------------------------------------------------------
Interface	Connector	Space	Comulative Total
--------------------------------------------------------
SASI Bus	50-pin Flat	4	4.00
Ethernet	15-pin D	1.75	5.75
Video		9-pin D		1.25	7.00
Serial 0	25-pin D	2.25	9.25
Serial 1	25-pin D	2.25	11.5
Serial 2 	RT-11J		0.5"	12.0
Serial 3	RT-11J		0.5"	12.5
Keyboard	RT11-J		0.5"	13.0
Mouse		RT11-J		0.5"	13.5
--------------------------------------------------------

```


This leaves space for one more RT11-J connector for future
telephone interfaces.
