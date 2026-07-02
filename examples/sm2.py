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

def sm2():
    matrix = get_matrix()
    rows, cols = len(matrix), len(matrix[0])
    
    # Helper to map a 1D index (e.g., 5) to 2D coordinates (Row 1, Col 1)
    def get_val(idx):
        return matrix[idx // cols][idx % cols]
        
    def set_val(idx, val):
        matrix[idx // cols][idx % cols] = val

    # Standard Quicksort, but using the virtual 1D indices
    def quicksort(low, high):
        if low < high:
            pivot_idx = partition(low, high)
            quicksort(low, pivot_idx - 1)
            quicksort(pivot_idx + 1, high)

    def partition(low, high):
        pivot = get_val(high)
        i = low - 1
        for j in range(low, high):
            if get_val(j) <= pivot:
                i += 1
                # Swap values using virtual indices
                temp = get_val(i)
                set_val(i, get_val(j))
                set_val(j, temp)
                
        temp = get_val(i + 1)
        set_val(i + 1, get_val(high))
        set_val(high, temp)
        return i + 1

    quicksort(0, (rows * cols) - 1)
    return matrix

print_matrix("Solution: ", sm2())