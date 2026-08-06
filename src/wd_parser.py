import logging
from dataclasses import dataclass, field
from pathlib import Path

from .word36 import left_half, right_half
from .drw_parser import HalfwordStream, ParseError

logger = logging.getLogger(__name__)

@dataclass
class WDBody:
    body_id: int
    approx_loc: int
    brsloc: int
    body_bits: int
    type_name: str
    package_name: str
    properties: dict[str, str] = field(default_factory=dict)

@dataclass
class WDPin:
    body_id: int
    pin_id: int
    pin_name: int
    bits: int
    is_cpin: bool = False

@dataclass
class WDSignal:
    names: list[str] = field(default_factory=list)
    pins: list[WDPin] = field(default_factory=list)
    run_bits: int = 0

@dataclass
class WDFile:
    version: int
    bodies: list[WDBody] = field(default_factory=list)
    signals: list[WDSignal] = field(default_factory=list)


class WDParser:
    """Parse a SUDS WD (Wire Data) file from a list of 36-bit words."""

    def __init__(self, words: list[int], debug: bool = False):
        self.stream = HalfwordStream(words)
        self.debug = debug
        self.result = WDFile(version=0)
        self._parse()

    def _dbg(self, msg: str):
        if self.debug:
            print(f"  [p={self.stream.p}] {msg}")

    def _parse(self):
        self._parse_header()
        self._parse_bodies()
        self._parse_signals()

    def _is_body_start(self, s_pos: int) -> bool:
        """Heuristic to detect the start of the Body list."""
        s = self.stream
        old_p = s.p
        s.p = s_pos
        try:
            w1 = s.read_full_word()
            w2 = s.read_full_word()
            w3 = s.read_full_word()
            
            lh1 = left_half(w1)
            rh1 = right_half(w1)
            # approx_loc (lh1) should be small non-zero, body_id (rh1) non-zero
            if lh1 == 0 or lh1 > 0o100000: return False
            if rh1 == 0: return False
            
            # body_bits word has 0 in right half
            if right_half(w3) != 0: return False
            
            # Next should be a valid 7-bit string (type name)
            val, ok = s.rstrz()
            if not ok or len(val) == 0: return False
            
            return True
        except ParseError:
            return False
        finally:
            s.p = old_p

    def _parse_header(self):
        """Parse version and skip header strings."""
        s = self.stream
        self.result.version = s.read_full_word()
        
        # Scan forward to find the first body
        body_start_p = -1
        # Max search limit based on typical header sizes (few dozen words)
        for i in range(1, 1000):
            # Check halfword position corresponding to word boundaries
            if self._is_body_start(i * 2):
                body_start_p = i * 2
                break
                
        if body_start_p == -1:
            raise ParseError("Could not find start of Body list")
            
        s.p = body_start_p

    def _parse_bodies(self):
        """Parse the list of components/bodies."""
        s = self.stream
        while not s.at_end():
            nxt = s.peek2()
            w1 = (nxt[0] << 18) | nxt[1]
            if left_half(w1) == 0:
                s.read_full_word()  # Consume terminator
                break

            w1 = s.read_full_word()
            w2 = s.read_full_word()
            w3 = s.read_full_word()

            type_name, _ = s.rstrz()
            package_name, _ = s.rstrz()

            # Read properties (null-terminated string list)
            props_list = []
            while True:
                prop_str, ok = s.rstrz()
                if not ok:
                    # Hit the zero word terminator
                    break
                props_list.append(prop_str)

            # Convert to dictionary (name, value pairs)
            properties = {}
            for i in range(0, len(props_list), 2):
                name = props_list[i]
                val = props_list[i+1] if i + 1 < len(props_list) else ""
                properties[name] = val

            body = WDBody(
                approx_loc=left_half(w1),
                body_id=right_half(w1),
                brsloc=w2,
                body_bits=left_half(w3),
                type_name=type_name,
                package_name=package_name,
                properties=properties
            )
            self.result.bodies.append(body)

    def _parse_signals(self):
        """Parse the signal/net list."""
        s = self.stream
        while not s.at_end():
            names = []
            while True:
                name, ok = s.rstrz()
                if not ok:
                    break
                names.append(name)

            if not names:
                # If we read a zero word immediately, it's the signal list terminator
                break

            pins = []
            while True:
                nxt = s.peek2()
                if nxt[0] == 0 and nxt[1] == 0:
                    s.read_full_word()  # Consume terminator
                    break

                w1 = s.read_full_word()
                w2 = s.read_full_word()
                w3 = s.read_full_word()

                is_cpin = (left_half(w1) != 0)
                if is_cpin:
                    pins.append(WDPin(
                        body_id=w1,           # CPIN-LOC,,BRS
                        pin_id=w2,            # PointID
                        pin_name=0,
                        bits=left_half(w3),
                        is_cpin=True
                    ))
                else:
                    pins.append(WDPin(
                        body_id=right_half(w1),
                        pin_id=left_half(w2),
                        pin_name=right_half(w2),
                        bits=left_half(w3),
                        is_cpin=False
                    ))

            run_bits = s.read_full_word()

            signal = WDSignal(
                names=names,
                pins=pins,
                run_bits=run_bits
            )
            self.result.signals.append(signal)

def parse_wd_file(path_or_words, debug: bool = False) -> WDFile:
    """Parse a WD file from a file path or pre-loaded word list.
    
    Args:
        path_or_words: Either a file path (str/Path) or list of 36-bit words
        debug: Enable debug output
    """
    if isinstance(path_or_words, (str, Path)):
        from .unpack import read_file
        words = read_file(str(path_or_words))
    else:
        words = path_or_words
    parser = WDParser(words, debug=debug)
    return parser.result

