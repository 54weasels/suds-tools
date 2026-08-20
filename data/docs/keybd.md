# keybd.mss

---
Subj:	Keyboard MEMO

From:	Andy Bechtolsheim

Date:	July 1, 1982

--------------------------------------------------------------------------------
Content:
	Evaluation Microswitch 103 Keyboard
	Evaluation Microswitch VT100 Keyboard
	Evaluation Keytronix IBM Keyboard
	Evaluation Keytronix VT100 Keyboard
	Recommendations

--------------------------------------------------------------------------------


---
Subj:	Keyboard MEMO

Evaluation Microswitch Keyboards

MICROSWITCH 103SD30

    LAYOUT:

    The following keys are different from the ANSI standard layout:

	Keyposition	Should be	Is

	TOP 2		@		"
	TOP 6		∧		&
	TOP 7		&		'
	TOP 8		*		(
	TOP 9		)		)
	TOP 0		)		0
	TOP -		_		=
	KEY =		=		~
	TOP =		+		∧
	TOP `		~		@
	KEY [		[		{
	KEY ]		]		}
	TOP [		{		[
	TOP ]		}		]
	TOP ;		:		+
	KEY '		'		:
	TOP '		"		*
	KEY RETURN	RETURN		_
	KEY RETURN	RETURN		\

	ESC		ESC		CAPS LOC
	CTRL		CTRL		SHIFTLOCK
	--		--		BACKTAB

   MISSING KEYS:

	DEL
	LF
	BREAK


MICROSWITCH VT100 LAYOUT

	SPACE KEY TOO SHORT
	NO SCL KEY NOT LABELLED
	NUMERIC KEYPAD NOT SCULPTURED
	KEYPOSITION OF RETURN/DEL/\ KEYS WRONG DOES NOT FIT STANDARD PACKAGE

MICROSWITCH KEYBOARD FEEL:

	LINEAR, FULL TRAVEL

OTHER COMMENTS:

	KEYBOARD DOES NOT SATISFY ERGONOMIC REQUIREMENTS

---
Subj:	Keyboard MEMO

Evaluation Keytronics Keyboards

FEEL:

	Low profile, reduced travel
	Claims to satisfy ergonomic requirements
	Touch-typing tests still under evaluation

The keytronix keyboards have a "mushy" feel that some people like
but others object to. Keys are activated when the first touch the "mush",
thus it is not necessary to fully depress the keys.
Typists not used to the keytronix have a tendency to activate
keys surrounding the target key. Full speed touch typing tests are
still under evaluation.
The keyshape, adopted from the IBM personal computer keyboard,
feels intuitively nice. However, the oversize keys should be full size
instead of the reduced size.

Both the IBM and the VT100 have layouts that are very similar.

IBM keyboard

    Advantages

	CTRL key in right place
	Backspace key good size
	~ key in acceptable location
	Has 10 well positioned function keys
	Has only 5 rows
	Keyboard with packaging and up/down available August 1.

    Disadvantages

	\ Key too close to left shift
	Misses Break and LF key (*/PRTSRC could be substituted)
	no scroll in wrong place (Function key could be substituted)

    Other comments

	Generic labels had been critizised (I don't find anything wrong with them)

VT100 keyboard

   Advantages

	has all ASCII keys
	has LEDs and beeper but requires serial communication for those.
	has parallel interface option for SUN-1.

   Disadvantages

	Ctrl key too far from keyboard (shift lock could be substituted)
	Packaging only available October 1st.
	No standard up/down option.

   Other comments

	IBM features white keys and light enclosure
	VT100 is dark keys and ??? enclosure


---
Subj:	Keyboard MEMO

Action Items:

	1) the Microswitch 103 keyboard has 25 differences over a standard keyboard.
	   The keyboard does not satisfy ergonomic requirements and is
	   excessively heavy and expensive.
	   We need to change from this keyboard ASAP, which is August 1st.

	2) Keytronix offers two keyboards that are both acceptable in terms
	   of layout, ergonomics, and cost. These are the IBM and VT100 low profile.

	Comparision	IBM		VT100
	------------------------------------------
	Layout		acceptable	acceptable
	Availability	August 1st	August 1st
	Packaging	August 1st	October 1st
	Interface	serial		serial or parallel
	up/down		optional	need to do it inhouse

	3) The parallel interface would be nice for the SUN-1
	   to retain two serial ports. On the other side, how
	   many of the current customers use more than one port?
	   The current plan for the SUN-2 is to use serial ports
	   for both keyboard and mouse.

	4) If we make an IBM compatible interface we can potentially
	   substituted original IBM keyboards for people who prefer
	   the break over key feel. On the other side, the IBM layout
	   might rise expectation of keyboard feel that are not met.

	5) The most important thing is to drop the Microswitch keyboard ASAP.
	   Put the Microswitch order on hold if anybody in the future
	   ever wants them. The microswitch will not be compatible with SUN-2.


---
∂31-Aug-82  1221	pratt@Shasta (SuNet)  	caps lock
Date: 31 August 1982   12:22:27-PDT (Tuesday)
From: pratt at Shasta
Subject: caps lock
To: avb
Cc: pratt

The caps lock key on the new keyboards bothers me.  For true VT100 emulation
it must be possible to make the caps lock key operate its light properly.
This could be done under 8748 control by complementing the caps lock led
at each down transition of the caps lock key, as usual.

The disadvantages of this are:

1.  The Sun might get out of phase with the light.

2.  The light may be distracting when the caps lock key is being used for
other things.

For 1 I propose to treat caps lock led transitions just like ordinary key
transitions as far as the 68000 is concerned.  As far as the user is concerned
the only way to induce a led transition is with a down transition of caps
lock.  Thus depressing caps lock sends two bytes (second is the led
transition), releasing it sends one.  On keyboard power up the led is cleared,
so the Sun should always find the keyboard in its idle state on power up
(there are no physically bistable keys on the Keytronics keyboard, unlike on
the Microswitch, hooray!).

For 2 I propose to have the 8748 recognize the two transitions Setup-down
followed by caps-lock-down as signalling the 8748 to complement the state of
a variable called caps-lock-enable, this state being indicated by the two
left-most leds of the 8-led row (the keyboard comes wired so that one or the
other is always on).  Caps-lock-enable off forces the caps lock led
permanently to off, overriding all subsequent caps lock key transitions, which
thereafter generate one byte per transition.  When caps-lock-enable goes
back on, it leaves the caps lock led off.

I also suggest that the key number for the Keytronics caps lock led be the
same as the key number for the Microswitch caps lock key, so that they appear
to the normal Ascii user to behave the same way.  (This hack comes free, and
may be handy in case we ever find ourselves using the Microswitch keyboard.
Unless the Microswitch caps lock key is made monostable there is little hope
to use it in the same way as the Keytronics caps lock key.)

The caps lock led may come in handy for some up-down-encoded applications
where a bistable key is useful.

The ability to disable the caps lock led altogether will make some users (like
me) deliriously happy, since it is all too easy to hit it instead of CTRL
while touch typing vi commands with the result that vi starts behaving very
strangely.

Since the Sun can track the state of caps-lock-enabled, there could be an
option on the Sun whereby, under caps-lock-disabled, caps lock is interpreted
identically to CTRL.  Another option could make it interpreted as an EDIT key,
delighting Datamedia users and all others who want an EDIT key.

What do you think?

Also, are there any other leds that are standard on the VT-100 itself that we
might consider emulating as part of the 8748's duties independently of the Sun?

-v

∂01-Sep-82  1028	AVB  	caps lock
Personally I hoped to redefine the CAPS LOCK key as control key,
but clearly this is not standard VT100.

Your suggestion how to deal with the LED seems the best solution.
The only other thing to keep in mind is that on the SUN-2 we will
have bidirectional serial communication, so the 68000 can set
the LEDs any way it wants.
