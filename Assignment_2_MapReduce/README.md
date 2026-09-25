# Assignment 2 — MapReduce: Grade Distribution per Subject

## Objective
Use the **MapReduce framework** to count how many students fall into each
grade category (S, A, B, C, D, E, F) for **every subject**, using previous
semester's final exam results as sample data.

## Dataset — real data, all subjects
`raw_data/` contains the **actual official grade sheets** issued by Sikkim
Manipal University for the May/June 2026 examinations — 8 subjects, 1,167
student-subject records in total:

| File | Subject |
|---|---|
| `CD204A1_DAA.txt` | Design and Analysis of Algorithms |
| `CD203A4_OOP_Java_Lab.txt` | Object Oriented Programming Using Java Lab |
| `CD207A3_Programming_in_Java.txt` | Programming in Java (Elective II) |
| `CD205A1_DBMS.txt` | Database Management Systems |
| `CD204A4_DBMS_Lab.txt` | Database Management Systems Lab |
| `CD202A5_PBL_II.txt` | Project Based Learning II |
| `MA206B1_Probability_Statistics.txt` | Probability, Statistics and Stochastic Processes |
| `GN201B1_Universal_Human_Values.txt` | Universal Human Value II |

`parse_grade_sheets.py` reads **every** `.txt` grade sheet in `raw_data/`
and merges them into one clean `student_results.csv`
(`StudentID, Subject, Marks, Status, OfficialGrade`) — so it automatically
covers all subjects, and any more sheets dropped into that folder later.
It also extracts each subject's own grading cutoffs into
`subject_cutoffs.csv` (see "Bonus analysis" below).

## Grade categories
Each student already has an official grade on the sheet:
`S, A, B, C, D, E, F` from their marks, plus two special statuses recorded
as their own category:
- `I` — Absent for the exam
- `DT` — Detained (not permitted to sit the exam)
- `MP` — Caught in a malpractice case

## MapReduce design
- **Mapper** (`mapper.py`): reads each
  `StudentID,Subject,Marks,Status,OfficialGrade` record and emits
  `Subject,OfficialGrade <TAB> 1` — i.e. it counts the grade the university
  already assigned, per subject. (Uses Python's `csv` module rather than a
  naive `split(",")`, since one subject name — *"Probability, Statistics And
  Stochastic Processes"* — contains a comma itself.)
- **Shuffle & Sort**: all values for the same `(Subject, Grade)` key are
  grouped together (Hadoop does this automatically between map and reduce).
- **Reducer** (`reducer.py`): sums the `1`s for each key, producing
  `Subject,Grade <TAB> TotalCount`.

Written in standard **Hadoop Streaming** format (reads stdin, writes
stdout), so it runs either locally (simulated) or on a real Hadoop cluster
unchanged.

## Files
| File | Purpose |
|---|---|
| `raw_data/*.txt` | Real official grade sheets — one per subject (source data) |
| `parse_grade_sheets.py` | Parses all grade-sheet `.txt` files -> `student_results.csv` + `subject_cutoffs.csv` |
| `student_results.csv` | Clean merged data, all 8 subjects (1,167 rows) |
| `subject_cutoffs.csv` | Each subject's own S/A/B/C/D/E grading cutoffs |
| `mapper.py` | Map phase: emits `(Subject, OfficialGrade, 1)` |
| `reducer.py` | Reduce phase: sums counts per `(Subject, Grade)` |
| `run_local.py` | Simulates the full pipeline locally (sort included) |
| `summarize.py` | Turns raw output into a readable Subject x Grade table |
| `derive_grade_from_marks.py` | Bonus: reconstructs grades from raw marks (see below) |
| `grade_distribution_output.txt` | Raw MapReduce output |
| `grade_distribution_table.csv` | Final readable table |

## How to run (Windows)
```powershell
python parse_grade_sheets.py
python run_local.py
python summarize.py
```

This is equivalent to the classic Hadoop Streaming pipeline:
```
cat student_results.csv | mapper.py | sort | reducer.py
```

## How to run on an actual Hadoop cluster
The same `mapper.py` / `reducer.py` work unchanged:
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input student_results.csv \
  -output grade_output \
  -mapper mapper.py \
  -reducer reducer.py \
  -file mapper.py \
  -file reducer.py
```

## Result — students per grade, per subject

| Subject | S | A | B | C | D | E | F | I | DT | MP | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Database Management Systems | 3 | 10 | 17 | 8 | 10 | 5 | 0 | 3 | 3 | 0 | 59 |
| Database Management Systems Lab | 6 | 13 | 15 | 11 | 8 | 2 | 0 | 0 | 3 | 0 | 58 |
| Design and Analysis of Algorithms | 0 | 4 | 15 | 14 | 11 | 9 | 1 | 3 | 2 | 0 | 59 |
| Object Oriented Programming Using Java Lab | 4 | 13 | 10 | 13 | 13 | 1 | 0 | 0 | 3 | 1 | 58 |
| Probability, Statistics and Stochastic Processes | 20 | 39 | 44 | 44 | 62 | 46 | 84 | 17 | 9 | 2 | 367 |
| Programming in Java (Elective II) | 1 | 2 | 7 | 19 | 12 | 8 | 5 | 1 | 3 | 1 | 59 |
| Project Based Learning II | 0 | 3 | 10 | 19 | 19 | 1 | 0 | 6 | 0 | 0 | 58 |
| Universal Human Value II | 5 | 43 | 123 | 143 | 76 | 19 | 14 | 10 | 14 | 2 | 449 |
| **ALL SUBJECTS (combined)** | **39** | **127** | **241** | **271** | **211** | **91** | **104** | **40** | **37** | **6** | **1167** |

## Bonus analysis — deriving grades from raw marks
`derive_grade_from_marks.py` independently reconstructs each grade from raw
Marks, using each subject's own cutoffs (each subject has *different*
cutoffs — e.g. DAA uses S≥85 while the OOP Lab uses S≥88 — extracted per
file into `subject_cutoffs.csv`). It matches the official grade for
**1,145 / 1,167 records (98.1%)**.

The 22 mismatches are all cases the university graded `F` where the
cutoff-only formula gave a higher grade from the Total. The sheets note
"IF UM < 35% ... Grade is F" — but that 35% refers to 35% of the end-sem
component's *own* maximum (not printed on the sheet, and less than 100 for
some subjects), not 35% of the 100-mark Total. This is why the main pipeline
(`mapper.py`) counts the `OfficialGrade` the university already computed,
rather than re-deriving it from marks.
