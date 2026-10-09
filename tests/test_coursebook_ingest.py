import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from coursebook_ingest import build_output, extract_records


class CoursebookIngestTests(unittest.TestCase):
    def setUp(self):
        self.fixture = Path(__file__).parent / "fixtures" / "manual_results.html"

    def test_extracts_synthetic_table(self):
        records = extract_records(self.fixture.read_text(encoding="utf-8"))
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["course_prefix"], "CS")
        self.assertEqual(records[1]["section"], "002")

    def test_output_records_source_filename(self):
        result = build_output(self.fixture)
        self.assertEqual(result["source_file"], "manual_results.html")
        self.assertEqual(result["record_count"], 2)
        self.assertIn("Offline extraction", result["notice"])


if __name__ == "__main__":
    unittest.main()
