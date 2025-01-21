from rest_framework import serializers
from ..models.billing_model import Billing


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'
        
class BillingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        exclude = [
            "company",
            "create_date",
            "write_date",
            "create_uid",
            "write_uid",
        ]
        
