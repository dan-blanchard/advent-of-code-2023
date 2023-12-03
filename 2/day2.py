import argparse
from collections import Counter
import fileinput
from math import prod


def parse_line(line):
    """Game line -> (id, pulls) where pulls is a list of Counter of color -> number"""
    id_chunk, pulls_chunk = line.split(": ")
    game_id = int(id_chunk[4:])
    pulls = [
        Counter(
            {
                color_number.split(" ")[1]: int(color_number.split(" ")[0])
                for color_number in pull.split(", ")
            }
        )
        for pull in pulls_chunk.split("; ")
    ]
    return game_id, pulls


def calculate_possible_games(lines, possible_for):
    possible_games = set()
    for line in lines:
        game_id, pulls = parse_line(line.strip())
        if all(pull <= possible_for for pull in pulls):
            possible_games.add(game_id)
    return possible_games


def calculate_cube_powers(lines):
    game_powers = {}
    for line in lines:
        game_id, pulls = parse_line(line.strip())
        min_counter = Counter()
        for pull in pulls:
            for color, number in pull.items():
                min_counter[color] = max(min_counter[color], number)
        game_powers[game_id] = prod(min_counter.values())
    return game_powers


def main():
    parser = argparse.ArgumentParser(description="Day 2: Cube Conundrum")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    possible_for = Counter({"red": 12, "green": 13, "blue": 14})
    print(f"Set of cubes we are testing for: {possible_for}")
    possible_games = calculate_possible_games(lines, possible_for)
    print(f"Possible games with that set: {possible_games}")
    print(f"Sum of IDs: {sum(possible_games)}")
    cube_powers = calculate_cube_powers(lines)
    print(f"Cube power sum: {sum(cube_powers.values())}")


if __name__ == "__main__":
    main()
