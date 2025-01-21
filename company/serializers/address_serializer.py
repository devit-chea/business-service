from rest_framework import serializers
from ..models.address_model import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        

class AddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = [
            "company",
            "create_date",
            "write_date",
            "create_uid",
            "write_uid",
        ]
        
