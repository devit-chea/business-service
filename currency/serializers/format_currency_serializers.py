from rest_framework import serializers
from ..utils.currency_utils import (
    format_number,
    round_or_keep_decimal,
    get_display_currency,
)
from ..utils.common_utils import get_company_currency_with_meta


class FormatCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        currency_field = None
        currency_fallback = True
        round_decimal_fields = []
        currency_format_fields = []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        new_data = {}

        # Retrieve company_currency once and reuse
        company_currency = get_company_currency_with_meta(self, instance)
        if not company_currency:
            return data

        # Apply formatting for specified fields
        for field in getattr(self.Meta, "currency_format_fields", []):
            if field in data:
                # value = to_decimal(data[field])
                value = data[field]
                formated_value = format_number(company_currency.rounding, value)
                new_data[f"display_{field}"] = get_display_currency(
                    company_currency, formated_value
                )

        for decimal_field in getattr(self.Meta, "round_decimal_fields", []):
            if decimal_field in data:
                # value = to_decimal(data[decimal_field])
                value = data[decimal_field]
                new_data[decimal_field] = round_or_keep_decimal(
                    value, company_currency.rounding
                )

        data.update(new_data)
        return data
