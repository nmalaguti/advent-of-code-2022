import fileinput


def part_1(lines):
    count = 0
    for line in lines:
        left, right = line.split(",")
        left_start, left_end = map(int, left.split("-"))
        right_start, right_end = map(int, right.split("-"))
        if (
            left_start <= right_start <= left_end
            and left_start <= right_end <= left_end
        ):
            count += 1
        elif (
            right_start <= left_start <= right_end
            and right_start <= left_end <= right_end
        ):
            count += 1
    return count


def part_2(lines):
    count = 0
    for line in lines:
        left, right = line.split(",")
        left_start, left_end = map(int, left.split("-"))
        right_start, right_end = map(int, right.split("-"))
        if right_start <= left_end <= right_end:
            count += 1
        elif right_start <= left_start <= right_end:
            count += 1
        elif left_start <= right_end <= left_end:
            count += 1
        elif left_start <= right_start <= left_end:
            count += 1
    return count


if __name__ == "__main__":
    input_lines = list(line.strip() for line in fileinput.input("input"))
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
