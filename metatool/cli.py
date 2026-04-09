from __future__ import annotations

import argparse
from pathlib import Path

from .models import ReviewRequest
from .pipeline import ReviewPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="review_code",
        description="Run Meta-Tool code review for a Python source file.",
    )
    parser.add_argument("source", type=Path, help="Python source file to review.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory for the markdown report and refactored code.",
    )
    parser.add_argument(
        "--provider",
        default="demo",
        help="AI provider name. Defaults to the offline demo provider.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.source.exists():
        parser.error(f"Source file not found: {args.source}")
    if args.source.suffix != ".py":
        parser.error("Meta-Tool demo currently supports only .py files.")

    request = ReviewRequest(
        source_path=args.source,
        output_dir=args.output_dir,
        provider_name=args.provider,
    )
    artifacts = ReviewPipeline(request).run()

    print(f"Review report written to: {artifacts.report_path}")
    print(f"Refactored code written to: {artifacts.refactored_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
