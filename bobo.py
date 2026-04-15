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

    def show(self, data, message=""):
        is_2d = isinstance(data[0], list)
        grid = data if is_2d else [data]

        # 1. Build the visual string first (don't print yet)
        current_state_string = ""
        for row in grid:
            for item in row:
                current_state_string += self.mapping.get(item, f" {item} ")
            current_state_string += "\n"

        # 2. If the grid looks exactly the same as the last frame, skip it!
        if current_state_string == self.last_state_string:
            return 

        # 3. If it's a new visual state, render it.
        self.last_state_string = current_state_string
        self.step_count += 1
        
        # Clear the terminal for that true "animation" feel
        if self.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')

        print(f"{self.BOLD_YELLOW}[Step {self.step_count}]{self.RESET} {message}")
        print(current_state_string)
        
        time.sleep(self.delay)

bobo = BoboVisualizer()