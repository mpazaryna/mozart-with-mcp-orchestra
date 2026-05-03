"""Unit tests for the converter engine: Converter."""

import pytest
from decimal import Decimal

from currency_converter.converter import Converter
from currency_converter.models import ConversionResult, InvalidAmountError
from currency_converter.rates import ExchangeRateRegistry, UnknownCurrencyPairError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _converter() -> Converter:
    return Converter(ExchangeRateRegistry.default())


# ---------------------------------------------------------------------------
# Happy path — correct amounts
# ---------------------------------------------------------------------------


class TestConverterHappyPath:
    def test_100_usd_to_eur_converted_amount(self):
        result = _converter().convert("100", "USD", "EUR")
        assert result.converted.amount == Decimal("92.00")

    def test_100_usd_to_eur_converted_currency(self):
        result = _converter().convert("100", "USD", "EUR")
        assert result.converted.currency.code == "EUR"

    def test_100_usd_to_eur_original_amount(self):
        result = _converter().convert("100", "USD", "EUR")
        assert result.original.amount == Decimal("100")

    def test_100_usd_to_eur_original_currency(self):
        result = _converter().convert("100", "USD", "EUR")
        assert result.original.currency.code == "USD"

    def test_100_usd_to_eur_rate(self):
        result = _converter().convert("100", "USD", "EUR")
        assert result.rate == Decimal("0.92")

    def test_55_usd_to_gbp_converted_amount(self):
        result = _converter().convert("55", "USD", "GBP")
        assert result.converted.amount == Decimal("43.45")

    def test_55_usd_to_gbp_converted_currency(self):
        result = _converter().convert("55", "USD", "GBP")
        assert result.converted.currency.code == "GBP"

    def test_zero_usd_to_eur_converted_amount(self):
        result = _converter().convert("0", "USD", "EUR")
        assert result.converted.amount == Decimal("0.00")

    def test_zero_usd_to_eur_original_amount(self):
        result = _converter().convert("0", "USD", "EUR")
        assert result.original.amount == Decimal("0")

    def test_returns_conversion_result_instance(self):
        result = _converter().convert("100", "USD", "EUR")
        assert isinstance(result, ConversionResult)


# ---------------------------------------------------------------------------
# Invalid amount strings
# ---------------------------------------------------------------------------


class TestConverterInvalidAmount:
    def test_non_numeric_string_raises_invalid_amount_error(self):
        with pytest.raises(InvalidAmountError):
            _converter().convert("abc", "USD", "EUR")

    def test_empty_string_raises_invalid_amount_error(self):
        with pytest.raises(InvalidAmountError):
            _converter().convert("", "USD", "EUR")

    def test_negative_amount_raises_invalid_amount_error(self):
        with pytest.raises(InvalidAmountError):
            _converter().convert("-1", "USD", "EUR")

    def test_mixed_string_raises_invalid_amount_error(self):
        with pytest.raises(InvalidAmountError):
            _converter().convert("12abc", "USD", "EUR")


# ---------------------------------------------------------------------------
# Unknown currency codes
# ---------------------------------------------------------------------------


class TestConverterUnknownCurrency:
    def test_unknown_from_code_raises_unknown_currency_pair_error(self):
        with pytest.raises(UnknownCurrencyPairError):
            _converter().convert("100", "JPY", "EUR")

    def test_unknown_to_code_raises_unknown_currency_pair_error(self):
        with pytest.raises(UnknownCurrencyPairError):
            _converter().convert("100", "USD", "JPY")

    def test_both_unknown_codes_raises_unknown_currency_pair_error(self):
        with pytest.raises(UnknownCurrencyPairError):
            _converter().convert("100", "JPY", "CHF")
