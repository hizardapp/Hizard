from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries import CountryField
from model_utils.models import TimeStampedModel

from companies.models import Company
from companysettings.models import Department, Question


class Opening(TimeStampedModel):
    title = models.CharField(max_length=770)
    description = models.TextField()
    is_private = models.BooleanField(default=False)
    department = models.ForeignKey(Department, blank=True, null=True)
    closing_date = models.DateTimeField(blank=True, null=True)
    loc_country = CountryField(_("Country"), blank=True)
    loc_city = models.CharField(_("City"), max_length=128, blank=True)
    loc_postcode = models.CharField(_("Post-code"), max_length=64, blank=True)

    company = models.ForeignKey(Company)
    questions = models.ManyToManyField(
        Question, blank=True, null=True, through='OpeningQuestion'
    )


class OpeningQuestion(TimeStampedModel):
    opening = models.ForeignKey(Opening)
    question = models.ForeignKey(Question)
    required = models.BooleanField(default=False)
