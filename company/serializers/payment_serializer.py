from rest_framework import serializers
from company.models.payment_model import Payment, PaymentDetail
from drf_writable_nested import WritableNestedModelSerializer



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

class PaymentSerializer(WritableNestedModelSerializer):
    payment_detail = PaymentDetailSerializer(many=True, required=True)
    class Meta:
        model = Payment
        fields = "__all__"
