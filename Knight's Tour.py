from bobo import bobo
bobo.configure(
    mapping={
        0: "\033[90m . \033[0m", 
        "KNIGHT": "\033[96m[♞]\033[0m"
    }, 
    delay=0.5, 
    clear_screen=True
)
# <-- bobo configuration insertion 1 -->

def knights_tour(n: int = 5, start_row: int = 0, start_col: int = 0) -> list[list[int]] | None:
    MOVES = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
             ( 1, -2), ( 1, 2), ( 2, -1), ( 2, 1)]

    def in_bounds(r, c):
        return 0 <= r < n and 0 <= c < n

    def degree(r, c, board):
        """Count how many unvisited squares the knight can reach from (r, c)."""
        return sum(
            1 for dr, dc in MOVES
            if in_bounds(r + dr, c + dc) and board[r + dr][c + dc] == 0
        )

    board = [[0] * n for _ in range(n)]
    r, c = start_row, start_col
    board[r][c] = 1

    # <-- bobo code insertion 2 -->
    bobo.show(board, message=f"Starting tour at ({r},{c})", overlays=[(r, c, "KNIGHT")])
    # <-- bobo code insertion 2 -->

    for move in range(2, n * n + 1):
        # Generate all valid next squares, sorted by Warnsdorff's degree
        neighbours = [
            (r + dr, c + dc)
            for dr, dc in MOVES
            if in_bounds(r + dr, c + dc) and board[r + dr][c + dc] == 0
        ]

        if not neighbours:
            return None  # Stuck — no solution from this starting point

        # Pick the neighbour with the smallest onward degree (Warnsdorff's rule)
        r, c = min(neighbours, key=lambda pos: degree(*pos, board))
        board[r][c] = move

        # <-- bobo code insertion 3 -->
        bobo.show(board, message=f"Move {move}: Jumped to ({r},{c})", overlays=[(r, c, "KNIGHT")])
        #<-- bobo code insertion 3 -->

    return board


def print_board(board: list[list[int]]) -> None:
    n = len(board)
    width = len(str(n * n))
    divider = "+" + ("-" * (width + 2) + "+") * n
    print(divider)
    for row in board:
        print("| " + " | ".join(f"{cell:{width}}" for cell in row) + " |")
        print(divider)


if __name__ == "__main__":
    N = 3
    START = (1, 1)

    print(f"Knight's Tour on a {N}×{N} board, starting at {START}\n")
    solution = knights_tour(N, *START)

    if solution:
        print_board(solution)
        print(f"\n✓ Complete tour of {N * N} squares found.")
    else:
        print("✗ No solution found from this starting position.")