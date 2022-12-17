from functools import lru_cache

import networkx as nx
from frozendict import frozendict
from stdlib import *


def caps(line):
    return [x for x in re.findall(r"[A-Z]{2}", line)]


def make_graph(lines):
    G = nx.DiGraph()
    for line in lines:
        source, *destinations = caps(line)
        flow_rate = one(ints(line))
        G.add_nodes_from([source, *destinations])
        G.nodes[source]["flow_rate"] = flow_rate
        for d in destinations:
            G.add_edge(source, d)

    return G


best_at = {}


@lru_cache(maxsize=2_500_000)
def visit_node(G, P, locations, open_valves, closed_valves, time_remaining):
    open_valves_sum = sum(open_valves.values())

    if not closed_valves:
        # nothing left to open
        return open_valves_sum * time_remaining, []

    if time_remaining == 0:
        return 0, []

    best_possible = 0
    for i, valves in enumerate(chunked(closed_valves.items(), len(locations)), 1):
        for loc, valve in valves:
            if loc in locations:
                continue

            best_possible += valve * max(0, (time_remaining - (2 * i)))

    location_actions = []

    if len(set(locations)) == 1:
        location = locations[0]

        seen = set()
        actions = []
        for target in closed_valves:
            path = P[location][target]
            if len(path) > 1 and path[1] not in seen:
                seen.add(path[1])
                actions.append(("MOVE_TO", path[1]))

        if location in closed_valves:
            best_possible += (time_remaining - 1) * closed_valves[location]
            actions.append(("OPEN", location))

        location_actions = [list(a) for a in distribute(2, actions)]
    else:
        already_sim = set()

        for location in locations:
            actions = []

            seen = set()
            for target in closed_valves:
                path = P[location][target]
                if len(path) > 1 and path[1] not in seen:
                    seen.add(path[1])
                    actions.append(("MOVE_TO", path[1]))

            if location in closed_valves:
                if location not in already_sim:
                    already_sim.add(location)
                    best_possible += (time_remaining - 1) * closed_valves[location]
                    actions.append(("OPEN", location))

            location_actions.append(actions)

    if best_possible == 0:
        return open_valves_sum * time_remaining, []

    no_action = open_valves_sum * (time_remaining - 1)

    best_choice = no_action
    best_action = [("WAIT", location) for location in locations]
    best_path = []

    seen_actions = set()
    for actions in product(*location_actions):

        if actions in seen_actions:
            continue

        seen_actions.add(actions)
        if len(actions) > 1:
            seen_actions.add((actions[1], actions[0]))

        best_at[time_remaining] = max(
            best_at.setdefault(time_remaining, 0), best_choice
        )

        if best_at[time_remaining] >= best_possible + no_action:
            break

        next_locations = []
        new_open = dict(open_valves)
        new_closed = dict(closed_valves)

        for action, next_location in actions:
            next_locations.append(next_location)

            if action == "OPEN":
                new_open[next_location] = closed_valves[next_location]
                new_closed.pop(next_location, None)

        res, new_path = visit_node(
            G,
            P,
            tuple(next_locations),
            frozendict(new_open),
            frozendict(new_closed),
            time_remaining - 1,
        )

        if res > best_choice:
            best_choice = res
            best_action = actions
            best_path = new_path

    return best_choice + open_valves_sum, [best_action, *best_path]


def print_path(G, path, time_limit):
    open_valves = {}
    total = 0
    for i, p in enumerate(path, 1):
        print(f"== Minute {i} ==")
        if not open_valves:
            print("No valves are open.")
        else:
            total += sum(open_valves.values())
            print(
                f"Valves {open_valves} are open, releasing {sum(open_valves.values())} pressure."
            )
        for action, location in p:
            print(action, location)
            if action == "OPEN":
                open_valves[location] = G.nodes[location]["flow_rate"]
        print()

    for i in range(len(path) + 1, time_limit + 1):
        print(f"== Minute {i} ==")
        if not open_valves:
            print("No valves are open.")
        else:
            total += sum(open_valves.values())
            print(
                f"Valves {open_valves} are open, releasing {sum(open_valves.values())} pressure."
            )
        print()

    print(total)


def part_1(lines):
    start_node = "AA"

    G = make_graph(lines)
    P = frozendict(
        {
            k: frozendict({k1: tuple(v1) for k1, v1 in v.items()})
            for k, v in nx.shortest_path(G).items()
        }
    )
    closed_valves = {
        n[0]: n[1]["flow_rate"]
        for n in sorted(
            G.nodes(data=True),
            key=lambda x: x[1]["flow_rate"],
            reverse=True,
        )
        if n[1]["flow_rate"] > 0
    }

    res, path = visit_node(
        G, P, tuple([start_node]), frozendict({}), frozendict(closed_valves), 30
    )

    if DEBUG:
        print_path(G, path, 30)

    return res


def part_2(lines):
    start_node = "AA"

    G = make_graph(lines)
    P = frozendict(
        {
            k: frozendict({k1: tuple(v1) for k1, v1 in v.items()})
            for k, v in nx.shortest_path(G).items()
        }
    )
    closed_valves = {
        n[0]: n[1]["flow_rate"]
        for n in sorted(
            G.nodes(data=True),
            key=lambda x: x[1]["flow_rate"],
            reverse=True,
        )
        if n[1]["flow_rate"] > 0
    }

    res, path = visit_node(
        G,
        P,
        tuple([start_node, start_node]),
        frozendict({}),
        frozendict(closed_valves),
        26,
    )

    if DEBUG:
        print_path(G, path, 26)

    return res


if __name__ == "__main__":
    input_lines = read_input("input")
    # print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
