# 1. Define two matrices of the same size (3x2)
matrix_a = [
    [1, 2],
    [3, 4],
    [5, 6]
]

matrix_b = [
    [10, 20],
    [30, 40],
    [50, 60]
]

# 2. Figure out the dimensions (number of rows and columns)
number_of_rows = len(matrix_a)
number_of_columns = len(matrix_a[0])

# 3. Manually build an empty result matrix filled with zeros
result_matrix = []

for i in range(number_of_rows):
    empty_row = []
    for j in range(number_of_columns):
        empty_row.append(0)  # Put a zero in every column slot
    result_matrix.append(empty_row)  # Add the filled row to the matrix

# 4. Do the actual addition
for i in range(number_of_rows):
    for j in range(number_of_columns):
        # Take the number from A and the number from B at the exact same spot, add them, and put them in the result
        result_matrix[i][j] = matrix_a[i][j] + matrix_b[i][j]

# 5. Print the result so it looks like a matrix
print("The added matrix is:")
for row in result_matrix:
    print(row)