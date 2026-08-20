---


---


# McSun Design Note 1


# Performance Estimates


Company Confidential

Sun Microsystems Inc.

[date]


>

This document describes the performance achieved by the McSun,
the Sun-2 low-cost workstation, for two different architectures.
In the first architecture, memory is synchronous with the CPU.
In the second architecture, memory is synchronous with the Video.
For both architectures, a number of cases will be considered.


>
This document describes subject matter proprietary to SUN MICROSYSTEMS INC.
This document may not be disclosed to third parties or copied or duplicated
in any form without the prior written consent of SUN MICROSYSTEMS INC.

Sun, McSun, and the combination of Sun with a numeric suffix
are trademarks of Sun Microsystems Inc.


---


---

# Definition of Overhead


In this analysis, we define overhead as the increase in execution time.
This is the inverse of a definition that measures reduction in clock speed.

It appears that measuring overhead as increase of execution time
more accurately reflects real-life benchmark situations,
which typically measurre execution times.

The baseline is a system with a 10 MHz 68010 system and 0 wait state memory,
which is approximated by a Sun-2/50.
If we compare a Sun-2/50 to one with 50% overhead,
it means that a program which takes 100 seconds
to execute on a Sun-2/50 would take 150 seconds on the other machine.

---

# Memory Synchronous with CPU, 68010 Processor


In the first type of architecture, memory is synchronous to the CPU.
This allows 0-wait state access as long as there is no video refresh.
Video is double buffered.
Whenever the first video buffer becomes empty a video request
is posted that will cause the next available memory slot
to be used for video refresh.

The overhead, which is the memory bandwith not available to the CPU,
is proportional to the bandwidth required for video refresh.
No overhead is caused during the video blanking intervals.
The overhead can be estimated by the following formula:


```


Definitions:

Pixel-Rate = 1 / (Resolution * Vertical-Refresh-Frequency)

Total-cycle = 64 * Pixel-Rate

Video-cycle = 0.3 usec (nibble mode RAS), 0.5 usec (no-nibble-mode RAMs).

Processor-cycle = Total-Cycle - Video-Cycle

Total Overhead = Total-Cycle / Processor-Cycle

Refresh Credit = 3% (0.5*256/4000)

Other Credit = 10% of total so far (assuming 90% bus utilization by the 68010).


```


The following table summarizes the overhead for nibble-mode memories:


```

-----------------------------------------------------------------------
Resolution	Rate	T-Cycle	P-Cycle T/P	Refresh	Other	Effective
[pixel*2*Hz]	[ns]	[ns]	[ns]	[%]	[%]	[%]	[%]
-------------------------------------------------------------------------
768*600*60	32 ns	2048	1748	17%	-3%	-2%	12%
896*700*60	25 ns	1600	1300	23%	-3%	-3%	17%
1024*800*60	20 ns	1280	980	31%	-3%	-3%	25%
1152*900*60	16 ns	1024	724 	41%	-3%	-4%	34%
-------------------------------------------------------------------------

```


With no-nibble mode RAMs, The same overhead considerations apply.
The only difference is that RAMs without nibble-mode
require a longer time to perform the video refresh cycle,
which increases from 300 nanoseconds to 500 nanoseconds.
The overhead for this case is summarized in the table below.


```

-----------------------------------------------------------------------
Resolution	Rate	T-Cycle	P-Cycle T/P	Refresh	Other	Effective
[pixel*2*Hz]	[ns]	[ns]	[ns]	[%]	[%]	[%]	[%]
-------------------------------------------------------------------------
768*600*60	32 ns	2048	1548	32%	-3%	-3%	26%
896*700*60	25 ns	1600	1100	45%	-3%	-4%	38%
1024*800*60	20 ns	1280	780	64%	-3%	-6%	55%
1152*900*60	16 ns	1024	524 	95%	-3%	-9%	83%
-------------------------------------------------------------------------

```


---

# Memory Synchronous with CPU, 68020 Processor


```


Definitions:

Pixel-Rate = 1 / (Resolution * Vertical-Refresh-Frequency)

Total-cycle = 64 * Pixel-Rate

Video-cycle = 0.4 usec (nibble mode RAS), 0.6 usec (no-nibble-mode RAMs).

Processor-cycle = Total-Cycle - Video-Cycle

Total Overhead = Total-Cycle / Processor-Cycle

Effective Overhead = 50% of total, assuming 50% cache hit.


```


The following table summarizes the overhead for nibble-mode memories:


```

-----------------------------------------------------------------------
Resolution	Rate	T-Cycle	P-Cycle T/P	Effective
[pixel*2*Hz]	[ns]	[ns]	[ns]	[%]	[%]
-------------------------------------------------------------------------
768*600*60	32 ns	2048	1648	24%	12%
896*700*60	25 ns	1600	1200	33%	16%
1024*800*60	20 ns	1280	880	45%	22%
1152*900*60	16 ns	1024	624 	64%	32%
-------------------------------------------------------------------------

```


With no-nibble mode RAMs, The same overhead considerations apply.
The only difference is that RAMs without nibble-mode
require a longer time to perform the video refresh cycle,
which increases from 400 nanoseconds to 600 nanoseconds.
The overhead for this case is summarized in the table below.


