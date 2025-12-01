import argparse
import os
import re
import sys
from collections import defaultdict
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

get_next = lambda cur, _in, _dir: cur + _in if _dir.lower() == "r" else cur - _in

# is there a numpy method to check a sign change?
# Answer: np.signbit does that


@timer(return_time=True)
def preprocess_input(input_data):
    # Preprocess the input data (if needed)
    return input_data.splitlines()


@timer(return_time=True)
def task1(day_input):
    pos_counter = defaultdict(int)
    current = 50
    for line in day_input:
        current = get_next(current, int(line[1:]), line[0]) % 100
        pos_counter[current] += 1
    return pos_counter[0]


@timer(return_time=True)
def task2(day_input):
    current = 50
    total_skips = 0
    for line in day_input:
        direction = line[0]
        dist = int(line[1:])

        if direction == "R":
            # current is always 0 <= current < 100
            skips, current = divmod(current + dist, 100)
        elif direction == "L":
            # to avoid counting 0, 100, ... again if on it currently by going left -1
            # // always floors down, so for example -1 // 100 = -1 <----- 5 -- L8 --> -3 // 100 = -1
            skips = ((current - 1) // 100) - ((current - dist - 1) // 100)
            current = (current - dist) % 100

        total_skips += skips

    return total_skips


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
