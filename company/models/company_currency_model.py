from django.db import models
from company.models.company_model import Company
from .abstract_model import AbstractBaseCompany
from .abstract_base_model import AbstractBaseModel
from currency.models.currency_models import Currency


class CompanyCurrency(AbstractBaseModel):
    POSITION_CHOICES = [
        ("before", "Before"),
        ("after", "After"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="company_currency",
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    is_base = models.BooleanField(default=False)
    decimal_places = models.FloatField()
    rounding = models.FloatField(blank=True, null=True)
    smallest_noted = models.IntegerField(blank=True, null=True)
    position = models.CharField(
        max_length=50, choices=POSITION_CHOICES, default="before"
    )
    active = models.BooleanField(default=True)

    model_description = "Company Currency"
    class Meta:
        db_table = "company_currency"
