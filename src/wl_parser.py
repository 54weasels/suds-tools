"""Parse SUDS wirelist (.wl) signal lists to extract authoritative netlists.

The WL signal list is the verified, cross-page merged netlist produced by
the SUDS WL (wirelister) tool. It serves as ground truth for validating
DRW-based netlist extraction.

Signal list format:
    %LOC(PIN)           ← unnamed net (local, identified by driving pin)
    SIGNAL_NAME         ← named net (schematic wire name)
    ! COMMENT           ← null wire / annotation
        LOC(PIN) TYPE LOW HI USE DIPTYPE BODY FILE POS
        LOC(PIN) TYPE LOW HI USE DIPTYPE BODY FILE POS
        ...
                    total_low/total_hi    [warnings]
"""
import re
import os
import glob
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class WLPin:
    """A pin connection within a net."""
    loc_pin: str        # e.g., 'U102(3)' — component ref + pin number
    pin_type: str       # TO, TI, TIS, TIP, TISP, TOT, TOC, Z
    low: float          # Source current (mA)
    hi: float           # Sink current (mA) 
    use: str            # Pin function name on IC (e.g., 'CLK1', '1G')
    diptype: str        # IC package type
    body: str           # Body symbol name
    page: str           # DRW page file (e.g., 'Q1', 'A07')
    grid_pos: str       # Grid position on schematic (e.g., 'B6')


@dataclass
class WLNet:
    """A single electrical net from the wirelist."""
    name: str                       # Signal name (or %LOC(PIN) for unnamed)
    pins: list[WLPin] = field(default_factory=list)
    is_named: bool = True           # True if named signal, False if %pin-ref
    warnings: list[str] = field(default_factory=list)
    
    @property
    def pages(self) -> set[str]:
        return {p.page for p in self.pins}
    
    @property
    def is_cross_page(self) -> bool:
        return len(self.pages) > 1
    
    @property 
    def pin_count(self) -> int:
        return len(self.pins)


@dataclass
class WLComponent:
    """A component from the WL LOC (location) table.
    
    Maps reference designators (U100, C100) to body types and schematic pages.
    This is the authoritative designator assignment from the WL tool.
    """
    designator: str             # e.g., 'U100', 'C604', 'R401'
    diptype: str                # e.g., '68010', '74F00'
    body: str                   # Body definition name (usually same as diptype)
    page: str                   # DRW page (e.g., 'Q1')
    grid_pos: str               # Grid position (e.g., 'B6')
    
    # Multi-section chips appear on multiple pages
    # Continuation entries have empty designator and share the previous one
    sections: list[tuple[str, str]] = field(default_factory=list)  # [(page, pos), ...]
    
    @property
    def prefix(self) -> str:
        """Component type prefix (U, C, R, J, etc.)."""
        for i, c in enumerate(self.designator):
            if c.isdigit():
                return self.designator[:i]
        return self.designator
    
    @property
    def number(self) -> int:
        """Numeric part of designator."""
        for i, c in enumerate(self.designator):
            if c.isdigit():
                try:
                    return int(self.designator[i:])
                except ValueError:
                    return 0
        return 0


@dataclass
class WLNetlist:
    """Complete netlist parsed from a wirelist file."""
    wirelist_name: str          # e.g., 'q'
    page_list: list[str]        # Pages included (from header)
    components: list[WLComponent] = field(default_factory=list)
    nets: list[WLNet] = field(default_factory=list)
    
    @property
    def named_nets(self) -> list[WLNet]:
        return [n for n in self.nets if n.is_named]
    
    @property
    def unnamed_nets(self) -> list[WLNet]:
        return [n for n in self.nets if not n.is_named]
    
    @property
    def cross_page_nets(self) -> list[WLNet]:
        return [n for n in self.nets if n.is_cross_page]
    
    def components_on_page(self, page: str) -> list[WLComponent]:
        """Get all components assigned to a specific page (case-insensitive)."""
        page_upper = page.upper()
        return [c for c in self.components if c.page.upper() == page_upper]


def _parse_pin_line(line: str) -> WLPin | None:
    """Parse a single pin entry line from the signal list."""
    # Format: \tLOC(PIN)  TYPE  LOW  HI  USE  DIPTYPE  BODY  FILE  POS
    # Some fields may have () around values, e.g., (-0.60)
    
    line = line.lstrip('\t')
    if not line or line.startswith('\t'):
        return None
    
    # Try full format with all fields
    # LOC(PIN) is like U102(3) or C100(1) or S103(8)
    m = re.match(
        r'(\S+\(\d+\))\s+'          # LOC(PIN)
        r'(\S+)\s+'                   # TYPE
        r'([\d.()-]+)\s+'             # LOW
        r'([\d.()-]+)\s*'             # HI
        r'(\S*)\s+'                   # USE (may be empty)
        r'(\S+)\s+'                   # DIPTYPE
        r'(\S+)\s+'                   # BODY
        r'(\S+)\s+'                   # FILE
        r'(\S+)',                     # POS
        line
    )
    if m:
        low_str = m.group(3).strip('()')
        hi_str = m.group(4).strip('()')
        try:
            low = float(low_str)
        except ValueError:
            low = 0.0
        try:
            hi = float(hi_str)
        except ValueError:
            hi = 0.0
        
        return WLPin(
            loc_pin=m.group(1),
            pin_type=m.group(2),
            low=low,
            hi=hi,
            use=m.group(5) if m.group(5) else '',
            diptype=m.group(6),
            body=m.group(7),
            page=m.group(8),
            grid_pos=m.group(9)
        )
    
    return None


