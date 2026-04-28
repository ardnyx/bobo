from bobo import bobo

# Configure our ghost markers for the query phase
bobo.configure(mapping={
    "ADD": "\033[92m [+]\033[0m",  # Green Plus
    "SUB": "\033[91m [-]\033[0m",  # Red Minus
}, delay=1, clear_screen=True)

def build_prefix_sum(grid):
    """Build a 2D prefix sum table from a grid."""
    rows = len(grid)
    cols = len(grid[0])

    # P is (rows+1) x (cols+1) with an extra row/col of zeros as padding
    P = [[0] * (cols + 1) for _ in range(rows + 1)]

    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            P[r][c] = (grid[r-1][c-1]
                       + P[r-1][c]
                       + P[r][c-1]
                       - P[r-1][c-1])
                    
        # ---> BOBO STANDARD CAMERA <---
        bobo.show(P, message=f"Calculating Prefix Sum for ({r},{c})")
    return P


def query_submatrix(P, r1, c1, r2, c2):
    """
    Return the sum of the submatrix from (r1, c1) to (r2, c2) inclusive.
    All indices are 0-based relative to the original grid.
    """
    # ---> BOBO GHOST OVERLAYS <---
    ghosts = [
        (r2+1, c2+1, "ADD"), # Bottom right corner (Total area)
        (r1,   c2+1, "SUB"), # Top right corner (Subtract upper block)
        (r2+1, c1,   "SUB"), # Bottom left corner (Subtract left block)
        (r1,   c1,   "ADD")  # Top left corner (Add back the double-subtracted intersection)
    ]
    bobo.show(P, message=f"Querying submatrix ({r1},{c1}) to ({r2},{c2})", overlays=ghosts)
    return (P[r2+1][c2+1]
            - P[r1][c2+1]
            - P[r2+1][c1]
            + P[r1][c1])


# --- Example ---
grid = [
    [3, 0, 1, 4, 2],
    [5, 6, 3, 2, 1],
    [1, 2, 0, 1, 5],
    [4, 1, 0, 1, 7],
    [1, 0, 3, 0, 5],
]

P = build_prefix_sum(grid)

# Optional: Pause longer before the query so the user can look at the finished table
import time
time.sleep(1)
# Query: sum of rows 1-3, cols 1-3
r1, c1, r2, c2 = 1, 1, 3, 3
result = query_submatrix(P, r1, c1, r2, c2)
print(f"Sum of submatrix ({r1},{c1}) → ({r2},{c2}): {result}")
# Output: Sum of submatrix (1,1) → (3,3): 17