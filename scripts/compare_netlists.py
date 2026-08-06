"""Extract netlists from DRW point graphs and compare with WL ground truth.

The DRW file contains a per-page connectivity graph where signal wires are 
represented as linked chains of "points". Points with the same signal name
on different pages belong to the same electrical net.

This module:
1. Extracts per-page signal→pin mappings from DRW point graphs
2. Merges them across pages (matching by signal name) to build a board netlist
3. Compares the result against WL (wirelist) ground truth
"""
import os
import sys
import re
from collections import defaultdict
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.drw_parser import parse_drw_file
from src.wl_parser import parse_wl_netlist, WLNetlist


@dataclass
class DRWPin:
    """A pin extracted from a DRW point graph."""
    point_index: int
    signal_name: str
    loc: tuple[int, int]
    page: str
    is_pin: bool
    body_id: int


@dataclass  
class DRWNet:
    """A merged net from DRW pages."""
    signal_name: str
    pins: list[DRWPin] = field(default_factory=list)
    
    @property
    def pages(self) -> set[str]:
        return {p.page for p in self.pins}
    
    @property
    def is_cross_page(self) -> bool:
        return len(self.pages) > 1


def extract_drw_signals(drw_path: str) -> dict[str, list[DRWPin]]:
    """Extract signal→pin mappings from a single DRW file.
    
    Returns dict mapping signal_name → list of DRWPin objects.
    """
    page_name = os.path.basename(drw_path).replace('.drw.O', '').upper()
    
    drw = parse_drw_file(drw_path)
    
    signals = defaultdict(list)
    
    for i, point in enumerate(drw.points):
        name = (point.name or '').strip()
        if not name:
            continue
        
        pin = DRWPin(
            point_index=i,
            signal_name=name,
            loc=point.loc,
            page=page_name,
            is_pin=point.is_pin,
            body_id=point.body_id if hasattr(point, 'body_id') else 0
        )
        signals[name].append(pin)
    
    return dict(signals)


def merge_drw_netlist(drw_dir: str, page_names: list[str]) -> dict[str, DRWNet]:
    """Build a merged netlist from multiple DRW pages.
    
    Args:
        drw_dir: Directory containing .drw.O files
        page_names: List of page names (e.g., ['Q1', 'Q2', ..., 'Q9'])
        
    Returns:
        Dict mapping signal_name → DRWNet with pins from all pages.
    """
    all_nets = defaultdict(lambda: DRWNet(signal_name=''))
    
    for page_name in page_names:
        filepath = os.path.join(drw_dir, f"{page_name.lower()}.drw.O")
        if not os.path.exists(filepath):
            # Try uppercase
            filepath = os.path.join(drw_dir, f"{page_name}.drw.O")
        if not os.path.exists(filepath):
            print(f"  Warning: {page_name}.drw.O not found")
            continue
        
        try:
            page_signals = extract_drw_signals(filepath)
            for sig_name, pins in page_signals.items():
                net = all_nets[sig_name]
                if not net.signal_name:
                    net.signal_name = sig_name
                net.pins.extend(pins)
        except Exception as e:
            print(f"  Warning: failed to parse {page_name}: {e}")
    
    return dict(all_nets)


def compare_netlists(drw_nets: dict[str, DRWNet], wl_netlist: WLNetlist, verbose: bool = False) -> dict:
    """Compare DRW-extracted netlist against WL ground truth.
    
    Returns comparison statistics dict.
    """
    results = {
        'wl_total_nets': len(wl_netlist.nets),
        'wl_named_nets': len(wl_netlist.named_nets),
        'wl_cross_page': len(wl_netlist.cross_page_nets),
        'drw_total_signals': len(drw_nets),
        'drw_cross_page': sum(1 for n in drw_nets.values() if n.is_cross_page),
        'matched': 0,
        'wl_only': [],       # Signals in WL but not in DRW
        'drw_only': [],      # Signals in DRW but not in WL
        'page_mismatches': [],  # Same signal but different page sets
    }
    
    # Build lookup from WL named signals
    wl_named = {}
    for net in wl_netlist.named_nets:
        # Normalize signal name for comparison
        name = net.name.strip()
        wl_named[name] = net
    
    # Build lookup from DRW signals (normalize names)
    drw_lookup = {}
    for sig_name, net in drw_nets.items():
        # DRW signal names may have leading spaces
        normalized = sig_name.strip()
        if normalized:
            drw_lookup[normalized] = net
    
    # Compare WL named signals against DRW
    for wl_name, wl_net in wl_named.items():
        wl_pages = wl_net.pages
        
        if wl_name in drw_lookup:
            drw_net = drw_lookup[wl_name]
            drw_pages = drw_net.pages
            
            if wl_pages == drw_pages:
                results['matched'] += 1
            else:
                results['page_mismatches'].append({
                    'signal': wl_name,
                    'wl_pages': sorted(wl_pages),
                    'drw_pages': sorted(drw_pages),
                    'wl_pins': wl_net.pin_count,
                    'drw_pins': len(drw_net.pins),
                })
        else:
            results['wl_only'].append({
                'signal': wl_name,
                'pages': sorted(wl_pages),
                'pins': wl_net.pin_count,
            })
    
    # Find DRW signals not in WL (may include power, ground, unnamed)
    for drw_name, drw_net in drw_lookup.items():
        if drw_name not in wl_named:
            # Skip common non-signal names (power, capacitor values, etc.)
            if drw_name in ('0', '1', 'GND', 'VCC', '+5', '+5V', '-5V', '+12V'):
                continue
            if drw_name.startswith('C('):
                continue
            results['drw_only'].append({
                'signal': drw_name,
                'pages': sorted(drw_net.pages),
                'pins': len(drw_net.pins),
            })
    
    return results


