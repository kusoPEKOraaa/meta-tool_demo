from __future__ import annotations

from pathlib import Path

from .models import ReviewArtifacts, ReviewRequest
from .providers import build_provider


class ReviewPipeline:
    """Coordinates the review workflow for the CLI."""

    def __init__(self, request: ReviewRequest) -> None:
        self.request = request
        self.provider = build_provider(request.provider_name)

    def run(self) -> ReviewArtifacts:
        source = self.request.source_path.read_text(encoding="utf-8")
        self.request.output_dir.mkdir(parents=True, exist_ok=True)

        report_path = self.request.output_dir / f"{self.request.source_path.stem}_review.md"
        refactored_path = (
            self.request.output_dir / f"{self.request.source_path.stem}_refactored.py"
        )

        findings = []
        summary = self.provider.summarize(source=source, findings=findings)

        report_path.write_text(
            "\n".join(
                [
                    "# Meta-Tool Review Report",
                    "",
                    f"- Source: {self.request.source_path}",
                    f"- Provider: {self.request.provider_name}",
                    "",
                    "## Summary",
                    "",
                    summary,
                ]
            ),
            encoding="utf-8",
        )
        refactored_path.write_text(source, encoding="utf-8")

        return ReviewArtifacts(
            report_path=report_path,
            refactored_path=refactored_path,
            findings=findings,
            summary=summary,
        )
