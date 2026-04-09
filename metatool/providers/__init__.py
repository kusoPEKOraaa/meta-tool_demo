from .base import ReviewProvider
from .compatible import CompatibleReviewProvider
from .demo import DemoReviewProvider


def build_provider(name: str) -> ReviewProvider:
    normalized = name.strip().lower()
    if normalized in {"demo", "offline"}:
        return DemoReviewProvider()
    if normalized in {"compatible", "api"}:
        return CompatibleReviewProvider()
    raise ValueError(f"Unsupported provider: {name}")
