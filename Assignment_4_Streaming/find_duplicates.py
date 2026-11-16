"""
Duplicate file checker
-----------------------
Two files are duplicates if their CONTENT is identical (names don't matter).
We compute a SHA-256 hash of every file; files with the same hash are duplicates.

Usage:  python find_duplicates.py [folder]
        (default folder is the current directory)
"""
import hashlib
import os
import sys
from collections import defaultdict


def file_hash(path):
    """Return the SHA-256 hash of a file, reading it in small chunks."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()


def find_duplicates(folder):
    groups = defaultdict(list)          # hash -> list of file paths

    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            try:
                groups[file_hash(path)].append(path)
            except OSError as e:
                print("Skipped", path, "->", e)

    return {h: paths for h, paths in groups.items() if len(paths) > 1}


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    duplicates = find_duplicates(folder)

    if not duplicates:
        print("No duplicate files found.")
    else:
        for i, paths in enumerate(duplicates.values(), start=1):
            print(f"\nDuplicate group {i}:")
            for p in paths:
                print("  ", p)
