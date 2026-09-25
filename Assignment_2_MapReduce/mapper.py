#!/usr/bin/env python3
"""
Mapper (Hadoop Streaming compatible)
-------------------------------------
Input  (stdin) : lines of "StudentID,Subject,Marks,Status,OfficialGrade"
                 (produced by parse_grade_sheets.py from real university
                 grade sheets)
Output (stdout): "Subject,Grade<TAB>1"   for every record

This mapper counts each student's ALREADY-ASSIGNED official grade (the
`OfficialGrade` column) per subject -- exactly what the assignment asks for:
"using the previous semester final exam results, calculate the number of
students in each category (S,A,B,C,D,E,F)". The university's own grade
sheets already assign every student a grade (including the special
categories `I` = Absent, `DT` = Detained, `MP` = Malpractice), so the
map-reduce job's task is to tally them per subject.

(See derive_grade_from_marks.py for a from-scratch reconstruction of the
grading logic from raw marks + each subject's own cutoffs -- it matches the
official grade for ~98% of records; see its docstring for the small
discrepancy that was discovered and why.)
"""

import sys
import csv


def main():
    # NOTE: use csv.reader, not line.split(","): some subject names (e.g.
    # "Probability, Statistics And Stochastic Processes") contain a comma
    # themselves. The CSV writer correctly quotes those fields, but a naive
    # split(",") would still cut them into extra pieces and silently drop
    # every row for that subject.
    reader = csv.reader(sys.stdin)
    for parts in reader:
        if not parts or parts[0].lower() == "studentid":
            continue  # skip blank lines / header
        if len(parts) != 5:
            continue
        _student_id, subject, _marks, _status, official_grade = parts
        print(f"{subject},{official_grade}\t1")


if __name__ == "__main__":
    main()
