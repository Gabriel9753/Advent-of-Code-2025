import argparse
import os
import re
import sys
from datetime import datetime
from functools import lru_cache

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
    return [tuple(map(int, l)) for l in input_data.splitlines()]


@lru_cache(maxsize=50000)
def get_max_args(l):
    return np.argmax(l)


def get_highest_joltage(day_input, batteries):
    cols = len(day_input[0])
    result = 0

    for l in day_input:
        pack = []
        new_b_idx = 0
        for b_limit in range(batteries, 0, -1):
            idx_max = get_max_args(l[new_b_idx : cols - b_limit + 1]) + new_b_idx
            pack.append(l[idx_max])
            new_b_idx = idx_max + 1
        result += int("".join(map(str, pack)))
    return result


@timer(return_time=True)
def task1(day_input):
    return get_highest_joltage(day_input, 2)


@timer(return_time=True)
def task2(day_input):
    return get_highest_joltage(day_input, 12)


def main(args):
    # Choose between the real input or the example input
    if args.example:
        day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    else:
        day_input = load_input(os.path.join(cur_dir, "input.txt"))

    day_input, t = preprocess_input(day_input)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)
    # print(f"Hits and size: {get_max_args.cache_info()} | {get_max_args.cache_parameters()}")

    print(f"\nDay {cur_day}")
    print("------------------")
    print(f"Processing data: {t:.6f} seconds")
    print(f"Task 1: {result_task1} ({time_task1:.6f} seconds)")
    print(f"Task 2: {result_task2} ({time_task2:.6f} seconds)")

    if args.timeit:
        avg_time_task1 = average_time(100, task1, [get_max_args], day_input)
        avg_time_task2 = average_time(100, task2, [get_max_args], day_input)
        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task2:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", type=int, help="Use the example input", default=1)
    parser.add_argument("--timeit", type=int, help="Average the execution time over 100 runs", default=0)
    main(parser.parse_args())
