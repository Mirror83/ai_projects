from collections import deque
from typing import Literal, Optional
from jug import Jug


class Outcome:
    def __init__(self, a: Jug, b: Jug, parent=None):
        self.a = a
        self.b = b
        self.parent: Optional[Outcome] = parent

    def depth(self) -> int:
        if self.parent is None:
            return 0
        return 1 + self.parent.depth()

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __str__(self):
        return f"({self.a}, {self.b})"

    def __repr__(self):
        return f"({self.a}, {self.b})"


class JugPuzzle:
    """
    Solves the problem of measuring 2 liters using only a pair of uncallibrated 
    (i.e do not have measurement markings) 3 and 4 liter jugs
    """

    @staticmethod
    def fill_jug(a: Jug, b: Jug, rev=False) -> Outcome:
        if rev:
            return Outcome(
                Jug(b.max_capacity, b.current_volume),
                Jug(a.max_capacity, a.max_capacity),
            )
        return Outcome(
            Jug(a.max_capacity, a.max_capacity), Jug(b.max_capacity, b.current_volume)
        )

    @staticmethod
    def pour(a: Jug, b: Jug, rev=False) -> Outcome:
        if rev:
            return Outcome(Jug(b.max_capacity, b.current_volume), Jug(a.max_capacity))
        return Outcome(Jug(a.max_capacity), Jug(b.max_capacity, b.current_volume))

    @staticmethod
    def transfer(a: Jug, b: Jug, rev=False) -> Outcome:
        transferrable_volume = b.max_capacity - b.current_volume
        volume_transferred = (
            a.current_volume
            if a.current_volume <= transferrable_volume
            else transferrable_volume
        )

        b_new_volume = b.current_volume + volume_transferred
        a_new_volume = a.current_volume - volume_transferred

        if rev:
            return Outcome(
                Jug(b.max_capacity, b_new_volume), Jug(a.max_capacity, a_new_volume)
            )
        else:
            return Outcome(
                Jug(a.max_capacity, a_new_volume), Jug(b.max_capacity, b_new_volume)
            )

    @staticmethod
    def outcomes(a: Jug, b: Jug) -> list[Outcome]:
        outcome_list: list[Outcome] = []

        if a.can_fill():
            outcome_list.append(JugPuzzle.fill_jug(a, b))
        if b.can_fill():
            outcome_list.append(JugPuzzle.fill_jug(b, a, rev=True))

        if a.can_pour():
            outcome_list.append(JugPuzzle.pour(a, b))
        if b.can_pour():
            outcome_list.append(JugPuzzle.pour(b, a, rev=True))

        if a.can_transfer(b):
            outcome_list.append(JugPuzzle.transfer(a, b))
        if b.can_transfer(a):
            outcome_list.append(JugPuzzle.transfer(b, a, rev=True))

        return outcome_list

    @staticmethod
    def solve_breadth_first_search(
        a: Jug, b: Jug, desired_volume=2
    ) -> Outcome | Literal[False]:
        """Solves using breadth first search"""
        start = Outcome(a, b)

        queue: deque[Outcome] = deque()
        queue.append(start)

        visited = set()
        visited.add(start)

        while len(queue) > 0:
            current = queue.popleft()
            if (
                current.a.current_volume == desired_volume
                or current.b.current_volume == desired_volume
            ):
                return current

            outcomes = JugPuzzle.outcomes(current.a, current.b)
            visited.add(current)

            for outcome in outcomes:
                if outcome not in visited:
                    outcome.parent = current
                    queue.append(outcome)

        return False

    @staticmethod
    def solve_depth_limited_search(
        a: Jug, b: Jug, desired_volume=2, max_depth=4
    ) -> list[Outcome]:
        all_solutions = []

        start = Outcome(a, b)

        stack: deque[Outcome] = deque()
        stack.append(start)

        while len(stack) > 0:
            current = stack.pop()

            if (
                current.a.current_volume == desired_volume
                or current.b.current_volume == desired_volume
            ):
                all_solutions.append(current)
                continue

            if current.depth() >= max_depth:
                continue

            outcomes = JugPuzzle.outcomes(current.a, current.b)
            for outcome in outcomes:
                outcome.parent = current
                stack.append(outcome)

        return all_solutions

    def print_solution_path(solution: Outcome):
        solution_list: list[Outcome] = []

        while solution:
            solution_list.append(solution)
            solution = solution.parent

        path = ""

        for i in range(len(solution_list) - 1, -1, -1):
            path += f"({solution_list[i].a}, {solution_list[i].b})"
            if i > 0:
                path += " -> "

        print(path)
