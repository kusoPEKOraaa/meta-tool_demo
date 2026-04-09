# Meta-Tool Demo

Meta-Tool is a Python command line demo for automated code review and standards-oriented refactoring.

The project is intentionally small and staged for coursework about software process and quality:

- phase 1: define the architecture and CLI entry
- phase 2: implement review, report generation, and tests
- phase 3: polish the demo assets and delivery docs

Target command:

```bash
review_code examples/bad_main.py
```

The final demo will read Python code, analyze style and risk signals, generate a markdown review report, and write a refactored version of the file.

## Current demo scope

- Python CLI entry: `review_code`
- deterministic checks for syntax, PEP 8 risks, and common bug patterns
- markdown review report generation
- safe, mechanical refactor output
- optional compatible AI summary provider through environment variables

## Quick start

```bash
pip install -e .
python3 -m metatool.cli examples/bad_main.py
# or
review_code examples/bad_main.py
```

Outputs are written to the `output/` directory by default.

## Architecture snapshot

```text
CLI -> ReviewPipeline -> Analyzers -> AI Provider -> Report Renderer -> Refactor Writer
```

## Staged development process

- Phase 1: scaffold the architecture, package, and provider abstraction
- Phase 2: implement review rules, markdown reports, safe refactors, and tests
- Phase 3: polish the CLI experience, delivery documents, and demo narrative

## Course relevance

This topic maps directly to software process and quality:

- it reduces the manual cost of code review
- it makes quality checks repeatable
- it demonstrates incremental engineering with versioned milestones
- it provides a clean basis for unit testing and future QA automation research
