# English Description


## Power


The Sun-2 Single board uses a single 5 Volt power supply only.
On-board charge pump/voltage converter `7660:U612,U614`
generate a -5V supply for the RS423 interface drivers `26LS29:U609,611`.


## Initialization


Upon application of power, capacitor `K:C100` begins to charge through
resistor `R:R100`.
When the voltage accross the capacitor reaches the threshold voltage of the
voltage comparator `8211:U120`, output POR\ is deasserted.
Feedback resistor `R:R101` and summing resistor `R:R102` introduce
a schmitt-trigger threshold into the operation of the voltage comparator.


## Clock Generation


All system clocks are derived from 19.6608 MHZ crystal oscillator
`K1114A:U200`. The oscillators output frequency, `C(50.0-25)`,
is divided into clock `C(100.0-50)` by flipflop `74F74:U201-0`.
This clock (and its inverse) drives the 68010 CPU, the timing flipflops,
as well as synchronizers and state machines on the board.
