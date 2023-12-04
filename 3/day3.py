import argparse
from enum import StrEnum
import fileinput
import math


class EngineSymbol(StrEnum):
    GEAR = "*"
    POUND = "#"
    PLUS = "+"
    DOLLAR = "$"
    MINUS = "-"
    AT = "@"
    EQUAL = "="
    PERCENT = "%"
    SLASH = "/"
    AND = "&"


def parse_input_file(lines):
    """Return a grid of entire input file and a list of all EngineSymbol locations"""
    print(f"Number of lines in file: {len(lines)}")
    grid = []
    engine_symbols = []
    for row_num, line in enumerate(lines):
        # Don't strip the line to make handling end of number simpler
        num_start = None
        row = []
        for col_num, char in enumerate(line):
            if char.isdigit():
                if num_start is None:
                    num_start = col_num
            else:
                if num_start is not None:
                    num = int(line[num_start:col_num])
                    row.extend([num] * (col_num - num_start))
                    num_start = None
                if char == ".":
                    row.append(None)
                elif char == "\n":
                    continue
                else:
                    row.append(EngineSymbol(char))
                    engine_symbols.append((row_num, col_num))
        grid.append(row)

    return grid, engine_symbols


def get_all_part_numbers(grid, engine_symbols):
    """Part numbers are numbers in the grid that are adjacent to EngineSymbols"""
    part_numbers = []
    num_rows = len(grid)
    num_cols = len(grid[0])
    for i, j in engine_symbols:
        # Look for numbers adjacent to EngineSymbols
        adjacent_numbers = set()
        for i_offset in range(-1, 2):
            for j_offset in range(-1, 2):
                i_adj = i + i_offset
                j_adj = j + j_offset
                if (
                    0 <= i_adj < num_rows
                    and 0 <= j_adj < num_cols
                    and isinstance(grid[i_adj][j_adj], int)
                ):
                    adjacent_numbers.add(grid[i_adj][j_adj])
        part_numbers.extend(adjacent_numbers)
    return part_numbers


def get_all_gear_ratios(grid, engine_symbols):
    """Gear ratio is product of two numbers adjacvent to EngineSymbol.GEAR"""
    gear_symbols = [
        (row, col) for row, col in engine_symbols if grid[row][col] == EngineSymbol.GEAR
    ]
    num_rows = len(grid)
    num_cols = len(grid[0])
    gear_ratios = []
    for i, j in gear_symbols:
        # Look for numbers adjacent to EngineSymbols
        adjacent_numbers = set()
        for i_offset in range(-1, 2):
            for j_offset in range(-1, 2):
                i_adj = i + i_offset
                j_adj = j + j_offset
                if (
                    0 <= i_adj < num_rows
                    and 0 <= j_adj < num_cols
                    and isinstance(grid[i_adj][j_adj], int)
                ):
                    adjacent_numbers.add(grid[i_adj][j_adj])
        if len(adjacent_numbers) == 2:
            gear_ratios.append(math.prod(adjacent_numbers))
    return gear_ratios


def main():
    parser = argparse.ArgumentParser(description="Day 3: Cube Conundrum")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    grid, engine_symbols = parse_input_file(lines)
    part_numbers = get_all_part_numbers(grid, engine_symbols)
    print(f"Engine symbols: {engine_symbols}")
    print(f"Part numbers: {part_numbers}")
    print(f"Sum of part numbers: {sum(part_numbers)}")
    gear_ratios = get_all_gear_ratios(grid, engine_symbols)
    print(f"Gear ratios: {gear_ratios}")
    print(f"Sum of gear ratios: {sum(gear_ratios)}")


if __name__ == "__main__":
    main()
