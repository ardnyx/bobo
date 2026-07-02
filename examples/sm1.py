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

def sm1():
    matrix = get_matrix()
    rows, cols = len(matrix), len(matrix[0])
    
    # Extract to 1D, sort, and create an iterator
    flat = sorted([val for row in matrix for val in row])
    flat_iter = iter(flat)
    
    # Rebuild the 2D grid
    for r in range(rows):
        for c in range(cols):
            matrix[r][c] = next(flat_iter)
            
    return matrix

print_matrix("Solution: ", sm1())