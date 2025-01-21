from rest_framework import serializers
from company.models.payment_model import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = [
            "company",
            "create_date",
            "write_date",
            "create_uid",
            "write_uid",
        ]
