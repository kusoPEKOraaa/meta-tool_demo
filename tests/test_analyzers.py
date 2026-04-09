from __future__ import annotations

import unittest

from metatool.analyzers import analyze_source


class AnalyzerTests(unittest.TestCase):
    def test_reports_syntax_error(self) -> None:
        findings = analyze_source("def broken(:\n    pass\n")
        self.assertEqual(findings[0].category, "syntax")
        self.assertEqual(findings[0].severity, "high")

    def test_reports_bug_risks(self) -> None:
        source = """
def sample(items=[]):
    handle = open("demo.txt")
    if handle == None:
        return []
    while True:
        print("x")
    try:
        return items
    except:
        return []
"""
        findings = analyze_source(source)
        titles = {item.title for item in findings}
        self.assertIn("Mutable default argument", titles)
        self.assertIn("Comparison to None uses == or !=", titles)
        self.assertIn("Potential infinite loop", titles)
        self.assertIn("Bare except", titles)
        self.assertIn("File opened outside context manager", titles)


if __name__ == "__main__":
    unittest.main()
