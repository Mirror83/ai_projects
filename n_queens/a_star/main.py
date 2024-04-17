import enum
import heapq
from typing import List, Tuple


# Visualization of the chessboard
# ♕ . . . . . . .
# . . . . ♕ . . .
# . . . . . . . ♕
# . . . . . ♕ . .
# . . ♕ . . . . .
# . . . . . . ♕ .
# . ♕ . . . . . .
# . . . ♕ . . . .
#

class CellState(enum.Enum):
    OCCUPIED = enum.auto()
    UNOCCUPIED = enum.auto()

    def draw(self) -> str:
        if self == CellState.UNOCCUPIED:
            return "."
        else:
            return "♕"

    def __str__(self) -> str:
        return self.draw()

    def __repr__(self) -> str:
        return self.draw()

    def __gt__(self, other: 'CellState') -> bool:
        if self == CellState.OCCUPIED and other == CellState.UNOCCUPIED:
            return True
        return False

    def __lt__(self, other: 'CellState') -> bool:
        if self == CellState.UNOCCUPIED and other == CellState.OCCUPIED:
            return True
        return False


class Cell:
    def __init__(self, row: int, col: int):
        self.value = CellState.UNOCCUPIED
        self.row = row
        self.col = col
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: 'Cell'):
        return self.row == other.row and self.col == other.col

    def __repr__(self):
        return f'\nCell({self.row}, {self.col}) -> {self.value} g: {self.g} h: {self.h} f: {self.f}\n'

    def __lt__(self, other: 'Cell'):
        return self.f < other.f

    def __gt__(self, other: 'Cell'):
        return self.f > other.f


class QueensBoard:
    def __init__(self, n) -> None:
        self.n = n
        self.board = [[Cell(i, j) for j in range(n)] for i in range(n)]

    def draw_board(self) -> None:
        for row in self.board:
            print(" ".join(cell.value.draw() for cell in row))

    def place_queen(self, row: int, col: int) -> None:
        self.board[row][col].value = CellState.OCCUPIED


class A_Star_Search:
    def __init__(self, n) -> None:
        self.n = n
        self.board = QueensBoard(n)

    def heuristic(self, cell: Cell) -> int:
        # Current row
        row = cell.row
        col = cell.col
        h = 0
        for i, cell in enumerate(self.board.board[row]):
            if i != col and cell.value == CellState.OCCUPIED:
                h += 1

        # Current column
        for current_row in range(self.board.n):
            if self.board.board[current_row][col].value == CellState.OCCUPIED:
                h += 1

        # Relative negatively sloping diagonal
        current_col = col + 1
        for current_row in range(row + 1, self.board.n):
            if current_col < self.board.n and self.board.board[current_row][current_col].value == CellState.OCCUPIED:
                h += 1
            current_col += 1

        # Relative positively sloping diagonal
        current_col = col - 1
        for current_row in range(row + 1, self.board.n):
            if current_col >= 0 and self.board.board[current_row][current_col].value == CellState.OCCUPIED:
                h += 1
            current_col -= 1

        return h

    def solve(self):

        for i in range(self.n):
            frontier = [v for v in self.board.board[i]]

            for front in frontier:
                front.h = self.heuristic(front)
                front.f = front.g + front.h

            heapq.heapify(frontier)

            print("Frontier at ", i, "th row")
            print(frontier)

            queen = heapq.heappop(frontier)

            print("Queen chosen: ", queen)

            self.board.place_queen(queen.row, queen.col)

        self.board.draw_board()


def main():
    n = 4
    a_star = A_Star_Search(n)
    a_star.solve()


if __name__ == "__main__":
    main()
