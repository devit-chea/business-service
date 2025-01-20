from rest_framework import serializers
from currency.models.currency_models import (
    Currency,
    RateCategory,
    ExchangeRate,
    ExchangeRateHistory,
    ExchangeRateDetail,
)
from currency.utils.common_utils import get_base_currency
from currency.views.view_sets import CurrencyApiView, FilterFields
from currency.serializers.currency_serializers import (
    RootCurrencySerializer,
    RateCategorySerializer,
    ExchangeRateSerializer,
    ExchangeRateHistoryListSerializer,
    ExchangeRateListSerializer,
)


CURRENCY_API_VIEW = CurrencyApiView


class CurrencyView(CURRENCY_API_VIEW):
    model = Currency
    queryset = Currency.objects.all()
    serializer_class = RootCurrencySerializer

    search = ["id", "name", "code"]


class RateCategoryView(CURRENCY_API_VIEW):
    model = RateCategory
    queryset = RateCategory.objects.all()
    serializer_class = RateCategorySerializer


class FindRateCategoryByCurrencyId(CURRENCY_API_VIEW):
    model = ExchangeRateDetail
    queryset = ExchangeRateDetail.objects.all()
    serializer_class = ExchangeRateListSerializer

    def get_queryset(self):
        company_id = self.request.user.base_company_id
        from_currency_id = self.request.query_params.get("from_currency_id")

        base_currency = get_base_currency(company_id)
        to_currency_id = base_currency.currency_id or base_currency.account_currency_id

        # Retrieve the exchange rate for the company and to_currency_id
        exchange_rate = ExchangeRate.objects.filter(
            company_id=company_id, to_currency_id=to_currency_id
        ).first()

        if not exchange_rate:
            raise serializers.ValidationError(
                "No exchange rate found for the company and target currency."
            )

        return ExchangeRateDetail.objects.filter(
            exchange_rate=exchange_rate,
            from_currency_id=from_currency_id,
        )


class ExchangeRateView(CURRENCY_API_VIEW):
    model = ExchangeRate
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer

    def get_queryset(self):
        objs = ExchangeRate.objects
        to_currency_id = self.request.query_params.get("to_currency_id")
        if to_currency_id:
            return objs.filter(to_currency_id=to_currency_id)
        else:
            return objs.all()


class ExchangeRateHistoryView(CURRENCY_API_VIEW):
    model = ExchangeRateHistory
    filter_backends = [FilterFields]
    queryset = ExchangeRateHistory.objects.all()
    serializer_class = ExchangeRateHistoryListSerializer
    lookup_field = "exchange_rate"
