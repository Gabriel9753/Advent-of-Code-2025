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


@timer(return_time=True)
def preprocess_input(input_data):
    return {(x, y): v for y, col in enumerate(input_data.splitlines()) for x, v in enumerate(col)}


def get_values(_map, col=None, row=None):
    values = []
    i = 0
    while True:
        value = _map.get((col, i), None) if col else _map.get((i, row), None)
        if value:
            values.append((i, value))
        else:
            break
        i += 1
    return values


@timer(return_time=True)
def task1(day_input):
    beams = set(x for (x, y), v in day_input.items() if v == "S")
    total_splits = 0
    row = 1
    while True:
        row_values = get_values(day_input, row=row)
        row += 1
        if len(row_values) <= 0:
            break
        splitters = {col for col, v in row_values if v == "^"}
        if len(splitters) <= 0:
            continue
        split_locations = beams.intersection(splitters)
        new_beams = set()
        for _split in split_locations:
            new_beams.add(_split - 1)
            new_beams.add(_split + 1)
            beams.remove(_split)
        beams.update(new_beams)
        total_splits += len(split_locations)
    return total_splits


@timer(return_time=True)
def task2(day_input):
    beams = list(x for (x, y), v in day_input.items() if v == "S")
    active_timelines = defaultdict(int)
    active_timelines[beams[0]] += 1
    beams = set(beams)

    row = 1
    while True:
        row_values = get_values(day_input, row=row)
        row += 1
        if len(row_values) <= 0:
            break
        splitters = {col for col, v in row_values if v == "^"}
        if len(splitters) <= 0:
            continue
        # no matter how many timelines split on the same splitter, we only need to check once for each which new unique beams are created
        split_locations = beams.intersection(splitters)

        new_beams = set()
        for _split in split_locations:
            new_left, new_right = _split - 1, _split + 1
            new_beams.add(new_left)
            new_beams.add(new_right)
            beams.remove(_split)
        beams.update(set(new_beams))

        # part two keeps track of timelines
        # so if there is a split, all timelines need to be updated (not as above, not unique)

        new_timelines = active_timelines.copy()
        for at, cnt in active_timelines.items():
            if at in split_locations:
                # split all timelines
                new_timelines[at - 1] += cnt
                new_timelines[at + 1] += cnt
                # remove all the beams which got splitted
                new_timelines[at] -= cnt
        active_timelines = new_timelines

    return sum(active_timelines.values())


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
