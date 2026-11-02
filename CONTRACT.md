# Reconciliation contract
Run python ledger.py LEFT RIGHT --key COLUMN. Inputs are UTF-8 comma-delimited CSV with distinct nonempty headers, an identical set of columns and a nonempty key per record. Header order is immaterial. All values compare as exact strings. Multiple rows with the same key on either side produce one ambiguous finding listing every source record.

Output is a JSON report sorted by key with match, changed, left_only, right_only and ambiguous groups. References identify side and logical data record (1-based, excluding header), including records spanning physical lines. Changed fields are named without printing their values. Keys are printed. Invalid inputs return 2 with no partial report. Differences return 1 and equality returns 0.
