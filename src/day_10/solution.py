import argparse
import os
import re
import sys
from collections import deque
from datetime import datetime

import numpy as np
import z3
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
    inp = [
        (re.findall(r"[.*#*]", x), re.findall(r"\(.+\)+", x), re.findall(r"\{.+\}+", x))
        for x in input_data.splitlines()
    ]
    inp = [
        (
            tuple(map(lambda x: "0" if x == "." else "1", c[0])),
            tuple(
                tuple(map(int, y)) for y in [x.replace("(", "").replace(")", "").split(",") for x in c[1][0].split()]
            ),
            tuple(map(int, c[2][0].replace("{", "").replace("}", "").split(","))),
        )
        for c in inp
    ]
    return inp


def bit_to_int(x):
    # converts something like 101 (as int list) to int value 5 (little endian)
    return int("".join(reversed(x)), 2)


@timer(return_time=True)
def task1(day_input):
    total = 0
    target = 0
    for lights, button_configs, _ in day_input:
        current_state = bit_to_int(lights)

        masks = []
        for bc in button_configs:
            mask = 0
            # setting 1 which light the button will activate
            for idx in bc:
                mask |= 1 << idx
            masks.append(mask)

        queue = deque([(current_state, 0)])
        visited = {current_state}

        while queue:
            state, pressed_yet = queue.popleft()

            if state == target:
                total += pressed_yet
                break

            for mask in masks:
                new_state = state ^ mask
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, pressed_yet + 1))

    return total


def dist(a, b):
    return sum(abs(np.array(a) - np.array(b)))


@timer(return_time=True)
def task2(day_input):
    total = 0

    for _, button_configs, target in day_input:
        s = z3.Optimize()

        counts = [z3.Int(f"c_{i}") for i in range(len(button_configs))]
        for c in counts:
            s.add(c >= 0)

        for i, t in enumerate(target):
            # per button, max presses
            s.add(z3.Sum([c for j, c in enumerate(counts) if i in button_configs[j]]) == t)
        total_presses = z3.Sum(counts)
        s.minimize(total_presses)

        if s.check() == z3.sat:
            total += s.model().eval(total_presses).as_long()

    return total


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
