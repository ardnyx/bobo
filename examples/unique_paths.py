def count_unique_paths(m, n):
    """Count unique paths on an m x n grid using dynamic programming."""
    dp = [[0] * n for _ in range(m)]

    # First row and first column have exactly 1 path each
    for i in range(m):
        dp[i][0] = 1
    for j in range(n):
        dp[0][j] = 1

    # Fill the rest: each cell = sum of cell above + cell to the left
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp, dp[m - 1][n - 1]


def count_unique_paths_with_obstacles(grid):
    """Count unique paths avoiding obstacles (1 = blocked, 0 = open)."""
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]

    # Starting cell
    dp[0][0] = 0 if grid[0][0] == 1 else 1

    # First column
    for i in range(1, m):
        dp[i][0] = 0 if grid[i][0] == 1 else dp[i - 1][0]

    # First row
    for j in range(1, n):
        dp[0][j] = 0 if grid[0][j] == 1 else dp[0][j - 1]

    # Fill the rest
    for i in range(1, m):
        for j in range(1, n):
            if grid[i][j] == 1:
                dp[i][j] = 0
            else:
                dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp, dp[m - 1][n - 1]


# --- Part 1: Basic unique paths ---
m, n = 5, 5
dp, result = count_unique_paths(m, n)
print(f"Part 1: Unique paths on a {m}x{n} grid = {result}")
print("DP table:")
for row in dp:
    print("  ".join(f"{v:3d}" for v in row))

print()

# --- Part 2: Unique paths with obstacles ---
grid = [
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0],
]

dp, result = count_unique_paths_with_obstacles(grid)
print(f"Part 2: Unique paths on a 4x4 grid with obstacles = {result}")
print("Obstacle grid:")
for row in grid:
    print("  ".join(str(v) for v in row))
print("DP table:")
for row in dp:
    print("  ".join(f"{v:3d}" for v in row))
