import fileinput
from enum import Enum, auto
from functools import cached_property, total_ordering


class Move(Enum):
    WIN = auto()
    TIE = auto()
    LOSE = auto()

    @classmethod
    def _missing_(cls, value):
        if value == "X":
            return cls.LOSE
        if value == "Y":
            return cls.TIE
        if value == "Z":
            return cls.WIN


@total_ordering
class RPS(Enum):

    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def _missing_(cls, value):
        if value in ("A", "X"):
            return cls.ROCK
        if value in ("B", "Y"):
            return cls.PAPER
        if value in ("C", "Z"):
            return cls.SCISSORS

    def __lt__(self, other):
        if self == RPS.ROCK and other == RPS.PAPER:
            return True
        if self == RPS.PAPER and other == RPS.SCISSORS:
            return True
        if self == RPS.SCISSORS and other == RPS.ROCK:
            return True
        return False

    def move_to(self, move: Move):
        if move == Move.LOSE:
            return self.will_lose
        if move == Move.TIE:
            return self
        if move == Move.WIN:
            return self.will_win

    @cached_property
    def will_lose(self):
        return next(rps for rps in RPS if self > rps)

    @cached_property
    def will_win(self):
        return next(rps for rps in RPS if self < rps)


def score(them: RPS, me: RPS):
    if me > them:
        return 6 + me.value
    if me == them:
        return 3 + me.value
    if me < them:
        return me.value


def part_1(lines):
    total_score = 0
    for line in lines:
        left, right = line.split()
        rps_them = RPS(left)
        rps_me = RPS(right)
        total_score += score(rps_them, rps_me)
    print(total_score)


def part_2(lines):
    total_score = 0
    for line in lines:
        left, right = line.split()
        rps_them = RPS(left)
        move = Move(right)
        total_score += score(rps_them, rps_them.move_to(move))
    print(total_score)


if __name__ == "__main__":
    input_lines = list(line.strip() for line in fileinput.input("input"))
    part_1(input_lines)
    part_2(input_lines)
