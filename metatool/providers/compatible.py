from __future__ import annotations

import json
import os
from urllib import request

from metatool.models import Finding

from .base import ReviewProvider


class CompatibleReviewProvider(ReviewProvider):
    """Call a chat-completions compatible endpoint for the summary layer."""

    def __init__(self) -> None:
        self.api_key = os.getenv("METATOOL_API_KEY", "")
        self.api_url = os.getenv("METATOOL_API_URL", "").strip()
        self.model = os.getenv("METATOOL_MODEL", "").strip()
        if not self.api_key or not self.api_url or not self.model:
            raise ValueError(
                "Compatible provider requires METATOOL_API_KEY, METATOOL_API_URL, and METATOOL_MODEL."
            )

    def summarize(self, source: str, findings: list[Finding]) -> str:
        prompt = _build_prompt(source=source, findings=findings)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior Python code reviewer. Summarize quality risks briefly.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        req = request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        return (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "Compatible provider returned an empty summary.")
            .strip()
        )


def _build_prompt(source: str, findings: list[Finding]) -> str:
    rendered_findings = "\n".join(
        f"- [{item.severity}] {item.title}: {item.detail}" for item in findings
    )
    return (
        "Review the following Python file based on the detected findings.\n"
        "Summarize the main quality risks, the likely root causes, and the refactor priority.\n\n"
        f"Detected findings:\n{rendered_findings or '- none'}\n\n"
        "Source code:\n"
        "```python\n"
        f"{source}\n"
        "```"
    )
