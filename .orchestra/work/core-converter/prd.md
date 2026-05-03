---
ticket: core-converter
status: approved
created_on: 2026-05-03
---

# Core Converter

## Problem
Developers working at the terminal have no lightweight way to convert a currency
amount without leaving the shell. Looking up a conversion requires opening a browser,
navigating to a tool, and reading a result — context-switching that interrupts flow.
Without a CLI tool, every conversion is a manual lookup.

## Objective
Give a developer a single command that converts an amount from one currency to
another and prints the result, without leaving the terminal.

## Success Criteria
- [ ] A developer can convert an amount between any two supported currencies
      using a single terminal command
- [ ] The result is numerically correct according to the configured exchange rates
- [ ] An unknown currency code produces a clear, human-readable error message
- [ ] A non-numeric amount produces a clear, human-readable error message
- [ ] Every behavior listed above is covered by a test that existed before
      the production code that satisfies it

## Context
This is the single milestone of the dogfood proof-of-concept for the
mcp-orchestra + Mozart pipeline. The currency converter is the vehicle; proving
that the pipeline runs cleanly from PRD through Gherkin to implementation is
the goal. Static exchange rates are sufficient — no live API dependency is needed
to validate the workflow.

## Materials

| Deliverable | Location | Status |
|-------------|----------|--------|
| CLI tool | src/ | Complete |
| Test suite | tests/ | Complete |
| Gherkin scenarios | .orchestra/work/core-converter/gherkin-spec.md | Complete |

## References
- Roadmap: .orchestra/roadmap.md
- ADR-000: .orchestra/adr/ADR-000-the-score.md
