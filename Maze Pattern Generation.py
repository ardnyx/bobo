from bobo import bobo
import random

# Tell Bobo how to draw the maze
bobo.configure(mapping={
    0: "\033[90m██\033[0m",  # Dark gray wall
    1: "  "                  # Empty space for passage
}, delay=0.05, clear_screen=True)

WALL    = 0
PASSAGE = 1
ROWS, COLS = 21, 41 

def make_grid():
    return [[WALL] * COLS for _ in range(ROWS)]

def generate_maze(grid):
    stack = [(1, 1)]
    grid[1][1] = PASSAGE

    while stack:
        r, c = stack[-1] 

        neighbors = []
        for dr, dc in [(-2,0),(2,0),(0,-2),(0,2)]:
            nr, nc = r+dr, c+dc
            if 1 <= nr < ROWS-1 and 1 <= nc < COLS-1:
                if grid[nr][nc] == WALL:
                    neighbors.append((nr, nc, dr, dc))

        if neighbors:
            nr, nc, dr, dc = random.choice(neighbors)
            grid[r + dr//2][c + dc//2] = PASSAGE  
            grid[nr][nc] = PASSAGE                
            stack.append((nr, nc))
            
            # ---> MAGIC BOBO LINE <---
            bobo.show(grid, "Carving maze...")
            
        else:
            stack.pop() 
            
            # ---> MAGIC BOBO LINE <---
            bobo.show(grid, "Backtracking...")

    return grid

grid = make_grid()
generate_maze(grid)
print("\n--- Maze Complete ---")