import argparse
import fileinput
from collections import Counter
from functools import cached_property, total_ordering


card_vals1 = {
    card: i
    for i, card in enumerate(
        [str(i) for i in range(2, 10)] + ["T", "J", "Q", "K", "A"], start=2
    )
}


card_vals2 = {
    card: i
    for i, card in enumerate(
        ["J"] + [str(i) for i in range(2, 10)] + ["T", "Q", "K", "A"], start=1
    )
}


@total_ordering
class Hand:
    def __init__(self, cards, bid, wild=None):
        self.cards = cards
        self.bid = bid
        self.wild = wild

    def __lt__(self, other):
        return self.score_type < other.score_type or (
            self.score_type == other.score_type and self.cards < other.cards
        )

    def __eq__(self, other):
        return self.cards == other.cards

    def __hash__(self):
        return hash(self.cards)

    def __repr__(self):
        return f"Hand({self.cards}, {self.bid})"

    @cached_property
    def score_type(self):
        counts = Counter(self.cards)
        if self.wild is not None:
            num_types = len(counts.keys())
            for card, _ in counts.most_common():
                if card != self.wild:
                    counts[card] += counts[self.wild]
                    del counts[self.wild]
                    break
        num_types = len(counts.keys())
        val = 0
        if num_types == 1:
            val = 7
        elif num_types == 5:
            val = 1
        else:
            highest = counts.most_common(1)[0][1]
            if highest == 4:
                val = 6
            elif highest == 3:
                if num_types == 2:
                    val = 5
                else:
                    val = 4
            elif highest == 2:
                if num_types == 3:
                    val = 3
                else:
                    val = 2
        return val

    def score(self, rank):
        return rank * self.bid


def parse_hands(lines, card_vals, wild=None):
    """Returns list of (hand, bid)"""
    hands = []
    for line in lines:
        hand, bid = line.strip().split()
        hand = tuple(card_vals[card] for card in hand)
        bid = int(bid)
        hands.append(Hand(hand, bid, wild=wild))
    return hands


def score_hands(hands):
    return sum(hand.score(i) for i, hand in enumerate(sorted(hands), start=1))


def main():
    parser = argparse.ArgumentParser(description="Day 7: Camel Cards")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    print(f"Num lines: {len(lines)}")
    hands = parse_hands(lines, card_vals1)
    # print(f"Hands: {hands}")
    print(f"Score 1: {score_hands(hands)}")
    hands = parse_hands(lines, card_vals2, wild=card_vals2["J"])
    print(f"Score 2: {score_hands(hands)}")


if __name__ == "__main__":
    main()
