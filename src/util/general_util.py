import functools
import os
import re
import sys
import time
from collections import deque
from typing import List

cur_dir = os.path.dirname(os.path.abspath(__file__))
# full path to the parent directory
readme_dir = os.path.dirname(os.path.dirname(cur_dir))
README_PATH = os.path.join(readme_dir, "README.md")


# Timer decorator to measure the execution time of a function
def timer(return_time=False):
    """
    Example usage:
    @timer(return_time=True)\\
    def example_function():
        # Your code here
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            if return_time:
                return result, execution_time
            else:
                print(f"{func.__name__}: {execution_time:.6f} seconds")
                return result

        return wrapper

    return decorator


def load_input(input_file_path):
    try:
        with open(input_file_path, "r", encoding="utf-8") as input_file:
            return input_file.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file not found ({input_file_path})")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading input {input_file_path}: {e}")
        sys.exit(1)


def average_time(runs, func, func_caches_to_reset: List[functools._lru_cache_wrapper] = [], *args, **kwargs):
    total_time = 0
    for _ in range(runs):
        _, time = func(*args, **kwargs)
        total_time += time
        for f in func_caches_to_reset:
            if hasattr(f, "cache_clear") and callable(getattr(f, "cache_clear")):
                # print(f"Clear cache of {f.__class__.__name__} with: {f.cache_info()}")
                f.cache_clear()

    return total_time / runs


def safe_pop(q: deque, popleft: bool = False):
    """
    To pop elements from a queue in a while loop:
    while (roll := safe_pop(q)):
        ...
    """
    try:
        return q.pop() if not popleft else q.popleft()
    except IndexError:
        return None


def write_times_to_readme(day, time_task1, time_task2):
    if not os.path.exists(README_PATH):
        print(f"Error: README file not found ({README_PATH})")
        sys.exit(1)

    with open(README_PATH, "r") as file:
        lines = file.readlines()
    # https://github.com/Gabriel9753/Advent-of-Code-2025/blob/main/src/day_01/solution.py
    # Extract the base URL dynamically
    base_url = None
    for line in lines:
        match = re.search(r"\[1\]\((.+?/day_01/solution\.py)\)", line)
        if match:
            base_url = match.group(1).rsplit("/day_01", 1)[0]
            break

    if base_url is None:
        print("Error: Could not determine the base URL from the table.")
        sys.exit(1)

    # Construct the regex pattern to find the correct day
    day_pattern = re.compile(
        rf"^\|\s*\[{day}\]\(.*day_{int(day):02d}/solution\.py\)\s*\|\s*([\d.-]+|-)\s*\|\s*([\d.-]+|-)\s*\|$"
    )

    updated = False
    for i, line in enumerate(lines):
        if day_pattern.match(line):
            lines[i] = (
                f"| [{day}]({base_url}/day_{int(day):02d}/solution.py)   "
                f"| {time_task1:.6f}      | {time_task2:.6f}      |\n"
            )
            updated = True
            break

    if not updated:
        print(f"Error: Day {day} not found in the table.")
        sys.exit(1)

    with open(README_PATH, "w") as file:
        file.writelines(lines)

    print(f"Times for Day {day} updated successfully.")
