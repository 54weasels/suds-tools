# km.mss

---
From:	Andy Bechtolsheim
Subj:	Analysis of video/keyboard/mouse issue
Date:	May 6, 1984

What are the problems we are trying to solve:

	1) Keyboard/Mouse does not work over distances greater than 15 feet
	   due to voltage drop.

	2) Keyboard/Mouse cable not shielded, potential EMI problem.
	   Not a known problem today.

	3) Mouse cable not long enough in current unit.

	4) Separate cables for keyboard/Mouse run to base unit.

There are simple solutions to these problems which are:

	1) Use better cable with multiple pairs for power and ground.

	2) Use shielded cable.

	3) Supply an extension cord.

	4) Bundle cables into single unit.

The proposal to combine keyboard/mouse/video into one connector
solves problems 1) through 4) above but creates the following new problems:

	1) rework all monitors (Moniterm, Philips, Dataray, Sun, Hitachi, Conrac etc).
	   to accept our keyboard/mouse plug.

	2) Above is incompatible with the plastic cutout for the b&w monitors.

	3) incompatible with a 2050 design paritioned on multiple standard VME Boards
	   where CPU+I/O is on one board and video on another (Ericson requirement).

	4) Unnecessary for Model 50.

	5) Too late for Model 120.

	6) Model 160 still has four separate coax for video anyway.
	   Thus whether there are five or six wires total makes little difference.

	7) It takes up space on the panel of the 2050 Board.
	   The space on this panel is very valuable because it determines
	   how many connectors we can ever have on future 2050 Boards.
	   There are plans for a future SCSI connectors and for a future
	   little Ethernet connector.

Considering these problems, I have made a list of the things I think
we do not want to change:

	1) The monitors.

	2) The keyboard/mouse.

	3) Plastic Tooling

	4) Connectors once we introduce them.


What does this leave to change?

	1) The cables.

Recommendations:

	1) Both the keyboard and the mouse should have cables long enough
	   to plug into the back of the unit.
	   This works for the Model 50 and for the McSun.

	2) Bundle the cables for video/keyboard/mouse and use that cable
	   to connect the display/keyboard/mouse with the base station.
	   The cable comes in a standard length of 15 feet but multiple cables
	   can be plugged in back-to-back up to 50 feet.
	   The same cable can be used for both the 160 and the 120.

This recommendation solves the problems given while not introducing new problems.
Unless I have overlooked something, I think this is what we should do.

---
If we don't like the telephone plug keyboard/mouse hookup,
then that's what should be changed.
Alternatives for new keyboard/mouse connection are:

1) Use a single 9-pin or 15-pin Subminitiature D Connectors on the electronics board.
   Have an adaptor from Sub-D to Telephone plugs for the Model 50 desktop.
   Insert the long distance keyboard/mouse cable for the 160.
   Use multiple pairs (4 pairs) of cable to deliver power and ground.
   On 9-pin, use 2 pairs for keyboard/mouse and 2 pairs for power/ground.
   On 15-pin, use 5 pairs for power/ground.

2) Plug the mouse into the keyboard.
   Change keyboard out from Telephone 4-pin jack to 6-pin jack (upwards compatible).
   Mate the new 6-pin telephone jack to the Sub-D connector on the other side.
