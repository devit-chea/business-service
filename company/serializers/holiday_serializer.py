from rest_framework import serializers
from ..models.holiday_model import Holiday


class HolidaySerializer():
    color = serializers.SerializerMethodField()
    class Meta:
        model = Holiday
        fields = '__all__'
        
        
class HolidayDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        exclude = [
            "company",
            "create_date",
            "write_date",
            "create_uid",
            "write_uid",
        ]
        
