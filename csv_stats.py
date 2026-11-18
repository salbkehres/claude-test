#!/usr/bin/env python3
"""Print basic statistics (count, mean, min, max) for each numeric column of a CSV file.

A column counts as numeric if every non-empty value in it parses as a number.
Empty cells are skipped and not included in the count.
"""

import argparse
import csv
import sys


def parse_number(value):
    """Return value as a float, or None if it isn't a number."""
    try:
        return float(value)
    except ValueError:
        return None


def column_stats(path):
    """Return {column: (count, mean, min, max)} for the numeric columns in the CSV at path."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return {}
        values = {name: [] for name in reader.fieldnames}
        non_numeric = set()
        for row in reader:
            for name in reader.fieldnames:
                cell = (row.get(name) or "").strip()
                if not cell or name in non_numeric:
                    continue
                number = parse_number(cell)
                if number is None:
                    non_numeric.add(name)
                else:
                    values[name].append(number)

    stats = {}
    for name, nums in values.items():
        if name in non_numeric or not nums:
            continue
        stats[name] = (len(nums), sum(nums) / len(nums), min(nums), max(nums))
    return stats


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv_file", help="path to the CSV file")
    args = parser.parse_args(argv)

    try:
        stats = column_stats(args.csv_file)
    except (OSError, csv.Error, UnicodeDecodeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if not stats:
        print("No numeric columns found.")
        return 0

    width = max(len("column"), *(len(name) for name in stats))
    print(f"{'column':<{width}}  {'count':>7}  {'mean':>12}  {'min':>12}  {'max':>12}")
    for name, (count, mean, lo, hi) in stats.items():
        print(f"{name:<{width}}  {count:>7}  {mean:>12.4g}  {lo:>12.4g}  {hi:>12.4g}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
