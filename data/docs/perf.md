---


---


# Performance of Frame Buffer in Memory Architectures


Company Confidential

Sun Microsystems Inc.

[date]


>

This document describes the performance achieved by a low-cost
workstation architecture that refreshes video from main memory
and discusses the advantages of such an architecture
over one with a separate frame buffer.


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.


---


---

# Video Refresh Overhead


In this analysis, we define overhead as the increase in execution time.
This is the inverse of a definition that measures degradation of clock speed.
This definition of overhead more accurately reflects real-life benchmark situations,
since almost all benchmark measure execution times.

We shall analyse an architecture in which
video is refreshed out of memory and is double buffered.
Whenever the first video buffer becomes empty a video request
is posted that will cause the next available memory slot
to be used for video refresh. The overhead for refreshing
video out of main memory is computed is defined below.
The overhead is expressed in percent and compares to a machine
with the same clock rate that does not have video refresh out of memory.

The average bus utilization of the 68020 CPU with the cache enabled
is 75%. Since there is no bus conflict while the CPU is not using the bus,
the 68020 cache reduces the video overhead to a factor of 0.75.

Video refresh performs memory refresh at the same time.
Sun-2 style memory refresh costs 3.2% overhead. Since the
memory refresh is performed for free, the effective overhead
is reduced by 3 %.


```

Video Overhead = (# of video cycles / second ) * cyclelength * 0.75 - 3%
# of video cycles / second = display resolution * refresh rate / readout width
cyclelength = length of video cycle in nanosecond; 12.5 MHz=320, 16 Mhz=250.

----------------------------------------------------------------------------
Display Resolution	Width	Cycles	Length	Total	Cache	Refresh
times refresh rate	(bits)	per sec	(nsec)	%	* 0.75	-3 %
----------------------------------------------------------------------------
896 * 700 * 66.6	64	646K	480	31%	23%	20%
896 * 700 * 66.6	64	646K	400	25%	19%	16%
896 * 700 * 66.6	64	646K	320	20%	15%	12%
1024 * 800 * 66.6	64	844K	320	27%	20%	17%
1152 * 900 * 66.6	64	1070K	320	34%	25%	22%
1152 * 900 * 66.6	128	535K	320	17%	13%	10%
1152 * 900 * 66.6	128	535K	250	13%	10%	7%
----------------------------------------------------------------------------

```
