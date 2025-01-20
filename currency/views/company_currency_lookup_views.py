from rest_framework import generics
from company.models.company_currency_model import CompanyCurrency
from ..models.currency_models import Currency
from ..mixins.company_currency_lookup_mixin import CompanyCurrencyLookupSerializer

class CompanyCurrencyLookupView(generics.RetrieveAPIView):
    model = Currency
    queryset = Currency.objects.all()
    serializer_class = CompanyCurrencyLookupSerializer
    ordering = ['id']  # Default ordering

    def get(self, request, *args, **kwargs):
        company_id = self.request.user.base_company_id
        company_currency = CompanyCurrency.objects.filter(
            company_id=company_id
        ).all()
        if company_currency:  # Simplified check
            currencies = company_currency.values_list('currency_id')
            query = Currency.objects.filter(id__in=currencies).all().order_by('id')
        else:
            query = Currency.objects.all()
        data = self.filter_queryset(query)
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
