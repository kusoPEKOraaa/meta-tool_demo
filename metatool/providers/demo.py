from __future__ import annotations

from metatool.models import Finding

from .base import ReviewProvider


class DemoReviewProvider(ReviewProvider):
    def summarize(self, source: str, findings: list[Finding]) -> str:
        if not source.strip():
            return "The file is empty, so no review findings were produced."
        if not findings:
            return "The demo provider did not detect obvious quality issues in the current rule set."

        high_risk = sum(1 for item in findings if item.severity == "high")
        medium_risk = sum(1 for item in findings if item.severity == "medium")
        style_risk = sum(1 for item in findings if item.category == "pep8")
        return (
            f"The demo provider found {len(findings)} issue(s): "
            f"{high_risk} high-risk, {medium_risk} medium-risk, and {style_risk} style-related findings. "
            "Prioritize correctness issues first, then apply the safe automatic refactors."
        )
