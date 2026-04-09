from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .models import Finding


def render_markdown_report(
    *,
    source_path: Path,
    provider_name: str,
    summary: str,
    findings: list[Finding],
    refactor_notes: list[str],
    refactored_path: Path,
) -> str:
    grouped = defaultdict(list)
    for finding in findings:
        grouped[finding.category].append(finding)

    lines = [
        "# Meta-Tool Review Report",
        "",
        "## Review Metadata",
        "",
        f"- Source file: `{source_path}`",
        f"- Provider: `{provider_name}`",
        f"- Total findings: `{len(findings)}`",
        f"- Refactored output: `{refactored_path}`",
        "",
        "## AI Review Summary",
        "",
        summary,
        "",
        "## Findings by Severity",
        "",
    ]

    if findings:
        for finding in findings:
            location = f"line {finding.line}" if finding.line else "line unknown"
            lines.append(
                f"- [{finding.severity.upper()}] {finding.title} ({finding.category}, {location})"
            )
            lines.append(f"  - Detail: {finding.detail}")
            if finding.recommendation:
                lines.append(f"  - Recommendation: {finding.recommendation}")
    else:
        lines.append("- No issues were detected by the current demo rules.")

    lines.extend(["", "## Category Breakdown", ""])
    for category in ("syntax", "pep8", "bug-risk", "general"):
        category_findings = grouped.get(category, [])
        if not category_findings:
            continue
        lines.append(f"### {category}")
        lines.append("")
        for finding in category_findings:
            location = f"line {finding.line}" if finding.line else "line unknown"
            lines.append(f"- {finding.title} ({location})")
        lines.append("")

    lines.extend(["## Automatic Refactor Actions", ""])
    for note in refactor_notes:
        lines.append(f"- {note}")

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "This report combines deterministic static checks with an AI-provider summary layer.",
            "The current demo focuses on Python source files and safe, mechanical refactor actions.",
        ]
    )
    return "\n".join(lines) + "\n"
