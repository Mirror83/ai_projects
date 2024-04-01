from enum import Enum, auto


class CellState(Enum):
    OCCUPIED = auto()
    UNOCCUPIED = auto()

    def draw(self) -> str:
        if self == CellState.UNOCCUPIED:
            return "."
        else:
            return "♕"


class QueensBoard:
    """
    The n-queens _board is used for positioning queens on a square _board
    for use in solving the n-queens problem. The _board consists of n x n
    squares arranged in rows and columns, with each square identified by indices
    in the range 0 - n (not including n).
    """

    def __init__(self, n: int = 4):
        """Creates an n x n empty _board."""
        self._board = [
            [CellState.UNOCCUPIED for _ in range(n)] for _ in range(n)]
        self._num_queens = 0

    def size(self):
        """Returns the size of the _board."""
        return len(self._board)

    def check_coord_validity(self, row: int, col: int) -> None:
        """:raises: ValueError if the row and col provided are not within the bounds of the grid."""
        if (row > self.size() or col > self.size()) or (row < 0 or col < 0):
            raise ValueError("Invalid coordinates")

    def num_queens(self):
        """Returns the number of queens currently positioned on the _board"""
        return self._num_queens

    def unguarded(self, row: int, col: int) -> bool:
        """Return whether the given square is currently guarded."""
        self.check_coord_validity(row, col)

        if self._board[row][col] == CellState.OCCUPIED:
            return False

        # Current row
        for i, cell in enumerate(self._board[row]):
            if i != col and cell == CellState.OCCUPIED:
                return False

        # Current column
        for current_row in range(self.size()):
            if self._board[current_row][col] == CellState.OCCUPIED:
                return False

        # Relative negatively sloping diagonal
        current_col = col + 1
        for current_row in range(row + 1, self.size()):
            if current_col >= self.size():
                break

            if (current_row != row and current_col != col) and self._board[current_row][current_col] == CellState.OCCUPIED:
                return False
            current_col += 1

        current_col = col - 1
        for current_row in range(row - 1, -1, -1):
            if current_col < 0:
                break
            if (current_row != row and current_col != col) and self._board[current_row][current_col] == CellState.OCCUPIED:
                return False
            current_col -= 1

        # Relative positively sloping diagonal
        current_col = col - 1
        for current_row in range(row + 1, self.size()):
            if current_col < 0:
                break

            if (current_row != row and current_col != col) and self._board[current_row][current_col] == CellState.OCCUPIED:
                return False
            current_col -= 1

        current_col = col + 1
        for current_row in range(row - 1, -1, -1):
            if current_col >= self.size():
                break
            if (current_row != row and current_col != col) and self._board[current_row][current_col] == CellState.OCCUPIED:
                return False
            current_col += 1

        # After all conditions have passed
        return True

    def place_queen(self, row: int, col: int):
        """Places a queen on the _board at position (row, col)"""
        self.check_coord_validity(row, col)

        if self._board[row][col] == CellState.UNOCCUPIED:
            self._board[row][col] = CellState.OCCUPIED
            self._num_queens += 1
        else:
            # Think of a better way to handle this
            raise Exception("Position is already occupied!")

    def remove_queen(self, row: int, col: int):
        """Removes the queen from position (row, col)"""
        self.check_coord_validity(row, col)

        if self._board[row][col] == CellState.OCCUPIED:
            self._board[row][col] = CellState.UNOCCUPIED
            self._num_queens -= 1
        else:
            # Think of a better way to handle this too
            raise Exception("Position is already unoccupied")

    def reset(self):
        """
        Resets the _board to its original state by removing all queens
        currently placed on the _board.
        """

        if self.num_queens() > 0:
            self._board = [[CellState.UNOCCUPIED for _ in range(
                self.size())] for _ in range(self.size())]
            self._num_queens = 0

    def draw(self):
        """
        Prints the _board in a readable format using characters to represent
        the squares containing the queens and the empty squares.
        """
        print(f"Occupied = {CellState.OCCUPIED.draw()}")
        print(f"Empty = {CellState.UNOCCUPIED.draw()}")
        print("\nBoard")
        print("-----")
        for row in self._board:
            for cell in row:
                print(f"{cell.draw()} ", end="")

            print()

        print()


def solve_n_queens(board: QueensBoard, col: int = 0) -> bool:
    """
    This function uses backtracking to solve the n-queens problem for
    an n by n board. It returns after finding the first solution

    :param board: The board in which the queens are placed.
    :param col: The current column in which we are attempting to place a queen.
                Default value is 0 as checking for the solution should start from
                the first column.
    :return: A boolean value showing whether a solution was found or not.
    """

    # A solution was found if n-queens have been placed on the board
    if board.num_queens() == board.size():
        return True
    else:
        # Find the next unguarded square within the current column
        for row in range(board.size()):
            if board.unguarded(row, col):
                board.place_queen(row, col)
                # Continue placing queens in the following columns
                if solve_n_queens(board, col + 1):
                    return True  # We are done if a solution is found
                else:
                    # No solution was found with the queen in this square,
                    # so it has to be removed from the _board
                    board.remove_queen(row, col)

        # If the loop terminates, no queen can be placed within the current column
        return False
