from django.db import models
from .abstract_model import AbstractBaseCompany


class Holiday(AbstractBaseCompany):
    name= models.CharField(max_length=255, blank=False, null=False)
    date= models.DateField()
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = "holiday"

    
  