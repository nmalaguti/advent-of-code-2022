import fileinput
from heapq import heappush, heappop, heapreplace


def part_1():
    max_cal = 0
    running_cal = 0

    for line in fileinput.input():
        line = line.strip()
        if not line:
            max_cal = max(max_cal, running_cal)
            running_cal = 0
        else:
            running_cal += int(line)

    max_cal = max(max_cal, running_cal)

    print(max_cal)

def part_2():
    max_cals = [0] * 3
    running_cal = 0

    for line in fileinput.input():
        line = line.strip()
        if not line:
            if running_cal > max_cals[0]:
                heapreplace(max_cals, running_cal)
            running_cal = 0
        else:
            running_cal += int(line)

    if running_cal > max_cals[0]:
        heapreplace(max_cals, running_cal)

    print(sum(max_cals))

if __name__ == "__main__":
    part_1()
    part_2()
