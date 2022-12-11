from dataclasses import dataclass

from stdlib import *


@dataclass
class Monkey:
    id: int
    items: deque[int]
    operation: str
    divisible_by: int
    true_destination: int
    false_destination: int
    inspected: int = 0


def read_state(lines):
    monkeys = {}
    for i, stanza in enumerate(split_at(lines, lambda x: not x)):
        items = deque()
        operation = None
        divisible_by = None
        true_destination = None
        false_destination = None

        for line in stanza:
            try:
                case, body = line.strip().split(": ")
            except ValueError:
                continue

            if case == "Starting items":
                items.extend(ints(body))
            elif case == "Operation":
                operation = body.split(" = ")[1]
            elif case == "Test":
                divisible_by = one(ints(body))
            elif case == "If true":
                true_destination = one(ints(body))
            elif case == "If false":
                false_destination = one(ints(body))

        monkeys[i] = Monkey(
            id=i,
            items=items,
            operation=operation,
            divisible_by=divisible_by,
            true_destination=true_destination,
            false_destination=false_destination,
        )

    return monkeys


def part_1(lines):
    monkeys = read_state(lines)
    if DEBUG:
        pprint(monkeys)
    for round in range(20):
        for i, monkey in monkeys.items():
            if DEBUG:
                print(f"Monkey {i}:")
            while monkey.items:
                monkey.inspected += 1
                item = monkey.items.popleft()
                if DEBUG:
                    print(f"  Monkey inspects an item with a worry level of {item}.")
                new_level = eval(monkey.operation, {}, {"old": item})
                if DEBUG:
                    print(f"    Worry level is {monkey.operation} to {new_level}.")
                bored_level = new_level // 3
                if DEBUG:
                    print(
                        f"    Monkey gets bored with item. Worry level is divided by 3 to {bored_level}."
                    )
                is_divisible = bored_level % monkey.divisible_by == 0
                destination = (
                    monkey.true_destination
                    if is_divisible
                    else monkey.false_destination
                )
                if DEBUG:
                    print(
                        f"    Current worry level {'is' if is_divisible else 'is not'} divisible by {monkey.divisible_by}."
                    )
                monkeys[destination].items.append(bored_level)
                if DEBUG:
                    print(
                        f"    Item with worry level {bored_level} is thrown to monkey {destination}."
                    )
        if DEBUG:
            pprint(monkeys)

    sorted_monkeys = sorted(monkeys.values(), key=lambda m: -m.inspected)
    if DEBUG:
        pprint(sorted_monkeys)
    top_1, top_2, *rest = sorted_monkeys
    return top_1.inspected * top_2.inspected


def part_2(lines):
    monkeys = read_state(lines)
    if DEBUG:
        pprint(monkeys)
    mod_by = 1
    for monkey in monkeys.values():
        mod_by *= monkey.divisible_by
    for round in range(10000):
        for i, monkey in monkeys.items():
            if DEBUG:
                print(f"Monkey {i}:")
            while monkey.items:
                monkey.inspected += 1
                item = monkey.items.popleft()
                if DEBUG:
                    print(f"  Monkey inspects an item with a worry level of {item}.")
                new_level = eval(monkey.operation, {}, {"old": item})
                if DEBUG:
                    print(f"    Worry level is {monkey.operation} to {new_level}.")
                bored_level = new_level % mod_by
                if DEBUG:
                    print(
                        f"    Monkey gets bored with item. Worry level is divided by 3 to {bored_level}."
                    )
                is_divisible = bored_level % monkey.divisible_by == 0
                destination = (
                    monkey.true_destination
                    if is_divisible
                    else monkey.false_destination
                )
                if DEBUG:
                    print(
                        f"    Current worry level {'is' if is_divisible else 'is not'} divisible by {monkey.divisible_by}."
                    )
                monkeys[destination].items.append(bored_level)
                if DEBUG:
                    print(
                        f"    Item with worry level {bored_level} is thrown to monkey {destination}."
                    )
        if DEBUG:
            pprint(monkeys)

    sorted_monkeys = sorted(monkeys.values(), key=lambda m: -m.inspected)
    if DEBUG:
        pprint(sorted_monkeys)
    top_1, top_2, *rest = sorted_monkeys
    return top_1.inspected * top_2.inspected


if __name__ == "__main__":
    input_lines = read_input("input")
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
