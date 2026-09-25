# Assignment 3 — Sales Category Analysis using PySpark (Google Colab)

## Objective
Take a real-world sales dataset (Kaggle) and write a **Spark program in
Python (PySpark)** to calculate the number of products sold in each
category.

## Dataset
- **Real data:** [Sample Superstore Sales dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)
  on Kaggle — retail order data with `Category` (Furniture, Office Supplies,
  Technology) and `Quantity` columns. Downloaded inside the notebook via the
  Kaggle API.
- **Fallback:** if no Kaggle API key is set up, the notebook auto-generates
  a synthetic sales dataset with the same structure (`Category`, `Product
  Name`, `Quantity`, `Sales`) so it still runs completely.

## How to run — Google Colab
1. Open [Google Colab](https://colab.research.google.com) -> **Upload
   notebook** -> select `sales_category_pyspark.ipynb`.
2. Run the cells top to bottom.
3. When prompted in Step 2, upload your `kaggle.json` API token (from Kaggle
   -> Account -> Create New API Token) to fetch the real dataset — or just
   let it skip/fail to use the bundled fallback data automatically.
4. The notebook computes the units sold per category two ways:
   - **DataFrame API:** `groupBy("Category").agg(sum("Quantity"))`
   - **RDD API:** classic Spark `map` -> `reduceByKey` (map-reduce style)
5. It saves `category_sales_summary.csv` and a bar chart
   `category_sales_chart.png`, and offers to download them.

## Files
| File | Purpose |
|---|---|
| `sales_category_pyspark.ipynb` | Main Colab notebook (upload & run this) |
| `build_notebook.py` | Script that generated the notebook (for reference/editing) |

## Sample output (fallback dataset, 1500 order lines, 5 categories)
| Category | Total Units Sold |
|---|---|
| Electronics | 1857 |
| Office Supplies | 1760 |
| Clothing | 1711 |
| Technology | 1618 |
| Furniture | 1590 |

(Exact numbers will differ with the real Kaggle dataset.)
