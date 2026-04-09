from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from .analyzers import analyze_source
from .models import Finding
from .providers import build_provider
from .refactor import refactor_source
from .reporting import render_markdown_report


def review_source_text(
    *,
    source: str,
    source_name: str,
    provider_name: str = "demo",
    output_dir: Path | None = None,
) -> dict[str, object]:
    source_path = Path(source_name)
    findings = analyze_source(source)
    summary = build_provider(provider_name).summarize(source=source, findings=findings)
    refactored_source, refactor_notes = refactor_source(source)
    severity_counts = Counter(item.severity for item in findings)
    category_counts = Counter(item.category for item in findings)
    report_path = Path("preview") / f"{source_path.stem}_review.md"
    refactored_path = Path("preview") / f"{source_path.stem}_refactored.py"

    markdown_report = render_markdown_report(
        source_path=source_path,
        provider_name=provider_name,
        summary=summary,
        findings=findings,
        refactor_notes=refactor_notes,
        refactored_path=refactored_path,
    )

    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        report_path = output_dir / f"{source_path.stem}_review.md"
        refactored_path = output_dir / f"{source_path.stem}_refactored.py"
        report_path.write_text(markdown_report, encoding="utf-8")
        refactored_path.write_text(refactored_source, encoding="utf-8")

    return {
        "source_name": source_name,
        "provider_name": provider_name,
        "summary": summary,
        "finding_objects": findings,
        "findings": [serialize_finding(item) for item in findings],
        "finding_count": len(findings),
        "severity_counts": {
            "high": severity_counts.get("high", 0),
            "medium": severity_counts.get("medium", 0),
            "low": severity_counts.get("low", 0),
        },
        "category_counts": dict(category_counts),
        "grouped_findings": group_findings(findings),
        "refactor_notes": refactor_notes,
        "refactored_source": refactored_source,
        "markdown_report": markdown_report,
        "report_path": str(report_path),
        "refactored_path": str(refactored_path),
    }


def serialize_finding(finding: Finding) -> dict[str, object]:
    return {
        "title": finding.title,
        "detail": finding.detail,
        "severity": finding.severity,
        "line": finding.line,
        "category": finding.category,
        "recommendation": finding.recommendation,
    }


def group_findings(findings: list[Finding]) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for finding in findings:
        grouped[finding.category].append(serialize_finding(finding))
    return dict(grouped)
