"""Board version coherence scoring and optimal grouping algorithm.

Given a set of DRW files for a board prefix, identifies distinct design
revisions by prioritizing the BOARD DESIGNATOR (the board name printed in
the lower-left title block) as the primary grouping signal.

The board designator is extracted from title_line_1 by stripping copyright
prefixes. Pages sharing the same designator belong to the same board design.
The "Page X of Y" total and title style are secondary signals.

Scoring formula:
    Score(S, Y) = w1*C_desig + w2*C_of + w3*C_coverage + w4*C_wl + w5*C_size

Where:
    C_desig    = fraction of pages sharing the dominant board designator
    C_of       = fraction of pages agreeing on "of Y"
    C_coverage = |S| / Y (how many of the Y pages we have)
    C_wl       = 1.0 if Y matches WL page count, else 0.0
    C_size     = Y / max(all Y values) — prefer later/larger revisions
"""
import re
import os
import glob
import logging
from dataclasses import dataclass, field
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

# Weights for scoring components — designator has maximum weight
W_DESIG = 0.35     # Board designator consistency (HIGHEST)
W_OF = 0.20        # Pages agreeing on total count
W_COVERAGE = 0.20  # Completeness (pages present / total)
W_WL = 0.15        # Match with wirelist page count
W_SIZE = 0.10      # Prefer larger/later revisions

# Copyright/company prefixes to strip from title_line_1
STRIP_PREFIXES = [
    '(C) 1984 SMI,', '(C) 1983 SMI,', '(C) 1982 SMI,', '(C) 1982 SMI.',
    '(C) 1982,', '(C) 1981 VSI,', '(C) 1981 VSI.',
    '(C) SUN-2 COLOR,', '(2) SUN-2 COLOR,',
    'PROPRIETARY SMI,', 'PROPRIETARY SUN,',
    'SUN MICROSYSTEMS INC',
    'SMI,',
]


@dataclass
class PageVersion:
    """A single DRW page with its revision metadata."""
    name: str               # e.g., 'q3b', 'a07'
    prefix: str             # e.g., 'q', 'a'
    page_num: str           # from trailer "page" field (e.g., '3')
    page_num_int: int       # integer parse of page_num, or 0
    of_total: str           # from trailer "of" field (e.g., '8')
    of_total_int: int       # integer parse, or 0
    title_line_1: str       # first title line from trailer (raw)
    title_line_2: str       # second title line from trailer (page function/part#)
    board_designator: str   # extracted board name (e.g., "SUN-3/F", "SUN 68010")
    page_function: str      # what this page covers (e.g., "CPU", "MMU", "CAPS")
    variant: str            # suffix after number (e.g., 'b', 'old', 'x')
    bodies: int             # body placement count
    points: int             # connection point count
    filepath: str           # full path to .drw.O file


@dataclass
class VersionSet:
    """A coherent set of pages forming one revision of a board."""
    of_total: int           # the target "Page X of Y" total
    board_designator: str   # the dominant board designator for this version
    pages: list[PageVersion] = field(default_factory=list)
    score: float = 0.0
    score_breakdown: dict = field(default_factory=dict)
    is_best: bool = False
    label: str = ''         # e.g., "v1 (of 9, score 0.87)"

    @property
    def coverage(self) -> float:
        if self.of_total <= 0:
            return 0.0
        return len(self.pages) / self.of_total

    @property
    def page_numbers(self) -> list[int]:
        return sorted(set(p.page_num_int for p in self.pages if p.page_num_int > 0))

    @property
    def missing_pages(self) -> list[int]:
        if self.of_total <= 0:
            return []
        present = set(self.page_numbers)
        return [i for i in range(1, self.of_total + 1) if i not in present]


