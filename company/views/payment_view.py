from company.serializers.payment_serializer import PaymentSerializer
from ..models.payment_model import Payment
from .base_view import BaseModelViewSet


class PaymentView(BaseModelViewSet):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
