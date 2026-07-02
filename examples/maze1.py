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

import random

def solve_random_mouse(maze):
    start, exit_pos = get_start_and_exit(maze)
    current = start
    steps = 0
    
    # BRUTE FORCE: Just keep walking randomly until we step on the 'E'.
    # Because the maze is a finite connected graph, mathematical probability 
    # dictates it WILL find the exit... eventually.
    while current != exit_pos:
        neighbors = get_neighbors(current[0], current[1], maze)
        current = random.choice(neighbors)
        steps += 1
        
        # Failsafe just in case it gets incredibly unlucky
        if steps > 500000:
            return f"Gave up after {steps} steps."
            
    return f"Found the exit! It only took {steps} entirely random steps."

print("Random Mouse:", solve_random_mouse(MAZE))