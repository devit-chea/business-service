from company.models.company_model import Company
from rest_framework import viewsets


class BaseModelViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        try:
            # ! Remove when authentication done
            company_id = self.request.data["company_id"]

            company = Company.objects.filter(id=company_id).first()
            if not company:
                raise ValueError("Create Company not found.")

            serializer.validated_data["company"] = company

            # save data
            _model_instance = serializer.save()
        except Exception as e:
            raise e

    def perform_update(self, serializer):
        try:
            # ! Remove when authentication done
            company_id = self.request.data["company_id"]

            company = Company.objects.filter(id=company_id).first()
            if not company:
                raise ValueError("Update Company not found.")

            serializer.validated_data["company"] = company

            # save data
            _model_instance = serializer.save()

        except Exception as e:
            raise e
