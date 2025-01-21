from rest_framework import serializers
from company.models.payment_model import Payment, PaymentDetail


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        
        extra_kwargs = {
            "company_id": {
                "required": True,
                "allow_null": False,
            },
        }


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        exclude = [
            "company",
            "create_date",
            "write_date",
            "create_uid",
            "write_uid",
        ]


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = "__all__"


class PaymentDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        exclude = [
            "company",
            "create_date",
            "write_date",
            "create_uid",
            "write_uid",
        ]
