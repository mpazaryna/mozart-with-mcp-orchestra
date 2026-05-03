"""CLI entry point: currency-converter <amount> <from_currency> <to_currency>."""

from __future__ import annotations

import argparse
import sys

from currency_converter.converter import Converter
from currency_converter.models import InvalidAmountError
from currency_converter.rates import ExchangeRateRegistry, UnknownCurrencyPairError


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="currency-converter",
        description="Convert an amount between two currencies.",
    )
    parser.add_argument("amount", help="Amount to convert (numeric)")
    parser.add_argument("from_currency", help="Source currency code (e.g. USD)")
    parser.add_argument("to_currency", help="Target currency code (e.g. EUR)")
    args = parser.parse_args()

    converter = Converter(ExchangeRateRegistry.default())

    try:
        result = converter.convert(args.amount, args.from_currency, args.to_currency)
    except InvalidAmountError as exc:
        print(f"Error: invalid amount — {exc}", file=sys.stderr)
        sys.exit(1)
    except UnknownCurrencyPairError as exc:
        print(f"Error: unknown currency — {exc}", file=sys.stderr)
        sys.exit(1)

    converted = result.converted.amount
    print(
        f"{args.amount} {args.from_currency} = {converted:.2f} {args.to_currency}"
    )
