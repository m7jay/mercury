from babel.numbers import parse_decimal, NumberFormatError, format_currency
from babel import Locale


def parse_amount(amount: str, locale: str = "en_IN") -> float:
    if not amount:
        return 0.0
    try:
        parsed_amount = parse_decimal(str(amount), locale=locale)
    except NumberFormatError as error:
        parsed_amount = 0.0
    return parsed_amount


def format_amount(amount, format_as_locale: str = "en_IN"):
    if format_as_locale == "en_IN":
        locale = Locale("en", "IN")
        return format_currency(abs(float(amount)), "INR", locale=locale)
    raise NotImplementedError
