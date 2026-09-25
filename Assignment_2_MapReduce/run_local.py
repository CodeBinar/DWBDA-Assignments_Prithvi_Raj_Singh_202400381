#!/usr/bin/env python3
"""
Local driver that simulates the Hadoop Streaming MapReduce pipeline:

    cat student_results.csv | mapper.py | sort | reducer.py

This lets the assignment be demonstrated on a laptop without an actual
Hadoop cluster. To run it for real on Hadoop, see README.md for the
`hadoop jar hadoop-streaming.jar ...` command using these same
mapper.py / reducer.py files unchanged.

Run:
    python run_local.py
"""

import subprocess
import sys


def main(data_file="student_results.csv"):
    with open(data_file) as f:
        data = f.read()

    map_proc = subprocess.run(
        [sys.executable, "mapper.py"], input=data, capture_output=True, text=True
    )
    if map_proc.returncode != 0:
        print("Mapper failed:", map_proc.stderr, file=sys.stderr)
        sys.exit(1)

    # Simulate Hadoop's shuffle-and-sort phase
    sorted_lines = sorted(map_proc.stdout.splitlines())
    sorted_input = "\n".join(sorted_lines) + "\n"

    reduce_proc = subprocess.run(
        [sys.executable, "reducer.py"], input=sorted_input, capture_output=True, text=True
    )
    if reduce_proc.returncode != 0:
        print("Reducer failed:", reduce_proc.stderr, file=sys.stderr)
        sys.exit(1)

    print("=== Raw MapReduce output (Subject,Grade -> Count) ===")
    print(reduce_proc.stdout)

    with open("grade_distribution_output.txt", "w") as out:
        out.write(reduce_proc.stdout)
    print("Saved raw output to grade_distribution_output.txt")


if __name__ == "__main__":
    main()
