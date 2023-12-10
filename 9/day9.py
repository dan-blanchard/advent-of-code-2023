import argparse
import fileinput


def get_difference_stack(line):
    line = line.strip()
    numbers = [int(x) for x in line.split()]
    num_stack = [numbers]
    differences = numbers
    while not all(diff == 0 for diff in differences):
        differences = [x - y for x, y in zip(differences[1:], differences[:-1])]
        num_stack.append(differences)
    return num_stack


def predict_next(line, verbose=False):
    num_stack = get_difference_stack(line)
    if verbose:
        print_stack(num_stack)

    # predict the next numbers
    for i, numbers in enumerate(reversed(num_stack)):
        if i == 0:
            prev_num = 0
        else:
            prev_num = num_stack[-i][-1]
        numbers.append(prev_num + numbers[-1])

    if verbose:
        print_stack(num_stack)
        print("-" * 40)
        print()

    return num_stack[0][-1]


def predict_prev(line, verbose=False):
    num_stack = get_difference_stack(line)

    if verbose:
        print_stack(num_stack)

    # predict the next numbers
    for i, numbers in enumerate(reversed(num_stack)):
        if i == 0:
            prev_num = 0
        else:
            prev_num = num_stack[-i][0]
        numbers.insert(0, numbers[0] - prev_num)

    if verbose:
        print_stack(num_stack)
        print("-" * 40)
        print()

    return num_stack[0][0]


def print_stack(num_stack):
    longest_num = len(str(num_stack[-1][-1]))
    padding = (longest_num + 1) * " "
    join_space = (longest_num + 2) * " "
    for i, numbers in enumerate(num_stack):
        print(padding * i, end="")
        print(join_space.join(str(x) for x in numbers))
    print(flush=True)


def main():
    parser = argparse.ArgumentParser(description="Day 9: Mirage Maintenance")
    parser.add_argument(
        "files",
        metavar="FILE",
        nargs="*",
        help="Files to read. If empty, stdin is used.",
    )
    args = parser.parse_args()
    lines = list(fileinput.input(args.files))
    print(f"Num lines: {len(lines)}")
    predictions = [predict_next(line) for line in lines]
    print(f"Prediction sum (-1): {sum(predictions)}")
    predictions = [predict_prev(line) for line in lines]
    print(f"Prediction sum (0): {sum(predictions)}")


if __name__ == "__main__":
    main()