```

-----------------------------------------------------------------------
Resolution	Rate	T-Cycle	P-Cycle T/P	Effective
[pixel*2*Hz]	[ns]	[ns]	[ns]	[%]	[%]
-------------------------------------------------------------------------
768*600*60	32 ns	2048	1448	41%	21%
896*700*60	25 ns	1600	1000	60%	30%
1024*800*60	20 ns	1280	680	88%	44%
1152*900*60	16 ns	1024	424 	240%	120%
-------------------------------------------------------------------------

```


---

# Memory Synchronous with Video Architectures


In this second type of architecture, memory is synchronized with the video refreh.
This has the advantage that video data needs not be double buffered,
because new video data is always available exactly when needed.
However, it incurs the disadvantage that the processor must wait
if a CPU cycle cannot be completed before the video cycle must start.

In the simplest implementation, this scheme alternates memory cycles
between video and processor. In this case, the memory bandwidth
is split into two equal pieces, one for the video and one for the
processor.

This scheme relies on the fact that memory cycle times are shorter
than processor cycle times, allowing to alternate between video cycles
and processor cycles without impacting the processor excessively.

The primary constraint of this architecture is memory cycle time.
With 150 nanosecond RAM chip, system cycle times of 320 nanoseconds are
fairly standard, and a cycle times of 300 nanoseconds seems feasible.
Since every second cycle goes to the video, the processor gets one
cycle every 640 or 600 nanoseconds, respectively. This last number
is the Total Cycle time, as seen by the processor.

The primary overhead of this architecture is the ratio of the
Total Cycle over Processor Cycle.
Assuming an Total Cycle time of 600 nanosecond
and a 10 Mhz 68010 featuring a Processor Cycle time of 400 nanoseconds,
the overhead is 200 nanoseconds over 400 nanoseconds or 50%.
With a 10 MHz 68010 CPU and an Total Cycle time of 640 nanoseconds
the overhead goes up to 60%.
With a 10 MHz 68020 CPU which has a CPU cycle time of 300 nanoseconds
and a 600 nanosecond Total Cycle time, the overhead is 100%.

A secondary cause for overhead is that the processor only can get
a memory cycle at certain time slots.
Assuming that the CPU is actually run synchronously with
the Total Cycle, for the simplest possible design,
any instruction time that is not an integer multiple of
4 cycles will be extended to the next multiple of 4 cycles.
This unfortunately applies to a substantial number of instructions,
including classes of addressing modes.
If we guess that 16% of the instructions have execution times
that are not a integer multiple of 4 and that we incur an average
of 2 wait states for these cases, we incur an additional execution
time increase of 8%.

On the positive side, the memory-synchronous-with-video architecture
performs automatic memory refresh, getting a 3% credit there.
It also benefits from the 90% CPU Bus utilization assumption,
which reduces the overhead for those cycles the CPU does not request the bus.

At first approximation, the refresh benefit, the bus utilization benefit,
and the 4-cycle slotting problem just cancel each other, leading to the table below:

```


-------------------------------------------------------------------------
Resolution	Rate	T-Cycle	P-Cycle T/P	Refresh	Other	Effective
[pixel*2*Hz]	[ns]	[ns]	[ns]	[%]	[%]	[%]	[%]
-------------------------------------------------------------------------
896*700*60/010	18.75	600	400	50%	-3%	+3%	50%
896*700*55/010	20.00	640	400	60%	-3%	+3%	60%
896*700*60/020	18.75	600	300	100%	-3%	+3%	100%
896*700*55/020	20.00	640	300	113%	-3%	+3%	113%
1024*800*60	not feasible with 150 ns RAM
1152*900*60	not feasible with 150 ns RAM
-------------------------------------------------------------------------

```


---

# Conclusions


The following table summarizes the overhead, measured as
increase in execution time, for a matrix of the two architectures
in two configurations each.


```

-------------------------------------------------------------------------------
Architecture			896*700*60	1024*800*60
-------------------------------------------------------------------------------
Memory sync with CPU

	68010/no-nibble		38%		55%
	68010/nibble		17%		25%
	68020/no-nibble		30%		44%
	68020/nibble		16%		22%

Memory sync with Video

	68010			50%		not feasible
	68020			100%		not feasible

-------------------------------------------------------------------------------

```


This table shows that:


Memory/CPU architecture with nibble-Mode RAM
is the lowest overhead architecture by a wide margin
and it is even more efficient for 68020 CPUs.

Memory/Video architecture is the highest overhead architecture
and it is even less efficient for 68020 CPUs.

Memory/CPU architectures allow 1024*800 and more resolution.
Memory/Video architectures are limited to 896*700 resolution.


My conclusion is that the McSun should use
the nibble-mode RAM architecture.
With a gatearray for the video-buffer, there is virtually
no cost-difference between the architectures.
Nibble-mode 256K RAMs have been announced by four major RAM vendors
and they are being sampled now.
Even if nibble-mode RAMs should not be available,
the design is readily compatible with standard RAMs at the higher overhead,
which is still substantially lower than video-RAM.
