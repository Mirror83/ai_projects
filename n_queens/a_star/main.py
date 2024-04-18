import enum
import heapq
import timeit
from typing import List, Tuple
import random
import tkinter as tk


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

        self.gui_board()

    def gui_board(self):
        root = tk.Tk()
        root.title(f'{self.n}-Queens')
        root.geometry('600x600')
        canvas = tk.Canvas(root, width=500, height=500)
        canvas.pack(padx=100, pady=100)
        for row in self.board:
            for cell in row:
                x = cell.col * 50
                y = cell.row * 50

                color = 'white' if (x + y) % 100 == 0 else 'black'
                piece_color = 'black' if (x + y) % 100 == 0 else 'white'

                canvas.create_rectangle(
                    x, y, x + 50, y + 50, fill=color, outline='black')

                if cell.value == CellState.OCCUPIED:
                    canvas.create_text(
                        x + 25, y + 25, text=cell.value.draw(), fill=piece_color, font=('Arial', 20))

        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                pass
        root.mainloop()

    def is_valid(self, row: int, col: int) -> bool:
        return (row >= 0 and row < self.n) and (col >= 0 and col <= self.n)

    def place_queen(self, row: int, col: int) -> None:
        if self.is_valid(row, col):
            self.board[row][col].value = CellState.OCCUPIED

        else:
            print('Out of range')

    def clear_board(self):
        self.board = [[Cell(i, j) for j in range(self.n)]
                      for i in range(self.n)]


class A_Star_Search:
    def __init__(self, n) -> None:
        self.n = n
        self.board = QueensBoard(n)

    def heuristic(self, cell: Cell) -> int:
        # Current row
        row = cell.row
        col = cell.col
        h = 0

        # Current row
        for i, cell in enumerate(self.board.board[row]):
            if i != col and cell.value == CellState.OCCUPIED:
                h += 1

        # Current column
        for current_row in range(self.n):
            if self.board.board[current_row][col].value == CellState.OCCUPIED:
                h += 1

        # Relative negatively sloping diagonal
        current_col = col - 1
        for r in range(row - 1, -1, -1):
            if current_col < 0:
                break
            if self.board.board[r][current_col].value == CellState.OCCUPIED:
                h += 1
            current_col -= 1

        current_col = col + 1
        for r in range(row - 1, -1, -1):
            if current_col >= self.n:
                break
            if self.board.board[r][current_col].value == CellState.OCCUPIED:
                h += 1
            current_col += 1

        return h

    def solve(self):
        queens: List[Cell] = []

        while len(queens) < self.n:
            queens.clear()
            self.board.clear_board()
            first_queen = random.randint(0, self.n - 1)
            for i in range(self.n):
                frontier = [v for v in self.board.board[i]]

                for front in frontier:
                    front.h = self.heuristic(front)
                    front.f = front.g + front.h

                heapq.heapify(frontier)

                queen = heapq.heappop(frontier)

                if i == 0:
                    self.board.place_queen(i, first_queen)
                    queen = self.board.board[i][first_queen]
                    queens.append(queen)

                if queen.h == 0 and i != 0:
                    self.board.place_queen(queen.row, queen.col)
                    queens.append(queen)

        self.board.draw_board()


def main():
    n = 8
    a_star = A_Star_Search(n)
    a_star.solve()


if __name__ == "__main__":
    # print(timeit.timeit("main()", globals=globals(), number=100))
    main()