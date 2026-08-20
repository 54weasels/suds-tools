## PROMs


This section describes the language for specifying PROMs.
The content of these elements is defined in a high-level
functional language which is automatically translated
into bitpatterns for programming.

Without attempting to give a full definition of the language,
the following explanation should provide sufficient information
to understand the programs.

*begin "name"* begins a program with the name *name*.

*require "prom.sai" source!file* requests inclusion of the prom library.

*$#1$#2* defines a PROM with *#1* addressable locations *#2* bits wide.

*adrs(bit, polarity, name)* assigns *<name>* to address bit *<bit>*.
If polarity is 1 then the function of the name is true, if 0, inverted.

*define "name" = [definition]* defines expressions or equations
that describe the function of the PROM.
The following are reserved identifiers: *D#* is the value of
data bit *#*, *A#* is true if address bit *#* is present in the
current value of the location counter (see below).
All standard operators, including logical AND and OR, are allowed
in expressions. Conditional and case expressions are also possible.

*prombegin* tells the program to evaluate the following statements
until *promend* for each location value of the location counter.

*bit(#1, #2, expression)*
puts the value of *expression* into PROM *#1* bit position *#2*.
A single program can define the contents of multiple PROMs by using
multiple PROM numbers *#1*.

*promend* terminates the evaluation of statements.

*writeprom("file",#)* writes the object code of PROM *#* into file *file*.
Each separate PROM needs to be written into a separate file.

*end* terminates the program.

The PROM source code is followed by the generated
hexadecimal object code which also includes a 16-bit checksum.
