from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from metatool.cli import main


class CliTests(unittest.TestCase):
    def test_cli_prints_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            source_path = Path(tmpdir) / "demo.py"
            source_path.write_text(
                "def sample(data=[]):\n\tif data == None:\n\t\treturn []\n",
                encoding="utf-8",
            )
            stdout = io.StringIO()
            with patch(
                "sys.argv",
                ["review_code", str(source_path), "--output-dir", str(Path(tmpdir) / "out")],
            ):
                with redirect_stdout(stdout):
                    code = main()

        output = stdout.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("Detected findings:", output)
        self.assertIn("Severity breakdown:", output)


if __name__ == "__main__":
    unittest.main()
