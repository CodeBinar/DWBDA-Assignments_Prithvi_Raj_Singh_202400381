"""
Builds sales_category_pyspark.ipynb — a Google Colab-ready notebook.
Run once: python build_notebook.py
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# --- Title / student info ---
cells.append(nbf.v4.new_markdown_cell(
"""# Assignment 3 — Sales Category Analysis using PySpark

**Name:** Prithvi
**USN / Roll No:** _fill in_
**Class / Section:** _fill in_
**Subject:** _fill in_
**Submission Date:** _fill in_

---

## Objective
Take a real-world sales dataset (from Kaggle) and write a **Spark program in
Python (PySpark)** to calculate the **number of products sold in each
category**.

**Dataset used:** [Sample Superstore Sales dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)
(Kaggle) — retail order-level data with a `Category` column (Furniture,
Office Supplies, Technology) and a `Quantity` column (units sold per order
line). If the Kaggle dataset can't be downloaded (e.g. no Kaggle API key set
up), this notebook automatically falls back to a bundled synthetic sales
dataset with the same structure, so it always runs end-to-end."""
))

# --- Install pyspark ---
cells.append(nbf.v4.new_markdown_cell("## Step 1 — Install PySpark (Colab)"))
cells.append(nbf.v4.new_code_cell(
"""!pip install pyspark -q"""
))

# --- Kaggle download instructions ---
cells.append(nbf.v4.new_markdown_cell(
"""## Step 2 — Get the dataset from Kaggle

**Option A — Download with the Kaggle API (recommended):**
1. Go to kaggle.com -> your profile -> **Account** -> **Create New API Token**.
   This downloads a `kaggle.json` file.
2. Run the cell below and upload `kaggle.json` when prompted.
3. The notebook will then download the real Superstore sales dataset.

**Option B — No Kaggle account:** just skip the upload / let it fail — the
notebook automatically falls back to a synthetic sample dataset with the
same columns, generated in Step 3."""
))
cells.append(nbf.v4.new_code_cell(
"""import os

USE_KAGGLE = True  # set to False to always use the bundled fallback dataset

if USE_KAGGLE:
    try:
        from google.colab import files
        print("Upload your kaggle.json (Kaggle -> Account -> Create New API Token):")
        uploaded = files.upload()
        os.makedirs("/root/.kaggle", exist_ok=True)
        for fname in uploaded:
            os.rename(fname, "/root/.kaggle/kaggle.json")
        os.chmod("/root/.kaggle/kaggle.json", 0o600)

        !pip install kaggle -q
        !kaggle datasets download -d rohitsahoo/sales-forecasting -p /content --unzip
        print("Downloaded real Kaggle dataset.")
    except Exception as e:
        print(f"Kaggle download skipped/failed ({e}). Will use fallback sample data.")
"""
))

# --- Fallback data generator ---
cells.append(nbf.v4.new_markdown_cell(
"""## Step 3 — Load the data (real Kaggle CSV, or generate a fallback sample)

The Superstore CSV has (among others) these columns: `Order ID`, `Category`,
`Sub-Category`, `Product Name`, `Quantity`, `Sales`.

If the real file isn't found (Kaggle step skipped), a synthetic dataset with
the same structure is generated instead, so every later cell still works
unchanged."""
))
cells.append(nbf.v4.new_code_cell(
"""import glob
import random
import pandas as pd

candidates = glob.glob("/content/*.csv") + glob.glob("/content/**/*.csv", recursive=True)
candidates = [c for c in candidates if "sample_sales_data" not in c]

csv_path = None
for c in candidates:
    try:
        cols = pd.read_csv(c, nrows=1).columns
        if "Category" in cols and "Quantity" in cols:
            csv_path = c
            break
    except Exception:
        continue

if csv_path:
    print(f"Using real Kaggle dataset: {csv_path}")
