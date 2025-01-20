from rest_framework import serializers
from company.models.payment_method_model import PaymentMethodModel


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethodModel
        fields = "__all__"


class PaymentMethodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethodModel
        exclude = [
            "company",
            "create_date",
            "write_date",
            "create_uid",
            "write_uid",
        ]
