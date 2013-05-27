from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries import CountryField
from model_utils import Choices
from model_utils.models import TimeStampedModel

from companies.models import Company
from companysettings.models import Department, Question, InterviewStage


class Opening(TimeStampedModel):
    EMPLOYMENT_TYPES = Choices(
        ('part_time', _('Part Time')),
        ('full_time', _('Full Time')),
        ('internship', _('Internship')),
    )

    title = models.CharField(max_length=770)
    description = models.TextField()
    is_private = models.BooleanField(default=False)
    department = models.ForeignKey(Department, blank=True, null=True)
    closing_date = models.DateTimeField(blank=True, null=True)
    loc_country = CountryField(_("Country"), blank=True)
    loc_city = models.CharField(_("City"), max_length=128, blank=True)
    loc_postcode = models.CharField(_("Post-code"), max_length=64, blank=True)
    employment_type = models.CharField(
        choices=EMPLOYMENT_TYPES,
        default=EMPLOYMENT_TYPES.full_time,
        max_length=20
    )

    company = models.ForeignKey(Company)
    questions = models.ManyToManyField(
        Question, blank=True, null=True, through='OpeningQuestion'
    )

    def applicants_stats(self):
        stages = []
        stages_indexes = dict()
        for i, stage in enumerate(InterviewStage.objects.filter(
                company=self.company).only("id", "name")):
            stages.append([stage.name, 0])
            stages_indexes[stage.name] = i

        for application in self.application_set.all():
            stages[stages_indexes[application.current_stage.name]][1] += 1

        return stages

    def get_apply_url(self):
        company_prefix = (
            settings.COMPANY_URL_PREFIX % self.company.subdomain
        )
        return "%s%s" % (company_prefix, reverse('public:apply', args=(self.id,)))

    def get_location_string(self):
        return '%s, %s' % (self.loc_city, unicode(self.loc_country.name))

    def get_status(self):
        if self.closing_date:
            return _('Closed')

        if self.is_private:
            return _('Private')

        #if self.is_published:
            #return _('Published')

        return _('Created')


class OpeningQuestion(TimeStampedModel):
    opening = models.ForeignKey(Opening)
    question = models.ForeignKey(Question)
    required = models.BooleanField(default=False)
