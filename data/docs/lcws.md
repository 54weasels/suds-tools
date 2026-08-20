---


---


# Low-Cost Sun Performance Estimates


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

The architecture anaylized is one in which
video is refreshed out of memory and is double buffered.
Whenever the first video buffer becomes empty a video request
is posted that will cause the next available memory slot
to be used for video refresh. The overhead for refreshing
video out of main memory is computed is computed with
the following assumptions.


The base system has a 68020 CPU at 12.5 MHZ with a memory cycle of 320 nsec.
Memory is built either 32-bit wide with nibble-mode RAM or 64-bit wide
with standard memory.
In either case, 64 bits of video are read in each 320 nsec cycle.

The video display has a resolution of 1024 by 800 pixels and is refreshed
non-interlaced 66.6 times per second. In each second this display
requires 1024*800*66.6/64 or about 800,000 video cycles.

The video overhead, which is the memory bandwith not available to the CPU,
is proportional to the bandwidth required for video refresh.
No overhead is caused during the video blanking intervals.
Since each video cycle requires 320 nsec, the time taken up by video cycles
is 800,000 * 320 nsec = 256 msec per second or 25.6%.

The average bus utilization of the 68020 CPU with the cache enabled
is 75%. Since there is no bus conflict while the CPU is not using the bus,
the 68020 cache reduces the video overhead to 25.6*0.75 = 19.2%.

Video refresh performs memory refresh at the same time.
Sun-2 style memory refresh costs 3.2% overhead. Since the
memory refresh is performed for free, the effective
video overhead is 19.2%-3.2% = 16%.


---

# Separete Frame Buffer Design


In the following, we compare the video refreshed from memory design
with a separate frame buffer design as it is used on current Sun workstations.

A separate frame buffer requires 30 additional chips over
video out of memory, of which 16 are 16k*4 dynamic RAM.
With a chip count of 150 for the base design, the
separate frame buffer increases chip count by 20%.
This also means corresponding increases in board space,
manufacturing and testing requirements and
a corresponding decrease in reliability.

The dollar cost of the separate frame buffer is $150 today.
This is 6% of the estimated system cost of $2500.
With future pricing of 256K RAM, it appears that
the cost of the separate frame buffer will increase to 10%
of the system cost in late 1986.

The current system cost is already 25% over our original targets due
to the increase in memory and going to a 17" display.
I am extremely concerned about increasing the cost any further.
We must be able to compete with competitors that employ a lower-cost
philosophy in their products.

If the goal is to increase performance, a more cost-effective approach
is to push the clock frequency of the 68020 above 12.5 MHZ.
A higher clock frequencies linearly increases CPU performance
and reduces video overhead, since faster memory cycles
also mean faster video refresh cycles. A clock frequency of 14 MHZ
achieves the same performance as the separate frame buffer design
with conceivably no increase in cost.

However, I do not think that a focus on performance
is the right philosophy to take.
The goal of the low-cost machine is to build the cheapest
and easiest to manufacture machine we know how to build.
To me, this means that we minimize chip count as much as we can.
Again and again it has been shown that chip count is a primary
cost factor in electronic design, beyond the dollar value of the
parts involved. We are already making the right steps with the
gatearrays replacing random logic.
Now we also have to take the next step to keep the architecture simple
and live with an architecture that is 16% slower than what is achievable,
but reduces the chipcount of the machine by 20%.

Performance is not everything. Just think of how many poeple
would like to buy this machine at half the cost for half the
performance. At this point, we got to keep the cost down.
Let's get on the steep learning curve of 256K RAMs and not clutter
up the design with components of the previous technology.
