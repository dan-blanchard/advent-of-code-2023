import argparse
from collections import Counter
import fileinput


def parse_line(line):
    """Card line -> (winners, given)"""
    id_chunk, numbers_chunk = line.split(": ")
    card_id = int(id_chunk[4:])
    winners, scratched = numbers_chunk.split(" | ")
    winners = {int(winner) for winner in winners.split()}
    scratched = {int(winner) for winner in scratched.split()}
    return card_id, winners, scratched


def parse_cards(lines):
    return {
        card_id: (winners, scratched)
        for card_id, winners, scratched in (parse_line(line) for line in lines)
    }


def score_card_simple(winners, scratched):
    num_matches = len(winners & scratched)
    return 2 ** (num_matches - 1) if num_matches > 0 else 0


def count_duplicated_cards(cards):
    copies = Counter()
    for card_id, (winners, scratched) in cards.items():
        num_matches = len(winners & scratched)
        copies[card_id] += 1
        for i in range(1, num_matches + 1):
            copies[card_id + i] += copies[card_id]
    return copies.total()


def main():
    parser = argparse.ArgumentParser(description="Day 4: Scratchcards")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    cards = parse_cards(lines)
    total_score = sum(
        score_card_simple(winners, scratched) for winners, scratched in cards.values()
    )
    print(f"Total score: {total_score}")
    print(f"Card count with duplication: {count_duplicated_cards(cards)}")


if __name__ == "__main__":
    main()
