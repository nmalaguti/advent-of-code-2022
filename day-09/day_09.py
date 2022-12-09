from stdlib import *


def move_knot(direction, h):
    x, y = h
    if direction == "U":
        return x, y - 1
    elif direction == "D":
        return x, y + 1
    elif direction == "L":
        return x - 1, y
    elif direction == "R":
        return x + 1, y


def follow_knot(h, t):
    hx, hy = h
    tx, ty = t
    dx, dy = tx - hx, ty - hy
    if dx > 1 and dy > 1:
        t = hx + 1, hy + 1
    elif dx < -1 and dy < -1:
        t = hx - 1, hy - 1
    elif dx > 1 and dy < -1:
        t = hx + 1, hy - 1
    elif dx < -1 and dy > 1:
        t = hx - 1, hy + 1
    elif dx > 1:
        t = hx + 1, hy
    elif dy > 1:
        t = hx, hy + 1
    elif dx < -1:
        t = hx - 1, hy
    elif dy < -1:
        t = hx, hy - 1

    return t


def part_1(lines):
    knots = [(0, 0)] * 2
    visited = set()
    for line in lines:
        direction, steps = line.split()
        for _ in range(int(steps)):
            knots[0] = move_knot(direction, knots[0])
            for i in range(1, len(knots)):
                knots[i] = follow_knot(knots[i - 1], knots[i])
            visited.add(knots[-1])
    return len(visited)


def grid(knots, visited):
    output = []
    for x in range(27):
        for y in range(22):
            output.append(".")
    for x, y in visited:
        output[(y + 16) * 27 + (x + 12)] = "#"
    output[16 * 27 + 12] = "s"
    for i, (x, y) in reversed(list(enumerate(knots))):
        output[(y + 16) * 27 + (x + 12)] = str(i) if i != 0 else "H"
    for line in chunked(output, 27):
        print("".join(line))
    print()
    print()


def part_2(lines):
    knots = [(0, 0)] * 10
    visited = set()
    for line in lines:
        direction, steps = line.split()
        if DEBUG:
            print("==", line, "==", "\n")
        for _ in range(int(steps)):
            knots[0] = move_knot(direction, knots[0])
            for i in range(1, len(knots)):
                knots[i] = follow_knot(knots[i - 1], knots[i])
            visited.add(knots[-1])
        if DEBUG:
            grid(knots, [])

    if DEBUG:
        grid([], visited)

    return len(visited)


if __name__ == "__main__":
    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
