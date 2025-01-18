from django.db import models
from company.constants import OFFICE_TYPE, CompanyType

class Company(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    active = models.BooleanField(default=True)
    account_name = models.CharField(max_length=255, null=True, blank=True)
    attention = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    phone1 = models.CharField(max_length=255, blank=True)
    phone2 = models.CharField(max_length=255, blank=True)
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    legal_name = models.CharField(max_length=255, blank=True)
    registration_tax_id = models.CharField(max_length=255, null=True, blank=True)
    exemption_tax_number = models.CharField(max_length=255, null=True, blank=True)
    email_mask = models.CharField(max_length=255, blank=True)
    phone_mask = models.CharField(max_length=255, blank=True)
    quantity_decimal_place = models.IntegerField(default=0)
    price_decimal_place = models.IntegerField(default=0)
    number_of_employee = models.CharField(max_length=255, null=True, blank=False)
    estimate_revenue = models.DecimalField(default=0.0, decimal_places=2, max_digits=4)
    industry = models.CharField(max_length=255, blank=True)
    latitude = models.CharField(max_length=255, blank=True)
    longitude = models.CharField(max_length=255, blank=True)
    established_at = models.DateField(blank=True, null=True)
    open_time = models.TimeField(blank=True, null=True)
    close_time = models.TimeField(blank=True, null=True)
    type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default=CompanyType.COMPANY,
        choices=OFFICE_TYPE
    )
    description = models.TextField(blank=True)

    # To define model description
    model_description = "Company"

    class Meta:
        db_table = "company"
