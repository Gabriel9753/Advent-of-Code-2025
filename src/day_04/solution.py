import argparse
import os
import re
import sys
from collections import deque
from datetime import datetime
from functools import lru_cache
from itertools import product

from rich import print

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, safe_pop, timer, write_times_to_readme

sys.setrecursionlimit(5000)

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


@timer(return_time=True)
def preprocess_input(input_data):
    return {(x, y): val for y, line in enumerate(input_data.splitlines()) for x, val in enumerate(line)}


@lru_cache(maxsize=12000)
def construct_adjacent_positions(x, y):
    return {(x + dx, y + dy) for dx, dy in filter(lambda d: d != (0, 0), product([-1, 0, 1], repeat=2))}


@timer(return_time=True)
def task1(day_input):
    all_paper_rolls = {(k[0], k[1]) for k, v in day_input.items() if v == "@"}
    queue = deque(all_paper_rolls)

    accessable_rolls = set()

    while roll := safe_pop(queue):
        adj_positions = construct_adjacent_positions(roll[0], roll[1])
        if len(adj_positions.intersection(all_paper_rolls)) < 4:
            accessable_rolls.add(roll)

    return len(accessable_rolls)


@timer(return_time=True)
def task2(day_input):
    accessable_rolls = set()
    last_intersections = set()

    while True:
        all_paper_rolls = {(k[0], k[1]) for k, v in day_input.items() if v == "@"}
        all_paper_rolls_of_interest = (
            {p for p in all_paper_rolls if p in last_intersections} if last_intersections else all_paper_rolls
        )
        last_intersections = set()
        new_rolls = set()
        queue = deque(all_paper_rolls_of_interest)

        while roll := safe_pop(queue):
            adj_positions = construct_adjacent_positions(roll[0], roll[1])
            inters = adj_positions.intersection(all_paper_rolls)
            if len(inters) < 4:
                new_rolls.add(roll)
                day_input[(roll[0], roll[1])] = "."
                last_intersections.update(inters)

        if len(new_rolls) <= 0:
            break
        accessable_rolls.update(new_rolls)

    return len(accessable_rolls)


def main(args):
    if not args.final:
        day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    else:
        day_input = load_input(os.path.join(cur_dir, "input.txt"))

    day_input, t = preprocess_input(day_input)
    result_task1, time_task1 = task1(day_input)
    result_task2, time_task2 = task2(day_input)
    print(f"Hits construct_adjacent_positions {construct_adjacent_positions.cache_info()}")

    print(f"\nDay {cur_day}")
    print("------------------")
    print(f"Processing data: {t:.6f} seconds")
    print(f"Task 1: {result_task1} ({time_task1:.6f} seconds)")
    print(f"Task 2: {result_task2} ({time_task2:.6f} seconds)")

    if args.timeit:
        avg_time_task1 = average_time(100, task1, [construct_adjacent_positions], day_input)
        avg_time_task2 = average_time(100, task2, [construct_adjacent_positions], day_input)
        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task2:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", help="Use the final input", action="store_true")
    parser.add_argument("--timeit", help="Average the execution time over 100 runs", action="store_true")
    main(parser.parse_args())
