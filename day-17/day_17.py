import operator
from textwrap import indent

from bitarray import bitarray
from bitarray.util import ba2int, zeros
from stdlib import *


class Shape:
    def __init__(self, shape, mask=None):
        self.shape = shape
        if mask is None:
            self.mask = reduce(operator.or_, shape, zeros(7))
        else:
            self.mask = mask

    def __len__(self):
        return len(self.shape)

    def __repr__(self):
        return (
            "Shape(\n"
            + indent("\n".join(f"|{ba.to01()}|" for ba in self.shape), "  ")
            + f"\n, mask={self.mask})"
        )

    def __and__(self, other):
        for o, s in zip(reversed(other), self.shape):
            if (o & s).any():
                return True

        return False

    def __lshift__(self, other):
        if not self.mask[0]:
            return Shape([ba << other for ba in self.shape], self.mask << other)

        return self

    def __rshift__(self, other):
        if not self.mask[-1]:
            return Shape([ba >> other for ba in self.shape], self.mask >> other)

        return self

    def __ilshift__(self, other):
        if not self.mask[0]:
            self.shape[:] = [ba << other for ba in self.shape]
            self.mask <<= other

        return self

    def __irshift__(self, other):
        if not self.mask[-1]:
            self.shape[:] = [ba >> other for ba in self.shape]
            self.mask >>= other

        return self


def shape1():
    return Shape(
        [
            bitarray("0011110"),
        ]
    )


def shape2():
    return Shape(
        [
            bitarray("0001000"),
            bitarray("0011100"),
            bitarray("0001000"),
        ]
    )


def shape3():
    return Shape(
        [
            bitarray("0000100"),
            bitarray("0000100"),
            bitarray("0011100"),
        ]
    )


def shape4():
    return Shape(
        [
            bitarray("0010000"),
            bitarray("0010000"),
            bitarray("0010000"),
            bitarray("0010000"),
        ]
    )


def shape5():
    return Shape(
        [
            bitarray("0011000"),
            bitarray("0011000"),
        ]
    )


LEFT_BA = bitarray("1000000")
RIGHT_BA = bitarray("0000001")


def shift_left(shape):
    for ba in shape:
        if ba[0]:
            return shape

    return [ba << 1 for ba in shape]


def shift_right(shape):
    for ba in shape:
        if ba[-1]:
            return shape

    return [ba >> 1 for ba in shape]


def print_column(view, shape, shape_pos):
    for floor in reversed(view[shape_pos:]):
        print(f"|{''.join('.' if x == 0 else '#' for x in floor)}|")

    for ba, floor in zip(shape.shape, reversed(view[1:shape_pos])):
        print(
            f"|{''.join('.' if ba[i] == 0 and floor[i] == 0 else '@' if ba[i] == 1 else '#' for i in range(len(floor)))}|"
        )

    for floor in reversed(view[1 : shape_pos - len(shape)]):
        print(f"|{''.join('.' if x == 0 else '#' for x in floor)}|")

    print("+-------+\n")


def part_1(lines):
    actions = cycle(lines[0])
    shapes = cycle(
        [
            shape1,
            shape2,
            shape3,
            shape4,
            shape5,
        ]
    )

    view = [
        bitarray("1111111"),
    ]

    for _ in range(2022):
        while not view[-1].any():
            view.pop()

        next_shape = next(shapes)()
        view.extend([zeros(7)] * (3 + len(next_shape)))
        shape_pos = len(view)
        if DEBUG:
            print_column(view, next_shape, shape_pos)
        while True:
            if next(actions) == "<":
                res = next_shape << 1
            else:
                res = next_shape >> 1

            if not res & view[:shape_pos]:
                next_shape = res

            if DEBUG:
                print_column(view, next_shape, shape_pos)

            if next_shape & view[: shape_pos - 1]:
                for i, ba in enumerate(next_shape.shape, 1):
                    view[shape_pos - i] = view[shape_pos - i] | ba
                break
            else:
                shape_pos -= 1

            if DEBUG:
                print_column(view, next_shape, shape_pos)

    while not view[-1].any():
        view.pop()
    return len(view) - 1


def part_2(lines):
    actions = cycle(lines[0])
    shapes = cycle(
        [
            shape1,
            shape2,
            shape3,
            shape4,
            shape5,
        ]
    )

    view = [
        bitarray("1111111"),
    ]

    for _ in range(10000):
        while not view[-1].any():
            view.pop()

        next_shape = next(shapes)()
        view.extend([zeros(7)] * (3 + len(next_shape)))
        shape_pos = len(view)
        if DEBUG:
            print_column(view, next_shape, shape_pos)
        while True:
            if next(actions) == "<":
                res = next_shape << 1
            else:
                res = next_shape >> 1

            if not res & view[:shape_pos]:
                next_shape = res

            if DEBUG:
                print_column(view, next_shape, shape_pos)

            if next_shape & view[: shape_pos - 1]:
                for i, ba in enumerate(next_shape.shape, 1):
                    view[shape_pos - i] = view[shape_pos - i] | ba
                break
            else:
                shape_pos -= 1

            if DEBUG:
                print_column(view, next_shape, shape_pos)

    while not view[-1].any():
        view.pop()

    seen = {}
    for i, chunk in enumerate(chunked(view[1:], 16)):
        res = ba2int(reduce(operator.add, chunk, bitarray()))
        if res in seen:
            print(seen[res], i * 16)
            print("SEEN", i * 16)
            return
        seen[res] = i * 16

    return len(view) - 1


if __name__ == "__main__":
    input_lines = read_input("example")
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