def extract_board_designator(title1: str, title2: str = '') -> str:
    """Extract the board designator (board identity) from title_line_1.

    Strips copyright/company prefixes, then returns the board name portion
    before the first comma-separated function descriptor.
    If title_line_1 yields empty after stripping, falls back to title_line_2
    (which often contains a Sun part number like 501-1007-08).

    Examples:
        "(C) 1982 SMI, SUN 68010, CPU" -> "SUN 68010"
        "PROPRIETARY SMI, SUN-2, CLOCKS" -> "SUN-2"
        "SUN-3/F" -> "SUN-3/F"
        "FERRARI" -> "FERRARI"
        "(C) 1982 SMI SUN 68000 MEMORY BOARD" -> "SUN 68000 MEMORY BOARD"
        "SUN MICROSYSTEMS INC" + "501-1007-08" -> "501-1007-08"
    """
    t = title1.strip()
    if not t:
        return title2.strip() if title2 else ''

    # Try to strip known prefixes
    t_upper = t.upper()
    for pfx in STRIP_PREFIXES:
        if t_upper.startswith(pfx.upper()):
            t = t[len(pfx):].strip()
            t = t.lstrip(',').lstrip('.').strip()
            break
    else:
        # No prefix matched — check if entire string is a raw board name
        # like "(C) 1982 SMI SUN 68000 MEMORY BOARD" (no comma after (C) year)
        m = re.match(r'^\(C\)\s*\d{4}\s*SMI\s*', t, re.IGNORECASE)
        if m:
            t = t[m.end():].strip()
        else:
            m = re.match(r'^\(C\)\s*\d{4}\s*', t, re.IGNORECASE)
            if m:
                t = t[m.end():].strip()

    if not t:
        # Fallback to title_line_2 (part number or subtitle)
        return title2.strip() if title2 else ''

    # Split by comma — first part is the board name
    parts = t.split(',')
    board = parts[0].strip()

    return board


def _extract_page_function(title1: str, title2: str) -> str:
    """Extract the page function (what this schematic page covers).

    This comes from the part after the first comma in title_line_1,
    or from title_line_2 if present.
    """
    # title_line_2 often has the page function
    if title2.strip():
        return title2.strip()

    # Otherwise, extract from title_line_1 after the board designator
    t = title1.strip()
    for pfx in STRIP_PREFIXES:
        if t.upper().startswith(pfx.upper()):
            t = t[len(pfx):].strip().lstrip(',').strip()
            break

    parts = t.split(',')
    if len(parts) > 1:
        return ', '.join(p.strip() for p in parts[1:])
    return ''


def _extract_page_versions(drw_dir: str, prefix: str,
                           parse_fn=None) -> list[PageVersion]:
    """Extract PageVersion metadata for all DRW files matching a prefix."""
    if parse_fn is None:
        from src.drw_parser import parse_drw_file
        parse_fn = parse_drw_file

    pattern = os.path.join(drw_dir, f'{prefix}*.drw.O')
    versions = []

    for filepath in sorted(glob.glob(pattern)):
        fname = os.path.basename(filepath)
        base = fname.replace('.drw.O', '')

        # Parse the filename into prefix + number + variant
        m = re.match(
            rf'^{re.escape(prefix)}(\d+)([a-zA-Z]*)$', base, re.IGNORECASE
        )
        if not m:
            continue

        num_str = m.group(1)
        variant = m.group(2).lower()

        try:
            drw = parse_fn(filepath)
            t = drw.trailer
            page_num = str(getattr(t, 'page', '') or '') if t else ''
            of_str = str(getattr(t, 'of_string', '') or '') if t else ''
            title1 = (getattr(t, 'title_line_1', '') or '') if t else ''
            title2 = (getattr(t, 'title_line_2', '') or '') if t else ''
            n_bodies = len(getattr(drw, 'body_placements', []))
            n_points = len(getattr(drw, 'points', []))
        except Exception as e:
            logger.warning(f"Failed to parse {filepath}: {e}")
            continue

        # Parse integers
        try:
            page_int = int(re.match(r'(\d+)', page_num).group(1)) if page_num else 0
        except (AttributeError, ValueError):
            page_int = 0

        try:
            of_int = int(re.match(r'(\d+)', of_str).group(1)) if of_str else 0
        except (AttributeError, ValueError):
            of_int = 0

        bd = extract_board_designator(title1, title2)
        pf = _extract_page_function(title1, title2)

        pv = PageVersion(
            name=base,
            prefix=prefix,
            page_num=page_num,
            page_num_int=page_int,
            of_total=of_str,
            of_total_int=of_int,
            title_line_1=title1,
            title_line_2=title2,
            board_designator=bd,
            page_function=pf,
            variant=variant,
            bodies=n_bodies,
            points=n_points,
            filepath=filepath,
        )
        versions.append(pv)

    return versions


