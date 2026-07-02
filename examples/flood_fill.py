def print_grid(label, g):
    """Pretty-print a grid with a label."""
    symbols = {0: " . ", 1: " # ", 2: " @ "}
    print(f"{label}:")
    for row in g:
        print("".join(symbols[cell] for cell in row))
    print()


# A grid with a connected region of 0s (background) bounded by 1s (walls)
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
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1],
]

print_grid("Initial", grid)


def flood_fill(g, r, c, target, replacement):
    """
    Recursive DFS flood fill: mutate the grid in-place, spreading
    outward from (r, c) into every connected cell that matches
    `target`, replacing it with `replacement`.

    This is ONE of several valid strategies. Others that produce the
    same final grid but with a visibly different mutation order:
      - Iterative DFS using an explicit stack instead of recursion
      - BFS using a queue (fills outward in "rings" instead of
        following one branch all the way before backtracking)
      - Scanline fill (fills whole contiguous row segments at once,
        then queues the segments above/below)
    """
    rows, cols = len(g), len(g[0])

    if r < 0 or r >= rows or c < 0 or c >= cols:
        return
    if g[r][c] != target:
        return

    # Mutate first, THEN recurse — this is the step that matters.
    # Doing it in the wrong order (recursing before mutating) is the
    # classic flood-fill bug: it re-visits the same cell forever.
    g[r][c] = replacement

    flood_fill(g, r + 1, c, target, replacement)
    flood_fill(g, r - 1, c, target, replacement)
    flood_fill(g, r, c + 1, target, replacement)
    flood_fill(g, r, c - 1, target, replacement)


flood_fill(grid, 1, 1, target=0, replacement=2)

print_grid("After flood fill from (1,1)", grid)