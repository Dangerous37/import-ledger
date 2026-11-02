import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

from domain import reconcile


def read_table(path, key):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        columns = next(reader, [])
        if not all(columns) or key not in columns or len(set(columns)) != len(columns):
            raise ValueError(f"{path.name}: invalid header or missing key column")
        rows = []
        for number, values in enumerate(reader, start=1):
            if len(values) != len(columns):
                raise ValueError(f"{path.name}: wrong width at record {number}")
            row = dict(zip(columns, values))
            if not row[key]:
                raise ValueError(f"{path.name}: empty key at record {number}")
            rows.append(row)
        return set(columns), rows


def main():
    parser = argparse.ArgumentParser(description="Compare two CSV imports by a stable key")
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--key", required=True)
    args = parser.parse_args()
    try:
        cols, left = read_table(args.left, args.key)
        other, right = read_table(args.right, args.key)
        if cols != other:
            raise ValueError("column sets differ")
        findings = reconcile(left, right, args.key)
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    print(json.dumps({"sources": [args.left.name, args.right.name],
                      "summary": dict(Counter(item["kind"] for item in findings)),
                      "findings": findings}, indent=2))
    return int(any(item["kind"] != "match" for item in findings))


if __name__ == "__main__":
    sys.exit(main())
