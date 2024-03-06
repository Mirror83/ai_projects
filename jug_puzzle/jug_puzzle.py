import math
from jug import Jug


class JugPuzzle:
    """
    Solves the problem of measuring 2 liters using only a pair of unmeasured
    3 and 4 liter jugs
    """

    def __init__(self, max_a, max_b) -> None:
        self.a = Jug(max_a)
        self.b = Jug(max_b)

    def fill_jug(self, a: Jug, b: Jug, rev=False):
        if rev:
            return Jug(b.max_capacity, b.current_volume), Jug(a.max_capacity, a.max_capacity)
        return (Jug(a.max_capacity, a.max_capacity), Jug(b.max_capacity, b.current_volume))

    def pour(self, a: Jug, b: Jug, rev=False):
        if rev:
            return Jug(b.max_capacity, b.current_volume), Jug(a.max_capacity)
        return (Jug(a.max_capacity), Jug(b.max_capacity, b.current_volume))

    def transfer(self, a: Jug, b: Jug, rev=False):
        transferrable_volume = b.max_capacity - b.current_volume
        volume_transferred = a.current_volume if a.current_volume <= transferrable_volume else a.current_volume - transferrable_volume

        b_new_volume = b.current_volume + volume_transferred
        a_new_volume = a.current_volume - volume_transferred

        if rev:
            return (Jug(b.max_capacity, b_new_volume), Jug(a.max_capacity, a_new_volume))
        else:
            return (Jug(a.max_capacity, a_new_volume), Jug(b.max_capacity, b_new_volume))

    def outcomes(self, a: Jug, b: Jug):
        outcome_list = []

        if a.can_fill():
            outcome_list.append(self.fill_jug(a, b))
        if b.can_fill():
            outcome_list.append(self.fill_jug(b, a, rev=True))

        if a.can_pour():
            outcome_list.append(self.pour(a, b))
        if b.can_pour():
            outcome_list.append(self.pour(b, a, rev=True))

        if a.can_transfer(b):
            outcome_list.append(self.transfer(a, b))
        if b.can_transfer(a):
            outcome_list.append(self.transfer(b, a, rev=True))

        return outcome_list
