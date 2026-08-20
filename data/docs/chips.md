**To:** Sun Engineering

**From:** Andy Bechtolsheim

**Date:** February 1, 1983

**Subj:** Plans for Graphics Chips


Sun is collaborating with a custom silicon house to define
custom chips that implement useful graphics functions.

Currently three chips are identified:


A RasterOp Chip

A Graphics Processor Chip

A Multiwindow Chip


The current state of these projects is as follows:

**RasterOp Chip:** The RasterOp chip is fairly well along.
We have a first draft specification,
we have designed a breadboard for the chip,
and we have designed the chip into a number of our future products.
The plan is to freeze the spec within 2 weeks. In this time,
we need to write a RasterOp library for the chip to understand
whether there is anything wrong with it.

**Graphics Processor:** The graphics processor is a primitive
generator that accepts commands from the 68010 or a future
tranform unit and generates addresses and bit masks for manipulating
rasters in memory. This chip is currently in conceptualization,
and we should work on a first specification for it over the next two weeks.
The area which requires the most attention is what functions to
implement on the chip and to understand whether the chip could
implement advanced primitives such as conic curves and splines.

**Multiwindow Chip:** The goal of the multiwindow chip is
to implement the functions of a window manager in software.
This chip is in a phase of early conceptualization, and we
will need to have a brainstorming session to determine
whether this chip is in fact practical. Key issues are
synchronization between the windows, cursors, and the
interface between the multiwindow chip and virtual memory.
