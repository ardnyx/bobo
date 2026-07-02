def iterative_backtracking_knights_tour(n):
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

    # Each frame: [curr_row, curr_col, next_move_number_to_assign, next_move_index_to_try]
    stack = []
    stack.append([0, 0, 1, 0])

    while len(stack) > 0:
        frame = stack[len(stack) - 1]
        curr_row = frame[0]
        curr_col = frame[1]
        move_count = frame[2]
        next_idx = frame[3]

        if move_count == n * n:
            return board

        advanced = False
        while next_idx < 8:
            nr = curr_row + move_row[next_idx]
            nc = curr_col + move_col[next_idx]
            next_idx = next_idx + 1
            frame[3] = next_idx  # remember progress for when we come back here

            if nr >= 0 and nr < n and nc >= 0 and nc < n:
                if board[nr][nc] == -1:
                    board[nr][nc] = move_count
                    stack.append([nr, nc, move_count + 1, 0])
                    advanced = True
                    break

        if advanced == False:
            popped = stack.pop()
            if len(stack) > 0:
                board[popped[0]][popped[1]] = -1

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
    result_board = iterative_backtracking_knights_tour(n)
    print("Iterative backtracking with an explicit stack:")
    print_board(result_board, n)
