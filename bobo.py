import time
import os

class BoboVisualizer:
    def __init__(self):
        self.RESET = "\033[0m"
        self.BOLD_YELLOW = "\033[1;33m"
        
        self.mapping = {
            0: "\033[90m . \033[0m",
            1: "\033[97m[ ]\033[0m",
            2: "\033[96m[■]\033[0m",
        }
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

bobo = BoboVisualizer()