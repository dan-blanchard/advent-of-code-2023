import argparse
import fileinput
import itertools


def parse_grid(lines):
    grid = []
    for line in lines:
        grid.append(list(line.strip()))
    return grid


def print_grid(grid):
    for line in grid:
        print("".join(line))


def find_empty_rows_cols(grid):
    empty_rows = [
        row for row, line in enumerate(grid) if all(char == "." for char in line)
    ]
    empty_cols = [
        col for col in range(len(grid[0])) if all(line[col] == "." for line in grid)
    ]
    return empty_rows, empty_cols


def shift_galaxies(galaxies, empty_rows, empty_cols, multiplier):
    new_galaxies = []
    for galaxy in galaxies:
        row, col = galaxy
        row_shift = sum(row > empty_row for empty_row in empty_rows) * (multiplier - 1)
        col_shift = sum(col > empty_col for empty_col in empty_cols) * (multiplier - 1)
        galaxy = (row + row_shift, col + col_shift)
        new_galaxies.append(galaxy)
    return new_galaxies


def find_galaxies(grid):
    return [
        (row, col)
        for row, line in enumerate(grid)
        for col, char in enumerate(line)
        if char == "#"
    ]


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def sum_shortest_paths(galaxies):
    return sum(
        manhattan_distance(galaxy1, galaxy2)
        for galaxy1, galaxy2 in itertools.combinations(galaxies, 2)
    )


def main():
    parser = argparse.ArgumentParser(description="Day 11: Cosmic Expansion")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    parser.add_argument("--multiplier", "-m", type=int, default=2, help="Multiplier")
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    print(f"Num lines: {len(lines)}")
    grid = parse_grid(lines)
    print_grid(grid)
    empty_rows, empty_cols = find_empty_rows_cols(grid)
    print(f"Empty rows: {empty_rows}")
    print(f"Empty cols: {empty_cols}")
    galaxies = find_galaxies(grid)
    shifted_galaxies = shift_galaxies(
        galaxies, empty_rows, empty_cols, multiplier=args.multiplier
    )
    print(f"Shifted Galaxies: {shifted_galaxies}")
    print(f"Sum shortest paths: {sum_shortest_paths(shifted_galaxies)}")


if __name__ == "__main__":
    main()
