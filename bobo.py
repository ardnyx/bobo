import time
import os
import re 

class BoboVisualizer:
    def __init__(self):
        self.RESET = "\033[0m"
        self.BOLD_YELLOW = "\033[1;33m"
        
        self.mapping = {}
        self.delay = 0.5
        self.step_count = 0
        self.last_state_string = "" 
        self.clear_screen = True
        self.cell_width = 5

    def configure(self, mapping=None, delay=None, clear_screen=None):
        if mapping: self.mapping.update(mapping)
        if delay is not None: self.delay = delay
        if clear_screen is not None: self.clear_screen = clear_screen

    def show(self, data, message="", overlays=None):
        is_2d = isinstance(data[0], list)
        grid = data if is_2d else [data]

        # NEW: Convert the list of tuples into a fast-lookup dictionary
        # Example: [(2, 3, 4)] becomes {(2, 3): 4}
        overlay_dict = {}
        if overlays:
            for item in overlays:
                # Handle both 2D (row, col, val) and 1D (col, val) overlays
                if len(item) == 3:
                    overlay_dict[(item[0], item[1])] = item[2]
                elif len(item) == 2:
                    overlay_dict[(0, item[0])] = item[1]

        # 1. Build the visual string first
        current_state_string = ""
        for r, row in enumerate(grid):
            for c, item in enumerate(row):
                
                # NEW: Check if there is a ghost overlay at this coordinate
                if (r, c) in overlay_dict:
                    display_val = overlay_dict[(r, c)]
                else:
                    display_val = item
                    
                # Look up the symbol (using the ghost value or the real value)
                current_state_string += self.mapping.get(display_val, f" {display_val} ")
            current_state_string += "\n"

        # 2. Visual Diffing (Skip if identical)
        if current_state_string == self.last_state_string:
            return 

        # 3. Render
        self.last_state_string = current_state_string
        self.step_count += 1
        
        if self.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')

        print(f"{self.BOLD_YELLOW}[Step {self.step_count}]{self.RESET} {message}")
        print(current_state_string)
        
        import time
        time.sleep(self.delay)

    def show_multi(self, grids, labels=None, message="", overlays=None):
        """Renders multiple 2D grids side-by-side."""
        self.step_count += 1
        
        if self.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')

        print(f"\n{self.BOLD_YELLOW}[Step {self.step_count}]{self.RESET} {message}\n")

        # Build the overlay dictionary for the multi-grid view!
        overlay_dict = {}
        if overlays:
            for item in overlays:
                if len(item) == 3:
                    overlay_dict[(item[0], item[1])] = item[2]
                elif len(item) == 2:
                    overlay_dict[(0, item[0])] = item[1]

        # 1. Print Header Labels (if provided)
        if labels:
            header_string = ""
            for i, label in enumerate(labels):
                # FIXED: Uses self.cell_width instead of the hardcoded 3
                width = len(grids[i][0]) * self.cell_width 
                header_string += f"{label:^{width}}" 
                if i < len(grids) - 1:
                    header_string += "    |    " 
            print(header_string)
            print("-" * len(header_string))

        # 2. Find the tallest grid
        max_rows = max(len(g) for g in grids)

        # 3. Zip the rows together!
        for r in range(max_rows):
            combined_row = ""
            
            for i, grid in enumerate(grids):
                if r < len(grid):
                    row_str = ""
                    for c, item in enumerate(grid[r]):
                        
                        # Apply overlay only to the very first grid (i == 0)
                        display_val = overlay_dict.get((r, c), item) if i == 0 else item 
                        
                        # Fetch mapped string or raw string, then apply smart padding
                        raw_text = self.mapping.get(display_val, str(display_val))
                        row_str += self._pad_cell(raw_text)
                        
                    combined_row += row_str
                else:
                    # FIXED: Uses self.cell_width for empty grid balancing
                    width = len(grids[i][0]) * self.cell_width
                    combined_row += " " * width

                # Add the visual divider spacing between grids
                if i < len(grids) - 1:
                    combined_row += "\033[90m    |    \033[0m" 
                    
            print(combined_row)
            
        import time
        time.sleep(self.delay)
    
    def _pad_cell(self, text):
        """Pads text to cell_width while ignoring invisible ANSI color codes."""
        text = str(text) # Ensure it is a string
        
        # Regex to match invisible ANSI escape sequences
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        
        # Calculate the length of the string without the color codes
        visible_length = len(ansi_escape.sub('', text))
        
        # Figure out how much space we need to add to reach cell_width
        padding_needed = max(0, self.cell_width - visible_length)
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        
        return (" " * left_pad) + text + (" " * right_pad)
bobo = BoboVisualizer()