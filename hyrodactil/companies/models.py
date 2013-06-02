
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel


class Company(TimeStampedModel):
    name = models.CharField(
        max_length=100,
        help_text=_('Name of your company')
    )
    subdomain = models.SlugField(
        unique=True,
        help_text=_('Your career page will be available at this.hizard.com')
    )
    website = models.URLField(
        blank=True,
        help_text=_('Your career page will have a link to your company website if this is filled')
    )
    description = models.TextField(
        blank=True,
        help_text=_('This description of your company will appear on your career site')
    )

    class Meta:
        verbose_name_plural = 'companies'

    def __unicode__(self):
        return self.name

    def get_career_site_url(self):
        company_prefix = (
            settings.COMPANY_URL_PREFIX % self.subdomain
        )
        return "%s%s" % (company_prefix, reverse('public:opening-list'))
