from django.db import models
from .abstract_model import AbstractBaseCompany


class Address(AbstractBaseCompany):
    house_no = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=120, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True)
    commune = models.CharField(max_length=255, blank=True)
    village = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    latitude = models.CharField(max_length=255, blank=True, null=False)
    longitude = models.CharField(max_length=255, blank=True, null=False)
    
    class Meta:
        db_table = "address"

    
  