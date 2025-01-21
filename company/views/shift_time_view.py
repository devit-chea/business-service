from company.serializers.shift_time_serializer import ShiftTimeSerializer
from ..models.shift_time_model import ShiftTime
from .base_view import BaseModelViewSet


class ShiftTimeView(BaseModelViewSet):
    model = ShiftTime
    queryset = ShiftTime.objects.all()
    serializer_class = ShiftTimeSerializer