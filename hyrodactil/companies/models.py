
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from model_utils.models import TimeStampedModel


class Company(TimeStampedModel):
    name = models.CharField(max_length=100)
    subdomain = models.SlugField(unique=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name

    def get_career_site_url(self):
        company_prefix = (
            settings.COMPANY_URL_PREFIX % self.subdomain
        )
        return "%s%s" % (company_prefix, reverse('public:opening-list'))
