from stdlib import *


def part_1(lines):
    grid = [list(map(int, (c for c in line))) for line in lines]
    visible = set()

    # top
    for x in range(len(grid[0])):
        col_height = -1
        for y in range(len(grid)):
            if grid[y][x] > col_height:
                visible.add((x, y))
                col_height = grid[y][x]

    # left
    for y in range(len(grid)):
        row_height = -1
        for x in range(len(grid[0])):
            if grid[y][x] > row_height:
                visible.add((x, y))
                row_height = grid[y][x]

    # right
    for y in range(len(grid) - 1, -1, -1):
        row_height = -1
        for x in range(len(grid[0]) - 1, -1, -1):
            if grid[y][x] > row_height:
                visible.add((x, y))
                row_height = grid[y][x]

    # bottom
    for x in range(len(grid[0]) - 1, -1, -1):
        col_height = -1
        for y in range(len(grid) - 1, -1, -1):
            if grid[y][x] > col_height:
                visible.add((x, y))
                col_height = grid[y][x]

    return len(visible)


def part_2(lines):
    grid = [list(map(int, (c for c in line))) for line in lines]
    best_scenic_score = 0
    for gx in range(len(grid[0])):
        for gy in range(len(grid)):
            left = 0
            right = 0
            top = 0
            bottom = 0
            for x in range(gx + 1, len(grid[0])):
                if grid[gy][x] < grid[gy][gx]:
                    right += 1
                if grid[gy][x] >= grid[gy][gx]:
                    right += 1
                    break
            for y in range(gy + 1, len(grid)):
                if grid[y][gx] < grid[gy][gx]:
                    bottom += 1
                if grid[y][gx] >= grid[gy][gx]:
                    bottom += 1
                    break
            for x in range(gx - 1, -1, -1):
                if grid[gy][x] < grid[gy][gx]:
                    left += 1
                if grid[gy][x] >= grid[gy][gx]:
                    left += 1
                    break
            for y in range(gy - 1, -1, -1):
                if grid[y][gx] < grid[gy][gx]:
                    top += 1
                if grid[y][gx] >= grid[gy][gx]:
                    top += 1
                    break
            best_scenic_score = max(best_scenic_score, left * right * bottom * top)

    return best_scenic_score


if __name__ == "__main__":
    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
