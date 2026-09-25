#!/usr/bin/env python3
"""
Turns the raw MapReduce reducer output (grade_distribution_output.txt) into a
readable Subject x Grade table, across all subjects, with a combined totals
row.

Run (after run_local.py):
    python summarize.py
"""

import pandas as pd

GRADES = ["S", "A", "B", "C", "D", "E", "F", "I", "DT", "MP"]


def main():
    rows = []
    with open("grade_distribution_output.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            key, count = line.split("\t")
            subject, grade = key.rsplit(",", 1)
            rows.append((subject, grade, int(count)))

    df = pd.DataFrame(rows, columns=["Subject", "Grade", "Count"])
    pivot = (
        df.pivot(index="Subject", columns="Grade", values="Count")
        .reindex(columns=GRADES)
        .fillna(0)
        .astype(int)
    )
    pivot["Total Students"] = pivot.sum(axis=1)
    pivot.loc["ALL SUBJECTS (combined)"] = pivot.sum()

    pd.set_option("display.width", 160)
    print(pivot)
    pivot.to_csv("grade_distribution_table.csv")
    print("\nSaved table to grade_distribution_table.csv")
    print("\n(I = Absent, DT = Detained, MP = Malpractice -- not exam-marks-based categories)")


if __name__ == "__main__":
    main()
