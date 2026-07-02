def recursive_backtracking_solve(path, step, curr_square, visited_mask, n, total_squares, move_row, move_col):
    if step == total_squares:
        return visited_mask, path

    curr_row = curr_square // n
    curr_col = curr_square % n

    move_idx = 0
    while move_idx < 8:
        nr = curr_row + move_row[move_idx]
        nc = curr_col + move_col[move_idx]

        if nr >= 0 and nr < n and nc >= 0 and nc < n:
            next_square = nr * n + nc
            bit = 1 << next_square
            if (visited_mask & bit) == 0:
                path[step] = next_square
                new_mask = visited_mask | bit
                res_mask, res_path = recursive_backtracking_solve(path, step + 1, next_square, new_mask, n, total_squares, move_row, move_col)
                if res_path is not None:
                    return res_mask, res_path
                path[step] = -1

        move_idx = move_idx + 1

    return visited_mask, None


def recursive_backtracking_knights_tour(n):
    total_squares = n * n
    move_row = [-2, -1, 1, 2, 2, 1, -1, -2]
    move_col = [-1, -2, -2, -1, 1, 2, 2, 1]

    path = []
    idx0 = 0
    while idx0 < total_squares:
        path.append(-1)
        idx0 = idx0 + 1

    start_square = 0
    path[0] = start_square
    visited_mask = 1 << start_square

    result_mask, result_path = recursive_backtracking_solve(path, 1, start_square, visited_mask, n, total_squares, move_row, move_col)

    if result_path is None:
        return None

    board = []
    r = 0
    while r < n:
        row_list = []
        c = 0
        while c < n:
            row_list.append(-1)
            c = c + 1
        board.append(row_list)
        r = r + 1

    step = 0
    while step < total_squares:
        square = result_path[step]
        row_val = square // n
        col_val = square % n
        board[row_val][col_val] = step
        step = step + 1

    return board


def print_board(board, n):
    if board is None:
        print("NO SOLUTION FOUND")
        return
    r = 0
    while r < n:
        line = ""
        c = 0
        while c < n:
            value = board[r][c]
            if value < 10:
                line = line + " " + str(value) + "  "
            else:
                line = line + str(value) + " "
            c = c + 1
        print(line)
        r = r + 1


if __name__ == "__main__":
    n = 5
    result_board = recursive_backtracking_knights_tour(n)
    print("recursive_backtracking -- bitmask-based visited tracking:")
    print_board(result_board, n)
