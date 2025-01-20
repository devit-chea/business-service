import logging
from decimal import ROUND_HALF_UP, Decimal
from django.core.exceptions import ValidationError

# Base and Dependency Modules
from service_business.util import to_decimal, to_int

# Local Modules
from ..constants import CurrencySymbolPosition
from ..selectors.currency_selector import get_exchange_rate_detail
from ..utils.common_utils import get_base_currency, get_company_currency

date_format = "%Y-%m-%d"


class CurrencySymbolPosition:
    BEFORE = "before"
    AFTER = "after"


def operator_value(param):
    field_value = ""
    expression = ""

    default_operator = [
        "like",
        "not_like",
        "equal",
        "not_equal",
        "is_set",
        "is_not_set",
        "true",
        "false",
        "lte",
        "gte",
        "gt",
        "lt",
        "in",
        "not_in",
    ]

    extra_operator = {
        ">": "gt",
        ">=": "gte",
        "<": "lt",
        "<=": "lte",
    }

    if param:
        if isinstance(param, str) and "," in param:
            string = param.split(",", 1)
            expression = string[0].strip()
            field_value = string[1].strip()

        elif param == "is_set" or param == "is_not_set":
            expression = param
        elif param == "true":
            field_value = True
        elif param == "false":
            field_value = False
        else:
            field_value = param

        if expression in extra_operator:
            expression = extra_operator.get(expression, "")

        if expression not in default_operator:
            expression = ""
    return field_value, expression


def has_decimal_value(number):
    # Convert the number to a string
    str_num = str(number)
    # Split the number at the decimal point
    if "." in str_num:
        integer_part, decimal_part = str_num.split(".")
        # Check if the decimal part is all zeros
        return any(int(digit) != 0 for digit in decimal_part)
    else:
        # No decimal point, so no decimal value
        return False


def round_number(rounding, value):
    """Round the number to the specified precision."""
    return f"{value:.{to_int(rounding)}f}"


def format_number(rounding, value):
    """Format the number with commas and decimal precision."""
    return f"{to_decimal(value):,.{to_int(rounding)}f}"


def round_or_keep_decimal(value, rounding):
    """Round value if it doesn't have decimals, otherwise keep as is."""
    return value if has_decimal_value(value) else round_number(rounding, value)


def get_number_format(company_id: int, value, round=None):
    base_currency = get_base_currency(company_id)
    rounding = round or to_int(base_currency.rounding)
    value_formatted = format_number(rounding, value)
    return value_formatted


def get_display_currency(company_currency, value):
    """Display value with currency symbol according to position."""
    currency = company_currency.account_currency or company_currency.currency
    return (
        f"{currency.code} {value}"
        if company_currency.position == CurrencySymbolPosition.BEFORE
        else f"{value} {currency.code}"
    )


def get_display_amount(company_id: int, currency_id: int, value):
    company_currency = get_company_currency(company_id, currency_id)
    formatted_value = format_number(company_currency.rounding, value)
    return get_display_currency(company_currency, formatted_value)


# Compute amount_currency base on (balance * rate_reciprocal)


def compute_amount_currency(balance, rate_reciprocal):
    try:
        return Decimal(balance) * Decimal(rate_reciprocal)
    except Exception as e:
        raise ValidationError(e)


def perform_conversion(amount, exchange_rate):
    # Perform currency conversion logic here
    converted_amount = Decimal(amount) * Decimal(exchange_rate)

    # Return the converted amount
    return converted_amount


def from_to_currency_to_rate_reciprocal_divide(from_currency, to_currency):
    """
    Compute from - to currency, to find rate reciprocal by Divide

    Args:
        from_currency (_type_): currency rate from(base currency)
        to_currency (_type_):  currency Exchange Rate to(user selected currency)

    Raises:
        ValidationError: Exception

    Returns:
        float: rate_reciprocal
    """

    try:
        rate_reciprocal = 0
        if not Decimal(to_currency).is_zero():
            rate_reciprocal = Decimal(from_currency) / Decimal(to_currency)

        return rate_reciprocal or 0

    except Exception as e:
        raise ValidationError(e)


def from_to_currency_to_rate_reciprocal_multi(from_currency, to_currency) -> Decimal:
    """
    Compute from - to currency, to find rate reciprocal by Multiply

    Args:
        from_currency (_type_): currency rate from
        to_currency (_type_):  currency rate to

    Raises:
        ValidationError: Exception

    Returns:
        float: rate_reciprocal
    """
    try:
        rate_reciprocal = Decimal(from_currency) * Decimal(to_currency)

        return rate_reciprocal or 0

    except Exception as e:
        raise ValidationError(e)


def get_collection_field_exchange_rate(data):
    company = data["company"]
    currency = data["currency"]
    # Determine the company's base currency
    company_currency = get_company_currency(company.id, currency.id)
    rate_category_id = data["rate_category"]
    exchange_rate_val = data[
        "exchange_rate"
    ]  # By default get from lookup rate_category, but allow user input new value
    # Get exchange rate detail
    exchange_rate_detail = get_exchange_rate_detail(currency, rate_category_id)
    origin_rate_reciprocal_val = Decimal(exchange_rate_detail.rate_reciprocal)
    origin_exchange_rate_val = Decimal(exchange_rate_detail.rate_value)

    # Calculate the reciprocal of the user-provided exchange rate
    base_rate_reciprocal = from_to_currency_to_rate_reciprocal_divide(
        from_currency=1, to_currency=exchange_rate_val
    )

    return {
        "base_currency": company_currency,
        "exchange_rate": exchange_rate_val,  # User-provided exchange rate
        "origin_exchange_rate": origin_exchange_rate_val,  # Original exchange rate before any user modifications
        "rate_reciprocal": round(
            base_rate_reciprocal, 8
        ),  # Reciprocal of the user-provided exchange rate, rounded to 8 decimal places
        "origin_rate_reciprocal": origin_rate_reciprocal_val,  # Original rate reciprocal before any user modifications
    }


# Applied Currency Exchange Rate
def get_conversion_amount_currency(data, exchange_rate):
    # Perform the currency conversion on specified fields
    fields_to_convert = [
        "prepayment_amount",
        "total_discount",
        "total_after_discount",
        "total_tax",
        "total_untaxed",
        "total_tax_incl",
        "total_open_balance",
        "total_balance",
    ]

    converted_data = {
        field: perform_conversion(data[field], exchange_rate)
        for field in fields_to_convert
    }

    return converted_data


def convert_currency_by_reciprocal(amount, reciprocal_rate):
    # Set the precision high enough for calculations
    # with localcontext() as ctx:
    #     ctx.prec = 5

    # Perform currency conversion logic here
    converted_amount = Decimal(amount) * Decimal(reciprocal_rate)

    # Return the converted amount
    return round(converted_amount, 8)


def calculate_rate_reciprocal(rate):
    # Set the precision high enough for calculations
    # with localcontext() as ctx:
    #     ctx.prec = 5

    # Calculate the reciprocal
    reciprocal = Decimal(1) / Decimal(rate)

    return round(reciprocal, 8)


def convert_reciprocal_to_exchange_rate(exchange_rate, reciprocal_rate):
    # Convert the amount from KHR to USD using the reciprocal rate
    amount_base_currency = exchange_rate * reciprocal_rate
    # Rounding to 6 places for a standard financial format
    amount_base_currency = Decimal(amount_base_currency).quantize(
        Decimal("0.00"), rounding=ROUND_HALF_UP
    )

    return amount_base_currency
