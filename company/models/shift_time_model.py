from django.db import models
from .abstract_model import AbstractBaseCompany
from .abstract_base_model import AbstractBaseModel


class ShiftTime(AbstractBaseCompany, AbstractBaseModel):
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_break = models.TimeField()
    end_break = models.TimeField()
    total_break = models.DecimalField(default=0.0, decimal_places=2, max_digits=4)
    description = models.CharField(max_length=55, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "shift_time"
