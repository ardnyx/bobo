UNSORTED_MATRIX = [
    [45, 12, 89,  3],
    [22,  5, 67, 18],
    [91, 34,  7, 50],
    [11, 76, 29,  2]
]

def get_matrix():
    return [row[:] for row in UNSORTED_MATRIX]

def print_matrix(name, matrix):
    print(f"\n=== {name} ===")
    for row in matrix:
        print(f"[{', '.join(f'{n:2}' for n in row)}]")

def student_d_over_thinker():
    matrix = get_matrix()
    rows, cols = len(matrix), len(matrix[0])
    
    while True:
        matrix_before = [row[:] for row in matrix]
        
        # Step 1: Sort all rows independently
        for r in range(rows):
            matrix[r].sort()
            
        # Step 2: Sort all columns independently
        for c in range(cols):
            # Extract the column, sort it, and put it back
            col_values = sorted([matrix[r][c] for r in range(rows)])
            for r in range(rows):
                matrix[r][c] = col_values[r]
                
        # If the matrix didn't change this pass, it has converged!
        if matrix == matrix_before:
            break
            
    return matrix

print_matrix("Solution: ", student_d_over_thinker())
# OUTPUT SPOILER:
# [ 2,  5,  7, 18]
# [ 3, 12, 29, 50]
# [11, 34, 67, 89]
# [22, 45, 76, 91]