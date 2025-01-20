import logging
from rest_framework import serializers
from rest_framework import serializers
from ..models.currency_models import Currency
from service_business.util import to_decimal, to_int
from company.models.company_currency_model import CompanyCurrency


class CurrencySymbolPosition:
    BEFORE = "before"
    AFTER = "after"


class RootCurrencyFormatSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        currency_field = None
        currency_fallback = True
        currency_format_fields = []

    def to_representation(self, instance):
        new_data = {}
        data = super().to_representation(instance)
        number_format_fields = (
            self.Meta.currency_format_fields
            if hasattr(self.Meta, "currency_format_fields")
            else []
        )

        company_currency = self.get_company_currency(instance)
        if not company_currency:
            return data

        for field in number_format_fields:
            if field in data:
                value = to_decimal(data[field])
                new_field = f"display_{field}"
                rounding = to_int(company_currency.rounding)
                new_value = self.format_number(rounding, value)
                new_value = self.get_display_currency(company_currency, new_value)
                new_data[new_field] = new_value

        data.update(new_data)
        return data

    def format_number(self, rounding, value):
        return str("{:,." + str(rounding) + "f}").format(to_decimal(value))

    def get_display_currency(self, company_currency, value):
        currency = company_currency.account_currency
        return (
            f"{currency.code} {value}"
            if company_currency.position == CurrencySymbolPosition.BEFORE
            else f"{value} {currency.code}"
        )

    def get_nested_instance(self, instance):
        currency_field = (
            self.Meta.currency_field
            if hasattr(self.Meta, "currency_field")
            and self.Meta.currency_field is not None
            else "currency"
        ).split("__")

        nested_instance = instance
        for key in currency_field:
            if hasattr(nested_instance, key):
                nested_instance = getattr(nested_instance, key, None)
                if not nested_instance:
                    return nested_instance

        return nested_instance if isinstance(nested_instance, Currency) else None

    def get_company_currency(self, instance):
        request = self.context.get("request")
        company_id = request.user.base_company_id if request else instance.company_id
        currency = self.get_nested_instance(instance)

        if currency is not None:
            try:
                return CompanyCurrency.objects.prefetch_related("currency").get(
                    account_currency=currency, company_id=company_id
                )
            except CompanyCurrency.DoesNotExist:
                logging.error("Company currency not found")

        if hasattr(self.Meta, "currency_fallback") and not self.Meta.currency_fallback:
            return None

        return CompanyCurrency.objects.filter(
            company_id=company_id, is_base=True
        ).first()
