import heapq

def heuristic(a, b):
    """Manhattan distance — works well for 4-directional grids."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    """
    A* pathfinding on a 2D grid.
    grid: list of lists — 0 = open, 1 = wall
    start, goal: (row, col) tuples
    Returns: list of (row, col) from start to goal, or None if no path.
    """
    rows, cols = len(grid), len(grid[0])

    # Min-heap: (f_score, tie-breaker, node)
    open_heap = [(heuristic(start, goal), 0, start)]
    counter = 1  # tie-breaker so we never compare tuples

    came_from = {}
    g_score = {start: 0}

    while open_heap:
        _, _, current = heapq.heappop(open_heap)

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        r, c = current
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == 1:
                continue  # wall

            neighbor = (nr, nc)
            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f, counter, neighbor))
                counter += 1

    return None  # no path exists


grid = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
]

start = (0, 1)
goal  = (4, 0)

path = astar(grid, start, goal)

if path:
    print(f"Path found ({len(path)-1} steps):")
    for step in path:
        print(f"  {step}")
else:
    print("No path found.")