def run_comparison(board_name: str, wl_path: str, drw_dir: str, page_names: list[str]):
    """Run a full comparison between WL and DRW netlists for one board."""
    print(f"\n{'='*70}")
    print(f"Board: {board_name}")
    print(f"WL: {wl_path}")
    print(f"Pages: {', '.join(page_names)}")
    print(f"{'='*70}")
    
    # Parse WL
    wl = parse_wl_netlist(wl_path)
    print(f"\nWL netlist: {len(wl.nets)} total nets, "
          f"{len(wl.named_nets)} named, "
          f"{len(wl.cross_page_nets)} cross-page")
    
    # Build DRW netlist
    drw_nets = merge_drw_netlist(drw_dir, page_names)
    drw_cross = sum(1 for n in drw_nets.values() if n.is_cross_page)
    print(f"DRW netlist: {len(drw_nets)} total signals, "
          f"{drw_cross} cross-page")
    
    # Compare
    results = compare_netlists(drw_nets, wl)
    
    print(f"\n--- Comparison Results ---")
    print(f"Matched (same signal, same pages): {results['matched']}")
    print(f"Page mismatches: {len(results['page_mismatches'])}")
    print(f"WL-only (in WL but not in DRW): {len(results['wl_only'])}")
    print(f"DRW-only (in DRW but not in WL named): {len(results['drw_only'])}")
    
    if results['page_mismatches']:
        print(f"\n--- Page Mismatches (first 20) ---")
        for m in results['page_mismatches'][:20]:
            wl_p = ','.join(m['wl_pages'])
            drw_p = ','.join(m['drw_pages'])
            print(f"  {m['signal']:20} WL:[{wl_p}] DRW:[{drw_p}]  "
                  f"(WL:{m['wl_pins']}pins, DRW:{m['drw_pins']}pins)")
    
    if results['wl_only']:
        print(f"\n--- WL-only signals (first 20) ---")
        for s in results['wl_only'][:20]:
            pages = ','.join(s['pages'])
            print(f"  {s['signal']:20} pages:[{pages}] ({s['pins']} pins)")
    
    if results['drw_only']:
        print(f"\n--- DRW-only signals (first 20) ---")
        for s in sorted(results['drw_only'], key=lambda x: x['signal'])[:20]:
            pages = ','.join(s['pages'])
            print(f"  {s['signal']:20} pages:[{pages}] ({s['pins']} pins)")
    
    return results


if __name__ == '__main__':
    # Run comparison for the Q board (well-understood test case)
    import argparse
    parser = argparse.ArgumentParser(description="Compare DRW vs WL netlists")
    parser.add_argument("--board", default="q", help="Board wirelist name (default: q)")
    parser.add_argument("--drw-dir", default="data/drw", help="DRW directory")
    parser.add_argument("--wl-dir", default="data/wirelists", help="WL directory")
    args = parser.parse_args()
    
    wl_path = os.path.join(args.wl_dir, f"{args.board}.wl")
    if not os.path.exists(wl_path):
        print(f"Error: {wl_path} not found")
        sys.exit(1)
    
    # Parse WL to get page list
    wl = parse_wl_netlist(wl_path)
    
    results = run_comparison(
        board_name=args.board.upper(),
        wl_path=wl_path,
        drw_dir=args.drw_dir,
        page_names=wl.page_list
    )
