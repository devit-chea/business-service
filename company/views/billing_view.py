from company.serializers.billing_serializer import BillingSerializer
from ..models.billing_model import Billing
from .base_view import BaseModelViewSet


class BillingView(BaseModelViewSet):
    model = Billing
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    

        
