from collections import deque

def flood_fill(grid, start_row, start_col, new_color):
    # 1. Store grid dimensions explicitly
    rows = len(grid)
    cols = len(grid[0])
    
    # 2. Identify the target color to replace
    old_color = grid[start_row][start_col]
    
    # 3. Base case: If the start is already the new color, do nothing
    if old_color == new_color:
        return grid
        
    # 4. Initialize a Queue for Breadth-First Search
    # Note: We use deque for O(1) pops, which is standard in DSA
    queue = deque()
    
    # Enqueue the starting coordinates as a tuple
    queue.append((start_row, start_col))
    
    # Change the color of the starting node immediately
    grid[start_row][start_col] = new_color
    
    # 5. Define explicit arrays for 4-directional movement (Up, Down, Left, Right)
    d_row = [-1, 1, 0, 0]
    d_col = [0, 0, -1, 1]
    
    # 6. Process the queue until it is empty
    while len(queue) > 0:
        # Dequeue the front element
        current = queue.popleft()
        
        # Explicitly assign coordinates without pythonic tuple unpacking
        curr_r = current[0]
        curr_c = current[1]
        
        # Loop through the 4 possible directions using a standard while loop
        i = 0
        while i < 4:
            next_r = curr_r + d_row[i]
            next_c = curr_c + d_col[i]
            
            # Explicit boundary checking (no chained comparisons)
            if next_r >= 0 and next_r < rows and next_c >= 0 and next_c < cols:
                # Check if the adjacent cell is the color we need to fill
                if grid[next_r][next_c] == old_color:
                    # Update the grid color
                    grid[next_r][next_c] = new_color
                    # Enqueue the new coordinates to process its neighbors later
                    queue.append((next_r, next_c))
            
            i += 1
            
    return grid

# --- Execution ---

grid = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 1, 1],
    [1, 1, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1],
]

# Let's run a test starting at row 1, column 1 (which is a 0) 
# and fill it with the number 2.
start_row_index = 1
start_col_index = 1
replacement_color = 2

# Call the function
filled_grid = flood_fill(grid, start_row_index, start_col_index, replacement_color)

# Print the result row by row (using a basic loop)
row_idx = 0
while row_idx < len(filled_grid):
    print(filled_grid[row_idx])
    row_idx += 1