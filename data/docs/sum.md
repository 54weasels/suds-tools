# Architecture Overview


## Specification Summary


### CPU





- 10-MHz M68010 CPU




### Memory





- 1 MByte of onboard main memory (64k RAM)

- 4 MByte of onboard main memory (256k RAM)

- high-speed, no-wait state operation

- main memory expandable to 2 MBytes/8 Mbytes

- transparent hardware memory refresh

- byte parity error detection




### Memory Management Unit





- two-level, multiprocess virtual memory management

- full support for demand paging

- 16 Mbytes virtual address space per process

- separate address spaces for supervisor and user

- valid, accessed, and modified tags to support paging algorithm

- separate read, write, and execute tags for user and supervisor accesses




### CPU OPtions





- Raster operation processor (proprietary)

- IEEE standard floating point processor (Intel 80287)

- DES encryption processor (AMD 9518)




### Display





- dedicated dual-ported frame buffer memory

- 1152 by 900 display format

- 100 MHz video clock

- 70 Hz non-interlaced video refresh




### Ethernet Interface





- VLSI Ethernet controller (Intel 82586)

- digital phase decoder

- direct virtual memory access

- extensive diagnostic capabilities




### SCSI Interface





- high-speed DVMA data transfers into main memory

- single initiator, multiple target interface

- up to 7 controllers with up to 8 devices per controller

- optional parity checking on transfers




### Serial I/O Ports





- six programmable serial i/o ports

- based on synchronous communication controller (Zilog 8530)

- software programmable baud rates (75 Baud to 19.2 Kbaud)

- asynchronous, synchronous, and bit-stuffing protocols

- two primary ports with full modem control, RS-423 levels

- two secondary ports with transmit/receive data only, RS-423 levels

- two tertiary ports with transmit/receive data only, TTL levels




### Other Features





- System bus interface compatible with VME Bus electrical specifications

- DVMA (direct virtual memory access) from VME Bus

- up to 64K bytes EPROM (2764, 27128, or 27256)

- five programmable 16-bit timers (AMD 9513)

- programmable sound generator (TI 76489)

- software interrupt capability

- software readable serial number and revision level




### Diagnostic Features





- diagnostic LED display

- bus error register

- watchdog reset timer

- bus timeout timer




### Electrical Characteristics





- +5V +-5% at 17 Amps, max.

- +12V +-10% at 0.5 Amps, max.




### Physical Characteristics





- Width: 14.44 in. (366.7 mm)

- Height: 15.75 in. (400.0 mm)

- Depth:  0.80 in. (20.0 cm)

- Weight: 64 oz.   (1788 g)




### Environmental Characteristics





- Operating Temperature: 0-50 C
