from typing import Tuple
from jug import Jug
from jug_puzzle import JugPuzzle
from collections import deque


def solve_bfs(a: Jug, b: Jug) -> bool:
    """Solves using breadth first search"""
    puzzle = JugPuzzle(3, 4)
    queue: deque[Tuple[Jug, Jug]] = deque()

    visited = []

    start = puzzle.a, puzzle.b

    outcomes = puzzle.outcomes(puzzle.a, puzzle.b)
    visited.append(start)
    print(start)

    for outcome in outcomes:
        queue.append(outcome)

    while len(queue) > 0:
        current = queue.popleft()
        print(current)
        if current[0].current_volume == 2 or current[1].current_volume == 2:
            return True

        a = current[0]
        b = current[1]

        outcomes = puzzle.outcomes(a, b)
        visited.append(current)

        for outcome in outcomes:
            if outcome not in visited:
                queue.append(outcome)

    return False


if __name__ == '__main__':
    a = Jug(3, 3)
    b = Jug(4, 3)
    puzzle = JugPuzzle(3, 4)
    print(solve_bfs(a, b))
