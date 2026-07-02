def print_grid(label, g):
    """Pretty-print a grid with a label."""
    print(f"{label}:")
    for row in g:
        print(" ".join(str(cell) if cell != 0 else "." for cell in row))
    print()

# 4x4 Sudoku: rows, columns, and 2x2 boxes must each contain 1-4.
# 0 marks an empty cell to be solved.
grid = [
    [0, 0, 0, 0],
    [0, 4, 2, 0],
    [0, 0, 0, 0],
    [3, 0, 1, 0],
]

print_grid("Initial", grid)

SIZE = 4
BOX = 2


def is_valid(g, r, c, val):
    """Check row, column, and 2x2 box constraints for placing val at (r, c)."""
    for i in range(SIZE):
        if g[r][i] == val or g[i][c] == val:
            return False

    box_r, box_c = (r // BOX) * BOX, (c // BOX) * BOX
    for i in range(box_r, box_r + BOX):
        for j in range(box_c, box_c + BOX):
            if g[i][j] == val:
                return False

    return True


def find_empty(g):
    """Find the next empty cell, scanning row-major."""
    for r in range(SIZE):
        for c in range(SIZE):
            if g[r][c] == 0:
                return r, c
    return None


def solve(g):
    """Backtracking solver: place a candidate, recurse, undo on failure."""
    empty = find_empty(g)
    if empty is None:
        return True  # No empty cells left — solved.

    r, c = empty
    for val in range(1, SIZE + 1):
        if is_valid(g, r, c, val):
            g[r][c] = val          # mutation #1: tentative placement

            if solve(g):
                return True

            g[r][c] = 0            # mutation #2: undo, backtrack

    return False

success = solve(grid)

if success:
    print_grid("Solved", grid)
else:
    print("No solution found.")