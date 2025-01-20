from django.urls import include, path
from rest_framework import routers
from currency.views.factory_currencies import FactoryCurrency

from currency.views.currency_views import (
    CurrencyView,
    RateCategoryView,
    FindRateCategoryByCurrencyId,
    ExchangeRateView,
    ExchangeRateHistoryView,
)
from currency.views.company_currency_lookup_views import CompanyCurrencyLookupView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"currency", CurrencyView)
router.register(r"currency/rate/category", RateCategoryView)
router.register(r"currency/exchange/rate", ExchangeRateView)
router.register(r"currency/exchange/rate/history", ExchangeRateHistoryView)

urlpatterns = [
    path(
        "currency/find-rate-category",
        FindRateCategoryByCurrencyId.as_view({"get": "list"}),
    ),
    path("", include(router.urls)),
    path("currency/lookup/company-currency", CompanyCurrencyLookupView.as_view()),
    path("currency/factory", FactoryCurrency.as_view()),
]
