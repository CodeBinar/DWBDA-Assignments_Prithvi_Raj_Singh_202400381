#!/usr/bin/env python3
"""
BONUS / supplementary analysis -- not required by the main MapReduce
pipeline (mapper.py just counts the official grades directly, see its
docstring).

This script instead tries to *derive* each grade from scratch, purely from
raw Marks, using each subject's own S/A/B/C/D/E cutoffs (from
subject_cutoffs.csv). It's here to demonstrate understanding of the
university's grading formula, and to validate it against the official
grades already on the sheets.

Result: 1145 / 1167 records (98.1%) match exactly.

The 22 mismatches are all cases officially graded 'F' where our cutoff-only
formula computed a higher grade (D or E) from the Total. Investigating the
raw numbers shows why: the sheets also apply a rule the NOTE describes as
"IF UM < 35 percent ... Grade is F" -- but "35 percent" here is 35% of the
END-SEM component's OWN maximum marks (which is not printed on the sheet and
is smaller than 100 for some subjects, e.g. 60), not 35 out of the Total's
100. E.g. on GN201B1, every mismatch has UM < 21 (= 35% of a 60-mark
end-sem paper), which forces grade F regardless of how high the Total is.
Since the per-subject end-sem maximum isn't printed anywhere on these
sheets, this rule can't be reconstructed exactly from the data we have --
which is exactly why the main pipeline (mapper.py) counts the OfficialGrade
that the university already computed, rather than re-deriving it.

Run:
    python derive_grade_from_marks.py
"""

import csv


def load_cutoffs(path="subject_cutoffs.csv"):
    cutoffs = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cutoffs[row["Subject"]] = {g: float(row[g]) for g in ["E", "D", "C", "B", "A", "S"]}
    return cutoffs


def marks_to_grade(marks, status, subject, cutoffs):
    if status == "Absent":
        return "I"
    if status == "Detained":
        return "DT"
    if status == "Malpractice":
        return "MP"

    marks = float(marks)
    c = cutoffs[subject]
    if marks >= c["S"]:
        return "S"
    elif marks >= c["A"]:
        return "A"
    elif marks >= c["B"]:
        return "B"
    elif marks >= c["C"]:
        return "C"
    elif marks >= c["D"]:
        return "D"
    elif marks >= c["E"]:
        return "E"
    else:
        return "F"


def main():
    cutoffs = load_cutoffs()
    total = matched = 0
    mismatches = []

    with open("student_results.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            computed = marks_to_grade(row["Marks"], row["Status"], row["Subject"], cutoffs)
            official = row["OfficialGrade"]
            if computed == official:
                matched += 1
            else:
                mismatches.append((row["StudentID"], row["Subject"], row["Marks"], computed, official))

    print(f"{matched}/{total} records match the official grade ({matched/total:.1%})")
    if mismatches:
        print(f"\n{len(mismatches)} mismatches (StudentID, Subject, Marks, ComputedGrade, OfficialGrade):")
        for m in mismatches:
            print(m)


if __name__ == "__main__":
    main()
