from django.db import models

class AbstractBaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    write_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_uid = models.IntegerField(blank=True, null=True, editable=False)
    write_uid = models.IntegerField(blank=True, null=True, editable=False)

    class Meta:
        abstract = True
