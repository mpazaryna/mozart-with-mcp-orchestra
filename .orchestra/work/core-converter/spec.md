---
ticket: core-converter
status: approved
created_on: 2026-05-03
---

# Core Converter

> PRD: .orchestra/work/core-converter/prd.md

## Objective
Deliver a Python CLI that converts a numeric amount from one currency to another
using static exchange rates, with clear errors for invalid input. Every production
file is preceded by a committed test file that fails before the implementation exists.

## Approach

### Step 1: Project scaffold
Create pyproject.toml with entry point, pytest config, and package skeleton.
No production logic yet — just the installable structure.
Commit: pyproject.toml, src/currency_converter/__init__.py, tests/__init__.py

### Step 2: Domain model (test-first)
Commit tests/unit/test_models.py (red), then src/currency_converter/models.py (green).
Defines: Currency (validated code), Money (amount + currency), ConversionResult.
Decimal used for all amounts to avoid float precision drift.

### Step 3: Exchange rate registry (test-first)
Commit tests/unit/test_rates.py (red), then src/currency_converter/rates.py (green).
ExchangeRateRegistry holds a static dict of rates keyed by (from, to) currency pair.
Raises UnknownCurrencyPairError for any unregistered pair.

### Step 4: Converter engine (test-first)
Commit tests/unit/test_converter.py (red), then src/currency_converter/converter.py (green).
Converter.convert(amount, from_currency, to_currency) → ConversionResult.
Propagates UnknownCurrencyPairError and InvalidAmountError from parsing.

### Step 5: Integration test (test-first)
Commit tests/integration/test_converter_with_rates.py (red), then wire Converter
to ExchangeRateRegistry without mocking. Proves the two components work together.

### Step 6: CLI interface (test-first)
Commit tests/e2e/test_cli.py (red), then src/currency_converter/cli.py (green).
argparse entry point: `currency-converter <amount> <from> <to>`.
Prints result to stdout. Prints error to stderr and exits non-zero on bad input.

## Testing Strategy

### Unit Tests
- Files: tests/unit/test_models.py, tests/unit/test_rates.py, tests/unit/test_converter.py
- Covers: Currency validation, Money construction, rate lookup, conversion math,
  error types for unknown currency and non-numeric amount
- Mocking: none — pure domain logic
- Run: `pytest tests/unit`
- Commit: test file before its corresponding implementation file

### Integration Tests
- Files: tests/integration/test_converter_with_rates.py
- Covers: Converter + ExchangeRateRegistry end-to-end with real static rate data,
  no mocking of either component
- Mocking: nothing
- Run: `pytest -m integration`
- Commit: test file before the wiring step

### E2E Tests
- Files: tests/e2e/test_cli.py
- Covers: subprocess invocation of the installed CLI — happy path conversion,
  unknown currency error, non-numeric amount error, exit codes
- Mocking: nothing
- Run: `pytest -m e2e`
- Commit: test file before cli.py

## Deliverables

| File | Purpose | Status |
|------|---------|--------|
| pyproject.toml | Project config, deps, pytest config, entry point | Not Started |
| src/currency_converter/__init__.py | Package init | Not Started |
| src/currency_converter/models.py | Currency, Money, ConversionResult | Not Started |
| src/currency_converter/rates.py | ExchangeRateRegistry, UnknownCurrencyPairError | Not Started |
| src/currency_converter/converter.py | Converter, InvalidAmountError | Not Started |
| src/currency_converter/cli.py | argparse CLI entry point | Not Started |
| tests/unit/test_models.py | Unit tests — domain model | Not Started |
| tests/unit/test_rates.py | Unit tests — rate registry | Not Started |
| tests/unit/test_converter.py | Unit tests — converter | Not Started |
| tests/integration/test_converter_with_rates.py | Integration tests | Not Started |
| tests/e2e/test_cli.py | E2E CLI subprocess tests | Not Started |

## Acceptance Criteria

### Functional
- [ ] `currency-converter 100 USD EUR` prints the converted amount to stdout
- [ ] An unknown currency code prints a human-readable error to stderr, exits non-zero
- [ ] A non-numeric amount prints a human-readable error to stderr, exits non-zero

### Unit
- [ ] test_models.py passes: Currency rejects invalid codes, Money stores amount + currency correctly
- [ ] test_rates.py passes: registry returns correct rate, raises UnknownCurrencyPairError on unknown pair
- [ ] test_converter.py passes: correct conversion math, error propagation

### Integration
- [ ] test_converter_with_rates.py passes: Converter + ExchangeRateRegistry work together without mocking

### E2E
- [ ] test_cli.py passes: subprocess invocation returns correct output, correct exit codes for all cases

## Dependencies
- Python 3.12+
- pytest (dev dependency)
- No external runtime dependencies — static rates, stdlib only

## Risks

| Risk | Mitigation |
|------|-----------|
| Float precision drift in conversion math | Use decimal.Decimal for all amounts throughout |
| TDD discipline breaks in implementation | Each step: test commit first, implementation commit second — enforced by commit order |
