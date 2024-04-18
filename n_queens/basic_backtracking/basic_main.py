import sys
import timeit

from queens_board import QueensBoard, solve_n_queens


def main():
    # try:
    #     n = int(input("Enter the size of the board (n): "))
    # except ValueError:
    #     print(f"Invalid input. The value entered should be an integer.", file=sys.stderr)
    #     exit(1)

    board = QueensBoard(8)

    if solve_n_queens(board):
        board.draw()
    else:
        print(f"Could not find a solution where n = {8}.")


if __name__ == '__main__':
    print(timeit.timeit("main()", globals=globals(), number=100))
