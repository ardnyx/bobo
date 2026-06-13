import os
import re
import time

class BoboVisualizer:
    def __init__(self):
        self.RESET = "\033[0m"
        self.BOLD_YELLOW = "\033[1;33m"
        self.REVERSE = "\033[7m"

        self.mapping = {}
        self.delay = 0.5
        self.step_count = 0
        self.clear_screen = True
        self.cell_width = 5

        self._last_state_string = ""

    def configure(self, mapping=None, delay=None, clear_screen=None, cell_width=None):
        if mapping:
            self.mapping.update(mapping)
        if delay is not None:
            self.delay = delay
        if clear_screen is not None:
            self.clear_screen = clear_screen
        if cell_width is not None:
            self.cell_width = cell_width

    def show(self, data, message="", overlays=None, highlights=None):
        is_2d = isinstance(data, list) and len(data) > 0 and isinstance(data[0], list)
        grid = data if is_2d else [data]

        overlay_dict = {}
        if overlays:
            for item in overlays:
                if len(item) == 3:
                    overlay_dict[(item[0], item[1])] = item[2]
                elif len(item) == 2:
                    overlay_dict[(0, item[0])] = item[1]

        highlight_set = set(highlights) if highlights else set()

        current_state_string = ""
        for r, row in enumerate(grid):
            for c, item in enumerate(row):
                display_val = overlay_dict.get((r, c), item)
                cell_text = self.mapping.get(display_val, str(display_val))
                cell_text = self._pad_cell(cell_text)
                if (r, c) in highlight_set:
                    cell_text = f"{self.REVERSE}{cell_text}{self.RESET}"
                current_state_string += cell_text
            current_state_string += "\n"

        if not highlights and current_state_string == self._last_state_string:
            return

        self._last_state_string = current_state_string
        self.step_count += 1

        if self.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')

        print(f"{self.BOLD_YELLOW}[Step {self.step_count}]{self.RESET} {message}")
        print(current_state_string)

        time.sleep(self.delay)

    def _pad_cell(self, text):
        text = str(text)
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        visible_length = len(ansi_escape.sub('', text))
        padding_needed = max(0, self.cell_width - visible_length)
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        return (" " * left_pad) + text + (" " * right_pad)
