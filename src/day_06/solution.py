import argparse
import os
import re
import sys
from bisect import bisect_left, bisect_right, insort
from collections import OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from functools import lru_cache, partial
from heapq import heapify, heappop, heappush
from itertools import chain, combinations, permutations, product
from math import ceil, floor, gcd, inf, lcm, log2, sqrt
from operator import mul
from typing import Dict, List, Set, Tuple

import numpy as np
import z3
from more_itertools import chunked, windowed
from rich import print

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, timer, write_times_to_readme

sys.setrecursionlimit(5000)

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


@timer(return_time=True)
def preprocess_input(input_data):
    inp = input_data.splitlines()
    return inp


op = {"+": np.sum, "*": np.prod}


@timer(return_time=True)
def task1(inp):
    inp = np.array([re.findall(r"\d+", r) for r in inp[:-1]] + [re.findall(r"\*|\+|\-", inp[-1])]).T
    return sum([op[x[-1]](list(map(int, x[:-1]))) for x in inp])


@timer(return_time=True)
def task2(inp):
    """
    123 328  51 64
     45 64  387 23
      6 98  215 314
    ->
    ['1' ' ' ' '] |
    ['2' '4' ' '] | GROUP I
    ['3' '5' '6'] |
    [' ' ' ' ' ']
    ['3' '6' '9'] |
    ['2' '4' '8'] | GROUP II
    ['8' ' ' ' '] |
    [' ' ' ' ' ']
    [' ' '3' '2'] |
    ['5' '8' '1'] | GROUP III
    ['1' '7' '5'] |
    [' ' ' ' ' ']
    ['6' '2' '3'] |
    ['4' '3' '1'] | GROUP IV
    [' ' ' ' '4'] |
    """
    inp, ops = np.array([list(r) for r in inp[:-1]]).T, re.findall(r"\*|\+", inp[-1])
    groups = defaultdict(list)
    group = 0
    for row in inp:
        if all([x == " " for x in row]):
            group += 1
        else:
            groups[group].append(int("".join(row)))

    """
    ['1' ' ' ' '] |
    ['2' '4' ' '] | GROUP I
    ['3' '5' '6'] |
    [' ' ' ' ' ']
    ['3' '6' '9'] |
    ['2' '4' '8'] | GROUP II
    ['8' ' ' ' '] |
    [' ' ' ' ' ']
    [' ' '3' '2'] |
    ['5' '8' '1'] | GROUP III
    ['1' '7' '5'] |
    [' ' ' ' ' ']
    ['6' '2' '3'] |
    ['4' '3' '1'] | GROUP IV
    [' ' ' ' '4'] |
    
    ->
    defaultdict(<class 'list'>, {0: [1, 24, 356], 1: [369, 248, 8], 2: [32, 581, 175], 3: [623, 431, 4]})
    
    ops = ['*', '+', '*', '+'] # group 0, 1, 2, 3...
    """
    return sum(op[ops[g]](x) for g, x in groups.items())


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
