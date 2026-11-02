import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent


def run(left, right):
    return subprocess.run([sys.executable, str(ROOT / "ledger.py"), str(left), str(right),
                           "--key", "id"], text=True, capture_output=True)


class LedgerTests(unittest.TestCase):
    def test_demo(self):
        result = run(ROOT / "before.csv", ROOT / "after.csv")
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["summary"], dict(match=1, changed=1, left_only=1,
                                                  ambiguous=1, right_only=1))
        self.assertEqual(report["findings"][1]["fields"], ["stage"])
        self.assertEqual(report["findings"][3]["left"], [4, 5])

    def test_bom_quotes_multiline_and_record_numbering(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "snapshot.csv"
            file.write_text('id,note\nA,"two,\nlines"\nB,"say ""hi"""\n', encoding="utf-8-sig")
            result = run(file, file)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["findings"][1]["left"], [2])

    def test_invalid_input_never_emits_partial_findings(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "invalid.csv"
            for contents in ["id,id\na,b", "id,stage\na", "id,stage\n,a",
                             'id,stage\na,"unfinished', "id,other\na,b"]:
                with self.subTest(contents=contents):
                    file.write_text(contents, encoding="utf-8")
                    result = run(file, ROOT / "after.csv")
                    self.assertEqual((result.returncode, result.stdout), (2, ""))
