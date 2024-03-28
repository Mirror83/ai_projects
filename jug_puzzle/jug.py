from typing import Self


class Jug:
    """
    This class represents a jug that can hold water of a given capacity
    (The units are of little relevance, but we can say litres)
    """

    def __init__(self, max_capacity: int, current_volume: int = 0):
        """Creates a new jug that is initially empty"""
        self.max_capacity = max_capacity

        self.current_volume = current_volume

    def __str__(self):
        return f"{self.current_volume}"

    def __repr__(self):
        return f"{self.current_volume}"

    def __eq__(self, jug: object) -> bool:
        if isinstance(jug, Jug):
            return (
                self.current_volume == jug.current_volume
                and self.max_capacity == jug.max_capacity
            )
        return False

    def __hash__(self) -> int:
        return hash((self.max_capacity, self.current_volume))

    def can_fill(self) -> bool:
        return self.current_volume < self.max_capacity

    def can_pour(self) -> bool:
        return self.current_volume > 0

    def can_transfer(self, b: Self) -> bool:
        """Check this jug can transfer water to another jug"""
        return self.current_volume > 0 and b.current_volume < b.max_capacity