def _normalize_designator(d: str) -> str:
    """Normalize a board designator for grouping comparison.

    Merges related board names into a canonical root:
    - SUN-3 and SUN-3/F -> SUN-3 family
    - SUN 68010 and SUN-2 CPU -> SUN-2 family (same board)
    - SUN 68000 stays separate (different architecture)
    - Part numbers like 501-1007-08 stay as-is
    """
    d = d.strip().upper()
    if not d:
        return d

    # SUN-2 family: SUN 68010, SUN-2 CPU, SUN-2, SUN-2/50, SUN-2/LC, etc.
    # These are all variants of the Sun-2 Multibus/VME boards
    if d in ('SUN 68010', 'SUN-2 CPU', 'SUN-2/50'):
        return 'SUN-2'

    # SUN-3 family: SUN-3/F, SUN-3/E, SUN-3 are different boards
    # but SUN-3 without suffix sometimes refers to SUN-3/F pages
    # so we merge SUN-3 with the longer SUN-3/* forms only when
    # they share the same 'of' total (handled in _merge_compatible_clusters)

    # SUN 68000 is the Sun-1 family — keep separate
    # FERRARI is the Sun-3/160 — keep separate

    return d


def score_version_sets(
    pages: list[PageVersion],
    wl_page_count: int | None = None,
) -> list[VersionSet]:
    """Score and rank all possible revision groupings for a board prefix.

    Strategy:
    1. Group pages by (board_designator, of_total) — these define candidate versions
    2. For each candidate, find the best page for each position
    3. Score each candidate set

    Args:
        pages: All PageVersion objects for this prefix.
        wl_page_count: Number of pages in the wirelist for this board, if known.

    Returns:
        List of VersionSet objects sorted by score (best first).
    """
    if not pages:
        return []

    # Step 1: Identify candidate versions by (designator, of_total)
    # Group pages into candidate clusters
    clusters = defaultdict(list)
    for p in pages:
        desig = _normalize_designator(p.board_designator) or '(unknown)'
        of_val = p.of_total_int or 0
        clusters[(desig, of_val)].append(p)

    # Step 2: Merge compatible clusters
    # If two clusters share the same designator root and "of" value, merge them
    # Also, if a designator is a sub-variant (e.g., "SUN-3" vs "SUN-3/F"),
    # and they share the same "of" value, consider them the same version
    merged = _merge_compatible_clusters(clusters)

    # Step 3: For each cluster, build a VersionSet
    max_of = max((k[1] for k in merged.keys() if k[1] > 0), default=1)
    version_sets = []

    for (desig, target_of), cluster_pages in sorted(merged.items()):
        if target_of <= 0:
            continue

        # Select best page for each position
        by_position = defaultdict(list)
        for p in cluster_pages:
            if p.page_num_int > 0:
                by_position[p.page_num_int].append(p)

        selected = {}
        for pos in range(1, target_of + 1):
            candidates = by_position.get(pos, [])
            if not candidates:
                continue
            # Prefer page whose designator matches and "of" matches
            def page_score(p):
                s = 0
                if _normalize_designator(p.board_designator) == desig:
                    s += 100
                if p.of_total_int == target_of:
                    s += 50
                s += (p.bodies + p.points) * 0.001
                return s
            best = max(candidates, key=page_score)
            selected[pos] = best

        if not selected:
            continue

        pages_list = [selected[pos] for pos in sorted(selected.keys())]
        n = len(pages_list)

        # Score components
        # C_desig: fraction with matching board designator
        matching_desig = sum(1 for p in pages_list
                            if _normalize_designator(p.board_designator) == desig)
        c_desig = matching_desig / n

        # C_of: fraction agreeing on target_of
        c_of = sum(1 for p in pages_list if p.of_total_int == target_of) / n

        # C_coverage
        c_coverage = n / target_of

        # C_wl: match with wirelist page count
        c_wl = 0.0
        if wl_page_count is not None and wl_page_count > 0:
            if target_of == wl_page_count:
                c_wl = 1.0
            elif abs(target_of - wl_page_count) == 1:
                c_wl = 0.5

        # C_size
        c_size = target_of / max_of if max_of > 0 else 0

        total_score = (
            W_DESIG * c_desig +
            W_OF * c_of +
            W_COVERAGE * c_coverage +
            W_WL * c_wl +
            W_SIZE * c_size
        )

        vs = VersionSet(
            of_total=target_of,
            board_designator=desig,
            pages=pages_list,
            score=round(total_score, 3),
            score_breakdown={
                'c_desig': round(c_desig, 3),
                'c_of': round(c_of, 3),
                'c_coverage': round(c_coverage, 3),
                'c_wl': round(c_wl, 3),
                'c_size': round(c_size, 3),
            },
        )

        # Label
        vs.label = (f"of_{target_of} \"{desig}\" ({n}/{target_of}p, "
                    f"score={vs.score:.2f})")

        version_sets.append(vs)

    # Sort by score descending
    version_sets.sort(key=lambda v: v.score, reverse=True)

    # Mark best
    if version_sets:
        version_sets[0].is_best = True

    return version_sets


