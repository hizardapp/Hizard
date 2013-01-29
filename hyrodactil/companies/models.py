from django.db import models

from model_utils.models import TimeStampedModel


class Company(TimeStampedModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name
