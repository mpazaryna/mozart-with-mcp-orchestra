"""Integration tests: Converter wired to ExchangeRateRegistry (no mocks)."""

import pytest
from decimal import Decimal

from currency_converter.converter import Converter
from currency_converter.models import InvalidAmountError
from currency_converter.rates import ExchangeRateRegistry, UnknownCurrencyPairError


@pytest.fixture(scope="module")
def converter() -> Converter:
    return Converter(ExchangeRateRegistry.default())


@pytest.mark.integration
class TestConverterWithRates:
    def test_100_usd_to_eur(self, converter: Converter) -> None:
        result = converter.convert("100", "USD", "EUR")
        assert result.converted.amount == Decimal("92.00")
        assert result.converted.currency.code == "EUR"

    def test_55_usd_to_gbp(self, converter: Converter) -> None:
        result = converter.convert("55", "USD", "GBP")
        assert result.converted.amount == Decimal("43.45")
        assert result.converted.currency.code == "GBP"

    def test_zero_usd_to_eur(self, converter: Converter) -> None:
        result = converter.convert("0", "USD", "EUR")
        assert result.converted.amount == Decimal("0.00")

    def test_unknown_currency_pair_raises(self, converter: Converter) -> None:
        with pytest.raises(UnknownCurrencyPairError) as exc_info:
            converter.convert("10", "GBP", "USD")
        assert exc_info.value.from_code == "GBP"
        assert exc_info.value.to_code == "USD"

    def test_non_numeric_amount_raises(self, converter: Converter) -> None:
        with pytest.raises(InvalidAmountError):
            converter.convert("abc", "USD", "EUR")

    def test_same_currency_returns_rate_one(self, converter: Converter) -> None:
        result = converter.convert("50", "USD", "USD")
        assert result.rate == Decimal("1")
        assert result.converted.amount == Decimal("50.00")

    def test_original_money_preserved(self, converter: Converter) -> None:
        result = converter.convert("200", "USD", "EUR")
        assert result.original.amount == Decimal("200")
        assert result.original.currency.code == "USD"
