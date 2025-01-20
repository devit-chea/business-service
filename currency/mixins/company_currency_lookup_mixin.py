from rest_framework import serializers
from ..models.currency_models import Currency

class CompanyCurrencyLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
            "id",
            "name",
            "code",
            "symbol"
        ]