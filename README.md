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
pip install 
```

### Use
```bash
bobo your_algorithm.py
```

### Example
```bash
bobo bfs.py
bobo knights_tour.py
bobo maze_generation.py --speed turbo
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
| `--var <variable>` | *(auto-detect)* | Only track a specific variable |
| `--no-clear` | | Don't clear terminal between frames (scrollback mode) |

### Examples
```bash
# Watch BFS pathfinding at default speed
bobo bfs.py

# Speed up maze generation
bobo bfs.py --speed turbo

# Only track the 'empty_grid' table
bobo 8queens.py --var empty_grid

# Keep all frames in scrollback for review
bobo bfs.py --no-clear --speed fast
```
___

# Supported Algorithms

bobo works with any algorithm that operates on 2D Python lists (spatial), anything that involves rows and columns.

___

# License

MIT
