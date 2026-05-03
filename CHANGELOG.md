# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-05-03

### Added

- `currency-converter` CLI: converts an amount between USD, EUR, and GBP using static exchange rates (USD→EUR 0.92, EUR→GBP 0.86, USD→GBP 0.79)
- Decimal-precision arithmetic (no float math)
- Clear error messages for unknown currency codes and non-numeric amounts
- 82 tests across unit, integration, and e2e layers — all written before the production code they cover (TDD-strict)
- Commits: `395be23` `749e739` `16de6cf` `13614d4` `31ae7ba` `dc94001` `962f594` `74cdc67` `c74eb22` `d20cdca` `c1e6496`
