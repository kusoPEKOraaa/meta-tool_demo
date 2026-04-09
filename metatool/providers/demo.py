from __future__ import annotations

from metatool.models import Finding

from .base import ReviewProvider


class DemoReviewProvider(ReviewProvider):
    def summarize(self, source: str, findings: list[Finding]) -> str:
        if not source.strip():
            return "The file is empty, so no review findings were produced."
        if not findings:
            return (
                "The offline demo provider completed the architecture-stage run. "
                "Detailed rule checks will be added in the next phase."
            )
        return f"The demo provider found {len(findings)} issue(s) for review."
