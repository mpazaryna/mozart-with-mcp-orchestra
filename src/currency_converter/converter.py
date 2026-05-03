"""Converter engine: Converter."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from currency_converter.models import (
    ConversionResult,
    Currency,
    InvalidAmountError,
    Money,
)
from currency_converter.rates import ExchangeRateRegistry


class Converter:
    """Converts a string amount between two currency codes using a registry."""

    def __init__(self, registry: ExchangeRateRegistry) -> None:
        self._registry = registry

    def convert(
        self, amount_str: str, from_code: str, to_code: str
    ) -> ConversionResult:
        """Parse amount_str and convert from_code → to_code.

        Raises:
            InvalidAmountError: if amount_str cannot be parsed as a Decimal or
                is negative.
            UnknownCurrencyPairError: if the registry has no rate for the pair.
        """
        try:
            amount = Decimal(amount_str)
        except InvalidOperation:
            raise InvalidAmountError(
                f"Cannot parse {amount_str!r} as a numeric amount"
            )

        # Money.__init__ raises InvalidAmountError for negative values, but we
        # surface it here with a more descriptive message before touching Money.
        if amount < Decimal("0"):
            raise InvalidAmountError(
                f"Amount must be non-negative, got {amount_str!r}"
            )

        from_currency = Currency(from_code)
        to_currency = Currency(to_code)

        rate = self._registry.get_rate(from_code, to_code)

        converted_amount = (amount * rate).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        return ConversionResult(
            original=Money(amount, from_currency),
            converted=Money(converted_amount, to_currency),
            rate=rate,
        )
