import sys

from queens_board import QueensBoard, solve_n_queens


def main():
    try:
        n = int(input("Enter the size of the board (n): "))
    except ValueError:
        print(f"Invalid input. The value entered should be an integer.", file=sys.stderr)
        exit(1)

    board = QueensBoard(n)

    if solve_n_queens(board):
        board.draw()
    else:
        print(f"Could not find a solution where n = {n}.")


if __name__ == '__main__':
    main()
