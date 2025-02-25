from rest_framework import serializers
from company.models.shift_time_model import ShiftTime


class ShiftTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftTime
        fields = "__all__"


class ShiftTimeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftTime
        exclude = [
            "company",
            "create_date",
            "write_date",
            "create_uid",
            "write_uid",
        ]
