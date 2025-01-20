from .company_model import Company
from django.db import models


class AbstractBaseCompany(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        editable=False,
        related_name="%(class)s_related",
    )

    class Meta:
        abstract = True


class AbstractReferenceNo(models.Model):
    reference_no = models.CharField(max_length=255, editable=False)

    class Meta:
        abstract = True
