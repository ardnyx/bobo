import os
import re
import time

from .detector import (
    RESET, REVERSE,
    OVERLAY_STYLES, CURSOR_COLOR, CURSOR_SYMBOL,
    FWD_HIGHLIGHT, BWD_HIGHLIGHT,
)


class BoboVisualizer:
    """Renders grids to the terminal with step-counting and visual diffing."""

    def __init__(self):
        self.BOLD_YELLOW = "\033[1;33m"

        self.mapping = {}
        self.delay = 0.5
        self.step_count = 0
        self.clear_screen = True
        self.cell_width = 5

        self._last_state_string = ""

    # -- Configuration --------------------------------------------------------

    def configure(self, mapping=None, delay=None, clear_screen=None,
                  cell_width=None):
        if mapping:
            self.mapping.update(mapping)
        if delay is not None:
            self.delay = delay
        if clear_screen is not None:
            self.clear_screen = clear_screen
        if cell_width is not None:
            self.cell_width = cell_width

    # -- Main render method ---------------------------------------------------

    def show(self, data, message="", overlays=None, highlights=None,
             aux_overlays=None, cursors=None,
             forward_cells=None, backward_cells=None, changed_cells=None,
             recursion_depth=None):
        """Render a 1-D or 2-D grid with optional overlays and highlights.

        Parameters
        ----------
        data : list
            1-D list or 2-D list-of-lists.
        message : str
            Status text shown in the header line.
        overlays : list[(row, col, val)], optional
            Manual "ghost" overlays (backward compat with v1 API).
        highlights : list[(row, col)], optional
            Generic reverse-video highlights (backward compat).
        aux_overlays : dict[str, list[(row,col)]], optional
            Auto-detected coordinate collections to overlay (e.g. visited, queue).
        cursors : list[(row_name, col_name, row, col)], optional
            Auto-detected cursor positions.
        forward_cells : list[(row,col)], optional
            Cells that changed empty->filled (green flash).
        backward_cells : list[(row,col)], optional
            Cells that changed filled->empty (red flash = backtrack).
        changed_cells : list[(row,col)], optional
            Cells with other value changes (yellow flash).
        recursion_depth : int, optional
            Current recursion depth (shown in header if > 1).
        """
        is_2d = (isinstance(data, list) and len(data) > 0
                 and isinstance(data[0], (list, str)))
        grid = data if is_2d else [data]

        # -- Build lookup dicts for fast (r,c) queries -----------------------

        # Manual overlay dict  (backward-compat)
        overlay_dict = {}
        if overlays:
            for item in overlays:
                if len(item) == 3:
                    overlay_dict[(item[0], item[1])] = item[2]
                elif len(item) == 2:
                    overlay_dict[(0, item[0])] = item[1]

        # Auxiliary overlay dict:  (r,c) -> (color, symbol)
        # Later entries override earlier ones; smallest collections get
        # highest priority (rendered last) so they sit "on top".
        aux_dict = {}
        aux_legend = []
        if aux_overlays:
            items_sorted = sorted(aux_overlays.items(),
                                  key=lambda kv: len(kv[1]), reverse=True)
            for style_idx, (var_name, coords) in enumerate(items_sorted):
                color, symbol = OVERLAY_STYLES[style_idx % len(OVERLAY_STYLES)]
                for coord in coords:
                    aux_dict[coord] = (color, symbol)
                aux_legend.append((color, symbol, var_name, len(coords)))

        # Cursor dict:  (r,c) -> label
        cursor_dict = {}
        if cursors:
            for rn, cn, rv, cv in cursors:
                cursor_dict[(rv, cv)] = f"{rn},{cn}"

        # Change sets
        fwd_set = set(forward_cells) if forward_cells else set()
        bwd_set = set(backward_cells) if backward_cells else set()
        chg_set = set(changed_cells) if changed_cells else set()
        hl_set = set(highlights) if highlights else set()

        # -- Build the rendered string ----------------------------------------

        rendered = ""
        for r, row in enumerate(grid):
            for c, item in enumerate(row):
                # Priority: cursor > aux overlay > manual overlay > grid value
                if (r, c) in cursor_dict:
                    cell_text = f"{CURSOR_COLOR}{CURSOR_SYMBOL}{RESET}"
                elif (r, c) in aux_dict:
                    color, symbol = aux_dict[(r, c)]
                    cell_text = f"{color}{symbol}{RESET}"
                elif (r, c) in overlay_dict:
                    dv = overlay_dict[(r, c)]
                    cell_text = self.mapping.get(dv, str(dv))
                else:
                    cell_text = self.mapping.get(item, str(item))

                cell_text = self._pad_cell(cell_text)

                # Apply directional change highlighting on top
                if (r, c) in bwd_set:
                    cell_text = f"{BWD_HIGHLIGHT}{cell_text}{RESET}"
                elif (r, c) in fwd_set:
                    cell_text = f"{FWD_HIGHLIGHT}{cell_text}{RESET}"
                elif (r, c) in chg_set or (r, c) in hl_set:
                    cell_text = f"{REVERSE}{cell_text}{RESET}"

                rendered += cell_text
            rendered += "\n"

        # -- Visual diffing ---------------------------------------------------

        has_transient = (fwd_set or bwd_set or chg_set or hl_set)
        if not has_transient and rendered == self._last_state_string:
            return  # identical frame — skip

        self._last_state_string = rendered
        self.step_count += 1

        # -- Output -----------------------------------------------------------

        if self.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')

        # Header
        depth_str = ""
        if recursion_depth is not None and recursion_depth > 2:
            depth_str = f"  {OVERLAY_STYLES[0][0]}[depth {recursion_depth}]{RESET}"
        print(f"{self.BOLD_YELLOW}[Step {self.step_count}]{RESET} {message}{depth_str}")

        # Grid
        print(rendered, end="")

        # Legend (only if there's something to label)
        if aux_legend or cursor_dict:
            parts = []
            if cursor_dict:
                parts.append(f"  {CURSOR_COLOR}{CURSOR_SYMBOL}{RESET} current")
            for color, symbol, var_name, count in aux_legend:
                parts.append(f"  {color}{symbol}{RESET} {var_name} ({count})")
            print("  ".join(parts))
            print()

        time.sleep(self.delay)

    # -- Helpers --------------------------------------------------------------

    def _pad_cell(self, text):
        """Pad *text* to ``cell_width``, ignoring invisible ANSI codes."""
        text = str(text)
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        visible_length = len(ansi_escape.sub('', text))
        padding_needed = max(0, self.cell_width - visible_length)
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        return (" " * left_pad) + text + (" " * right_pad)
