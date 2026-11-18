# claude-test

## CSV statistics

`csv_stats.py` reads a CSV file and prints the count, mean, min and max of each numeric column.
It needs only Python 3 (standard library, no installs).

```bash
python3 csv_stats.py sample.csv
```

Output for the included `sample.csv`:

```
column       count          mean           min           max
age              5          33.8            23            45
height_cm        5         169.8         158.7           180
score            4         88.69         79.25            95
```

A column counts as numeric when every non-empty cell in it is a number; text columns
(like `name` and `city`) are skipped. Empty cells are ignored and not counted.
