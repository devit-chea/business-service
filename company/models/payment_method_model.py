from django.db import models
from company.constants import ModelFieldChoices
from .abstract_model import AbstractBaseCompany


class PaymentMethodModel(AbstractBaseCompany):
    bank_name = models.CharField(blank=False, null=False)
    account_holder_name = models.CharField(blank=True)
    account_number = models.CharField(blank=True)
    method_type = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        choices=ModelFieldChoices.METHOD_TYPE,
    )
    note = models.TextField(blank=True)

    # To define model description
    model_description = "Payment Method"

    class Meta:
        db_table = "payment_method"
