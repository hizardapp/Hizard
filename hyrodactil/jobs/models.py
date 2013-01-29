from django.db import models

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
    loc_country = CountryField(blank=True)
    loc_city = models.CharField(max_length=128, blank=True)
    loc_postcode = models.CharField(max_length=64, blank=True)

    company = models.ForeignKey(Company)
    questions = models.ManyToManyField(Question, blank=True, null=True)


class Application(TimeStampedModel):
    first_name = models.CharField(max_length=770)
    last_name = models.CharField(max_length=770)

    opening = models.ForeignKey(Opening)


class ApplicationAnswer(TimeStampedModel):
    answer = models.TextField(blank=True, null=True)

    question = models.ForeignKey(Question)
    application = models.ForeignKey(Application)
