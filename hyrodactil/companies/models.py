from django.db import models

from model_utils.models import TimeStampedModel


class Company(TimeStampedModel):
    name = models.CharField(max_length=100)
    subdomain = models.SlugField(unique=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def get_public_openings_list(self):
        pass

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name
