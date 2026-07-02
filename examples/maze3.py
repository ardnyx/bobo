# The Shared 30x30 Maze
# 'S' = Start, 'E' = Exit, '#' = Wall, '.' = Path
MAZE = [
    "##############################",
    "#S.......#.......#...........#",
    "##.#####.#.#####.#.#########.#",
    "#..#...#...#.....#.#.......#.#",
    "#.##.#.#####.###.#.#.#####.#.#",
    "#....#.......#...#...#...#...#",
    "####.#########.#######.#.###.#",
    "#....#.........#.......#.#...#",
    "#.####.#########.#####.#.#.###",
    "#....#.#.......#.....#...#...#",
    "####.#.#.#####.#####.#######.#",
    "#....#...#...#.....#.......#.#",
    "#.########.#.#####.#########.#",
    "#..........#.....#...........#",
    "#.##########.###.###########.#",
    "#.#..........#.#.#.........#.#",
    "#.#.##########.#.#.#######.#.#",
    "#.#.#..........#...#.....#.#.#",
    "#.#.#.##########.###.###.#.#.#",
    "#.#.#.#..........#...#...#.#.#",
    "#.#.#.#.##########.###.###.#.#",
    "#...#.#..........#.#.......#.#",
    "#####.##########.#.#.#######.#",
    "#.....#..........#.#.#.....#.#",
    "#.#####.##########.#.#.###.#.#",
    "#.#.....#..........#...#...#.#",
    "#.#.#####.##############.###.#",
    "#.#.......#................#E#",
    "##############################"
]

def get_start_and_exit(maze):
    start = exit_pos = None
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == 'S': start = (r, c)
            if maze[r][c] == 'E': exit_pos = (r, c)
    return start, exit_pos

def get_neighbors(r, c, maze):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    valid = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] != '#':
            valid.append((nr, nc))
    return valid

from collections import deque

def solve_bfs(maze):
    start, exit_pos = get_start_and_exit(maze)
    
    # The Queue stores tuples of (current_position, steps_taken)
    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        current, steps = queue.popleft()
        
        if current == exit_pos:
            return f"Found the absolute shortest path! It takes exactly {steps} steps."
            
        for neighbor in get_neighbors(current[0], current[1], maze):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, steps + 1))
                
    return "Exit is unreachable."

print("BFS:", solve_bfs(MAZE))