import argparse
import fileinput


def parse_almanac(lines, use_seed_ranges=False):
    seeds = set()
    mappings = {}
    current_mapping = {}
    name = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("seeds:"):
            numbers = [int(num) for num in line[7:].split()]
            if use_seed_ranges:
                for start, length in zip(numbers[::2], numbers[1::2]):
                    seeds.add((start, length))
            else:
                seeds.update(numbers)
        elif not line[0].isdigit():
            if name is None:
                name = line.split()[0]
                continue
            mappings[name] = current_mapping
            name = line.split()[0]
            current_mapping = {}
        else:
            dest_start, src_start, length = (int(chunk) for chunk in line.split())
            current_mapping[src_start, src_start + length] = dest_start - src_start
    mappings[name] = current_mapping
    return seeds, mappings


def location_for_seed(seed, almanac):
    category = "seed"
    src_num = seed
    # print(f"{category.title()}: {src_num}", end=", ")
    while category != "location":
        name, mapping = next(
            (
                (name, mapping)
                for name, mapping in almanac.items()
                if name.startswith(category)
            ),
            (None, None),
        )
        if name is None or mapping is None:
            raise ValueError(f"Unknown category: {category}")
        for (src_start, src_end), delta in mapping.items():
            if src_start <= src_num < src_end:
                src_num += delta
                break
        category = name.split("-")[-1]
    #     print(f"{category.title()}: {src_num}", end=", ")
    # print()
    return src_num


def find_lowest_seed_location(seeds, almanac):
    return min(location_for_seed(seed, almanac) for seed in seeds)


def find_lowest_seed_location_ranges(seeds, almanac):
    min_location = float("inf")
    for seed_start, length in seeds:
        for seed in range(seed_start, seed_start + length):
            location = location_for_seed(seed, almanac)
            if location < min_location:
                min_location = location
    return min_location


def main():
    parser = argparse.ArgumentParser(
        description="Day 5: If You Give A Seed A Fertilizer"
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    print(f"Num lines: {len(lines)}")
    seeds, almanac = parse_almanac(lines)
    # print("Seeds:", seeds)
    # print("Almanac:", almanac)
    print("Lowest seed location:", find_lowest_seed_location(seeds, almanac))
    seeds, almanac = parse_almanac(lines, use_seed_ranges=True)
    print(
        "Lowest seed location (with ranges):",
        find_lowest_seed_location_ranges(seeds, almanac),
    )


if __name__ == "__main__":
    main()
