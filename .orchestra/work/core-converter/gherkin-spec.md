# Gherkin Scenarios: Core Converter

> Source: .orchestra/work/core-converter/spec.md
> Generated: 2026-05-03

```gherkin
Feature: Core Converter
  A developer converts currency amounts from the command line using static exchange rates

  Background:
    Given the rate registry contains "USD" to "EUR" at 0.92
    And the rate registry contains "EUR" to "GBP" at 0.86
    And the rate registry contains "USD" to "GBP" at 0.79

  Scenario: Converting an amount between two supported currencies
    When the developer runs `currency-converter 100 USD EUR`
    Then the output contains "92.00"
    And the exit code is 0

  Scenario: Conversion result is mathematically correct for fractional amounts
    When the developer runs `currency-converter 55 USD GBP`
    Then the output contains "43.45"
    And the exit code is 0

  Scenario: Converting zero amount produces zero
    When the developer runs `currency-converter 0 USD EUR`
    Then the output contains "0.00"
    And the exit code is 0

  Scenario: Unknown source currency produces a human-readable error
    When the developer runs `currency-converter 100 XYZ EUR`
    Then stderr contains "unknown currency"
    And the exit code is non-zero

  Scenario: Unknown target currency produces a human-readable error
    When the developer runs `currency-converter 100 USD XYZ`
    Then stderr contains "unknown currency"
    And the exit code is non-zero

  Scenario: Non-numeric amount produces a human-readable error
    When the developer runs `currency-converter abc USD EUR`
    Then stderr contains "invalid amount"
    And the exit code is non-zero
```
