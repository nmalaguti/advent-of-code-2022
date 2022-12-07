from stdlib import *


def part_1(lines):
    line = lines[0]
    n = 4
    for i, window in enumerate(windowed(line, n)):
        if len(set(window)) == n:
            return i + n


def part_2(lines):
    line = lines[0]
    n = 14
    for i, window in enumerate(windowed(line, n)):
        if len(set(window)) == n:
            return i + n


if __name__ == "__main__":
    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")

