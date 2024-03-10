import numpy as np
from grid import grid

print("\nGrid:")
print(np.matrix(grid))

def possible(y, x, n):
    global grid
    # Check row and column
    if n in grid[y] or n in [grid[i][x] for i in range(9)]:
        return False
    # Check 3x3 grid
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[y0 + i][x0 + j] == n:
                return False
    return True

def solve():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        grid[y][x] = n
                        if solve():  # Recursively call itself
                            return True
                        grid[y][x] = 0  # Backtrack if contradiction
                return False
    return True

solve()  # Call solve function to solve Sudoku

print("\nSolution:")
print(np.matrix(grid))
