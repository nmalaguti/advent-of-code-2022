from funcy import compose
from stdlib import *


def walk_grid(width, height):
    for x in range(width):
        yield -1, -1
        for y in range(height):
            yield x, y


def rotate(pair):
    return pair[1], pair[0]


def part_1(lines):
    grid = [list(map(int, (c for c in line))) for line in lines]
    visible = set()

    x_max = len(grid[0])
    y_max = len(grid)

    rotated = partial(map, rotate)
    pipeline = [(), (reversed,), (rotated,), (rotated, reversed)]

    for steps in pipeline:
        func = compose(*steps, list, walk_grid)
        height = -1
        for x, y in func(x_max, y_max):
            if x == -1 and y == -1:
                height = -1
            elif grid[y][x] > height:
                visible.add((x, y))
                height = grid[y][x]

    return len(visible)


def part_2(lines):
    grid = [list(map(int, (c for c in line))) for line in lines]
    best_scenic_score = 0

    x_max = len(grid[0])
    y_max = len(grid)

    for gx in range(x_max):
        for gy in range(y_max):
            left = 0
            right = 0
            top = 0
            bottom = 0
            for x in range(gx + 1, x_max):
                right += 1
                if grid[gy][x] >= grid[gy][gx]:
                    break
            for y in range(gy + 1, y_max):
                bottom += 1
                if grid[y][gx] >= grid[gy][gx]:
                    break
            for x in range(gx - 1, -1, -1):
                left += 1
                if grid[gy][x] >= grid[gy][gx]:
                    break
            for y in range(gy - 1, -1, -1):
                top += 1
                if grid[y][gx] >= grid[gy][gx]:
                    break
            best_scenic_score = max(best_scenic_score, left * right * bottom * top)

    return best_scenic_score


if __name__ == "__main__":
    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
