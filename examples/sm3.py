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

def sm3():
    matrix = get_matrix()
    rows, cols = len(matrix), len(matrix[0])
    
    # Find the absolute maximum value in the matrix
    max_val = max(max(row) for row in matrix)
    
    # Create a frequency array
    counts = [0] * (max_val + 1)
    for row in matrix:
        for val in row:
            counts[val] += 1
            
    # Overwrite the matrix sequentially
    current_val = 0
    for r in range(rows):
        for c in range(cols):
            # Fast-forward to the next number that actually exists
            while counts[current_val] == 0:
                current_val += 1
            
            matrix[r][c] = current_val
            counts[current_val] -= 1
            
    return matrix

print_matrix("Solution: ", sm3())