## Schematics


The schematics is contained in the file with extension ".PRE".

Whenever possible, standard drawing conventions are employed.
Signal flow is shown from left to right, and top to bottom.
Connected Sections of the design are logically grouped together,
as much as the available space allowed.

Component identifiers are chosen to reflect the location on the
schematics in the first digit.
For example, component U100 is most likely positioned on page 1.

Schematics file names are chosen to reflect the drawing page number.


---

## Parts List


The partslist is contained in the file with extension ".PRT".
This list is organized under the following heading:


```


PART NUMBER	DIPTYPE		COUNT	DESCRIPTION				LOCATIONS


```


*Partnumber* is not used.

*Diptype* is the generic component name.

*Count* is the number of times the component is used on the board.

*Description* are properties attached to the component to fully specify it.

*Locations* are the labels where the component is used.


---

## Wirelist Summary


The wirelist is contained in the file with extension ".WLS".
The wirelist is comprised of the following sections which are
distinguished by the header lines on each page.


#### Component Summary


The Component Summary lists the DIPTYPE, the BODY NAME,
the number of sections, DIPS, and spare sections with and without location,
and the estimated power consumption.


```

DIPTYPE	BODY NAME	# SECTION	TOTAL DIPS	#SPARE SECTIONS	  MA    V

```


This listing ends with the total chip count and the total current of the design.


#### Runs With No Output


This section contains those signals that are not connected to an output pin.
These signals include connector signals, unused inputs, signals connected
to jumpers (that are not being driven), and signals connected to special
components that do not have standard output/input types.


#### Runs Which Are Overloaded


These signals, as the name implies, are not driven sufficiently
for the total input current connected.


#### Runs With No Inputs


These signals do not have inputs connected to them.
They are typically unused outputs or connector outputs.


#### Unused Extra Outputs


These signals are outputs that are not tristated and
without any connections. Similar to previous category.


#### Runs With No Inputs Or Outputs


These are signals with neither outputs or inputs
connected to them. They include unused connector pins, comments, etc.


#### Runs With Wire-Or Warning


These signals have multiple outputs connected to them, including
signals terminated with pullups and inactive tri-state outputs.

---

## Wirelist


The wirelist is contained in the file with extension ".WL".
The wirelist is comprised of the following sections which are
distinguished by the header lines on each page.


#### Schematics List


The schematics list summarizes all schematics files with titles and pages.
It starts with the following header:


```


FILNAM	P,PN		DATE	   TIME	MODULE(DWG NUM)	REV	AUTHOR
	TITLE 1				PROJECT		BOARD TYPE


```


#### Location List


The location list translates all location labels
into diptype and component names and locations on the schematics.
The location list start with the following header:


```


LOC	DIPTYPE	BODY	FILE	POS


```


#### Signal List


The signal list describes all signals and synonyms in alphabetical order.
Signals that have no explicit name are automatically assigned a
computer-generated name that consists of the percent symbol ("%")
followed by the alphabetically lowest location and pin name connected to
this particular signal run. The signal list pages carry the following header:


```


SIGNAL NAME
	LOC(PIN#) TYPE	LOW	HI	USE	DIPTYPE	BODY	FILE	POS


```


For each signal, the connected component locations are listed together
with the pin number, type (input, output, tri-state, open-collector),
low and high currents, usage on component, the component diptype and bodyname,
and a crossreference to the schematic file where this location is used.
Each signal is followed by a calculation of static current loading.


#### Unused Pin List


The last section of the wirelist displays all unused pin locations in a format
similar to the signal list. The header for this section is:


```


UNUSED PINS
	LOC(PIN#) TYPE	LOW	HI	USE	DIPTYPE	BODY	FILE	POS


```
