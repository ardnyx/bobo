import random

ROWS = 10
COLS = 10

# Initialize grid: all walls (0)
grid = [[0] * COLS for _ in range(ROWS)]


def carve_maze(start_r, start_c):
    """Carve passages through the grid using stack-based DFS."""
    # Directions: (row_step, col_step) — move by 2 to skip wall cells
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    stack = [(start_r, start_c)]
    grid[start_r][start_c] = 1  # Mark starting cell as passage

    while stack:
        r, c = stack[-1]

        # Find unvisited neighbors (2 cells away)
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 < nr < ROWS - 1 and 0 < nc < COLS - 1 and grid[nr][nc] == 0:
                neighbors.append((nr, nc, dr, dc))

        if neighbors:
            # Pick a random unvisited neighbor
            nr, nc, dr, dc = random.choice(neighbors)

            # Carve passage: open the wall between current and neighbor
            grid[r + dr // 2][c + dc // 2] = 1
            grid[nr][nc] = 1

            stack.append((nr, nc))
        else:
            # Backtrack
            stack.pop()


# Start carving from (1, 1)
random.seed(42)  # Fixed seed for reproducible output
carve_maze(1, 1)

# Display the maze
for row in grid:
    print("".join("  " if cell == 1 else "##" for cell in row))

print("\nMaze Complete")
