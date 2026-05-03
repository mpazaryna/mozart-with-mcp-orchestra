"""Unit tests for the exchange rate registry: ExchangeRateRegistry, UnknownCurrencyPairError."""

import pytest
from decimal import Decimal

from currency_converter.rates import ExchangeRateRegistry, UnknownCurrencyPairError


# ---------------------------------------------------------------------------
# UnknownCurrencyPairError
# ---------------------------------------------------------------------------


class TestUnknownCurrencyPairError:
    def test_is_exception_subclass(self):
        assert issubclass(UnknownCurrencyPairError, Exception)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(UnknownCurrencyPairError):
            raise UnknownCurrencyPairError("USD", "XYZ")

    def test_message_contains_from_code(self):
        try:
            raise UnknownCurrencyPairError("USD", "XYZ")
        except UnknownCurrencyPairError as exc:
            assert "USD" in str(exc)

    def test_message_contains_to_code(self):
        try:
            raise UnknownCurrencyPairError("USD", "XYZ")
        except UnknownCurrencyPairError as exc:
            assert "XYZ" in str(exc)


# ---------------------------------------------------------------------------
# ExchangeRateRegistry — construction and direct lookup
# ---------------------------------------------------------------------------


class TestExchangeRateRegistry:
    def _registry(self) -> ExchangeRateRegistry:
        return ExchangeRateRegistry(
            {
                ("USD", "EUR"): Decimal("0.92"),
                ("EUR", "GBP"): Decimal("0.86"),
                ("USD", "GBP"): Decimal("0.79"),
            }
        )

    def test_get_rate_usd_to_eur(self):
        assert self._registry().get_rate("USD", "EUR") == Decimal("0.92")

    def test_get_rate_eur_to_gbp(self):
        assert self._registry().get_rate("EUR", "GBP") == Decimal("0.86")

    def test_get_rate_usd_to_gbp(self):
        assert self._registry().get_rate("USD", "GBP") == Decimal("0.79")

    def test_get_rate_returns_decimal(self):
        rate = self._registry().get_rate("USD", "EUR")
        assert isinstance(rate, Decimal)

    def test_unknown_pair_raises_unknown_currency_pair_error(self):
        with pytest.raises(UnknownCurrencyPairError):
            self._registry().get_rate("JPY", "CHF")

    def test_unknown_pair_error_message_contains_codes(self):
        with pytest.raises(UnknownCurrencyPairError, match="JPY"):
            self._registry().get_rate("JPY", "CHF")

    def test_same_currency_returns_one(self):
        # Same-currency conversions are always a 1:1 rate.
        assert self._registry().get_rate("USD", "USD") == Decimal("1")


# ---------------------------------------------------------------------------
# ExchangeRateRegistry.default() — factory with canonical project rates
# ---------------------------------------------------------------------------


class TestExchangeRateRegistryDefault:
    def test_default_usd_to_eur(self):
        assert ExchangeRateRegistry.default().get_rate("USD", "EUR") == Decimal("0.92")

    def test_default_eur_to_gbp(self):
        assert ExchangeRateRegistry.default().get_rate("EUR", "GBP") == Decimal("0.86")

    def test_default_usd_to_gbp(self):
        assert ExchangeRateRegistry.default().get_rate("USD", "GBP") == Decimal("0.79")

    def test_default_returns_registry_instance(self):
        assert isinstance(ExchangeRateRegistry.default(), ExchangeRateRegistry)
