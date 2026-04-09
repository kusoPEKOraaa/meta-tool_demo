from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from metatool.service import review_source_text


class ServiceTests(unittest.TestCase):
    def test_review_source_text_returns_dashboard_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = review_source_text(
                source="def sample(items=[]):\n\tif items == None:\n\t\treturn []\n",
                source_name="sample.py",
                output_dir=Path(tmpdir),
            )

        self.assertGreater(result["finding_count"], 0)
        self.assertIn("summary", result)
        self.assertIn("markdown_report", result)
        self.assertIn("refactored_source", result)
        self.assertEqual(result["severity_counts"]["medium"], 3)


if __name__ == "__main__":
    unittest.main()
