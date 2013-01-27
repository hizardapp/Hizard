from django.conf import settings
from django.db import models

from model_utils.models import TimeStampedModel


class Company(TimeStampedModel):
    name = models.CharField(max_length=100)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name
