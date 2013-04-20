from autoslug import AutoSlugField
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
        ('textbox', _('Single Line')),
        ('textarea', _('Multi Line')),
        ('checkbox', _('Checkbox')),
        ('file', _('File upload')),
    )

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')

    type = models.CharField(
        choices=TYPE_QUESTIONS,
        default=TYPE_QUESTIONS.textbox,
        max_length=20
    )

    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name


class InterviewStage(TimeStampedModel):
    name = models.CharField(max_length=100)
    position = models.PositiveIntegerField()

    company = models.ForeignKey(Company)

    class Meta:
        unique_together = ('company', 'position')
        ordering = ['position']

    def __unicode__(self):
        return self.name

    def get_previous_stage(self):
        previous_position = InterviewStage.objects.filter(
            company=self.company,
            position__lt=self.position
        ).aggregate(models.Max('position'))['position__max']

        previous = InterviewStage.objects.filter(
            company=self.company,
            position=previous_position
        )[0]

        return previous

    def get_next_stage(self):
        next_position = InterviewStage.objects.filter(
            company=self.company,
            position__gt=self.position
        ).aggregate(models.Min('position'))['position__min']

        next = InterviewStage.objects.filter(
            company=self.company,
            position=next_position
        )[0]

        return next

    def save(self, *args, **kwargs):
        if not self.pk:
            max_position = InterviewStage.objects.filter(
                company=self.company
            ).aggregate(models.Max('position'))['position__max']

            if not max_position:
                self.position = 1
            else:
                self.position = max_position + 1

        super(InterviewStage, self).save(*args, **kwargs)
