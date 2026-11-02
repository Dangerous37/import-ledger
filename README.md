# Import Ledger

A nightly CRM import says it completed. Which records actually changed? Compare the source and destination CSV snapshots with one command and trace each result to the records that produced it.

## Run the synthetic audit

Python 3.12, standard library only. From the repository root:

```sh
python ledger.py before.csv after.csv --key id
python -m unittest -v
```

The demo intentionally exits **1**. A matches, B changed stage, C disappeared, E appeared, and D is ambiguous because the source contains two D records. The report identifies their logical record numbers (4 and 5). Exit 0 means exact agreement. Exit 2 means invalid input and no report. Redirect stdout to retain JSON for review.

## Design and limits

The CSV adapter validates the entire input before emitting results. The comparison indexes both snapshots by a shared key. Duplicate groups remain ambiguous even if some values coincide. Sorting keys and changed field names gives stable output across runs. Time is proportional to input size plus sorting; both inputs and the report must fit in memory. Use on trusted local exports. Reported keys and filenames may identify records. Reports omit non-key values. No fuzzy matching, type coercion or repair is performed. See [the input and output contract](CONTRACT.md) for details.

## Resumen en español

Compara dos exportaciones CSV mediante una clave estable y entrega un informe JSON trazable. Los duplicados quedan marcados como ambiguos para que el operador decida cómo resolverlos.
