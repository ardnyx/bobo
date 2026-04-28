def unique_paths(rows: int, cols: int) -> int:
    """Count unique paths from top-left to bottom-right (right/down only)."""
    dp = [[0] * cols for _ in range(rows)]

    # Base cases: entire first row and first column = 1 way each
    for r in range(rows):
        dp[r][0] = 1
    for c in range(cols):
        dp[0][c] = 1

    # Fill rest: ways to reach (r,c) = ways from above + ways from left
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]

    return dp[rows-1][cols-1]


def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    """
    Same problem, but grid[r][c] == 1 means there's an obstacle.
    Returns 0 if start or end is blocked.
    """
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[rows-1][cols-1] == 1:
        return 0

    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = 1

    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                continue
            if grid[r][c] == 1:      # obstacle
                dp[r][c] = 0
            else:
                from_top  = dp[r-1][c] if r > 0 else 0
                from_left = dp[r][c-1] if c > 0 else 0
                dp[r][c] = from_top + from_left

    return dp[rows-1][cols-1]


# --- Examples ---
print(unique_paths(5, 6))          # 126

grid = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],   # obstacle at (1,1)
    [0, 0, 0, 1, 0, 0],   # obstacle at (2,3)
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]
print(unique_paths_with_obstacles(grid))   # some number < 126