else:
    print("Real dataset not found — generating a synthetic fallback sample instead.")
    random.seed(42)
    categories = {
        "Furniture": ["Chair", "Desk", "Bookcase", "Table"],
        "Office Supplies": ["Binder", "Paper", "Stapler", "Pens"],
        "Technology": ["Laptop", "Monitor", "Printer", "Phone"],
        "Electronics": ["Headphones", "Speaker", "Charger", "Cable"],
        "Clothing": ["T-Shirt", "Jacket", "Shoes", "Cap"],
    }
    rows = []
    for order_id in range(1, 1501):
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        quantity = random.randint(1, 10)
        sales = round(quantity * random.uniform(10, 200), 2)
        rows.append([f"ORD-{order_id:05d}", category, product, quantity, sales])

    df_fallback = pd.DataFrame(rows, columns=["Order ID", "Category", "Product Name", "Quantity", "Sales"])
    csv_path = "/content/sample_sales_data.csv"
    df_fallback.to_csv(csv_path, index=False)
    print(f"Wrote fallback dataset to {csv_path} ({len(df_fallback)} rows)")
"""
))

# --- Spark session ---
cells.append(nbf.v4.new_markdown_cell("## Step 4 — Start a Spark session and load the data"))
cells.append(nbf.v4.new_code_cell(
"""from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, countDistinct

spark = SparkSession.builder.appName("SalesCategoryAnalysis").getOrCreate()

sales_df = spark.read.csv(csv_path, header=True, inferSchema=True)
sales_df = sales_df.withColumn("Quantity", col("Quantity").cast("int"))

print(f"Loaded {sales_df.count()} rows")
sales_df.select("Category", "Quantity").show(5)
"""
))

# --- DataFrame API approach ---
cells.append(nbf.v4.new_markdown_cell(
"""## Step 5 — Products sold per category (Spark DataFrame API)

Sums the `Quantity` column, grouped by `Category`, to get the total number
of product units sold in each category."""
))
cells.append(nbf.v4.new_code_cell(
"""category_totals_df = (
    sales_df.groupBy("Category")
    .agg(
        spark_sum("Quantity").alias("TotalUnitsSold"),
        countDistinct("Product Name").alias("DistinctProducts"),
    )
    .orderBy(col("TotalUnitsSold").desc())
)

category_totals_df.show(truncate=False)
"""
))

# --- RDD map-reduce approach ---
cells.append(nbf.v4.new_markdown_cell(
"""## Step 6 — Same result using Spark's RDD map/reduce API

This shows the underlying map-reduce style computation (similar in spirit to
Assignment 2's Hadoop MapReduce), expressed with Spark RDD transformations:
`map` -> `reduceByKey`."""
))
cells.append(nbf.v4.new_code_cell(
"""rdd = sales_df.select("Category", "Quantity").rdd

category_totals_rdd = (
    rdd.map(lambda row: (row["Category"], row["Quantity"] or 0))
    .reduceByKey(lambda a, b: a + b)
    .sortBy(lambda kv: -kv[1])
)

for category, total_qty in category_totals_rdd.collect():
    print(f"{category}: {total_qty} units sold")
"""
))

# --- Visualization ---
cells.append(nbf.v4.new_markdown_cell("## Step 7 — Visualize the results"))
cells.append(nbf.v4.new_code_cell(
"""import matplotlib.pyplot as plt

pdf = category_totals_df.toPandas()

plt.figure(figsize=(8, 5))
plt.bar(pdf["Category"], pdf["TotalUnitsSold"], color="steelblue")
plt.xlabel("Category")
plt.ylabel("Total Units Sold")
plt.title("Number of Products Sold per Category")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("category_sales_chart.png")
plt.show()
"""
))

# --- Save results ---
cells.append(nbf.v4.new_markdown_cell(
"""## Step 8 — Save results (for the GitHub submission)"""
))
cells.append(nbf.v4.new_code_cell(
"""pdf.to_csv("category_sales_summary.csv", index=False)
print("Saved category_sales_summary.csv and category_sales_chart.png")

# In Colab: download these to your computer before pushing to GitHub
try:
    from google.colab import files
    files.download("category_sales_summary.csv")
    files.download("category_sales_chart.png")
except Exception:
    pass
"""
))

cells.append(nbf.v4.new_markdown_cell(
"""## Notes for GitHub submission
1. In Colab: **File -> Download -> Download .ipynb** (or **File -> Save a
   copy in GitHub** to push directly).
2. Add this notebook, `category_sales_summary.csv`, and
   `category_sales_chart.png` to your `Assignment_3_Spark/` folder in the
   repo alongside this project's other assignments.
3. See the top-level `README.md` for the `git push` steps."""
))

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3"},
    "colab": {"provenance": []},
}

with open("sales_category_pyspark.ipynb", "w") as f:
    nbf.write(nb, f)

print("Notebook written: sales_category_pyspark.ipynb")
