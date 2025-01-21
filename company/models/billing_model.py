from django.db import models
from .abstract_model import AbstractBaseCompany


class Billing(AbstractBaseCompany):
    legal_name = models.CharField(max_length=255, blank=True)
    registration_tax_id = models.CharField(max_length=255, null=True, blank=True)
    exemption_tax_number = models.CharField(max_length=255, null=True, blank=True)
    phone1 = models.CharField(max_length=255, blank=True, null=True)
    phone2 = models.CharField(max_length=255, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = "billing"

    
  