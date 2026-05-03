"""End-to-end tests for the currency-converter CLI entry point."""

import subprocess
import sys
from pathlib import Path

import pytest

# Resolve the CLI entry point from the same bin directory as the running Python,
# so this works in any virtual environment without hard-coding a path.
CLI = str(Path(sys.executable).parent / "currency-converter")


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [CLI, *args],
        capture_output=True,
        text=True,
    )


@pytest.mark.e2e
class TestCLIHappyPath:
    def test_100_usd_to_eur_output_contains_amount(self):
        result = _run("100", "USD", "EUR")
        assert "92.00" in result.stdout

    def test_100_usd_to_eur_exit_code_zero(self):
        result = _run("100", "USD", "EUR")
        assert result.returncode == 0

    def test_55_usd_to_gbp_output_contains_amount(self):
        result = _run("55", "USD", "GBP")
        assert "43.45" in result.stdout

    def test_55_usd_to_gbp_exit_code_zero(self):
        result = _run("55", "USD", "GBP")
        assert result.returncode == 0

    def test_zero_usd_to_eur_output_contains_amount(self):
        result = _run("0", "USD", "EUR")
        assert "0.00" in result.stdout

    def test_zero_usd_to_eur_exit_code_zero(self):
        result = _run("0", "USD", "EUR")
        assert result.returncode == 0


@pytest.mark.e2e
class TestCLIUnknownCurrency:
    def test_unknown_source_currency_stderr_contains_keyword(self):
        result = _run("100", "XYZ", "EUR")
        assert "unknown currency" in result.stderr.lower()

    def test_unknown_source_currency_exit_code_nonzero(self):
        result = _run("100", "XYZ", "EUR")
        assert result.returncode != 0

    def test_unknown_target_currency_stderr_contains_keyword(self):
        result = _run("100", "USD", "XYZ")
        assert "unknown currency" in result.stderr.lower()

    def test_unknown_target_currency_exit_code_nonzero(self):
        result = _run("100", "USD", "XYZ")
        assert result.returncode != 0


@pytest.mark.e2e
class TestCLIInvalidAmount:
    def test_non_numeric_amount_stderr_contains_keyword(self):
        result = _run("abc", "USD", "EUR")
        assert "invalid amount" in result.stderr.lower()

    def test_non_numeric_amount_exit_code_nonzero(self):
        result = _run("abc", "USD", "EUR")
        assert result.returncode != 0
