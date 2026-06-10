```text
 mm                  mm                 
 ##                  ##                 
 ##m###m    m####m   ##m###m    m####m  
 ##"  "##  ##"  "##  ##"  "##  ##"  "## 
 ##    ##  ##    ##  ##    ##  ##    ## 
 ###mm##"  "##mm##"  ###mm##"  "##mm##" 
 "" """      """"    "" """      """"                                       
```
A zero-config terminal visualizer for grid-based algorithms, written in Python.

___

# Quick Start

### Install
```bash
pip install -e .
```

### Use
```bash
bobo your_algorithm.py
```

### Example
```bash
bobo examples/bfs.py
bobo examples/knights_tour.py
bobo examples/maze_generation.py --speed turbo
```
___

# How It Works

This "algorithm visualizer" which is built on Python (I know, gets pretty slow on *maybe* larger stuff), relies heavily on Python's `sys.settrace`. Basically what this does it on every line of code, it inspects local variables for 2D lists (grids/matrices) and bobo does the following:

1. **Detects** the grid automatically (no annotations needed)
2. **Diffs** the new state against the previous snapshot
3. **Highlights** which cells just changed (reverse video)
4. **Renders** the frame with auto-assigned colors

Without touching the source code itself.

___

# CLI Options

```
bobo <script> [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `<script>` | *(required)* | Path to the Python script to visualize |
| `--delay <seconds>` | `0.5` | Seconds to pause between frames |
| `--speed <preset>` | `normal` | `slow` (1s) · `normal` (0.5s) · `fast` (0.1s) · `turbo` (0.01s) |
| `--var <name>` | *(auto-detect)* | Only track a specific variable |
| `--no-clear` | | Don't clear terminal between frames (scrollback mode) |

### Examples
```bash
# Watch BFS pathfinding at default speed
bobo examples/bfs.py

# Speed up maze generation
bobo examples/maze_generation.py --speed turbo

# Only track the 'dp' table, not the obstacle grid
bobo examples/unique_paths.py --var dp

# Keep all frames in scrollback for review
bobo examples/knights_tour.py --no-clear --speed fast
```

___

# Manual API (Advanced)

If you are an experienced developer and you kinda want to have a fine-grained control of how bobo should function, or if you want to customize the mappings, you could use this guide.

```python
from bobo import bobo

bobo.configure(
    mapping={
        0: "\033[90m . \033[0m",   # Dark gray dots for 0
        1: "\033[97m[█]\033[0m",   # White blocks for 1
        '#': "\033[91m[#]\033[0m", # Red for walls
    },
    delay=0.3,
    clear_screen=True
)

# Put this inside your algorithm loop
bobo.show(grid, message="Processing step")
```

### `bobo.configure(mapping, delay, clear_screen)`
Set up the visualizer. `mapping` is a dictionary converting cell values into colored terminal symbols using ANSI escape codes.

### `bobo.show(grid, message, overlays)`
Take a snapshot of a 1D or 2D list. Bobo uses visual diffing — if the grid hasn't changed since the last frame, it skips rendering.

___

# ANSI Color Cheat Sheet

| Color | Example | Code |
|-------|---------|------|
| ⚫ Dark Gray | ` . ` | `\033[90m . \033[0m` |
| 🔴 Red | `[X]` | `\033[91m[X]\033[0m` |
| 🟢 Green | `[*]` | `\033[92m[*]\033[0m` |
| 🟡 Yellow | `[?]` | `\033[93m[?]\033[0m` |
| 🔵 Cyan | `[@]` | `\033[96m[@]\033[0m` |
| ⚪ White | `[█]` | `\033[97m[█]\033[0m` |

Always end with `\033[0m` to reset the color.

___

# Supported Algorithms

bobo works with any algorithm that operates on 2D Python lists. Some tested examples:

- **Pathfinding**: BFS, DFS, Dijkstra, A*
- **Dynamic Programming**: Unique Paths, Edit Distance, LCS
- **Backtracking**: N-Queens, Sudoku Solver, Knight's Tour
- **Matrix Operations**: Rotate, Transpose, Spiral Traversal
- **Generation**: Maze Generation, Game of Life
- **Prefix/Range**: 2D Prefix Sum, Range Queries

# HOWEVER! 
Do take note that for algorithms like BFS where the grid itself never changes (uses a separate visited set (I'm not sure if you can code a BFS where the grid itself changes)), bobo only shows 1 frame (the initial grid). The tracer only visualizes actual grid mutations. 
___

# License

MIT
