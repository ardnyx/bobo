from bobo import bobo

# Configure our animation speed
bobo.configure(delay=0.8)

# 0 = empty, 1 = tetromino block, 2 = center pivot point
grid = [
    [0, 1, 0],
    [0, 2, 0],
    [0, 1, 1]
]

bobo.show(grid, "Initial L-Piece")

def rotate_matrix(matrix):
    n = len(matrix)
    
    # Step 1: Transpose the matrix (swap rows and columns)
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
            # Visualize every swap during the transpose phase
            bobo.show(matrix, f"Transposing: swapped ({i},{j}) with ({j},{i})")
            
    # Step 2: Reverse each row
    for i in range(n):
        matrix[i].reverse()
        # Visualize the row reversal
        bobo.show(matrix, f"Reversing row {i}")

print("\n--- Starting Algorithm ---")
rotate_matrix(grid)
print("\n--- Algorithm Finished ---")