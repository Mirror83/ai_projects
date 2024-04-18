import random
from typing import List
from collections import deque
import enum


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

    def remove_queen(self, row: int, col: int) -> None:
        self.board[row][col].value = CellState.UNOCCUPIED

    def is_safe(self, row: int, col: int) -> bool:
        for i in range(self.n):
            if self.board[row][i].value == CellState.OCCUPIED:
                return False
            if self.board[i][col].value == CellState.OCCUPIED:
                return False

        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if self.board[i][j].value == CellState.OCCUPIED:
                return False

        for i, j in zip(range(row, -1, -1), range(col, self.n)):
            if self.board[i][j].value == CellState.OCCUPIED:
                return False

        return True

    def is_valid(self, row: int, col: int) -> bool:
        return row >= 0 and col >= 0 and row < self.n and col < self.n

    def is_goal(self) -> bool:
        for row in self.board:
            for cell in row:
                if cell.value == CellState.UNOCCUPIED:
                    return False
        return True


class CSP:
    def __init__(self, board: QueensBoard) -> None:
        self.board = board
        self.domain = board.board

    def initialize_domain(self) -> List:
        chosen_indices = set()

        for i in range(self.board.n):
            j = random.randint(0, self.board.n - 1)

            while j in chosen_indices:
                j = random.randint(0, self.board.n - 1)

            self.board.place_queen(i, j)
            chosen_indices.add(j)

        print('Initial Domain: ')
        self.board.draw_board()

    def solve(self) -> bool:
        self.initialize_domain()
        self.ac3()
        self.board.board = self.domain

        print('Arc consistent Domain: ')
        self.board.draw_board()

    def ac3(self):
        queue = deque()
        for row in self.domain:
            for cell in row:
                queue.append(cell)

        while queue:
            cell = queue.popleft()
            if self.revise(cell):
                if not cell.value:
                    return False

    def revise(self, cell: Cell) -> bool:
        revised = False
        neighbors = self.get_neighbors(cell)

        for neighbor in neighbors:
            if neighbor.value == CellState.OCCUPIED:
                cell.value = CellState.UNOCCUPIED
                revised = True
        return revised

    def get_neighbors(self, cell: Cell):
        neighbors = []

        for row in self.domain:
            if row[cell.col] != cell:
                neighbors.append(row[cell.col])

        for i in range(len(self.domain)):
            if 0 <= cell.row + i < len(self.domain) and 0 <= cell.col + i < len(self.domain):
                neighbor = self.domain[cell.row + i][cell.col + i]
                if neighbor != cell:
                    neighbors.append(neighbor)
            if 0 <= cell.row - i < len(self.domain) and 0 <= cell.col - i < len(self.domain):
                neighbor = self.domain[cell.row - i][cell.col - i]
                if neighbor != cell:
                    neighbors.append(neighbor)

        for i in range(len(self.domain)):
            if 0 <= cell.row + i < len(self.domain) and 0 <= cell.col - i < len(self.domain):
                neighbor = self.domain[cell.row + i][cell.col - i]
                if neighbor != cell:
                    neighbors.append(neighbor)
            if 0 <= cell.row - i < len(self.domain) and 0 <= cell.col + i < len(self.domain):
                neighbor = self.domain[cell.row - i][cell.col + i]
                if neighbor != cell:
                    neighbors.append(neighbor)
        return neighbors


if __name__ == "__main__":
    board = QueensBoard(4)

    ac3 = CSP(board)

    ac3.solve()
