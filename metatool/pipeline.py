from __future__ import annotations

from .models import ReviewArtifacts, ReviewRequest
from .service import review_source_text


class ReviewPipeline:
    """Coordinates the review workflow for the CLI."""

    def __init__(self, request: ReviewRequest) -> None:
        self.request = request

    def run(self) -> ReviewArtifacts:
        source = self.request.source_path.read_text(encoding="utf-8")
        result = review_source_text(
            source=source,
            source_name=str(self.request.source_path),
            provider_name=self.request.provider_name,
            output_dir=self.request.output_dir,
        )

        return ReviewArtifacts(
            report_path=self.request.output_dir
            / f"{self.request.source_path.stem}_review.md",
            refactored_path=self.request.output_dir
            / f"{self.request.source_path.stem}_refactored.py",
            findings=list(result["finding_objects"]),
            summary=str(result["summary"]),
            refactor_notes=list(result["refactor_notes"]),
        )
