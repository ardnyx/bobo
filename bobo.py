import time
import os

class BoboVisualizer:
    def __init__(self):
        self.RESET = "\033[0m"
        self.BOLD_YELLOW = "\033[1;33m"
        
        self.mapping = {}
        self.delay = 0.5
        self.step_count = 0
        
        # NEW: Track the last visual state so we skip redundant frames
        self.last_state_string = "" 
        # NEW: Animate in place instead of scrolling down
        self.clear_screen = True 

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

        # NEW: Build the overlay dictionary for the multi-grid view!
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
                width = len(grids[i][0]) * 3 
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
                        
                        # NEW: Check if there is a ghost overlay, but ONLY apply it 
                        # to the very first grid (i == 0) so we don't accidentally 
                        # draw ghosts on the DP/Distance tables!
                        if i == 0 and (r, c) in overlay_dict:
                            display_val = overlay_dict[(r, c)]
                        else:
                            display_val = item
                            
                        # Look up symbol in mapping, or print raw value
                        row_str += self.mapping.get(display_val, f" {display_val} ")
                    combined_row += row_str
                else:
                    width = len(grids[i][0]) * 3
                    combined_row += " " * width

                # Add the visual divider spacing between grids
                if i < len(grids) - 1:
                    combined_row += "\033[90m    |    \033[0m" 
                    
            print(combined_row)
            
        import time
        time.sleep(self.delay)
bobo = BoboVisualizer()