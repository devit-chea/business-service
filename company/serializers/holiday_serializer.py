from rest_framework import serializers
from ..models.holiday_model import Holiday


class HolidaySerializer():
    color = serializers.SerializerMethodField()
    class Meta:
        model = Holiday
        fields = '__all__'
        
