"""Domain model: Currency, Money, ConversionResult, InvalidAmountError."""

from __future__ import annotations

from decimal import Decimal


class InvalidAmountError(Exception):
    """Raised when a monetary amount is not a valid non-negative Decimal."""


class Currency:
    """A validated ISO-style currency code (uppercase alphabetic, non-empty)."""

    __slots__ = ("_code",)

    def __init__(self, code: str) -> None:
        if not isinstance(code, str) or not code:
            raise ValueError("Currency code must be a non-empty string")
        if not code.isalpha() or code != code.upper():
            raise ValueError(
                f"Currency code must be uppercase alphabetic characters; got {code!r}"
            )
        self._code = code

    @property
    def code(self) -> str:
        return self._code

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Currency):
            return NotImplemented
        return self._code == other._code

    def __hash__(self) -> int:
        return hash(self._code)

    def __repr__(self) -> str:
        return f"Currency({self._code!r})"


class Money:
    """An immutable monetary value: a non-negative Decimal amount and a Currency."""

    __slots__ = ("_amount", "_currency")

    def __init__(self, amount: Decimal, currency: Currency) -> None:
        if not isinstance(amount, Decimal):
            raise InvalidAmountError(
                f"amount must be a Decimal, got {type(amount).__name__}"
            )
        if amount < Decimal("0"):
            raise InvalidAmountError(
                f"amount must be non-negative, got {amount!r}"
            )
        self._amount = amount
        self._currency = currency

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> Currency:
        return self._currency

    def __setattr__(self, name: str, value: object) -> None:
        # Permit writes only while the slot has never been populated.
        # Once a slot exists (hasattr returns True), it is frozen.
        if name in self.__slots__ and not hasattr(self, name):
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Money is immutable; cannot set {name!r}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self._amount == other._amount and self._currency == other._currency

    def __hash__(self) -> int:
        return hash((self._amount, self._currency))

    def __repr__(self) -> str:
        return f"Money({self._amount!r}, {self._currency!r})"


class ConversionResult:
    """The outcome of a currency conversion: original, converted, and the rate used."""

    __slots__ = ("_original", "_converted", "_rate")

    def __init__(
        self, original: Money, converted: Money, rate: Decimal
    ) -> None:
        self._original = original
        self._converted = converted
        self._rate = rate

    @property
    def original(self) -> Money:
        return self._original

    @property
    def converted(self) -> Money:
        return self._converted

    @property
    def rate(self) -> Decimal:
        return self._rate

    def __repr__(self) -> str:
        return (
            f"ConversionResult(original={self._original!r}, "
            f"converted={self._converted!r}, rate={self._rate!r})"
        )
