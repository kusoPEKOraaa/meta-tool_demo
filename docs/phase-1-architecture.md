# Phase 1: Abstract Framework and Module Design

## Phase goal

Build a minimal but extensible command line architecture for an AI-assisted code review tool. This phase focuses on the process skeleton instead of fully detailed review logic.

## Why this phase exists

The course topic is software process and quality, so the demo should not start from ad hoc scripting. It should first define:

1. clear responsibilities
2. stable interfaces
3. traceable iteration boundaries

This mirrors an engineering workflow where architecture is approved before feature density increases.

## Reference condensation

- `anc95/ChatGPT-CodeReview`: inspired the markdown-oriented review output
- `appleboy/CodeGPT`: inspired the terminal-first interaction model
- `qodo-ai/pr-agent`: inspired the staged pipeline design with separated responsibilities

The demo intentionally does not replicate all of their features. It extracts only the parts that support a course-friendly proof of concept.

## Proposed architecture

### CLI layer

Receives the file path and optional output directory from the user.

### Pipeline layer

Coordinates the full review flow:

1. read source
2. run analyzers
3. ask an AI provider for a structured review summary
4. render a markdown report
5. write the refactored code

### Analyzer layer

Will later contain deterministic checks for:

- PEP 8 style risks
- syntax errors
- potential bugs

### Provider layer

Abstracts the AI call so the demo can run in two modes:

- `demo` mode for offline classroom demonstration
- `compatible` mode for a real API endpoint

### Renderer layer

Turns the collected findings into stable markdown output for teaching and evaluation.

## Directory design

```text
metatool/
  cli.py
  models.py
  pipeline.py
  providers/
    __init__.py
    base.py
    demo.py
```

## Deliverables completed in this phase

- project packaging with `pyproject.toml`
- CLI command placeholder: `review_code`
- data structures for findings and artifacts
- provider abstraction
- pipeline skeleton

## Commit strategy

This phase ends with a dedicated commit so later functional additions can be traced against a stable architectural baseline.
