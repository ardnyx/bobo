import time
import os

class BoboVisualizer:
    def __init__(self):
        # ANSI Escape codes for styling
        self.RESET = "\033[0m"
        self.BOLD_YELLOW = "\033[1;33m"
        
        # Default visual mapping
        self.mapping = {
            0: "\033[90m . \033[0m",   # Dark gray dot (empty)
            1: "\033[97m[ ]\033[0m",   # White hollow box
            2: "\033[96m[■]\033[0m",   # Cyan filled box (pivot/active)
        }
        self.delay = 0.5
        self.step_count = 0

    def configure(self, mapping=None, delay=None):
        """Allows the user to customize the symbols, colors, and speed."""
        if mapping:
            self.mapping.update(mapping)
        if delay is not None:
            self.delay = delay

    def show(self, data, message=""):
        """Renders the 1D or 2D list to the terminal."""
        self.step_count += 1
        
        # Print a clear header for the step
        print(f"\n{self.BOLD_YELLOW}[Step {self.step_count}]{self.RESET} {message}")

        # Normalize 1D arrays into 2D for consistent rendering
        is_2d = isinstance(data[0], list)
        grid = data if is_2d else [data]

        for row in grid:
            row_str = ""
            for item in row:
                # Use mapped symbol, or fallback to the raw item if unmapped
                row_str += self.mapping.get(item, f" {item} ")
            print(row_str)

        time.sleep(self.delay)

# Export a default instance for easy importing
bobo = BoboVisualizer()