"""
Auto-detection of grid variables, coordinate collections, cursors,
and automatic color-mapping.
"""

import re
from collections import deque as _deque_type

# -- ANSI Escape Codes --------------------------------------------------------

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
REVERSE = "\033[7m"

FG_RED = "\033[91m"
FG_GREEN = "\033[92m"
FG_YELLOW = "\033[93m"
FG_BLUE = "\033[94m"
FG_MAGENTA = "\033[95m"
FG_CYAN = "\033[96m"
FG_WHITE = "\033[97m"
FG_GRAY = "\033[90m"

_COLOR_CYCLE = [FG_GREEN, FG_CYAN, FG_YELLOW, FG_BLUE, FG_MAGENTA, FG_WHITE]

# -- Overlay / Cursor / Highlight Styles --------------------------------------

# Each auxiliary collection gets a distinct (color, symbol) from this list.
# Ordered by "most common role" — visited first, then frontier, etc.
OVERLAY_STYLES = [
    (FG_GREEN,   "[*]"),   # 0: visited / seen
    (FG_YELLOW,  "[?]"),   # 1: queue / frontier
    (FG_MAGENTA, "[+]"),   # 2: third aux
    (FG_BLUE,    "[~]"),   # 3: fourth aux
]

CURSOR_COLOR = "\033[1;96m"   # bold cyan
CURSOR_SYMBOL = "[@]"

# Directional change highlights (reverse-video tinted)
FWD_HIGHLIGHT = "\033[7;92m"  # reverse + bright green  → fill / place
BWD_HIGHLIGHT = "\033[7;91m"  # reverse + bright red    → clear / backtrack

# -- Well-known grid value mappings -------------------------------------------

_KNOWN_SYMBOLIC = {
    ".":  f"{FG_GRAY} . {RESET}",
    " ":  "   ",
    "#":  f"{FG_RED}[#]{RESET}",
    "W":  f"{FG_RED}[W]{RESET}",
    "X":  f"{FG_RED}[X]{RESET}",
    "*":  f"{FG_CYAN}[*]{RESET}",
    "@":  f"{FG_YELLOW}[@]{RESET}",
}

# Values treated as "empty" for backtracking detection
_EMPTY_VALUES = {0, 0.0, "", None, " ", "."}

# -- Grid Detection -----------------------------------------------------------

def is_grid(value):
    """True if *value* is a 2-D list with uniform row length and simple cells.
    Also accepts a list of strings (common for read-only mazes)."""
    if not isinstance(value, list) or len(value) == 0:
        return False
    first = value[0]
    if not isinstance(first, (list, str)) or len(first) < 2:
        return False
        
    is_str_grid = isinstance(first, str)
    row_len = len(first)
    
    for row in value:
        if is_str_grid:
            if not isinstance(row, str) or len(row) != row_len:
                return False
        else:
            if not isinstance(row, list) or len(row) != row_len:
                return False
                
    if not is_str_grid:
        for cell in (first[0], first[-1], value[-1][0], value[-1][-1]):
            if isinstance(cell, (list, dict, set, tuple)):
                return False
                
    return True


# -- Auto Color-Mapping -------------------------------------------------------

def auto_map(grid):
    """Generate ANSI-colored display strings for every unique value in *grid*."""
    unique_values = set()
    for row in grid:
        for cell in row:
            unique_values.add(cell)

    mapping = {}
    all_numeric = all(isinstance(v, (int, float)) for v in unique_values)
    color_idx = 0
    sorted_vals = sorted(unique_values, key=lambda x: (isinstance(x, str), str(x)))

    for val in sorted_vals:
        if isinstance(val, str) and val in _KNOWN_SYMBOLIC:
            mapping[val] = _KNOWN_SYMBOLIC[val]
            continue

        if all_numeric and unique_values <= {0, 1}:
            mapping[val] = f"{FG_GRAY} . {RESET}" if val == 0 else f"{FG_WHITE}[#]{RESET}"
            continue

        if all_numeric and isinstance(val, (int, float)):
            if val == 0:
                mapping[val] = f"{FG_GRAY} . {RESET}"
            else:
                color = _COLOR_CYCLE[color_idx % len(_COLOR_CYCLE)]
                color_idx += 1
                mapping[val] = f"{color}{val}{RESET}"
            continue

        color = _COLOR_CYCLE[color_idx % len(_COLOR_CYCLE)]
        color_idx += 1
        mapping[val] = f"{color}{str(val)}{RESET}"

    return mapping


def compute_cell_width(mapping):
    """Minimum cell width that fits every mapped display string."""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    max_visible = 1
    for text in mapping.values():
        vl = len(ansi_escape.sub('', str(text)))
        if vl > max_visible:
            max_visible = vl
    return max(max_visible + 2, 3)


# -- Coordinate-Collection Detection -----------------------------------------

