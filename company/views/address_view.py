from company.serializers.address_serializer import AddressSerializer
from ..models.shift_time_model import ShiftTime
from .base_view import BaseModelViewSet


class AddressView(BaseModelViewSet):
    model = ShiftTime
    queryset = ShiftTime.objects.all()
    serializer_class = AddressSerializer