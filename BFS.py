from collections import deque
from bobo import bobo

bobo.configure(
    mapping={
        '.': "\033[90m . \033[0m", # . for Pathing
        '#': "\033[91m[W]\033[0m",  # W for Wall
        "HEAD": "\033[96m[@]\033[0m", # @ for the BFS Head
    },
    delay=0.6, # Slightly faster delay for BFS since it checks many cells
    clear_screen=True
)

def bfs_grid(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = {start}

    bobo.show(grid, message=f"Starting BFS at {start}")

    while queue:
        (r, c), path = queue.popleft()

        bobo.show(grid, message=f"Exploring cell ({r},{c})", overlays=[(r, c, "HEAD")])

        if (r, c) == end:
            return path  # Return the path taken to reach the end

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:  # Up, Down, Left, Right
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in visited
                    and grid[nr][nc] != '#'):   # '#' = wall
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))  # Highlight current cell
    return None  # No path found


# Example usage
grid = [
    ['.', '.', '.', '#', '.'],
    ['#', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.'],
    ['.', '#', '#', '#', '.'],
    ['.', '.', '.', '.', '.'],
]

start = (0, 0)
end   = (4, 4)
path  = bfs_grid(grid, start, end)
print("Path found:", path)