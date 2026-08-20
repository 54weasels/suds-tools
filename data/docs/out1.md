**To:** Bill Joy, Tony West, Vinod Khosla

**From:** Andy Bechtolsheim

**Date:** February 8, 1983

**Subj:** Packaging for Sun-2 Electronics Enclosure

This memo discusses the requirements for the Sun-2 electronics base.

**Width:** The Width dimension has to allow for a 14.44" PC Board
plus a 5" power supply plus material thickness (two times 0.25").
Thus the minimal width is 20". In addition, the width should match
the width of the keyboard enclosure which is also 20" minimal.

**Depth:** The Depth dimension has to provide for a 15.75" PC board
dimension plus material thickness. The pC board may line
up with the sheetmetal dimension on the backpanel. Thus the
minimum depth dimension is 15.75" plus one material thickness of 0.25"
or 16".

**Height:** The height dimension has to provide space for a 2.2" power supply
and two PC boards each requiring 0.8" height.
It will be possible to modify the height dimension by changing the base
sheet metal.

Thus the minimal inside dimensions of the electronics enclosure
are WxDxH 20" by 16" by 2.2".

The most important choice for the base now is whether it is
a logically separate piece or whether it is molded
together with the tilt&swivel base of the monitor foot.

A separate electronics box makes the workstation easier to manufacture and to service
because it makes the electronics enclosure a completely removable component.
It gives people the flexibility to separate the electronics
from the display, for example for noise-less (fan-less) applications.

Combining the electronics base with the workstation has the advantage
of reduced material cost (one less piece of plastic) and allows to
drop the height of the workstation by about 0.25".
It does not save tooling or design cost over the separate electronics base.

However, there most important reason in favor of a separate electronics base
is that we need packaging for three products based on the Sun-2 single board:


1) a Multiuser Berkeley Unix Machine,
2) an Ethernet Fileserver with SASI interface, and
3) a laserprinter controller.


A separate electronics enclosure will satisfy all these requirements.
Although I have in the past personally fighted for every 1/4" reduction
in height that was feasible, it seems here that the advantages of a separate
electronics enclosure greatly outweight the aestetic implications of
increasing the height by 0.25". It is also likely that the diving line
between tilt&swivel and electronics base will compensate visually
for the added height.
