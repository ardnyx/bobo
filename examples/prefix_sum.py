def build_prefix_sum(matrix):
    """Build a 2D prefix sum table P where P[i][j] = sum of matrix[0..i-1][0..j-1]."""
    m, n = len(matrix), len(matrix[0])

    # P is (m+1) x (n+1) with a zero-padded border for simpler indexing
    P = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            P[i][j] = (
                matrix[i - 1][j - 1]
                + P[i - 1][j]
                + P[i][j - 1]
                - P[i - 1][j - 1]
            )

    return P


def submatrix_sum(P, r1, c1, r2, c2):
    """
    Query the sum of the submatrix from (r1, c1) to (r2, c2) inclusive
    using the prefix sum table P. All indices are 0-based.
    """
    return (
        P[r2 + 1][c2 + 1]
        - P[r1][c2 + 1]
        - P[r2 + 1][c1]
        + P[r1][c1]
    )


# Source matrix
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

print("Source matrix:")
for row in matrix:
    print("  ".join(f"{v:3d}" for v in row))

# Build prefix sum table
P = build_prefix_sum(matrix)

print("\nPrefix sum table P (1-indexed, with zero border):")
for row in P:
    print("  ".join(f"{v:4d}" for v in row))

# Query: sum of submatrix from (1,1) to (2,2)  →  6 + 7 + 10 + 11 = 34
r1, c1, r2, c2 = 1, 1, 2, 2
result = submatrix_sum(P, r1, c1, r2, c2)
print(f"\nSubmatrix sum from ({r1},{c1}) to ({r2},{c2}) = {result}")
print(f"  (Expected: {sum(matrix[i][j] for i in range(r1, r2+1) for j in range(c1, c2+1))})")
