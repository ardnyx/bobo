from collections import deque

grid = [
    ['.', '.', '.', '#', '.'],
    ['#', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.'],
    ['.', '#', '#', '#', '.'],
    ['.', '.', '.', '.', '.'],
]

rows, cols = len(grid), len(grid[0])
start = (0, 0)
end = (4, 4)

# BFS
queue = deque()
queue.append((start, [start]))
visited = {start}

path_found = None

while queue:
    (r, c), path = queue.popleft()

    if (r, c) == end:
        path_found = path
        break

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == '.':
            visited.add((nr, nc))
            queue.append(((nr, nc), path + [(nr, nc)]))

if path_found:
    print(f"Path found ({len(path_found)} steps):")
    for step in path_found:
        print(f"  {step}")
else:
    print("No path found.")
