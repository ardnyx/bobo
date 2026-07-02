def warnsdorff_count_onward_moves(board, row, col, n, move_row, move_col):
    count = 0
    idx = 0
    while idx < 8:
        nr = row + move_row[idx]
        nc = col + move_col[idx]
        if nr >= 0 and nr < n and nc >= 0 and nc < n:
            if board[nr][nc] == -1:
                count = count + 1
        idx = idx + 1
    return count


def warnsdorff_solve(board, curr_row, curr_col, move_count, n, move_row, move_col):
    if move_count == n * n:
        return True

    candidates_row = []
    candidates_col = []
    candidates_degree = []

    idx = 0
    while idx < 8:
        nr = curr_row + move_row[idx]
        nc = curr_col + move_col[idx]
        if nr >= 0 and nr < n and nc >= 0 and nc < n:
            if board[nr][nc] == -1:
                deg = warnsdorff_count_onward_moves(board, nr, nc, n, move_row, move_col)
                candidates_row.append(nr)
                candidates_col.append(nc)
                candidates_degree.append(deg)
        idx = idx + 1

    # Manual selection sort (ascending by degree) -- deliberately avoiding
    # the built-in sorted() function.
    total = len(candidates_degree)
    i = 0
    while i < total - 1:
        min_idx = i
        j = i + 1
        while j < total:
            if candidates_degree[j] < candidates_degree[min_idx]:
                min_idx = j
            j = j + 1
        if min_idx != i:
            temp_d = candidates_degree[i]
            candidates_degree[i] = candidates_degree[min_idx]
            candidates_degree[min_idx] = temp_d

            temp_r = candidates_row[i]
            candidates_row[i] = candidates_row[min_idx]
            candidates_row[min_idx] = temp_r

            temp_c = candidates_col[i]
            candidates_col[i] = candidates_col[min_idx]
            candidates_col[min_idx] = temp_c
        i = i + 1

    k = 0
    while k < total:
        nr = candidates_row[k]
        nc = candidates_col[k]
        board[nr][nc] = move_count
        result = warnsdorff_solve(board, nr, nc, move_count + 1, n, move_row, move_col)
        if result == True:
            return True
        board[nr][nc] = -1
        k = k + 1

    return False


def warnsdorff_knights_tour(n):
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

    success = warnsdorff_solve(board, 0, 0, 1, n, move_row, move_col)

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
    result_board = warnsdorff_knights_tour(n)
    print("Warnsdorff heuristic ordering, with backtracking fallback:")
    print_board(result_board, n)
