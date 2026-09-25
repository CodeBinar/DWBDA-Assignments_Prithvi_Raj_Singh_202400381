"""
Parses official Sikkim Manipal University grade-sheet .txt files (one file
per subject) into two clean CSVs:

    student_results.csv   -> StudentID,Subject,Marks,Status,OfficialGrade
    subject_cutoffs.csv   -> Subject,E,D,C,B,A,S

Each subject sheet prints its OWN relative-grading cutoffs (mean/SD based),
which differ from subject to subject -- e.g. DAA uses S>=85, while the OOP
Lab uses S>=88. So the cutoffs are extracted per file rather than assumed to
be fixed, and mapper.py looks them up per subject at grading time.

Status handles all three non-numeric UM markers used on these sheets:
    AB -> Absent
    DT -> Detained
    MP -> Malpractice

To add more subjects: drop more official grade-sheet .txt files (same
format) into raw_data/ and re-run this script -- every file becomes one
more subject automatically.

Run:
    python parse_grade_sheets.py
Produces:
    student_results.csv
    subject_cutoffs.csv
"""

import glob
import os
import re
import csv

RAW_DATA_DIR = "raw_data"
RESULTS_CSV = "student_results.csv"
CUTOFFS_CSV = "subject_cutoffs.csv"

CUTOFF_LINE_RE = re.compile(r"Lower cut off for\s+([A-Za-z])\s*=\s*([\d.]+)")


def extract_subject(lines):
    """Pull a clean subject name out of the 'Subject Title' header line."""
    for line in lines:
        if line.strip().lower().startswith("subject title"):
            value = line.split(":", 1)[1].strip()
            value = re.sub(r"\s*\([^)]*\)\s*$", "", value)  # drop trailing "(CODE)"
            return value.title()
    return "Unknown Subject"


def extract_cutoffs(lines):
    """Pull this subject's own S/A/B/C/D/E cutoffs from its stats block."""
    cutoffs = {}
    for line in lines:
        m = CUTOFF_LINE_RE.search(line)
        if m:
            grade, value = m.group(1).upper(), float(m.group(2))
            cutoffs[grade] = value
    return cutoffs


def status_for(um_token):
    token = um_token.upper()
    if token == "AB":
        return "Absent"
    if token == "DT":
        return "Detained"
    if token == "MP":
        return "Malpractice"
    return "Normal"


def parse_file(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    subject = extract_subject(lines)
    cutoffs = extract_cutoffs(lines)

    records = []
    for line in lines:
        tokens = line.split()
        # A valid data row is exactly: REGNO INT UM TOT GRADE
        if len(tokens) != 5 or not tokens[0].isdigit():
            continue
        regno, _int_marks, um, tot, official_grade_raw = tokens

        status = status_for(um)
        try:
            marks = float(tot)
        except ValueError:
            continue

        records.append((regno, subject, marks, status, official_grade_raw.upper()))

    return subject, cutoffs, records


def main():
    files = sorted(glob.glob(os.path.join(RAW_DATA_DIR, "*.txt")))
    if not files:
        print(f"No .txt grade sheets found in {RAW_DATA_DIR}/")
        return

    all_records = []
    all_cutoffs = {}

    for path in files:
        subject, cutoffs, records = parse_file(path)
        print(f"{os.path.basename(path)}: subject='{subject}', {len(records)} records, cutoffs={cutoffs}")
        all_records.extend(records)
        all_cutoffs[subject] = cutoffs

    with open(RESULTS_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["StudentID", "Subject", "Marks", "Status", "OfficialGrade"])
        writer.writerows(all_records)

    with open(CUTOFFS_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Subject", "E", "D", "C", "B", "A", "S"])
        for subject, c in all_cutoffs.items():
            writer.writerow([subject, c.get("E", ""), c.get("D", ""), c.get("C", ""),
                              c.get("B", ""), c.get("A", ""), c.get("S", "")])

    print(f"\nWrote {len(all_records)} total records across {len(all_cutoffs)} subjects to {RESULTS_CSV}")
    print(f"Wrote per-subject cutoffs to {CUTOFFS_CSV}")


if __name__ == "__main__":
    main()
