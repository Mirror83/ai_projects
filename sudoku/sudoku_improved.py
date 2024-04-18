import numpy as np
from grid import grid

print("\nGrid:")
print(np.matrix(grid))

def is_valid_move(grid, row, col, num):
    """
    Check if placing 'num' at position (row, col) is a valid move.
    """
    # Check row
    if num in grid[row]:
        return False
    
    # Check column
    if num in [grid[i][col] for i in range(9)]:
        return False
    
    # Check subgrid
    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[subgrid_row + i][subgrid_col + j] == num:
                return False
    
    return True

def find_empty_cell(grid):
    """
    Find an empty cell in the Sudoku grid.
    """
    #create a list of tuples containing the indices of empty cells
    empty_cells = [(i, j) for i in range(9) for j in range(9) if grid[i][j] == 0] 
    if empty_cells:
        return min(empty_cells, key=lambda cell: len(get_possible_values(grid, *cell))) #heuristic selection
    return None, None  # No empty cell found

def get_possible_values(grid, row, col):
    """
    Get possible values that can be placed in the cell at (row, col).
    """
    possible_values = set(range(1, 10))
    possible_values -= set(grid[row])  # Remove values in the row
    possible_values -= set(grid[i][col] for i in range(9))  # Remove values in the column
    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    possible_values -= set(grid[subgrid_row + i][subgrid_col + j] for i in range(3) for j in range(3))  # Remove values in the subgrid
    return possible_values

def enforce_arc_consistency(grid):
    """
    Enforce arc consistency on the Sudoku grid.
    """
    # Initialize the queue with coordinates of empty cells
    queue = [(i, j) for i in range(9) for j in range(9) if grid[i][j] == 0]
    while queue:
        row, col = queue.pop(0)  # Pop coordinates of a cell from the queue for processing
        possible_values = get_possible_values(grid, row, col)  # Get possible values for the current cell
         # Iterate through possible values for the current cell
        for val in possible_values.copy():
            if not is_valid_move(grid, row, col, val): 
                possible_values.remove(val)
                grid[row][col] = 0 #reset the cell
                 # Add related cells to the queue for reprocessing
                queue.extend((row, j) for j in range(9) if grid[row][j] == 0) #same row
                queue.extend((i, col) for i in range(9) if grid[i][col] == 0) #same column
                #add the cells in the same subgrid
                subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
                queue.extend((subgrid_row + i, subgrid_col + j) for i in range(3) for j in range(3) if grid[subgrid_row + i][subgrid_col + j] == 0)
    return True # If the loop completes without returning False, the grid is consistent

def solve_sudoku(grid):
    """
    Solve the Sudoku puzzle using backtracking with arc consistency and heuristic selection of cells and values.
    """
    if not enforce_arc_consistency(grid):
        return False
    return backtrack_solve(grid)

def backtrack_solve(grid):
    """
    Recursively solve the Sudoku puzzle using backtracking with heuristic selection.
    """
    row, col = find_empty_cell(grid)  # Find the indices of the next empty cell in the grid
    if row is None:  # If no empty cell is found, the puzzle is solved
        return True
    
    # Try placing values in the empty cell based on heuristic selection
    possible_values = get_possible_values(grid, row, col)
    for num in sorted(possible_values):
        if is_valid_move(grid, row, col, num): #check if placing num is valid
            grid[row][col] = num #update grid
            enforce_arc_consistency(grid)
            if backtrack_solve(grid):  # Recursively solve the Sudoku puzzle
                return True
            grid[row][col] = 0  # Backtrack if the current configuration is not valid
    
    return False  # No valid number found for the current empty cell

# Solve the Sudoku puzzle
if solve_sudoku(grid):
    print("\nSolution:")
    print(np.matrix(grid))
else:
    print("\nNo solution exists.")


#Improvement by reduction of search space, early prunning of invalid choices, improved heuristic selection, systematic approch(rarely overlook valid options)
