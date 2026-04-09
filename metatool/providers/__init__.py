from .base import ReviewProvider
from .demo import DemoReviewProvider


def build_provider(name: str) -> ReviewProvider:
    normalized = name.strip().lower()
    if normalized in {"demo", "offline"}:
        return DemoReviewProvider()
    raise ValueError(f"Unsupported provider: {name}")
