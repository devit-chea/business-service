from company.serializers.holiday_serializer import HolidaySerializer
from ..models.holiday_model import Holiday
from .base_view import BaseModelViewSet



class HolidayView(BaseModelViewSet):
    model = Holiday
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer