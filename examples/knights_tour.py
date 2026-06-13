BOARD_SIZE = 5

# All 8 possible L-shaped knight moves
MOVES = [
    (-2, -1), (-2, 1), (-1, -2), (-1, 2),
    (1, -2), (1, 2), (2, -1), (2, 1),
]

board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]


def is_valid(r, c):
    """Check if (r, c) is on the board and unvisited."""
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == 0


def count_onward_moves(r, c):
    """Count the number of valid moves from (r, c)."""
    return sum(1 for dr, dc in MOVES if is_valid(r + dr, c + dc))


def solve_knights_tour(start_r, start_c):
    """Attempt to solve the Knight's Tour starting from (start_r, start_c)."""
    board[start_r][start_c] = 1
    r, c = start_r, start_c

    for move_num in range(2, BOARD_SIZE * BOARD_SIZE + 1):
        # Gather all valid next moves
        candidates = []
        for dr, dc in MOVES:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc):
                candidates.append((count_onward_moves(nr, nc), nr, nc))

        if not candidates:
            return False  # Stuck — no valid moves

        # Warnsdorff's rule: pick the move with fewest onward moves
        candidates.sort()
        _, r, c = candidates[0]
        board[r][c] = move_num

    return True


# Solve starting from corner (0, 0)
success = solve_knights_tour(0, 0)

if success:
    print(f"Knight's Tour on {BOARD_SIZE}x{BOARD_SIZE} board:")
    for row in board:
        print("  ".join(f"{cell:2d}" for cell in row))
else:
    print("No solution found.")
