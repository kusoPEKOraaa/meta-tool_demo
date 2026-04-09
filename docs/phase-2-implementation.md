# Phase 2: Rule Engine, Report Generation, and Testing

## Phase goal

Turn the architecture scaffold into a working quality-assurance demo.

## Functional additions

### 1. Deterministic analyzers

The demo now scans Python files for a small but explainable set of issues:

- syntax errors
- trailing whitespace
- tab indentation
- lines longer than 79 characters
- `== None` or `!= None`
- mutable default arguments
- bare `except`
- `while True` without `break`
- `open()` outside a `with` block

This keeps the project easy to defend in class because every rule has a direct software quality rationale.

### 2. AI summary layer

The provider abstraction now supports:

- `demo`: offline summary mode for local presentation and testing
- `compatible`: a generic chat-completions compatible API mode

The demo does not depend on network access to show the full workflow.

### 3. Markdown report

The report now contains:

- review metadata
- AI summary
- findings ordered by severity
- category breakdown
- automatic refactor actions

### 4. Refactor output

The automatic refactor stage intentionally applies only safe, mechanical edits:

- strip trailing whitespace
- replace tabs with spaces
- rewrite `== None` to `is None`
- rewrite `!= None` to `is not None`
- ensure final newline

This design avoids pretending that the demo can safely auto-fix every semantic problem.

### 5. Unit tests

Tests cover:

- syntax error detection
- end-to-end report generation
- refactor behavior

## Process note

This phase is the key transition from abstract design to detailed implementation. It demonstrates incremental development instead of building the final tool in one uncontrolled step.
