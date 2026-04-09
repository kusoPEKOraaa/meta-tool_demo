from __future__ import annotations

from abc import ABC, abstractmethod

from metatool.models import Finding


class ReviewProvider(ABC):
    @abstractmethod
    def summarize(self, source: str, findings: list[Finding]) -> str:
        """Return a concise review summary."""
