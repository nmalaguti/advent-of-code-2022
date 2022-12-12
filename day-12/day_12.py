import networkx as nx
from stdlib import *


def neighbors(loc, G):
    x, y = loc
    for n in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if n in G and G.nodes[n]["value"] - G.nodes[loc]["value"] <= 1:
            yield n


def make_graph(lines):
    G = nx.DiGraph()
    start = None
    end = None
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            loc = x, y
            if char == "S":
                start = loc
                value = ord("a") - ord("a")
            elif char == "E":
                end = loc
                value = ord("z") - ord("a")
            else:
                value = ord(char) - ord("a")
            G.add_node(loc, value=value)

    for loc, value in G.nodes(data="value"):
        for n in neighbors(loc, G):
            G.add_edge(loc, n)

    if DEBUG:
        print(start, end)
        pprint(nx.to_dict_of_lists(G))

    return G, start, end


def part_1(lines):
    return nx.shortest_path_length(*make_graph(lines))


def part_2(lines):
    G, start, end = make_graph(lines)
    P = nx.shortest_path_length(G, target=end)
    return min(P[loc] for loc in P if G.nodes[loc]["value"] == 0)


if __name__ == "__main__":
    input_lines = read_input()
    print("Part 1:", part_1(input_lines) or "")
    print("Part 2:", part_2(input_lines) or "")
