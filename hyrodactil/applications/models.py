from django.db import models

from model_utils.models import TimeStampedModel

from accounts.models import CustomUser
from companysettings.models import Question, InterviewStage
from jobs.models import Opening


class Applicant(TimeStampedModel):
    first_name = models.CharField(max_length=770)
    last_name = models.CharField(max_length=770)
    email = models.EmailField(max_length=254)


class Application(TimeStampedModel):
    applicant = models.ForeignKey(Applicant)
    opening = models.ForeignKey(Opening)


class ApplicationStageTransition(TimeStampedModel):
    application = models.ForeignKey(Application, related_name="stage_transitions")
    user = models.ForeignKey(CustomUser)
    stage = models.ForeignKey(InterviewStage)

    class Meta:
        ordering = "created",


class ApplicationAnswer(TimeStampedModel):
    answer = models.TextField(blank=True, null=True)

    question = models.ForeignKey(Question)
    application = models.ForeignKey(Application)
