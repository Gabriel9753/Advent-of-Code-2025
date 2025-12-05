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
    # return input_data.splitlines()
    input_data = input_data.split("\n" * 2)
    input_data = [x.split("\n") for x in input_data]
    input_data[0] = [tuple(map(int, r.split("-"))) for r in input_data[0]]
    input_data[1] = list(map(int, input_data[1]))
    return input_data


@timer(return_time=True)
def task1(day_input):
    freshes = day_input[0]
    ings = day_input[1]

    fresh_ctr = 0

    for ing in ings:
        for fs, fe in freshes:
            if fs <= ing <= fe:
                fresh_ctr += 1
                break

    return fresh_ctr


@timer(return_time=True)
def task2(day_input):
    freshes = day_input[0]

    freshes = sorted(freshes, key=lambda x: (x[0], -x[1]))
    for i, (_, fe) in enumerate(freshes):
        j = i + 1
        while j < len(freshes):
            nfs, nfe = freshes[j]

            if nfs > fe:
                break
            elif nfe <= fe:
                freshes.pop(j)
                j = j - 1
            else:
                freshes[j] = (fe + 1, nfe)

            j += 1

    return sum([fe - fs + 1 for fs, fe in freshes])


def main(args):
    if not args.final:
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
        avg_time_task1 = average_time(100, task1, [], day_input)
        avg_time_task2 = average_time(100, task2, [], day_input)
        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task2:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", help="Use the final input", action="store_true")
    parser.add_argument("--timeit", help="Average the execution time over 100 runs", action="store_true")
    main(parser.parse_args())
