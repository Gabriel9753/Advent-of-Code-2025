import argparse
import os
import re
import sys
from datetime import datetime

import numpy as np
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
    return [list(map(int, l)) for l in input_data.splitlines()]


@timer(return_time=True)
def task1(day_input):
    packs = []
    cols = len(day_input[0])
    max_batts = 2

    # OLD SOLUTION FOR PART I
    # for l in day_input:
    #     idx_max = np.argmax(l, axis=0)
    #     val_max = l[idx_max]
    #     if idx_max < cols - 1:  # there is a max value right
    #         idx_second_max = np.argmax(l[idx_max + 1 :]) + idx_max + 1
    #         val_second_max = l[idx_second_max]
    #         packs.append(int(f"{val_max}{val_second_max}"))
    #     else:  # edge case, if max value is the last value
    #         idx_replace_max = np.argmax(l[:idx_max])
    #         val_replace_max = l[idx_replace_max]
    #         packs.append(int(f"{val_replace_max}{val_max}"))

    for l in day_input:
        pack = ""
        new_b_idx = 0
        for b_limit in range(max_batts, 0, -1):
            idx_max = np.argmax(l[new_b_idx : cols - b_limit + 1]) + new_b_idx
            pack += str(l[idx_max])
            new_b_idx = idx_max + 1
        packs.append(int(pack))

    return sum(packs)


@timer(return_time=True)
def task2(day_input):
    packs = []
    cols = len(day_input[0])
    max_batts = 12

    for l in day_input:
        pack = ""
        new_b_idx = 0
        for b_limit in range(max_batts, 0, -1):
            idx_max = np.argmax(l[new_b_idx : cols - b_limit + 1]) + new_b_idx
            pack += str(l[idx_max])
            new_b_idx = idx_max + 1
        packs.append(int(pack))

    return sum(packs)


# 3121910778619
# 3110379966860


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
