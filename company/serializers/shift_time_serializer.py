from rest_framework import serializers
from company.models.shift_time_model import ShiftTimeModel


class ShiftTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftTimeModel
        fields = "__all__"


class ShiftTimeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftTimeModel
        exclude = ["write_date", "create_uid", "write_uid"]