def _merge_compatible_clusters(clusters):
    """Merge clusters with related designators and same 'of' value.

    For example, "SUN-3" of 15 and "SUN-3/F" of 15 should be merged.
    """
    def _designator_root(d):
        """Extract root board family for comparison."""
        d = d.strip().upper()
        # SUN-3/F -> SUN-3, SUN-2/LC -> SUN-2
        m = re.match(r'^(SUN-\d+)', d)
        if m:
            return m.group(1)
        return d

    # Group by (root, of_total)
    root_groups = defaultdict(list)
    for (desig, of_val), pages in clusters.items():
        root = _designator_root(desig)
        root_groups[(root, of_val)].append((desig, pages))

    # Merge groups with the same root + of_total
    merged = {}
    for (root, of_val), entries in root_groups.items():
        if len(entries) == 1:
            desig, pages = entries[0]
            merged[(desig, of_val)] = pages
        else:
            # Multiple designator variants for same root + of
            # Use the most specific designator as the label
            all_pages = []
            best_desig = ''
            for desig, pages in entries:
                all_pages.extend(pages)
                if len(desig) > len(best_desig):
                    best_desig = desig
            merged[(best_desig, of_val)] = all_pages

    return merged


def analyze_board_versions(
    prefix: str,
    drw_dir: str,
    wl_page_count: int | None = None,
    parse_fn=None,
) -> list[VersionSet]:
    """Full analysis pipeline for a board prefix.

    Args:
        prefix: Board prefix (e.g., 'q', 'a', 'x').
        drw_dir: Directory containing .drw.O files.
        wl_page_count: Page count from wirelist, if available.
        parse_fn: Optional custom DRW parser function.

    Returns:
        List of VersionSet objects sorted by score (best first).
    """
    pages = _extract_page_versions(drw_dir, prefix, parse_fn=parse_fn)

    if not pages:
        return []

    return score_version_sets(pages, wl_page_count)


def print_diagnostic_table(
    prefix: str,
    pages: list[PageVersion],
    versions: list[VersionSet],
):
    """Print a diagnostic table showing all pages and their grouping assignment."""
    print(f"\n{'='*110}")
    print(f"  DIAGNOSTIC TABLE: {prefix.upper()} prefix — {len(pages)} DRW files")
    print(f"{'='*110}")

    # Header
    print(f"  {'File':12} {'Pg':>3}/{'Of':>3}  {'Board Designator':28}  "
          f"{'Function':24}  {'Assigned To'}")
    print(f"  {'-'*12} {'-'*3}/{'-'*3}  {'-'*28}  {'-'*24}  {'-'*30}")

    # Build assignment map: page_name -> version label
    assigned = {}
    for vi, vs in enumerate(versions, 1):
        best = " ★" if vs.is_best else ""
        for p in vs.pages:
            assigned[p.name] = f"v{vi} of_{vs.of_total} ({vs.score:.2f}){best}"

    # Print each page
    for p in sorted(pages, key=lambda x: (x.page_num_int, x.name)):
        assignment = assigned.get(p.name, '(unassigned)')
        print(f"  {p.name:12} {p.page_num:>3}/{p.of_total:>3}  "
              f"{p.board_designator[:28]:28}  {p.page_function[:24]:24}  "
              f"{assignment}")

    # Version summary
    print(f"\n  VERSIONS ({len(versions)}):")
    for vi, vs in enumerate(versions, 1):
        best = " ★ BEST" if vs.is_best else ""
        pages_str = ', '.join(p.name for p in vs.pages)
        missing = vs.missing_pages
        print(f"    v{vi}: {vs.label}{best}")
        print(f"        Pages: {pages_str}")
        print(f"        Score: {vs.score_breakdown}")
        if missing:
            print(f"        Missing: {missing}")
    print()
