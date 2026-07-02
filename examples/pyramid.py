# 1. Decide how tall the pyramid should be
pyramid_height = 5
width = (pyramid_height * 2) - 1

# 2. Pre-allocate the entire 2D grid filled with blank dots
# This allows bobo to show the full canvas right from the start!
grid = []
for r in range(pyramid_height):
    row = []
    for c in range(width):
        row.append(".")
    grid.append(row)

# 3. Fill in the pyramid cell-by-cell so bobo can animate every step
for r in range(pyramid_height):
    number_of_stars = (r * 2) + 1
    
    # Calculate where the stars should start on this row
    start_col = pyramid_height - 1 - r
    end_col = start_col + number_of_stars
    
    # Manually place each star, one by one
    for c in range(start_col, end_col):
        grid[r][c] = "*"

# 4. Print the finished grid
print("Finished Pyramid:")
for row in grid:
    print("".join(row))