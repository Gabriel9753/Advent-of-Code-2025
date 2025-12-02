import argparse
import os
import re
import sys
from datetime import datetime

from rich import print

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


@timer(return_time=True)
def preprocess_input(input_data):
    # Preprocess the input data (if needed)
    return [x.split("-") for x in input_data.split(",")]


@timer(return_time=True)
def task1(day_input):
    # Day-specific code for Task 1
    total = 0

    for pair in day_input:
        start, end = int(pair[0]), int(pair[1])
        for num in range(start, end + 1):
            s_id = str(num)
            length = len(s_id)

            if length % 2 == 1:
                continue

            half = length // 2
            if s_id[:half] == s_id[half:]:
                total += num

    return total


@timer(return_time=True)
def task2(day_input):
    total = 0

    for pair in day_input:
        start, end = int(pair[0]), int(pair[1])
        for num in range(start, end + 1):
            s_id = str(num)
            dup = f"{s_id}{s_id}"
            # total += num if any(dup[i : i + len(s_id)] == s_id for i in range(1, len(s_id) // 2 + 1)) else 0
            for i in range(1, len(s_id) // 2 + 1):
                if dup[i : i + len(s_id)] == s_id:
                    total += num
                    break

    return total


def main(args):
    # Choose between the real input or the example input
    if args.example:
        day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    else:
        day_input = load_input(os.path.join(cur_dir, "input.txt"))

    day_input, t = preprocess_input(day_input)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    print(f"Processing data: {t:.6f} seconds")
    print(f"Task 1: {result_task1} ({time_task1:.6f} seconds)")
    print(f"Task 2: {result_task2} ({time_task2:.6f} seconds)")

    if args.timeit:
        avg_time_task1 = average_time(100, task1, day_input)
        avg_time_task2 = average_time(100, task2, day_input)
        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task2:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", type=int, help="Use the example input", default=1)
    parser.add_argument("--timeit", type=int, help="Average the execution time over 100 runs", default=0)
    main(parser.parse_args())
