from rest_framework import serializers
from ..models.currency_models import ExchangeRateDetail


def get_exchange_rate_detail(from_currency, rate_category: int) -> ExchangeRateDetail:
    exchange_rate_detail = ExchangeRateDetail.objects.filter(
        from_currency_id=from_currency.id, rate_category_id=rate_category
    ).first()
    if not exchange_rate_detail:
        raise serializers.ValidationError(
            detail={
                "missing_config": f"Exchange rate detail not found for the provided currency {from_currency.code} and rate category."
            },
            code="exchange_rate_detail",
        )
    return exchange_rate_detail
