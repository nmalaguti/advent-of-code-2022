import fileinput

from more_itertools import divide, ichunked, one


def priority(char):
    if ord("a") <= ord(char) <= ord("z"):
        return ord(char) - ord("a") + 1
    return ord(char) - ord("A") + 27


def part_1(lines):
    sum_priorities = 0
    for line in lines:
        left, right = divide(2, line)
        sum_priorities += priority(one(set(left) & set(right)))
    return sum_priorities


def part_2(lines):
    sum_priorities = 0
    for group in ichunked(lines, 3):
        a, b, c = group
        sum_priorities += priority(one(set(a) & set(b) & set(c)))
    return sum_priorities


if __name__ == "__main__":
    input_lines = list(line.strip() for line in fileinput.input("input"))
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
