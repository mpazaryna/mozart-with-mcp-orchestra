# Plan: core-converter

> Source: .orchestra/work/core-converter/spec.md (approved 2026-05-03)
> PRD: .orchestra/work/core-converter/prd.md

## Overview

Python CLI that converts a numeric amount from one currency to another using static
exchange rates. TDD-strict: every test file is committed before its implementation.

## Phases

- [x] **Phase 1**: Project scaffold — pyproject.toml, package skeleton, pytest config — committed `395be23`
- [x] **Phase 2**: Domain model (test-first) — test_models.py → models.py — committed `749e739`, `16de6cf`
- [x] **Phase 3**: Exchange rate registry (test-first) — test_rates.py → rates.py — committed `13614d4`, `31ae7ba`
- [x] **Phase 4**: Converter engine (test-first) — test_converter.py → converter.py — committed `dc94001`, `962f594`
- [x] **Phase 5**: Integration test (test-first) — test_converter_with_rates.py → wire Converter + Registry — committed `74cdc67`
- [x] **Phase 6**: CLI interface (test-first) — test_cli.py → cli.py — committed `c74eb22`, `d20cdca`

## Deliverables

| File | Purpose |
|------|---------|
| pyproject.toml | Project config, deps, pytest config, entry point |
| src/currency_converter/__init__.py | Package init |
| src/currency_converter/models.py | Currency, Money, ConversionResult |
| src/currency_converter/rates.py | ExchangeRateRegistry, UnknownCurrencyPairError |
| src/currency_converter/converter.py | Converter, InvalidAmountError |
| src/currency_converter/cli.py | argparse CLI entry point |
| tests/unit/test_models.py | Unit tests — domain model |
| tests/unit/test_rates.py | Unit tests — rate registry |
| tests/unit/test_converter.py | Unit tests — converter |
| tests/integration/test_converter_with_rates.py | Integration tests |
| tests/e2e/test_cli.py | E2E CLI subprocess tests |

## Acceptance Criteria (from spec)

- `currency-converter 100 USD EUR` prints the converted amount to stdout
- Unknown currency → human-readable error on stderr, exit non-zero
- Non-numeric amount → human-readable error on stderr, exit non-zero
- All Gherkin scenarios in `.orchestra/work/core-converter/gherkin-spec.md` pass

## Out of Scope

- Live exchange rate API (static rates only)
- Currency pairs beyond USD/EUR/GBP for the initial build
- Rate persistence or configuration files

## Notes

Entry point: `currency-converter` (installed via pyproject.toml `[project.scripts]`).
Decimal precision throughout — no float math.
