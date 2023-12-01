import argparse
import fileinput


def sum_calibration_numbers(lines, handle_words):
    total = 0
    words_to_digits = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    reversed_words = {"".join(reversed(word)): word for word in words_to_digits}
    for line in lines:
        first = None
        last = None
        line = line.strip()
        for i, c in enumerate(line):
            if c.isdigit():
                first = c
            elif handle_words:
                for word, digit in words_to_digits.items():
                    if line[i : i + len(word)] == word:
                        first = digit
            if first is not None:
                break

        reversed_line = "".join(reversed(line))
        for i, c in enumerate(reversed_line):
            if c.isdigit():
                last = c
            elif handle_words:
                for reversed_word, word in reversed_words.items():
                    if reversed_line[i : i + len(reversed_word)] == reversed_word:
                        last = words_to_digits[word]
            if last is not None:
                break

        val = int(f"{first}{last}")
        total += val
    return total


def main():
    parser = argparse.ArgumentParser(
        description="Calculate sum of calibration numbers in a file."
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    print(f"Total without words: {sum_calibration_numbers(lines, False)}")
    print(f"Total with words: {sum_calibration_numbers(lines, True)}")


if __name__ == "__main__":
    main()
