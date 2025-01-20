from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from currency.serializers.format_currency_serializers import FormatCurrencySerializer
from currency.models.currency_models import (
    Currency,
    RateCategory,
    ExchangeRate,
    ExchangeRateDetail,
    ExchangeRateHistory,
)


class RootCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"
        date_format_fields = ["create_date", "write_date"]


class RootCurrencyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "name", "code"]


class RateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RateCategory
        fields = "__all__"
        date_format_fields = ["create_date", "write_date"]


class RateCategoryInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateCategory
        fields = ["id", "name", "code"]


class ExchangeRateDetailSerializer(WritableNestedModelSerializer):
    from_currency = PresentablePrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        presentation_serializer=RootCurrencyInfoSerializer,
        required=False,
    )
    rate_category = PresentablePrimaryKeyRelatedField(
        queryset=RateCategory.objects.all(),
        presentation_serializer=RateCategoryInfoSerializer,
    )

    class Meta:
        model = ExchangeRateDetail
        fields = [
            "id",
            "from_currency",
            "effective_date",
            "rate_category",
            "rate",
            "multi_or_divide",
            "rate_value",
            "rate_reciprocal",
        ]
        date_format_fields = ["create_date", "write_date"]

    def to_internal_value(self, data):
        request = self.context.get("request")
        validated_data = super().to_internal_value(data)
        validated_data["company"] = request.user.base_company
        validated_data["create_uid"] = request.user.create_uid

        get_choices = data["multi_or_divide"]

        if get_choices == "multi":
            reciprocal = data["rate"] * data["rate_value"]
        else:
            reciprocal = data["rate"] / data["rate_value"]

        validated_data["rate_reciprocal"] = reciprocal

        return validated_data

    def to_representation(self, instance):
        """
        To Represent field list detail
        (rate, rate_value) -> value as number
        """
        data = super().to_representation(instance)
        data["rate"] = instance.rate
        data["rate_value"] = instance.rate_value
        return data


class ExchangeRateListSerializer(FormatCurrencySerializer):
    rate_category = PresentablePrimaryKeyRelatedField(
        queryset=RateCategory.objects.all(),
        presentation_serializer=RateCategoryInfoSerializer,
        required=False,
    )

    class Meta:
        model = ExchangeRateDetail
        fields = [
            "id",
            "from_currency",
            "effective_date",
            "rate",
            "multi_or_divide",
            "rate_value",
            "rate_reciprocal",
            "rate_category",
        ]
        round_decimal_fields = ["rate_value"]


class ExchangeRateHistoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateHistory
        fields = "__all__"
        date_format_fields = ["create_date", "write_date"]


class ExchangeRateSerializer(WritableNestedModelSerializer):
    exchange_rate_details = ExchangeRateDetailSerializer(many=True, required=False)
    to_currency = PresentablePrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        presentation_serializer=RootCurrencyInfoSerializer,
        required=False,
    )

    class Meta:
        model = ExchangeRate
        fields = "__all__"
        date_format_fields = ["create_date", "write_date"]

    def create(self, data):
        try:
            request = self.context.get("request")
            entry = ExchangeRate.objects.prefetch_related("to_currency").get(
                to_currency=data["to_currency"]
            )

            # Serialize the data for the history
            # Create a copy of the existing object (history) |  Serialize the data
            serialized_entry = ExchangeRateSerializer(entry, context=self.context).data
            histories = {
                "exchange_rate": entry,
                "company": entry.company,
                "create_uid": request.user.id,
                "histories": serialized_entry,
            }

            ExchangeRateHistory.objects.create(**histories)

            # Update the existing object with the new data
            return super().update(entry, data)

        except ExchangeRate.DoesNotExist:
            return super().create(data)
