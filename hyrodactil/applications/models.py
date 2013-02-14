from django.db import models

from model_utils.models import TimeStampedModel

from companysettings.models import Question, InterviewStage
from jobs.models import Opening


class Application(TimeStampedModel):
    first_name = models.CharField(max_length=770)
    last_name = models.CharField(max_length=770)

    opening = models.ForeignKey(Opening)
    stage = models.ForeignKey(InterviewStage, blank=True, null=True)


class ApplicationAnswer(TimeStampedModel):
    answer = models.TextField(blank=True, null=True)

    question = models.ForeignKey(Question)
    application = models.ForeignKey(Application)

