from bisect import bisect
from functools import cmp_to_key
from json import loads

from funcy import compose
from stdlib import *


def less_than(left, right) -> int:
    # list, list - compare all elements
    if isinstance(left, list) and isinstance(right, list):
        for l, r in zip_longest(left, right):
            res = less_than(l, r)
            if res == 0:
                continue
            else:
                return res
    # list, int - turn int into list and compare
    elif isinstance(left, list) and isinstance(right, int):
        return less_than(left, [right])
    elif isinstance(left, int) and isinstance(right, list):
        return less_than([left], right)
    elif isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        if left < right:
            return -1
        return 1
    # zip_longest has a None
    elif left is None and right is not None:
        return -1
    elif left is not None and right is None:
        return 1
    return 0


Signal = cmp_to_key(less_than)

str_to_signal = compose(Signal, loads)


def part_1(lines):
    total = 0
    for i, group in enumerate(split_at(lines, inverse_identity), start=1):
        left, right = map(str_to_signal, group)
        if left < right:
            total += i

    return total


def part_2(lines):
    res = sorted(map(str_to_signal, filter(identity, lines)))
    a = bisect(res, Signal([[2]]))
    b = bisect(res, Signal([[6]]))
    return (a + 1) * (b + 2)


if __name__ == "__main__":
    input_lines = read_input("input")
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
