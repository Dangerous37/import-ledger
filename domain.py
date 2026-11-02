"""Exact-key reconciliation independent of CSV and filesystem access."""
from collections import defaultdict


def by_key(records, key):
    index = defaultdict(list)
    for number, row in enumerate(records, start=1):
        index[row[key]].append((number, row))
    return index


def reconcile(left, right, key):
    a, b = by_key(left, key), by_key(right, key)
    results = []
    for value in sorted(a.keys() | b.keys()):
        before, after = a[value], b[value]
        fields = []
        if len(before) > 1 or len(after) > 1:
            kind = "ambiguous"
        elif not after:
            kind = "left_only"
        elif not before:
            kind = "right_only"
        else:
            old, new = before[0][1], after[0][1]
            fields = sorted(col for col in old if old[col] != new[col])
            kind = "changed" if fields else "match"
        results.append(dict(key=value, kind=kind, fields=fields,
                            left=[i for i, _ in before], right=[i for i, _ in after]))
    return results
