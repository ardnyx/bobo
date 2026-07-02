# Shared Setup: A helper function to draw the chessboard
def print_board(name, solution_array):
    print(f"\n=== {name} ===")
    for col in solution_array:
        # Draw a row of 8 dots, and replace one dot with a 'Q'
        row_str = ['.'] * 8
        if col != -1:
            row_str[col] = 'Q'
        print(" ".join(row_str))

import copy

def solve_raycaster():
    def place_queen(grid, row):
        if row == 8: return grid
        
        for col in range(8):
            if grid[row][col] == '.':
                new_grid = copy.deepcopy(grid)
                new_grid[row][col] = 'Q'
                
                for r in range(row + 1, 8):
                    new_grid[r][col] = 'x'
                    
                # Block the Diagonals
                for dr, dc in [(1, -1), (1, 1)]:
                    r, c = row + dr, col + dc
                    while r < 8 and 0 <= c < 8:
                        new_grid[r][c] = 'x'
                        r, c = r + dr, c + dc
                        
                # Recurse into the next row
                result = place_queen(new_grid, row + 1)
                if result: return result
                
        return None

    # Start with a pristine 2D grid
    empty_grid = [['.'] * 8 for _ in range(8)]
    solved_grid = place_queen(empty_grid, 0)
    
    # Translate the 2D grid back into our 1D format for printing
    solution = [-1] * 8
    for r in range(8):
        for c in range(8):
            if solved_grid[r][c] == 'Q': solution[r] = c
    return solution

print_board("Solution: ", solve_raycaster())