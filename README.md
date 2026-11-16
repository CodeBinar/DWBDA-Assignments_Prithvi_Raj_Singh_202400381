# 👤 Student Information

| Field | Details |
|---|---|
| **Name** | Prithvi Raj Singh|
| **Subject** | Data warehousing and big data analytics |
| **Semester** | 5th Semester, B.Tech CSE in DATA SCIENCE |
| **Submission Date** | 25th Sep 2026|

---

 # Assignments — MBA, MapReduce, PySpark & Spark Streaming

## Contents
- `Assignment_1_MBA/` — Market Basket Analysis on real-world retail data (Apriori, association rules) — Python
- `Assignment_2_MapReduce/` — MapReduce framework to compute grade distribution (S–F) per subject — Python (Hadoop Streaming style)
- `Assignment_3_Spark/` — PySpark program to count products sold per category on Kaggle sales data — Python, run in Google Colab
- * `Assignment_4_Spark_Streaming/` — Spark Structured Streaming with checkpointing and fault tolerance, plus a duplicate file checker — Python, run locally on Windows

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
Quick start (Windows) — Assignment 4

Requires Java (8/11/17) and `pip install pyspark`. Use two Command Prompt windows.

```
cd Assignment_4_Spark_Streaming

:: Window 1 - data source
python data_generator.py

:: Window 2 - streaming job (stop with Ctrl+C and rerun to test checkpoint recovery)
python spark_streaming.py

:: Duplicate file checker (any folder)
python find_duplicates.py
```



