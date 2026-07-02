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

def solve_pheromones(maze):
    start, exit_pos = get_start_and_exit(maze)
    
    # Dictionary to track how many times we've stepped on a tile
    visited_counts = {start: 1}
    current = start
    steps = 0
    
    while current != exit_pos:
        neighbors = get_neighbors(current[0], current[1], maze)
        
        # CREATIVE LOGIC: Look at all valid adjacent tiles. 
        # Move to the one with the lowest "visited" score. 
        # This naturally pushes the algorithm out of dead ends, 
        # because dead ends build up a high "scent" score.
        best_neighbor = None
        lowest_visits = float('inf')
        
        for n in neighbors:
            visits = visited_counts.get(n, 0)
            if visits < lowest_visits:
                lowest_visits = visits
                best_neighbor = n
                
        current = best_neighbor
        visited_counts[current] = visited_counts.get(current, 0) + 1
        steps += 1
        
    return f"Found the exit in {steps} steps using pheromones."

print("Pheromone Trail:", solve_pheromones(MAZE))