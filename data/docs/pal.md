## PROMs


This section contains the definition of the PAL circuits used.
The function of these circuits is defined in a high-level
functional language which is automatically translated
into bitpatterns for programming.

Without attempting to give a full definition of the language,
the following explanation should provide sufficient information
to understand the programs.

*"%"* indicates a comment, everything to the right of it is ignored.

*"#include "pal...""* requests inclusion of the respective PAL definition file.

*"pin#"* is a reserved name for the pin with the number #.

*"#define symbol1 symbol2"* causes a verbatim substitution of symbol1 into symbol2.

*"{{ }}"*: the min-term within the double curly brackets is the
tri-state enable condition for the current output.

*"/"* is the negation operator, ("/ /") indicates double negation.

*"*"* is the AND operator which combines inputs into min-expressions.

*"+"* is the OR operator which combines min-expressions into max-expressions.

*":+:"* is the XOR operator which combines max-expressions into xor-expressions
for those PALs which offer this feature.

*":="* is the assignment operator which assigns the expression on the
right-hand-side to the output pin on the left.
