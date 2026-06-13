def print_grid(label, g):
    """Pretty-print a grid with a label."""
    symbols = {0: " . ", 1: " # ", 2: " O "}
    print(f"{label}:")
    for row in g:
        print("".join(symbols[cell] for cell in row))
    print()


# T-tetromino centered on pivot
grid = [
    [0, 0, 0],
    [1, 2, 1],
    [0, 0, 1],
]

print_grid("Initial", grid)

# Step 1: Transpose
n = len(grid)
for i in range(n):
    for j in range(i + 1, n):
        grid[i][j], grid[j][i] = grid[j][i], grid[i][j]

# Step 2: Reverse each row
for row in grid:
    row.reverse()

print_grid("Rotated 90° clockwise", grid)
