# timing.mss

The SAIL timing verifier is a tool to verify the operation constraints
of components in logic design.

namel 	A name means the maximum time at which this signal is asserted or
	a maximum propagation delay.

name!	A name followed by an exclamation mark means the minimum
	time when this signal is asserted or a minimum propagation delay,

!name	A name prefixed with an exlamation mark means the
	maximum time when this signal is deasserted or invalid.

!name!	A name prefixed and postfixed with an exlamation mark means the
 	minimum time when this signal is deasserted or invalid.

+-*/	The arithmetic operators work as normal.
	Standard precedence rules applies.

v ( label, min_interval, left_time, right_time)

	label		is a comment describing the component being checked,
	min_interval	is the constraint to be checked,
	left_time	is the left (earlier) event in time,
			typically computed through a path with maximum delays,
	right_time	is the right (later) event in time,
			typically computed through a path with minimum delays,

	An error will be reported if right_time - left_time < min_interval.

w ( label, max_interval, left_time, right_time)

	label		is a comment describing the component being checked,
	max_interval	is the constraint to be checked,
	left_time	is the left (earlier) event in time,
			typically computed through a path with minimum delays,
	right_time	is the right (later) event in time,
			typically computed through a path with maximum delays,

	An error will be reported if right_time - left_time > max_interval.
