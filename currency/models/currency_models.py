from company.models.abstract_base_model import AbstractBaseModel
from company.models.abstract_model import AbstractBaseCompany
from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MinLengthValidator
from django.db import models


class ModelFieldChoices:
    MULTI_DIVIDE_CHOICE = [
        ("multi", "Multi"),
        ("divide", "Divide"),
    ]


class Currency(AbstractBaseModel):
    code = models.CharField(
        unique=True,
        max_length=5,
        blank=False,
        null=False,
        validators=[MinLengthValidator(3)],
    )
    name = models.CharField(max_length=100, blank=False, null=False)
    name_plural = models.CharField(max_length=100, blank=False, null=False)
    symbol = models.CharField(max_length=50, blank=False, null=False)
    symbol_native = models.CharField(max_length=50, blank=False, null=False)

    model_description = "Currency"
    class Meta:
        db_table = "currency"


class RateCategory(AbstractBaseModel, AbstractBaseCompany):
    code = models.CharField(max_length=50, unique=True, blank=False, null=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    model_description = "Currency Rate Currency"
    class Meta:
        db_table = "currency_rate_currency"


class ExchangeRate(AbstractBaseModel, AbstractBaseCompany):
    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="id_to_currency",
        null=False,
        blank=False,
    )

    model_description = "Currency Exchange Rate"
    class Meta:
        db_table = "currency_exchange_rate"


class ExchangeRateDetail(AbstractBaseModel, AbstractBaseCompany):
    exchange_rate = models.ForeignKey(
        ExchangeRate,
        on_delete=models.CASCADE,
        related_name="exchange_rate_detail",
        null=False,
        blank=False,
    )
    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        related_name="id_from_currency",
        null=False,
        blank=False,
    )
    effective_date = models.DateField(null=False, blank=False, editable=True)
    rate_category = models.ForeignKey(
        RateCategory,
        on_delete=models.CASCADE,
        related_name="id_rate_category",
        null=False,
        blank=False,
    )
    rate = models.DecimalField(
        blank=False, null=False, default=0, max_digits=6, decimal_places=2
    )
    multi_or_divide = models.CharField(
        max_length=10,
        choices=ModelFieldChoices.MULTI_DIVIDE_CHOICE,
        default=False,
        blank=False,
        null=False,
    )
    rate_value = models.DecimalField(
        blank=False, null=False, default=0, max_digits=26, decimal_places=14
    )
    rate_reciprocal = models.DecimalField(
        blank=False, null=False, default=0, max_digits=44, decimal_places=32
    )

    model_description = "Currency Exchange Rate detail"

    class Meta:
        db_table = "currency_exchange_rate_detail"


class ExchangeRateHistory(AbstractBaseModel, AbstractBaseCompany):
    exchange_rate = models.ForeignKey(
        ExchangeRate,
        on_delete=models.CASCADE,
        related_name="exchange_rate_history",
        null=False,
        blank=False,
    )
    histories = models.JSONField(encoder=DjangoJSONEncoder, null=False, blank=False)

    model_description = "Currency Exchange Rate History"

    class Meta:
        db_table = "currency_exchange_rate_history"
