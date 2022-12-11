from stdlib import *


def part_1(lines):
    counter = 1
    register_x = 1
    queue = deque()
    signal_strength = 0
    cycles = {20 + (i * 40) for i in range(6)}

    for line in lines:
        op, *rest = line.split(" ", 1)
        if op == "noop":
            queue.append(0)
        elif op == "addx":
            queue.append(0)
            queue.append(int(rest[0]))

        while queue:
            register_x += queue.popleft()
            counter += 1
            if counter in cycles:
                signal_strength += counter * register_x

    return signal_strength


def part_2(lines):
    register_x = 1
    queue = deque()
    screen = []

    for line in lines:
        op, *rest = line.split(" ", 1)
        if op == "noop":
            queue.append(0)
        elif op == "addx":
            queue.append(0)
            queue.append(int(rest[0]))

        while queue:
            if register_x - 1 <= len(screen) % 40 <= register_x + 1:
                screen.append("#")
            else:
                screen.append(" ")

            register_x += queue.popleft()

    output = "\n"
    for screen_line in chunked(screen, 40):
        output += "".join(screen_line) + "\n"

    return output


if __name__ == "__main__":
    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
