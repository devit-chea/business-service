import logging
from decimal import Decimal
from typing import Optional

from ..constants import ReciprocalMethod
from company.models.company_currency_model import CompanyCurrency
from django.core.exceptions import ObjectDoesNotExist
from ..models.currency_models import (
    Currency,
    ExchangeRate,
    ExchangeRateDetail,
    RateCategory,
)


class RaiseError(Exception):
    """Raised when no exchange rate detail is found."""

    pass


def _company_currency(company_id: int, currency_id: int) -> Optional[CompanyCurrency]:
    # Attempt to fetch the company currency with specified parameters.
    company_currency = (
        CompanyCurrency.objects.select_related("currency", "account_currency")
        .filter(
            active=True,
            company_id=company_id,
            account_currency_id=currency_id,
        )
        .first()
    )

    if not company_currency:
        logging.warning(
            f"No company currency found for company ID: {company_id}, currency ID: {currency_id}"
        )

    return company_currency


def get_base_currency(company_id: int) -> CompanyCurrency:
    """
    Retrieve the base currency for a given company.

    Parameters:
        company_id (int): The company ID.

    Returns:
        CompanyCurrency: The company's base currency.

    Raises:
        RaiseError: If no base currency is configured for the company.
    """

    base_currency = (
        CompanyCurrency.objects.select_related("currency")
        .filter(company_id=company_id, is_base=True)
        .first()
    )

    if base_currency is None:
        raise RaiseError(
            "No base currency configured. Please configure a base currency for the company."
        )

    return base_currency


def get_company_currency(company_id: int, currency_id: int) -> CompanyCurrency:
    if currency_id:
        return _company_currency(company_id, currency_id)

    return get_base_currency(company_id)


def get_nested_instance(self, instance):
    """Retrieve nested currency instance based on `currency_field`."""
    currency_field = getattr(self.Meta, "currency_field", "currency").split("__")
    nested_instance = instance
    for key in currency_field:
        nested_instance = getattr(nested_instance, key, None)
        if not nested_instance:
            return None
    return nested_instance if isinstance(nested_instance, Currency) else None


def get_company_currency_with_meta(self, instance):
    """Get or fallback to base company currency for the given instance."""
    request = self.context.get("request")
    company_id = request.user.base_company_id if request else None
    currency = get_nested_instance(self, instance)

    if currency:
        return _company_currency(company_id, currency.id)

    if not getattr(self.Meta, "currency_fallback", True) or company_id is None:
        return None

    return get_base_currency(company_id)


def get_exchange_rate(
    company_id: int, from_currency_id: int, category_id: int, to_currency_id=None
) -> ExchangeRateDetail:
    """
    Retrieve the exchange rate between two currencies.

    Parameters:
        company_id (int): The company ID.
        to_currency_id (int): The target currency ID (currency to convert to).
        from_currency_id (int): The source currency ID (currency to convert from).
        category_id (int): The exchange rate category ID.

    Returns:
        ExchangeRateDetail: The exchange rate detail.

    Raises:
        RaiseError: If no matching exchange rate detail is found.
    """
    try:
        # Check if the rate category exists
        if not RateCategory.objects.filter(id=category_id).exists():
            raise RaiseError(
                "No rate category found. Please provide a valid rate category."
            )

        # If no to_currency_id provided, get the company's base currency
        if to_currency_id is None:
            base_currency = get_base_currency(company_id)
            to_currency_id = (
                base_currency.currency_id or base_currency.account_currency_id
            )

        # Retrieve the exchange rate for the company and to_currency_id
        exchange_rate = ExchangeRate.objects.filter(
            company_id=company_id, to_currency_id=to_currency_id
        ).first()

        if not exchange_rate:
            raise RaiseError(
                "No exchange rate found for the company and target currency."
            )

        # Retrieve the exchange rate detail for the from_currency_id and rate category
        exchange_rate_detail = ExchangeRateDetail.objects.filter(
            exchange_rate=exchange_rate,
            from_currency_id=from_currency_id,
            rate_category_id=category_id,
        ).first()

        if not exchange_rate_detail:
            currency_name = Currency.objects.get(pk=from_currency_id).name
            raise RaiseError(f"No exchange rate found for the {currency_name}")

        return exchange_rate_detail

    except ObjectDoesNotExist:
        raise RaiseError(
            "No exchange rate found. Please configure an exchange rate for the company."
        )


def adjust_rate_reciprocal(exchange_rate_detail, adjust_exchange_rate):
    if adjust_exchange_rate > 0:
        if exchange_rate_detail.multi_or_divide == ReciprocalMethod.DIVIDE:
            rate_reciprocal = exchange_rate_detail.rate / adjust_exchange_rate
        else:
            rate_reciprocal = exchange_rate_detail.rate * adjust_exchange_rate
    else:
        rate_reciprocal = exchange_rate_detail.rate_reciprocal

    return rate_reciprocal


def exchange_amount(
    company_id: int,
    to_currency_id: int,
    from_currency_id: int,
    category_id: int,
    **kwargs,
) -> Decimal:
    if "amount" not in kwargs:
        raise RaiseError("The 'amount' parameter is required but was not provided.")

    exchange_rate_detail = get_exchange_rate(
        company_id, from_currency_id, category_id, to_currency_id
    )

    exchange_rate = kwargs.get("exchange_rate") or 0
    rate_reciprocal = adjust_rate_reciprocal(exchange_rate_detail, exchange_rate)
    return kwargs["amount"] * rate_reciprocal


def exchange_base_amount(
    company_id: int,
    from_currency_id: int,
    category_id: int,
    **kwargs,
) -> Decimal:
    base_currency = get_base_currency(company_id)
    base_currency_id = base_currency.currency_id or base_currency.account_currency_id
    return exchange_amount(
        company_id,
        base_currency_id,
        from_currency_id,
        category_id,
        **kwargs,
    )


def exchange_rate_fields(
    company_id: int,
    from_currency_id: int,
    category_id: int,
    **kwargs,
):
    exchange_rate_detail = get_exchange_rate(
        company_id, from_currency_id, category_id, kwargs.get("to_currency_id")
    )

    adjust_exchange_rate = kwargs.get("exchange_rate") or 0
    origin_exchange_rate = exchange_rate_detail.rate_value
    origin_rate_reciprocal = exchange_rate_detail.rate_reciprocal
    adjusted_rate_reciprocal = adjust_rate_reciprocal(
        exchange_rate_detail, adjust_exchange_rate
    )

    result = {
        "base_currency": get_base_currency(company_id),
        "exchange_rate": adjust_exchange_rate,
        "rate_reciprocal": adjusted_rate_reciprocal,
        "origin_exchange_rate": origin_exchange_rate,
        "origin_rate_reciprocal": origin_rate_reciprocal,
    }
    return result
