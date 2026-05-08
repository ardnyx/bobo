# bobo
A terminal array/grid-based algorithm visualizer for Python
___
# Code Insertion Guide
`bobo.configure()`
You need to put this line at the top of your file to set up your visualizer. By default, Bobo prints raw numbers. You can use the `mapping` dictionary to convert specific numbers or strings into colored symbols.
Here is an example:
```python
bobo.configure(
    mapping={
        0: "\033[90m . \033[0m",  # Turns 0s into dark gray dots
        1: "\033[97m[ ]\033[0m",  # Turns 1s into white boxes
    }, 
    delay=0.3,              # (0.3) Seconds to pause between frames
    clear_screen=True       # Clears terminal to create an animation effect
)
```

`bobo.show(grid, message, overlays)`
You must put this in a section where the state of the grid changes (usually, inside a loop). The purpose of this is to take a snapshot of the list/array or grid. Bobo also uses "Visual Diffing", meaning if the grid hasn't changed since the last frame, it skips printing to avoid screen flickering.
```python
# Basic Usage
bobo.show(my_grid, message=" <insert message here> ")

# For read-only pathfinding
bobo.show(my_grid, overlays=[(row, col, "\033[91m[ <insert your custom legend here> ]\033[0m")])
```

`bobo.show_multi(grids, labels, message, overlays)`
A split-screen camera gid to render them perfectly aligned side-to-side (I personally haven't tested them on 3 grids altogether yet). So far, I have tested this on Dynamic Programming grid algorithms.
```python
bobo.show_multi(
    grids=[<grid_1>, <grid_2>],
    labels=[" <label for grid_1> ", " <label for grid_2> "],
    message=" <insert message here> "
)
```
___
Configuration with Basic ANSI Escape Codes
Bobo uses standard terminal ANSI codes to colorize text. An ANSI code acts like an invisible wrapper around your text. The Syntax: "\033[COLOR_CODEm" + "Your Text" + "\033[0m"(Always remember to end with \033[0m to reset the color, otherwise your whole terminal will change color.)

# Basic Cheat Sheet of the best colors to use in your bobo.configure(mapping={...}):ColorANSI String FormatBest Used ForDark Gray"\033[90m . \033[0m"Empty space, background grids, 0sRed"\033[91m[X]\033[0m"Obstacles, dead ends, subtracted valuesGreen"\033[92m[*]\033[0m"Winning paths, added values, targetsYellow"\033[93m[?]\033[0m"Current search nodes, warningsCyan"\033[96m[@]\033[0m"The "Head" of a search algorithm, pivotsWhite"\033[97m[ ]\033[0m"Standard walls, generic blocks
