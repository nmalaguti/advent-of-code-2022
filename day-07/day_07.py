from stdlib import *
from pathlib import PurePosixPath


def make_fs(lines):
    mem_fs = {"/": {}}
    curr_dict = mem_fs

    for line in lines:
        if line.startswith("$"):
            _, command, *rest = line.split()
            if command == "ls":
                continue
            else:
                directory, = rest
                curr_dict = curr_dict[directory]
        else:
            size, name = line.split()
            if size == "dir":
                curr_dict[name] = {"..": curr_dict}
            else:
                curr_dict[name] = int(size)

    return mem_fs


def calc_dir_sizes(mem_fs):
    dir_sizes = {}

    def recursive_walk_dirs(d, path):
        if isinstance(d, dict):
            for key, value in d.items():
                if key == "..":
                    continue
                yield from recursive_walk_dirs(value, path / key)
            yield path, d

    for path, dir_dict in recursive_walk_dirs(mem_fs["/"], PurePosixPath("/")):
        size = 0
        for key, value in dir_dict.items():
            if key == "..":
                continue

            if isinstance(value, int):
                size += value
            else:
                size += dir_sizes[str(path / key)]
        dir_sizes[str(path)] = size

    return dir_sizes


def part_1(lines):
    mem_fs = make_fs(lines)
    dir_sizes = calc_dir_sizes(mem_fs)

    total_size = 0
    for size in dir_sizes.values():
        if size <= 100_000:
            total_size += size

    return total_size


def part_2(lines):
    total_space = 70_000_000
    needed_space = 30_000_000

    mem_fs = make_fs(lines)
    dir_sizes = calc_dir_sizes(mem_fs)

    used_space = dir_sizes["/"]
    unused_space = total_space - used_space
    space_to_delete = needed_space - unused_space

    return min(size for size in dir_sizes.values() if size > space_to_delete)


if __name__ == "__main__":
    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
