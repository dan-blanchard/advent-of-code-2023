import argparse
import fileinput


# Part 1


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


# Part 2


def apply_mapping(ranges, mapping):
    new_ranges = set()

    for src_start, length in sorted(ranges):
        src_end = src_start + length
        for (curr_start, curr_end), curr_delta in sorted(mapping.items()):
            if curr_start >= src_end:
                break
            if curr_end <= src_start:
                continue
            overlap_start = max(src_start, curr_start)
            overlap_end = min(src_end, curr_end)
            if overlap_start >= overlap_end:
                raise ValueError(
                    f"Overlap start {overlap_start} >= overlap end {overlap_end}"
                )
            # pre-overlap
            if src_start < curr_start:
                new_ranges.add((src_start, curr_start - src_start))
            # overlap
            new_ranges.add((overlap_start + curr_delta, overlap_end - overlap_start))
            src_start = overlap_end
        if src_start > src_end:
            raise ValueError(f"src_start {src_start} > src_end {src_end}")
        if src_start < src_end:
            new_ranges.add((src_start, src_end - src_start))
    new_ranges = sorted(new_ranges)
    return new_ranges


def location_for_seed_ranges(seeds, almanac):
    category = "seed"
    ranges = seeds
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
        ranges = apply_mapping(ranges, mapping)
        category = name.split("-")[-1]
    return ranges


def find_lowest_seed_location_ranges(seeds, almanac):
    locations = location_for_seed_ranges(seeds, almanac)
    return min(locations)[0]


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
