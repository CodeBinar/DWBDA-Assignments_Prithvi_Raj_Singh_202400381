"""
Generates a realistic sample grocery-store transaction dataset.
This is used as a fallback dataset for the Market Basket Analysis assignment
in case the real UCI "Online Retail" dataset cannot be downloaded (no internet
access, blocked institute network, etc.). The item co-occurrence patterns
below (bread-butter-jam, diapers-beer, pasta-sauce-cheese, etc.) mirror the
well-known patterns found in real retail basket data.

Run once:
    python generate_grocery_data.py
Produces:
    grocery_transactions.csv
"""

import random
import csv

random.seed(42)

# Each "theme" is a realistic shopping trip pattern. Core items almost always
# appear together; extra items are added at random to make baskets realistic.
THEMES = [
    {"core": ["bread", "butter", "jam"], "extra": ["milk", "eggs", "coffee"]},
    {"core": ["milk", "bread", "eggs"], "extra": ["butter", "cereal", "juice"]},
    {"core": ["diapers", "beer"], "extra": ["chips", "soda", "bread"]},
    {"core": ["pasta", "tomato sauce", "cheese"], "extra": ["garlic", "olive oil"]},
    {"core": ["chips", "soda", "beer"], "extra": ["chocolate", "biscuits"]},
    {"core": ["tea", "sugar", "biscuits"], "extra": ["milk", "bread"]},
    {"core": ["coffee", "sugar", "milk"], "extra": ["biscuits", "bread"]},
    {"core": ["rice", "chicken", "vegetables"], "extra": ["yogurt", "spices"]},
    {"core": ["cereal", "milk", "juice"], "extra": ["fruit", "bread"]},
    {"core": ["chocolate", "biscuits"], "extra": ["tea", "coffee", "soda"]},
]

ALL_ITEMS = sorted({item for t in THEMES for item in (t["core"] + t["extra"])})

N_TRANSACTIONS = 400


def make_transaction():
    theme = random.choice(THEMES)
    items = set(theme["core"])
    for item in theme["extra"]:
        if random.random() < 0.5:
            items.add(item)
    # occasionally throw in a completely random item
    if random.random() < 0.15:
        items.add(random.choice(ALL_ITEMS))
    return sorted(items)


def main():
    with open("grocery_transactions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["TransactionID", "Items"])
        for i in range(1, N_TRANSACTIONS + 1):
            items = make_transaction()
            writer.writerow([i, ", ".join(items)])
    print(f"Wrote {N_TRANSACTIONS} transactions to grocery_transactions.csv")


if __name__ == "__main__":
    main()
