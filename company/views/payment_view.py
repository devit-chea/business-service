from company.serializers.payment_serializer import PaymentSerializer
from ..models.payment_model import Payment
from rest_framework import viewsets


class PaymentView(viewsets.ModelViewSet):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer