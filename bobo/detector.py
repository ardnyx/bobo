import re

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

_KNOWN_SYMBOLIC = {
    ".":  f"{FG_GRAY} . {RESET}",
    " ":  "   ",
    "#":  f"{FG_RED}[#]{RESET}",
    "W":  f"{FG_RED}[W]{RESET}",
    "X":  f"{FG_RED}[X]{RESET}",
    "*":  f"{FG_CYAN}[*]{RESET}",
    "@":  f"{FG_YELLOW}[@]{RESET}",
}

def is_grid(value):
    """
      - Must be a list of lists
      - At least 2 rows
      - At least 2 columns
      - All rows must have the same length
      - Cells must be simple values (int, float, str, bool)
    """
    if not isinstance(value, list) or len(value) < 2:
        return False
    first = value[0]
    if not isinstance(first, list) or len(first) < 2:
        return False
    row_len = len(first)
    for row in value:
        if not isinstance(row, list) or len(row) != row_len:
            return False

    for cell in (first[0], first[-1], value[-1][0], value[-1][-1]):
        if isinstance(cell, (list, dict, set, tuple)):
            return False
    return True

def auto_map(grid):
    """
      1. Collect all unique values.

    Returns:
        dict mapping value → ANSI-colored display string
    """
    unique_values = set()
    for row in grid:
        for cell in row:
            unique_values.add(cell)

    mapping = {}

    return mapping


def compute_cell_width(mapping):
    """Calculate the minimum cell width needed to display all mapped values.

    Inspects the visible (non-ANSI) length of each mapped string and returns
    a width that can comfortably fit the widest value with 1-char padding
    on each side.
    """
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    max_visible = 1
    for text in mapping.values():
        visible_len = len(ansi_escape.sub('', str(text)))
        if visible_len > max_visible:
            max_visible = visible_len
    # Add padding: at least 1 space on each side, minimum total width of 3
    return max(max_visible + 2, 3)