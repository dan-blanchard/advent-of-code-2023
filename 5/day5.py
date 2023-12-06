import argparse
from collections import defaultdict
import fileinput


def parse_almanac(lines):
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


def parse_compressed_almanac(lines, use_seed_ranges):
    seeds = set()
    current_mapping = defaultdict(int)
    prev_mapping = {}
    for line in lines:
        line = line.strip()
        if line.startswith("seeds:"):
            numbers = [int(num) for num in line[7:].split()]
            if use_seed_ranges:
                for start, length in zip(numbers[::2], numbers[1::2]):
                    seeds.add((start, length))
            else:
                seeds.update(numbers)
        elif line and not line[0].isdigit():
            continue
        elif not line:
            unused_prev = set(prev_mapping.keys())
            to_remove = set()
            for (curr_start, curr_end), curr_delta in sorted(current_mapping.items()):
                overlapped = False
                for (prev_start, prev_end), prev_delta in sorted(prev_mapping.items()):
                    if prev_start >= curr_end:
                        break
                    if prev_end <= curr_start:
                        continue
                    unused_prev.discard((prev_start, prev_end))
                    overlap_start = max(prev_start, curr_start)
                    overlap_end = min(prev_end, curr_end)
                    if overlap_start >= overlap_end:
                        raise ValueError(
                            f"Overlap start {overlap_start} >= overlap end {overlap_end}"
                        )
                    overlapped = True
                    breakpoint()
                    current_mapping[overlap_start, overlap_end] = (
                        prev_delta + curr_delta
                    )
                    if overlap_start > curr_start:
                        current_mapping[curr_start, overlap_start] = curr_delta
                    if overlap_end < curr_end:
                        current_mapping[overlap_end, curr_end] = curr_delta
                if overlapped:
                    to_remove.add((curr_start, curr_end))
            for del_key in to_remove:
                del current_mapping[del_key]
            for unused in unused_prev:
                current_mapping[unused] = prev_mapping[unused]
            prev_mapping = current_mapping
            current_mapping = {}
        else:
            dest_start, src_start, length = (int(chunk) for chunk in line.split())
            curr_delta = dest_start - src_start
            curr_end = src_start + length
            current_mapping[src_start, curr_end] = curr_delta

    return seeds, prev_mapping


def location_for_seed(seed, almanac):
    category = "seed"
    src_num = seed
    print(f"{category.title()}: {src_num}", end=", ")
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
        print(f"{category.title()}: {src_num}", end=", ")
    print()
    return src_num


def location_for_seed_compressed(seed, compressed_almanac):
    for (src_start, src_end), delta in compressed_almanac.items():
        if src_start <= seed < src_end:
            return seed + delta
    return seed


def find_lowest_seed_location_compressed(seeds, compressed_almanac):
    return min(location_for_seed_compressed(seed, compressed_almanac) for seed in seeds)


def find_lowest_seed_location(seeds, almanac):
    return min(location_for_seed(seed, almanac) for seed in seeds)


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
    _, compressed_almanac = parse_compressed_almanac(lines, use_seed_ranges=False)
    print("Seeds:", seeds)
    print("Almanac:", almanac)
    print("Compressed Almanac:", compressed_almanac)
    print("Lowest seed location:", find_lowest_seed_location(seeds, almanac))
    print(
        "Lowest seed location (compressed):",
        find_lowest_seed_location_compressed(seeds, compressed_almanac),
    )
    # seeds, almanac = parse_almanac(lines, use_seed_ranges=True)
    # print(
    #     "Lowest seed location (with ranges):", find_lowest_seed_location(seeds, almanac)
    # )


if __name__ == "__main__":
    main()
