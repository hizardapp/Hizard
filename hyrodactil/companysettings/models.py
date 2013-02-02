from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import TimeStampedModel
from companies.models import Company


class Department(TimeStampedModel):
    name = models.CharField(max_length=100)

    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name


class Question(TimeStampedModel):
    TYPE_QUESTIONS = Choices(
        ('textbox', _('textbox')),
        ('textarea', _('textarea')),
        ('checkbox', _('checkbox')),
        ('file', _('file')),
        ('ddl', _('ddl'))
    )

    name = models.CharField(max_length=200)
    label = models.CharField(max_length=200)

    type = models.CharField(
        choices=TYPE_QUESTIONS,
        default=TYPE_QUESTIONS.textbox,
        max_length=20
    )
    options = models.CharField(max_length=770, blank=True)

    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name


class InterviewStage(TimeStampedModel):
    name = models.CharField(max_length=100)

    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name