from jug import Jug
from puzzle import JugPuzzle


def main():
    print("Breadth-first search")
    solution = JugPuzzle.solve_breadth_first_search(Jug(3), Jug(4))

    if solution:
        JugPuzzle.print_solution_path(solution)
    else:
        print("No solution found")

    print("Depth-limited search")

    depth = 6
    depthInput = input(
        f"Enter the desired depth (Leave empty for default depth of {depth}): "
    )

    if depthInput != "":
        depth = int(depthInput)

    solutions = JugPuzzle.solve_depth_limited_search(Jug(3), Jug(4), max_depth=depth)

    if len(solutions) > 0:
        print(f"Found {len(solutions)} solution(s)")

        if len(solutions) > 10:
            print("Printing only the first 10 solutions")
            solutions = solutions[:10]

        for solution in solutions:
            JugPuzzle.print_solution_path(solution)
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
