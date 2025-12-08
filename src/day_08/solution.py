import argparse
import os
import re
import sys
from collections import namedtuple
from datetime import datetime
from typing import Counter

import numpy as np
from rich import print
from scipy.spatial import KDTree

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, timer, write_times_to_readme

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


class uf_ds:
    def __init__(self):
        self.parent_node = {}
        self.last_connected = []
        self.num_sets = 0

    def make_set(self, u):
        for i in u:
            self.parent_node[i] = i
        self.num_sets = len(self.parent_node)

    def op_find(self, k):
        if self.parent_node[k] == k:
            return k
        self.parent_node[k] = self.op_find(self.parent_node[k])
        return self.parent_node[k]

    def op_union(self, a, b):
        x = self.op_find(a)
        y = self.op_find(b)
        self.last_connected = [a, b]
        if x != y:
            self.parent_node[x] = y
            self.num_sets -= 1

    def get_toal_parents(self):
        return self.num_sets


@timer(return_time=True)
def preprocess_input(input_data):
    Point = namedtuple("Point", ["x", "y", "z"])
    inp = input_data.splitlines()
    return [Point(*map(int, p.split(","))) for p in inp]


@timer(return_time=True)
def task1(points):
    steps = 1000
    tree = KDTree(points)
    dist, ind = tree.query(points, k=10)

    edges = []
    for i in range(len(points)):
        for j in range(1, 10):
            if i < ind[i][j]:
                edges.append((float(dist[i][j]), i, int(ind[i][j])))
    edges.sort(key=lambda x: x[0])

    uf = uf_ds()
    uf.make_set([x[1] for x in edges] + [x[2] for x in edges])

    for step in range(steps):
        uf.op_union(edges[step][1], edges[step][2])

    circuits = []
    for i, p in enumerate(points):
        circuits.append((p, uf.op_find(i)))

    circuit_count = Counter([x[1] for x in circuits])
    return np.prod([x[1] for x in circuit_count.most_common(3)])


@timer(return_time=True)
def task2(points):
    tree = KDTree(points)
    dist, ind = tree.query(points, k=10)

    edges = []
    for i in range(len(points)):
        for j in range(1, 10):
            if i < ind[i][j]:
                edges.append((float(dist[i][j]), i, int(ind[i][j])))
    edges.sort(key=lambda x: x[0])

    uf = uf_ds()
    uf.make_set([x[1] for x in edges] + [x[2] for x in edges])

    for step in range(len(edges)):
        uf.op_union(edges[step][1], edges[step][2])
        if uf.get_toal_parents() <= 1:
            return points[uf.last_connected[0]].x * points[uf.last_connected[1]].x


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
