"""
Assignment 1: Market Basket Analysis (MBA) on Real-World Data
================================================================

Primary dataset : UCI "Online Retail" dataset - real transaction-level
                   data from a UK-based online retailer (Dec 2010-2011),
                   ~540,000 rows. Downloaded automatically at runtime.
Fallback dataset : grocery_transactions.csv (bundled in this folder) -
                   used only if the download fails (e.g. no internet on
                   the machine running this script), so the assignment
                   still runs end-to-end and can be demoed offline.

Method: Apriori algorithm -> frequent itemsets -> association rules
        (support, confidence, lift), via the mlxtend library.

Install once:
    pip install pandas mlxtend openpyxl

Run:
    python mba_analysis.py
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

ONLINE_RETAIL_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
)


def load_online_retail():
    """Download and clean the real UCI Online Retail dataset."""
    df = pd.read_excel(ONLINE_RETAIL_URL)
    df.dropna(subset=["InvoiceNo", "Description", "CustomerID"], inplace=True)
    df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]  # drop cancelled orders
    df["Description"] = df["Description"].str.strip()

    transactions = (
        df.groupby("InvoiceNo")["Description"]
        .apply(lambda items: sorted(set(items)))
        .tolist()
    )
    return transactions


def load_fallback_sample(path="grocery_transactions.csv"):
    """Bundled sample transactions (see generate_grocery_data.py)."""
    df = pd.read_csv(path)
    transactions = df["Items"].apply(lambda s: [i.strip() for i in s.split(",")]).tolist()
    return transactions


def run_mba(transactions, min_support=0.05, min_confidence=0.3):
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    basket_df = pd.DataFrame(te_array, columns=te.columns_)

    frequent_itemsets = apriori(basket_df, min_support=min_support, use_colnames=True)
    frequent_itemsets = frequent_itemsets.sort_values("support", ascending=False).reset_index(drop=True)

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    rules = rules.sort_values(["confidence", "lift"], ascending=False).reset_index(drop=True)

    return frequent_itemsets, rules


def main():
    try:
        print("Attempting to download the real UCI Online Retail dataset...")
        transactions = load_online_retail()
        print(f"Loaded {len(transactions)} REAL transactions from UCI Online Retail.")
        min_support = 0.02  # real dataset has many more unique items -> lower threshold
    except Exception as e:
        print(f"Download failed ({e}).")
        print("Falling back to bundled sample dataset (grocery_transactions.csv)...")
        transactions = load_fallback_sample()
        print(f"Loaded {len(transactions)} sample transactions.")
        min_support = 0.05

    frequent_itemsets, rules = run_mba(transactions, min_support=min_support)

    print("\n=== Top 10 Frequent Itemsets ===")
    print(frequent_itemsets.head(10).to_string(index=False))

    print("\n=== Top 10 Association Rules (sorted by confidence, lift) ===")
    cols = ["antecedents", "consequents", "support", "confidence", "lift"]
    print(rules[cols].head(10).to_string(index=False))

    frequent_itemsets.to_csv("frequent_itemsets.csv", index=False)
    rules.to_csv("association_rules.csv", index=False)
    print("\nSaved: frequent_itemsets.csv, association_rules.csv")


if __name__ == "__main__":
    main()
