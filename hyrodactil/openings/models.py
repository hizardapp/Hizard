from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries import CountryField
from model_utils import Choices
from model_utils.models import TimeStampedModel

from companies.models import Company
from companysettings.models import Question, InterviewStage


class Opening(TimeStampedModel):
    EMPLOYMENT_TYPES = Choices(
        ('part_time', _('Part Time')),
        ('full_time', _('Full Time')),
        ('internship', _('Internship')),
    )

    title = models.CharField(max_length=770)
    description = models.TextField()
    is_private = models.BooleanField(default=False)
    department = models.CharField(_("Department"), max_length=128, blank=True)
    country = CountryField(_("Country"), blank=True)
    city = models.CharField(_("City"), max_length=128, blank=True)
    published_date = models.DateTimeField(blank=True, null=True)
    employment_type = models.CharField(
        choices=EMPLOYMENT_TYPES,
        default=EMPLOYMENT_TYPES.full_time,
        max_length=20
    )

    company = models.ForeignKey(Company)
    questions = models.ManyToManyField(
        Question, blank=True, null=True, through='OpeningQuestion'
    )

    def stage_counts(self):
        for stage in InterviewStage.objects.filter(company=self.company):
            yield self.application_set.filter(current_stage_id=stage).count()

    def get_apply_url(self):
        company_prefix = (
            settings.COMPANY_URL_PREFIX % self.company.subdomain
        )
        return "%s%s" % (
            company_prefix, reverse('public:apply', args=(self.id,))
        )

    def get_location_string(self):
        location = ''

        if self.city:
            location += '%s' % self.city
            if self.country:
                location += ', '

        if self.country:
            location += '%s' % unicode(self.country.name)
        return location

    def get_status(self):
        if self.is_private:
            return _('Private')

        if self.published_date:
            return _('Published')

        return _('Created')

    def __unicode__(self):
        return u"<Opening: %s>" % self.title


class OpeningQuestion(TimeStampedModel):
    opening = models.ForeignKey(Opening)
    question = models.ForeignKey(Question)
    required = models.BooleanField(default=False)
