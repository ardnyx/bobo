def recursive_solve(board, curr_row, curr_col, move_count, n, move_row, move_col):
    if move_count == n * n:
        return True

    move_index = 0
    while move_index < 8:
        next_row = curr_row + move_row[move_index]
        next_col = curr_col + move_col[move_index]

        if next_row >= 0 and next_row < n and next_col >= 0 and next_col < n:
            if board[next_row][next_col] == -1:
                board[next_row][next_col] = move_count
                result = recursive_solve(board, next_row, next_col, move_count + 1, n, move_row, move_col)
                if result == True:
                    return True
                board[next_row][next_col] = -1

        move_index = move_index + 1

    return False


def recursive_knights_tour(n):
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

    move_row = [-2, -1, 1, 2, 2, 1, -1, -2]
    move_col = [-1, -2, -2, -1, 1, 2, 2, 1]

    board[0][0] = 0

    success = recursive_solve(board, 0, 0, 1, n, move_row, move_col)

    if success == True:
        return board
    else:
        return None


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
    result_board = recursive_knights_tour(n)
    print("Plain recursive backtracking, fixed move order:")
    print_board(result_board, n)
