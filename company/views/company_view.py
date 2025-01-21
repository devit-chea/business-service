from company.models.company_model import Company
from django.db.models import Q
from company.serializers.company_serializer import (
    CompanyListSerializer,
    CompanySerializer,
)
from company.constants import CompanyType
from .base_view import BaseModelViewSet

class CompanyView(BaseModelViewSet):
    permission_classes = []
    
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CompanyListSerializer
        if self.action in ["create", "update"]:
            return CompanySerializer
        return CompanySerializer

    def list(self, request):
        data = Company.objects.filter(
			Q(parent__isnull=True) | Q(type=CompanyType.COMPANY)
		).all()

        data = self.filter_queryset(data)
        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

