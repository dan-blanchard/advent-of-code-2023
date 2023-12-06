import argparse
import fileinput
from math import prod


def parse_races(lines):
    """Returns list of times and distances"""
    times = [int(x) for x in lines[0].strip().split(":")[1].split()]
    distances = [int(x) for x in lines[1].strip().split(":")[1].split()]
    return list(zip(times, distances, strict=True))


def calc_num_winners(time, distance_record):
    return sum(
        1
        for push_time in range(time + 1)
        if (time - push_time) * push_time > distance_record
    )


def calc_winner_product(races):
    return prod(calc_num_winners(*race) for race in races)


def parse_single_race(lines):
    """Returns tuple of time and distance for race with spaces removed"""
    time = int(lines[0].strip().split(":")[1].replace(" ", ""))
    distance = int(lines[1].strip().split(":")[1].replace(" ", ""))
    return time, distance


def main():
    parser = argparse.ArgumentParser(description="Day 6: Wait For It")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    print(f"Num lines: {len(lines)}")
    races = parse_races(lines)
    print(f"Races: {races}")
    print(f"Winner product: {calc_winner_product(races)}")
    single_race = parse_single_race(lines)
    print(f"Race: {single_race}")
    print(f"Number of ways to win single race: {calc_num_winners(*single_race)}")


if __name__ == "__main__":
    main()
