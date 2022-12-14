from dataclasses import dataclass

from stdlib import *


@dataclass
class Grid:
    grid: dict
    origin: tuple[int, int]
    min_x: int
    max_x: int
    min_y: int
    max_y: int


def read_grid(lines):
    origin = (500, 0)
    grid = {origin: "+"}
    min_x = max_x = origin[0]
    min_y = max_y = origin[1]
    for line in lines:
        for start, end in windowed(line.split(" -> "), 2):
            start_x, start_y = ints(start)
            end_x, end_y = ints(end)

            min_x = min(min_x, start_x, end_x)
            max_x = max(max_x, start_x, end_x)

            min_y = min(min_y, start_y, end_y)
            max_y = max(max_y, start_y, end_y)

            for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
                for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
                    grid[(x, y)] = "#"

    return Grid(grid, origin, min_x, max_x, min_y, max_y)


def draw_grid(generation, grid: Grid, floor="."):
    print(f"---- {generation} -----\n")
    for y in range(grid.min_y - 1, grid.max_y + 2):
        for x in range(grid.min_x - 1, grid.max_x + 2):
            print(grid.grid.get((x, y), "." if y != grid.max_y else floor), end="")
        print()
    print("\n")


def part_1(lines):
    grid = read_grid(lines)
    generation = 0

    if DEBUG:
        draw_grid(generation, grid)

    sand_path = deque()

    while True:
        generation += 1

        if not sand_path:
            sand_path.append(grid.origin)

        new_sand_x, new_sand_y = sand_path.pop()
        while True:
            sand_path.append((new_sand_x, new_sand_y))
            if grid.grid.get((new_sand_x, new_sand_y + 1), ".") == ".":
                new_sand_y += 1
            elif grid.grid.get((new_sand_x - 1, new_sand_y + 1), ".") == ".":
                new_sand_x -= 1
                new_sand_y += 1
            elif grid.grid.get((new_sand_x + 1, new_sand_y + 1), ".") == ".":
                new_sand_x += 1
                new_sand_y += 1
            else:
                sand_path.pop()
                break

            if (
                not grid.min_x < new_sand_x < grid.max_x
                or not grid.min_y < new_sand_y < grid.max_y
            ):
                return generation - 1

        grid.grid[(new_sand_x, new_sand_y)] = "o"
        if DEBUG:
            draw_grid(generation, grid)


def part_2(lines):
    grid = read_grid(lines)
    grid.max_y += 2
    generation = 0

    if DEBUG:
        draw_grid(generation, grid, floor="$")

    sand_path = deque()

    while True:
        generation += 1
        if not sand_path:
            sand_path.append(grid.origin)

        new_sand_x, new_sand_y = sand_path.pop()

        while True:
            sand_path.append((new_sand_x, new_sand_y))
            if (
                grid.grid.get(
                    (new_sand_x, new_sand_y + 1),
                    "." if new_sand_y + 1 != grid.max_y else "$",
                )
                == "."
            ):
                new_sand_y += 1
            elif (
                grid.grid.get(
                    (new_sand_x - 1, new_sand_y + 1),
                    "." if new_sand_y + 1 != grid.max_y else "$",
                )
                == "."
            ):
                new_sand_x -= 1
                new_sand_y += 1
            elif (
                grid.grid.get(
                    (new_sand_x + 1, new_sand_y + 1),
                    "." if new_sand_y + 1 != grid.max_y else "$",
                )
                == "."
            ):
                new_sand_x += 1
                new_sand_y += 1
            else:
                sand_path.pop()
                break

            if not grid.min_x < new_sand_x < grid.max_x:
                grid.min_x = min(grid.min_x, new_sand_x)
                grid.max_x = max(new_sand_x, grid.max_x)

        grid.grid[(new_sand_x, new_sand_y)] = "o"
        if DEBUG:
            draw_grid(generation, grid, floor="$")

        if (new_sand_x, new_sand_y) == grid.origin:
            return generation


if __name__ == "__main__":
    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
