from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Finding:
    title: str
    detail: str
    severity: str
    line: int | None = None
    category: str = "general"


@dataclass(slots=True)
class ReviewRequest:
    source_path: Path
    output_dir: Path
    provider_name: str = "demo"


@dataclass(slots=True)
class ReviewArtifacts:
    report_path: Path
    refactored_path: Path
    findings: list[Finding] = field(default_factory=list)
    summary: str = ""
