# Phase 4: Visual Frontend and Report Analysis Dashboard

## Phase goal

Add a lightweight frontend so the Meta-Tool demo can be operated visually in class instead of only through the terminal.

## Design choice

The frontend uses Python standard library HTTP serving instead of a third-party web framework. This keeps the project:

- easy to run
- easy to explain
- independent from extra backend dependencies

## Added capabilities

### 1. Web dashboard

The new `review_web` command starts a local dashboard for:

- pasting or editing Python code
- loading the built-in sample file
- choosing the review provider
- triggering the analysis pipeline

### 2. Visual report analysis

The dashboard presents:

- total issue count
- high, medium, and low severity cards
- category distribution bars
- AI summary text
- finding cards with recommendations
- automatic refactor notes
- markdown report preview
- refactored code preview

### 3. Shared service layer

To avoid duplicated logic, both CLI and frontend now depend on a common review service. This is also a software process improvement because one source of truth reduces divergence between interfaces.

## Presentation value

The frontend makes the project easier to demonstrate to teachers because it shows:

- visible interaction flow
- observable quality metrics
- clear before/after output
- a stronger product form than a pure terminal script
