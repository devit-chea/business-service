from company.serializers.holiday_serializer import HolidaySerializer
from ..models.holiday_model import Holiday
from rest_framework import viewsets



class HolidayView(viewsets.ModelViewSet):
    model = Holiday
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer