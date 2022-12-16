import sys
from math import sqrt

import portion as P
from scipy.spatial.distance import cityblock, euclidean
from stdlib import *


def discretize(i, incr=1):
    # https://github.com/AlexandreDecan/portion/issues/24#issuecomment-604456362
    first_step = lambda s: (
        P.OPEN,
        (s.lower - incr if s.left is P.CLOSED else s.lower),
        (s.upper + incr if s.right is P.CLOSED else s.upper),
        P.OPEN,
    )
    second_step = lambda s: (
        P.CLOSED,
        (s.lower + incr if s.left is P.OPEN and s.lower != -P.inf else s.lower),
        (s.upper - incr if s.right is P.OPEN and s.upper != P.inf else s.upper),
        P.CLOSED,
    )
    return i.apply(first_step).apply(second_step)


def part_1(lines):
    y = 2000000

    sensors = []
    beacon_intervals = P.empty()
    for line in lines:
        sensor, beacon = map(tuple, chunked(ints(line), 2))
        distance = cityblock(sensor, beacon)
        sensors.append((sensor, distance))
        if beacon[1] == 10:
            beacon_intervals |= P.singleton(beacon[0])

    if DEBUG:
        pprint(sensors)

    intervals = P.empty()

    for sensor, radius in sensors:
        sx, sy = sensor
        if sy - radius < y < sy + radius:
            cells = radius - cityblock(sensor, (sx, y))
            intervals |= P.closed(sx - cells, sx + cells)

    no_beacon_intervals = intervals - beacon_intervals
    if DEBUG:
        print(no_beacon_intervals)

    total = 0
    for atomic_interval in no_beacon_intervals:
        total += atomic_interval.upper - atomic_interval.lower

    return total


def sensor_interval(sensor, y):
    (sx, sy), radius = sensor
    if sy - radius < y < sy + radius:
        cells = radius - cityblock((sx, sy), (sx, y))
        return P.closed(sx - cells, sx + cells)
    return P.empty()


def point_on_line(a, b, c):
    side_a = cityblock(a, b)
    side_b = cityblock(b, c)
    side_c = cityblock(c, a)

    semi_perimeter = (side_a + side_b + side_c) // 2

    if semi_perimeter in (side_a, side_b, side_c):
        return min(side_a, side_b, side_c)

    return False


def segments_intersect(a, b, c, d):
    x = point_on_line(a, b, c)
    y = point_on_line(b, c, d)
    if x and y and x == y:
        return x


def part_2(lines):
    sensors = []
    for line in lines:
        sensor, beacon = map(tuple, chunked(ints(line), 2))
        sensors.append((sensor, cityblock(sensor, beacon)))

    if DEBUG:
        pprint(sensors)

    # 2_634_117 - 2_907_690

    # 273_573
    # 2_743_135
    # 840602
    # 1902533

    # ((3088287, 2966967), 767923) 767923
    # ((3928889, 1064434), 1975212) 1975212

    # 3523360, 2634117
    # 3796933, 2907690

    # 2721114 3367718

    # y = 2_634_117
    y = 0
    while y <= 4_000_000:
        if DEBUG:
            print("y:", y)

        intervals = reduce(
            P.Interval.union, (sensor_interval(sensor, y) for sensor in sensors)
        )
        slots = discretize(P.closed(0, 4_000_000) - intervals)
        if not slots.empty:
            return slots.lower * 4_000_000 + y

        min_overlap = sys.maxsize

        overlaps = P.empty()
        for sensor in sensors:
            intervals_without = reduce(
                P.Interval.union,
                (sensor_interval(s, y) for s in sensors if s != sensor),
            )
            overlaps |= intervals_without & sensor_interval(sensor, y)

        if not overlaps.empty:
            for ai in overlaps:
                overlap_amount = ai.upper - ai.lower + 1
                if overlap_amount > 0:
                    if overlap_amount == 1:
                        matching_sensors = []
                        for s, r in sensors:
                            d = cityblock(s, (ai.lower, y))
                            if d <= r:
                                matching_sensors.append((s, r))

                        shapes = []
                        for (sx, sy), radius in matching_sensors:
                            vertices = [
                                (sx, sy - radius),
                                (sx + radius, sy),
                                (sx, sy + radius),
                                (sx - radius, sy),
                            ]
                            edges = list(windowed(chain(vertices, [vertices[0]]), 2))
                            shapes.append(edges)

                        line_pairs = list(product(*shapes))

                        intersect_lengths = []
                        for ((a, b), (c, d)) in line_pairs:
                            intersect = segments_intersect(a, b, c, d)
                            if intersect:
                                intersect_lengths.append(intersect)

                        if intersect_lengths:
                            overlap_amount = min(intersect_lengths)

                    min_overlap = min(min_overlap, overlap_amount)

        if DEBUG:
            print("min_overlap:", min_overlap)
        y += max(1, min_overlap // 4)


if __name__ == "__main__":
    input_lines = read_input("input")
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