def detect_coord_collections(variables, max_rows, max_cols, exclude_names=None):
    """Find variables whose value is a collection of (row, col) coordinate tuples.

    Recognises ``set``, ``frozenset``, ``list``, and ``collections.deque``.
    Handles both flat ``(r, c)`` tuples and one level of nesting such as
    ``((r, c), path)`` or ``(cost, (r, c))``.

    Returns
    -------
    dict[str, list[tuple[int,int]]]
        Variable name -> list of extracted (row, col) pairs.
    """
    exclude = exclude_names or set()
    result = {}

    for name, value in variables.items():
        if name.startswith('_'):
            continue
        if name in exclude:
            continue

        # Must be a collection (but not a string, dict, or grid-list)
        if not isinstance(value, (set, frozenset, list, _deque_type)):
            continue
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], list):
            continue  # skip grids
        if len(value) == 0:
            continue

        coords = []
        for item in value:
            c = _extract_coord(item, max_rows, max_cols)
            if c is not None:
                coords.append(c)

        # Accept if >= 50 % of items yielded valid coordinates
        if coords and len(coords) >= len(value) * 0.5:
            result[name] = coords

    return result


def _extract_coord(item, max_rows, max_cols):
    """Try to pull a single (row, col) from *item*.

    Patterns handled:
      (r, c)               — direct coordinate
      ((r, c), ...)        — first element is a coordinate
      (x, (r, c), ...)     — second element is a coordinate
    """
    if not isinstance(item, tuple) or len(item) < 2:
        return None

    # Direct (r, c) tuple
    if (len(item) == 2
            and isinstance(item[0], int) and isinstance(item[1], int)):
        r, c = item
        if 0 <= r < max_rows and 0 <= c < max_cols:
            return (r, c)

    # Nested: first element is a (r, c) tuple
    if isinstance(item[0], tuple) and len(item[0]) == 2:
        r, c = item[0]
        if (isinstance(r, int) and isinstance(c, int)
                and 0 <= r < max_rows and 0 <= c < max_cols):
            return (r, c)

    # Nested: second element is a (r, c) tuple  (e.g. priority-queue entries)
    if len(item) >= 2 and isinstance(item[1], tuple) and len(item[1]) == 2:
        r, c = item[1]
        if (isinstance(r, int) and isinstance(c, int)
                and 0 <= r < max_rows and 0 <= c < max_cols):
            return (r, c)

    return None


# -- Cursor Detection ---------------------------------------------------------

_CURSOR_PAIRS = [
    ('r', 'c'), ('row', 'col'), ('i', 'j'), ('x', 'y'),
    ('nr', 'nc'), ('cr', 'cc'), ('sr', 'sc'), ('er', 'ec'),
    ('r1', 'c1'), ('r2', 'c2'),
    ('cur_r', 'cur_c'), ('next_r', 'next_c'),
]

def detect_cursors(variables, max_rows, max_cols):
    """Find pairs of scalar integer variables that look like (row, col),
    as well as tuple variables of length 2 (like `current = (r, c)`).

    Returns
    -------
    list[tuple[str, str, int, int]]
        Each entry is (row_var_name, col_var_name, row_value, col_value).
        For tuples, the variable name is repeated (name, name, row, col).
    """
    cursors = []
    
    # Check for paired scalars
    for rn, cn in _CURSOR_PAIRS:
        rv = variables.get(rn)
        cv = variables.get(cn)
        if (isinstance(rv, int) and isinstance(cv, int)
                and 0 <= rv < max_rows and 0 <= cv < max_cols):
            cursors.append((rn, cn, rv, cv))
            
    # Check for single tuples of length 2
    for name, value in variables.items():
        if name.startswith('_'):
            continue
        if isinstance(value, tuple) and len(value) == 2:
            rv, cv = value
            if (isinstance(rv, int) and isinstance(cv, int)
                    and 0 <= rv < max_rows and 0 <= cv < max_cols):
                cursors.append((name, name, rv, cv))
                
    return cursors


# -- Change Classification ----------------------------------------------------

def classify_changes(old_grid, new_grid):
    """Classify cell differences as *forward*, *backward*, or *other*.

    Forward  = empty -> filled   (algorithm is placing / filling)
    Backward = filled -> empty   (algorithm is clearing / backtracking)
    Other    = value changed to a different non-empty value

    Returns (forward, backward, other) — each a list of (row, col).
    """
    forward, backward, other = [], [], []

    for r in range(min(len(old_grid), len(new_grid))):
        for c in range(min(len(old_grid[r]), len(new_grid[r]))):
            ov, nv = old_grid[r][c], new_grid[r][c]
            if ov == nv:
                continue
            oe = ov in _EMPTY_VALUES
            ne = nv in _EMPTY_VALUES
            if oe and not ne:
                forward.append((r, c))
            elif not oe and ne:
                backward.append((r, c))
            else:
                other.append((r, c))

    # New rows / columns count as forward
    for r in range(min(len(old_grid), len(new_grid)), len(new_grid)):
        for c in range(len(new_grid[r])):
            forward.append((r, c))

    return forward, backward, other