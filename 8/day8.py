import argparse
import fileinput
import itertools
import math


direction_indices = {"L": 0, "R": 1}


def parse_directions_and_network(lines):
    """Returns (directions, network)"""
    directions = list(lines[0].strip())
    network = {}
    for line in lines[2:]:
        name, children = line.strip().split(" = ")
        children = children.strip("()").split(", ")
        network[name] = children
    return directions, network


def traverse_network(directions, network, start="AAA", end="ZZZ"):
    """Returns the path traversed"""
    path = [start]
    while path[-1] != end:
        for direction in directions:
            path.append(network[path[-1]][direction_indices[direction]])
    return path


def multi_traverse_network(directions, network):
    """Returns the path length of a multi-traversal of the network"""
    curr_nodes = tuple(node for node in network if node.endswith("A"))
    path_lengths = []
    for node in curr_nodes:
        path_length = 0
        for direction in itertools.cycle(directions):
            dir_idx = direction_indices[direction]
            node = network[node][dir_idx]
            path_length += 1
            if node.endswith("Z"):
                path_lengths.append(path_length)
                break
    return math.lcm(*path_lengths)


def main():
    parser = argparse.ArgumentParser(description="Day 8: Haunted Wasteland")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    print(f"Num lines: {len(lines)}")
    directions, network = parse_directions_and_network(lines)
    if "AAA" in network:
        path = traverse_network(directions, network)
        # print(f"Path: {path}")
        print(f"Num steps (not including start): {len(path) - 1}")
    print(f"Multi-traversal length: {multi_traverse_network(directions, network)}")


if __name__ == "__main__":
    main()
