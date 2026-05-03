"""Exchange rate registry: ExchangeRateRegistry, UnknownCurrencyPairError."""

from __future__ import annotations

from decimal import Decimal


class UnknownCurrencyPairError(Exception):
    """Raised when no rate is registered for the requested currency pair."""

    def __init__(self, from_code: str, to_code: str) -> None:
        super().__init__(f"No rate registered for {from_code!r} → {to_code!r}")
        self.from_code = from_code
        self.to_code = to_code


_DEFAULT_RATES: dict[tuple[str, str], Decimal] = {
    ("USD", "EUR"): Decimal("0.92"),
    ("EUR", "GBP"): Decimal("0.86"),
    ("USD", "GBP"): Decimal("0.79"),
}


class ExchangeRateRegistry:
    """Holds a mapping of (from_code, to_code) → Decimal exchange rate."""

    def __init__(self, rates: dict[tuple[str, str], Decimal]) -> None:
        self._rates = dict(rates)

    def get_rate(self, from_code: str, to_code: str) -> Decimal:
        """Return the Decimal rate for the given pair.

        Same-currency pairs always return Decimal("1"). Unknown pairs raise
        UnknownCurrencyPairError.
        """
        if from_code == to_code:
            return Decimal("1")
        try:
            return self._rates[(from_code, to_code)]
        except KeyError:
            raise UnknownCurrencyPairError(from_code, to_code)

    @classmethod
    def default(cls) -> ExchangeRateRegistry:
        """Return an instance pre-loaded with the canonical project rates."""
        return cls(_DEFAULT_RATES)
