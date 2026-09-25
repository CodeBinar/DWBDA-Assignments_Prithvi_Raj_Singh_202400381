# 👤 Student Information

| Field | Details |
|---|---|
| **Name** | Prithvi |
| **USN / Roll No** | _fill in_ |
| **Class / Section** | _fill in_ |
| **Subject** | _fill in_ |
| **Semester** | 5th Semester, B.Tech CSE |
| **Submission Date** | _fill in_ |

---

# Assignments — MBA, MapReduce & PySpark

## Contents
- `Assignment_1_MBA/` — Market Basket Analysis on real-world retail data (Apriori, association rules) — Python
- `Assignment_2_MapReduce/` — MapReduce framework to compute grade distribution (S–F) per subject — Python (Hadoop Streaming style)
- `Assignment_3_Spark/` — PySpark program to count products sold per category on Kaggle sales data — Python, run in Google Colab

Each folder has its own `README.md` with dataset details, method, and exact
run instructions.

## Quick start (Windows) — Assignments 1 & 2
```powershell
pip install pandas mlxtend openpyxl

cd Assignment_1_MBA
python mba_analysis.py

cd ..\Assignment_2_MapReduce
python generate_student_data.py
python run_local.py
python summarize.py
```

## Assignment 3 (Google Colab)
1. Upload `Assignment_3_Spark/sales_category_pyspark.ipynb` to
   [Google Colab](https://colab.research.google.com).
2. Run all cells top to bottom (see `Assignment_3_Spark/README.md` for
   details — it downloads a real Kaggle dataset if you provide a
   `kaggle.json` API key, or falls back to a bundled sample automatically).
3. Download the finished `.ipynb`, the results CSV, and the chart PNG back
   into the `Assignment_3_Spark/` folder before pushing to GitHub.

## Uploading to GitHub
From this folder (after downloading/extracting it), in PowerShell or
Command Prompt:
```powershell
git init
git add .
git commit -m "Assignment 1: MBA, Assignment 2: MapReduce, Assignment 3: PySpark category sales"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```
(Create an empty repo on github.com first, then copy its URL into the
`git remote add origin ...` line above.)

Due date: submit the GitHub repo link by next Friday.
