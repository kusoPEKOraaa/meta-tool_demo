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
python3 -m metatool.cli examples/bad_main.py
```

Outputs are written to the `output/` directory by default.
