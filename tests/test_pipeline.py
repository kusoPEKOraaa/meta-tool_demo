from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from metatool.models import ReviewRequest
from metatool.pipeline import ReviewPipeline
from metatool.refactor import refactor_source


class PipelineTests(unittest.TestCase):
    def test_pipeline_writes_report_and_refactor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_path = Path(tmpdir) / "bad.py"
            output_dir = Path(tmpdir) / "output"
            source_path.write_text(
                "def demo(data=[]):\n\tvalue = open('x.txt')    \n\tif value == None:\n\t\treturn data\n",
                encoding="utf-8",
            )

            artifacts = ReviewPipeline(
                ReviewRequest(source_path=source_path, output_dir=output_dir)
            ).run()

            report = artifacts.report_path.read_text(encoding="utf-8")
            refactored = artifacts.refactored_path.read_text(encoding="utf-8")

            self.assertIn("Meta-Tool Review Report", report)
            self.assertIn("Mutable default argument", report)
            self.assertIn("Automatic Refactor Actions", report)
            self.assertIn("value is None", refactored)
            self.assertNotIn("\t", refactored)

    def test_refactor_source_applies_safe_changes(self) -> None:
        updated, notes = refactor_source("if value != None:\n\tprint('x')    ")
        self.assertIn("is not None", updated)
        self.assertNotIn("\t", updated)
        self.assertTrue(updated.endswith("\n"))
        self.assertGreaterEqual(len(notes), 1)


if __name__ == "__main__":
    unittest.main()
