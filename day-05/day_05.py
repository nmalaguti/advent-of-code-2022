from stdlib import *


def parse_input(lines):
    # split on first blank newline
    stacks, moves = before_and_after(identity, lines)
    rstacks = deque(reversed(list(stacks)))

    result = []

    ids = rstacks.popleft()
    for _ in range(len(ids) // 4 + 1):
        result.append(deque())

    for row in rstacks:
        for i, column in enumerate(chunked(row, 4)):
            if column[1] != " ":
                result[i].appendleft(column[1])

    parsed_moves = []
    for line in moves:
        if not line:
            continue
        count, source, dest = ints(line)
        parsed_moves.append((count, source - 1, dest - 1))

    return result, parsed_moves


def part_1(lines):
    stacks, moves = parse_input(lines)
    for count, source, dest in moves:
        for _ in range(count):
            stacks[dest].appendleft(stacks[source].popleft())

    return "".join([stack[0] for stack in stacks])


def part_2(lines):
    stacks, moves = parse_input(lines)

    for count, source, dest in moves:
        carry = deque()
        for _ in range(count):
            carry.appendleft(stacks[source].popleft())
        stacks[dest].extendleft(carry)

    return "".join([stack[0] for stack in stacks])


if __name__ == "__main__":
    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
