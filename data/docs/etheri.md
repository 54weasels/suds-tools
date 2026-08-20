# SUN 3MBit/sec Ethernet Board Installation Manual


<center>SUN Microsystems Inc.</center>


<center>May 1982</center>


**General Description**

The SUN 3 MBit/sec Ethernet Board provides the connection of
the SUN Workstation and other machines using the Intel Multibus (TM) backplane
to Ethernet-1, the experimental 3 MBit/sec Ethernet developed by Xerox `PARC`.

The SUN 3 MBit/sec Ethernet Board interfaces with the CPU
via programmed I/O and interrupt.
In Multibus notation, the board is a I/O slave with 16-bit
addressing and 16-bit data paths. Note that the board is not readily
compatible with 8-bit Multibus I/O.


**Unpacking Instructions**

Inspect the shipping carton immediately upon receipt for evidence of damage.
If the shipping carton is severely damaged, request that the carrier's agent
be present when the carton is opened.
If the carrier's agent is not present when the carton is opened
and the contents are damaged, keep the content and carton for the
agent's inspection.

It is suggested that salvageable shipping cartons and packing material
be saved for future use in the event the product must be reshipped.

**Installation Considerations**

The board is designed for installation into a Intel Multibus compatible
backplane or cardcage.

`POWER`: The Board requires a 5V power supply and draws a maximum
current of 6 Amp. The board includes an on-board voltage converter
that generates the 15V power for the Xerox transceiver.

`COOLING`: The board dissipates 30 Watts. When installing the board
in an enclosed environment or under restricted airflow conditions,
ensure that the internal operating temperature does not exceed 130 degree
F or 55 degree C.

`CAUTION`: To prevent possible equipment damage,
do not install board in a cardcage while power is on.
Also, to prevent damage due to static voltages,
avoid exposing the board to plastic materials.


**Ethernet Tranceiver and Cable**

The SUN 3-Mbit Ethernet Board is designed to interface directly
to the Xerox 3-Mbit Transceiver part # 209926. This transceiver is also
available as TLC Part # 2000. The cables described below apply
to this particular transceiver.

The 3 MBit/sec Ethernet transceiver is designed for RG-8/U Type Foam Coax
with a solid center conductor and a characteristic impedance of 75 Ohm.
The Ethernet cable must be terminated at both ends with a 75 Ohm terminator.

**Cable between Transceiver and Board**

The cable that connects the transceiver to computing equipment
is Xerox Part # 216411D. The cable contains six twisted pairs
of wire and features a female 15-pin D-connector on the transceiver side
and a male 25-pin D-connector on the receiver side. The cable can be
up to 15 meter long. The connector assignments are shown in Figure 1.

The SUN Ethernet board is designed to interface directly
to the above Transceiver cable via a flat-cable assembly.
The flat cable consists of a 26-pin header and a 25-pin D-type female connector,
with wire-1 connecting to pin-1 of both sides and wire-26 ommitted for the
25-pin connector. This assembly is shown in Figure 2.
It is recommended that the flat cable not exceeds 1 meter in length.

**Switches on SUN Ethernet Board**

The SUN Ethernet Board has two octal dip-switches: one to select
the Multibus base address and one to select the local Ethernet host address.
The location of these switches is shown in Figure 3.

**Switch Setting for Multibus Base Address **

The SUN 3 Mbit/sec Ethernet interface communicates with the host CPU
via 4 read and 4 write registers located in Multibus I/O space.
The registers are located on successive word (16-bit) boundaries
starting on a 256-byte boundary within the 64k Multibus I/O space.
Only the eight high-order address bits are decoded for the selection
of the board; thus the interface will respond to 256 consecutive byte addresses
even if only 4 word addresses are decoded.

To select the Multibus base address, take address bits A8..A15
of the desired address and encode them into dip-switch S505.
Switch #1 is the least significant bit, and "1" bits correspond to "ON" switches.

By convention, 0x100 is the normal address for the first Ethernet board,
and subsequent boards if any are placed at successively higher addresses.


**Switch Setting for Ethernet Host Address**

After obtaining an Ethernet host number from your local Ethernet administrator,
express it in binary and set it into dip-switch S507.
Switch #1 is the least significant bit, and "0" bits correspond to "ON" switches,
unlike the correspondance used for the Multibus base address.

Note: Ethernet addresses "0" and "0377" (octal) are reserved for
special Ethernet functions and should not be used as a host address.


![Placeholder: etheri.press]()


*Figure: **The SUN 68000 Board Architecture***
