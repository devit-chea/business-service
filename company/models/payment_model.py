from django.db import models
from company.constants import ModelFieldChoices
from .abstract_model import AbstractBaseCompany


class Payment(AbstractBaseCompany):
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

    class Meta:
        db_table = "payment"
        

class PaymentDetail(AbstractBaseCompany):
    bank_name = models.CharField(blank=False, null=False)
    account_holder_name = models.CharField(blank=True)
    account_number = models.CharField(blank=True)
    method_type = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        choices=ModelFieldChoices.METHOD_TYPE,
    )
    note = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        Payment,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="payment_detail"
    )

    class Meta:
        db_table = "payment_detail"