def parse_wl_netlist(wl_path: str) -> WLNetlist:
    """Parse a wirelist file and extract the complete netlist.
    
    Args:
        wl_path: Path to .wl file
        
    Returns:
        WLNetlist with all nets and their pin connections.
    """
    wl_name = os.path.basename(wl_path).replace('.wl', '')
    
    with open(wl_path, 'r', errors='replace') as f:
        content = f.read()
    
    # Phase 1: Extract page list from header
    pages = []
    lines = content.split('\n')
    in_header = True
    signal_section = False
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        i += 1
        
        if 'FILNAM' in line:
            i += 3  # Skip format lines
            continue
        
        if '\f' in line:
            in_header = False
            continue
        
        if in_header and line and not line.startswith('\t'):
            parts = line.split('\t')
            page_name = parts[0].strip()
            if page_name and len(page_name) < 20:
                pages.append(page_name)
    
    # Phase 1b: Parse LOC table (component designator assignments)
    # Format: LOC\tDIPTYPE\tBODY\tFILE\tPOS
    # Continuation lines for multi-section chips have empty LOC.
    components = []
    in_loc_section = False
    current_designator = None
    
    for line in lines:
        line_stripped = line.rstrip()
        
        if '\f' in line_stripped:
            continue
        
        if line_stripped.startswith('LOC\tDIPTYPE'):
            in_loc_section = True
            continue
        
        if line_stripped.startswith('SIGNAL NAME'):
            in_loc_section = False
            continue
        
        if not in_loc_section:
            continue
        
        # Skip empty lines
        if not line_stripped.strip():
            continue
        
        # Parse LOC entry
        parts = line_stripped.split('\t')
        if len(parts) < 5:
            # Continuation line for multi-section chip
            if current_designator and len(parts) >= 3:
                page = parts[-2].strip() if len(parts) >= 2 else ''
                pos = parts[-1].strip() if parts else ''
                if page and current_designator:
                    current_designator.sections.append((page, pos))
            continue
        
        loc = parts[0].strip()
        diptype = parts[1].strip()
        body = parts[2].strip()
        page = parts[3].strip()
        pos = parts[4].strip()
        
        if not loc:
            # Continuation of previous component (multi-section)
            if current_designator:
                current_designator.sections.append((page, pos))
            continue
        
        comp = WLComponent(
            designator=loc,
            diptype=diptype,
            body=body,
            page=page,
            grid_pos=pos
        )
        components.append(comp)
        current_designator = comp
    
    # Phase 2: Parse signal list section
    # The WL file has two main sections:
    #   1. LOC table (component locations) - starts with "LOC\tDIPTYPE..."
    #   2. SIGNAL NAME section (netlist) - starts with "SIGNAL NAME"
    # We only want to parse the SIGNAL NAME section.
    nets = []
    current_net = None
    in_signal_section = False
    
    for line in lines:
        line_stripped = line.rstrip()
        
        # Skip form feed / page headers
        if '\f' in line_stripped:
            continue
        
        # Detect start of signal section
        if line_stripped.startswith('SIGNAL NAME'):
            in_signal_section = True
            continue
        
        # Skip column header lines within signal section
        if line_stripped.startswith('\tLOC(PIN'):
            continue
        
        # Skip everything before signal section
        if not in_signal_section:
            continue
        
        # Net header: starts at column 0, not a tab
        if line_stripped and not line_stripped.startswith('\t') and not line_stripped.startswith(' '):
            # Save previous net
            if current_net:
                nets.append(current_net)
            
            # Named signals may have signal name + first pin on same line:
            #   ACC\tU307(13)   TOT\t8.00\t-4.00\tIO3\t2168\t2168\tQ3\tA7
            # Unnamed signals are just %LOC(PIN):
            #   %U102(3)
            # Capacitor/power nets may be name-only:
            #   C(100.0-50)
            
            # Split on first tab to separate signal name from pin entry
            parts = line_stripped.split('\t', 1)
            name = parts[0].strip()
            
            # Skip null wires (comments starting with !)
            if name.startswith('!'):
                current_net = None
                continue
            
            is_named = not name.startswith('%')
            current_net = WLNet(name=name, is_named=is_named)
            
            # If there's a pin entry on the same line, parse it
            if len(parts) > 1:
                pin_text = '\t' + parts[1]  # Re-add tab for parser
                pin = _parse_pin_line(pin_text)
                if pin:
                    current_net.pins.append(pin)
            
            continue
        
        # Pin entry or summary line (tab-indented)
        if current_net and line_stripped.startswith('\t'):
            # Summary line: \t\t\tLOW/HI [warnings]
            if line_stripped.startswith('\t\t\t'):
                rest = line_stripped.strip()
                if 'UNUSED' in rest or '←' in rest or 'WARNING' in rest:
                    current_net.warnings.append(rest)
                continue
            
            # Pin entry
            pin = _parse_pin_line(line_stripped)
            if pin:
                current_net.pins.append(pin)
    
    # Save last net
    if current_net:
        nets.append(current_net)
    
    return WLNetlist(
        wirelist_name=wl_name,
        page_list=pages,
        components=components,
        nets=nets
    )


def parse_all_wl_netlists(wl_dir: str) -> dict[str, WLNetlist]:
    """Parse all wirelist files in a directory."""
    results = {}
    for wl_path in sorted(glob.glob(os.path.join(wl_dir, '*.wl'))):
        wl_name = os.path.basename(wl_path).replace('.wl', '')
        try:
            netlist = parse_wl_netlist(wl_path)
            if netlist.nets:
                results[wl_name] = netlist
        except Exception as e:
            print(f"  Warning: failed to parse {wl_name}.wl: {e}")
    return results
