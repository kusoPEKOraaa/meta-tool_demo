from __future__ import annotations

from .analyzers import analyze_source
from .models import ReviewArtifacts, ReviewRequest
from .providers import build_provider
from .refactor import refactor_source
from .reporting import render_markdown_report


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

        findings = analyze_source(source)
        summary = self.provider.summarize(source=source, findings=findings)
        refactored_source, refactor_notes = refactor_source(source)

        report_path.write_text(
            render_markdown_report(
                source_path=self.request.source_path,
                provider_name=self.request.provider_name,
                summary=summary,
                findings=findings,
                refactor_notes=refactor_notes,
                refactored_path=refactored_path,
            ),
            encoding="utf-8",
        )
        refactored_path.write_text(refactored_source, encoding="utf-8")

        return ReviewArtifacts(
            report_path=report_path,
            refactored_path=refactored_path,
            findings=findings,
            summary=summary,
            refactor_notes=refactor_notes,
        )
