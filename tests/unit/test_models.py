"""Unit tests for the domain model: Currency, Money, ConversionResult."""

import pytest
from decimal import Decimal

from currency_converter.models import Currency, Money, ConversionResult, InvalidAmountError


# ---------------------------------------------------------------------------
# Currency
# ---------------------------------------------------------------------------


class TestCurrency:
    def test_valid_iso_codes_accepted(self):
        assert Currency("USD").code == "USD"
        assert Currency("EUR").code == "EUR"
        assert Currency("GBP").code == "GBP"

    def test_non_standard_length_uppercase_accepted(self):
        # Spec says don't hardcode 3 chars; e.g. "USDT" should be valid
        assert Currency("USDT").code == "USDT"

    def test_empty_string_rejected(self):
        with pytest.raises(ValueError, match="non-empty"):
            Currency("")

    def test_lowercase_rejected(self):
        with pytest.raises(ValueError):
            Currency("usd")

    def test_mixed_case_rejected(self):
        with pytest.raises(ValueError):
            Currency("Usd")

    def test_digits_rejected(self):
        with pytest.raises(ValueError):
            Currency("US1")

    def test_whitespace_rejected(self):
        with pytest.raises(ValueError):
            Currency("US D")

    def test_special_chars_rejected(self):
        with pytest.raises(ValueError):
            Currency("US$")

    def test_equality(self):
        assert Currency("USD") == Currency("USD")

    def test_inequality(self):
        assert Currency("USD") != Currency("EUR")

    def test_repr_contains_code(self):
        r = repr(Currency("EUR"))
        assert "EUR" in r


# ---------------------------------------------------------------------------
# Money
# ---------------------------------------------------------------------------


class TestMoney:
    def test_stores_amount_and_currency(self):
        m = Money(Decimal("100.00"), Currency("USD"))
        assert m.amount == Decimal("100.00")
        assert m.currency == Currency("USD")

    def test_zero_amount_accepted(self):
        m = Money(Decimal("0"), Currency("EUR"))
        assert m.amount == Decimal("0")

    def test_fractional_amount_accepted(self):
        m = Money(Decimal("0.01"), Currency("GBP"))
        assert m.amount == Decimal("0.01")

    def test_large_amount_accepted(self):
        m = Money(Decimal("999999999.99"), Currency("USD"))
        assert m.amount == Decimal("999999999.99")

    def test_negative_amount_rejected(self):
        with pytest.raises(InvalidAmountError):
            Money(Decimal("-0.01"), Currency("USD"))

    def test_string_amount_rejected(self):
        with pytest.raises((InvalidAmountError, TypeError)):
            Money("100", Currency("USD"))  # type: ignore[arg-type]

    def test_float_amount_rejected(self):
        with pytest.raises((InvalidAmountError, TypeError)):
            Money(100.0, Currency("USD"))  # type: ignore[arg-type]

    def test_none_amount_rejected(self):
        with pytest.raises((InvalidAmountError, TypeError)):
            Money(None, Currency("USD"))  # type: ignore[arg-type]

    def test_immutability_amount(self):
        m = Money(Decimal("50"), Currency("USD"))
        with pytest.raises(AttributeError):
            m.amount = Decimal("100")  # type: ignore[misc]

    def test_immutability_currency(self):
        m = Money(Decimal("50"), Currency("USD"))
        with pytest.raises(AttributeError):
            m.currency = Currency("EUR")  # type: ignore[misc]

    def test_equality(self):
        a = Money(Decimal("10"), Currency("USD"))
        b = Money(Decimal("10"), Currency("USD"))
        assert a == b

    def test_inequality_amount(self):
        a = Money(Decimal("10"), Currency("USD"))
        b = Money(Decimal("20"), Currency("USD"))
        assert a != b

    def test_inequality_currency(self):
        a = Money(Decimal("10"), Currency("USD"))
        b = Money(Decimal("10"), Currency("EUR"))
        assert a != b


# ---------------------------------------------------------------------------
# ConversionResult
# ---------------------------------------------------------------------------


class TestConversionResult:
    def _make_result(self):
        original = Money(Decimal("100"), Currency("USD"))
        converted = Money(Decimal("92.50"), Currency("EUR"))
        rate = Decimal("0.9250")
        return ConversionResult(original=original, converted=converted, rate=rate)

    def test_stores_original(self):
        result = self._make_result()
        assert result.original == Money(Decimal("100"), Currency("USD"))

    def test_stores_converted(self):
        result = self._make_result()
        assert result.converted == Money(Decimal("92.50"), Currency("EUR"))

    def test_stores_rate(self):
        result = self._make_result()
        assert result.rate == Decimal("0.9250")

    def test_rate_is_decimal(self):
        result = self._make_result()
        assert isinstance(result.rate, Decimal)


# ---------------------------------------------------------------------------
# InvalidAmountError
# ---------------------------------------------------------------------------


class TestInvalidAmountError:
    def test_is_exception_subclass(self):
        assert issubclass(InvalidAmountError, Exception)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(InvalidAmountError):
            raise InvalidAmountError("amount must be non-negative")

    def test_message_preserved(self):
        try:
            raise InvalidAmountError("bad amount: -5")
        except InvalidAmountError as exc:
            assert "bad amount: -5" in str(exc)
