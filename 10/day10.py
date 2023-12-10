import argparse
import fileinput


# (row, col)
pipes_to_dirs = {
    "|": ((-1, 0), (1, 0)),
    "-": ((0, -1), (0, 1)),
    "L": ((-1, 0), (0, 1)),
    "J": ((-1, 0), (0, -1)),
    "7": ((0, -1), (1, 0)),
    "F": ((0, 1), (1, 0)),
}
dirs_to_pipes = {val: key for key, val in pipes_to_dirs.items()}


GROUND = "."
START = "S"


def find_start(grid):
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == START:
                return row, col


def parse_grid(lines):
    grid = []
    for line in lines:
        grid.append(list(line.strip()))
    return grid


def calc_start_pipe(grid, start):
    num_rows = len(grid)
    num_cols = len(grid[0])
    connections = []
    for row in (-1, 0, 1):
        for col in (-1, 0, 1):
            if row == 0 and col == 0 or row != 0 and col != 0:
                continue
            # If we have a valid non-ground cell, check if it is connected to start
            if (
                0 <= start[0] + row < num_rows
                and 0 <= start[1] + col < num_cols
                and grid[start[0] + row][start[1] + col] != GROUND
            ):
                search_row = start[0] + row
                search_col = start[1] + col
                pipe = grid[search_row][search_col]
                for direction in pipes_to_dirs[pipe]:
                    if (
                        search_row + direction[0] == start[0]
                        and search_col + direction[1] == start[1]
                    ):
                        connections.append((row, col))
    connections = tuple(sorted(connections))
    return dirs_to_pipes[connections]


def next_dirs(pipe, curr_dir):
    return next(
        ((row, col) for (row, col) in pipes_to_dirs[pipe] if (-row, -col) != curr_dir),
        None,
    )


def add_dir(pos, direction):
    return pos[0] + direction[0], pos[1] + direction[1]


def calc_loop_max_distance(grid, start):
    start_pipe = calc_start_pipe(grid, start)
    grid[start[0]][start[1]] = start_pipe

    distances = {start: 0}
    curr1_dirs = pipes_to_dirs[start_pipe][0]
    curr2_dirs = pipes_to_dirs[start_pipe][1]
    curr1 = add_dir(start, curr1_dirs)
    curr2 = add_dir(start, curr2_dirs)
    steps = 1
    while curr1 != curr2:
        # print(
        #     f"Step {steps}: {curr1} {grid[curr1[0]][curr1[1]]}, {curr2} {grid[curr2[0]][curr2[1]]}"
        # )
        if curr1 in distances or curr2 in distances:
            print(f"Loop detected at step {steps} curr1 {curr1} curr2 {curr2}")
            print(distances)
            break
        distances[curr1] = steps
        distances[curr2] = steps
        curr1_dirs = next_dirs(grid[curr1[0]][curr1[1]], curr1_dirs)
        curr2_dirs = next_dirs(grid[curr2[0]][curr2[1]], curr2_dirs)
        if curr1_dirs is None or curr2_dirs is None:
            raise ValueError(
                f"Invalid state at step {steps}: {curr1_dirs}, {curr2_dirs}"
            )
        curr1 = add_dir(curr1, curr1_dirs)
        curr2 = add_dir(curr2, curr2_dirs)
        steps += 1
        if curr1 == curr2:
            distances[curr1] = steps
    return max(distances.values())


def main():
    parser = argparse.ArgumentParser(description="Day 10: Pipe Maze")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    print(f"Num lines: {len(lines)}")
    grid = parse_grid(lines)
    # print(f"Grid: {grid}")
    start = find_start(grid)
    # print(f"Start: {start}")
    max_loop_distance = calc_loop_max_distance(grid, start)
    print(f"Max loop distance: {max_loop_distance}")


if __name__ == "__main__":
    main()
