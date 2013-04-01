from django.db import models

from model_utils.models import TimeStampedModel

from accounts.models import CustomUser
from companysettings.models import Question, InterviewStage
from openings.models import Opening


class Applicant(TimeStampedModel):
    first_name = models.CharField(max_length=770)
    last_name = models.CharField(max_length=770)
    # 254 is the max length of an email
    email = models.EmailField(max_length=254)
    resume = models.FileField(upload_to='resumes')


class Application(TimeStampedModel):
    applicant = models.ForeignKey(Applicant)
    opening = models.ForeignKey(Opening)

    rating = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(default=0)

    class Meta:
        ordering = 'position',

    def current_stage(self):
        transitions = self.stage_transitions.all()
        if transitions:
            return transitions[0].stage


class ApplicationStageTransition(TimeStampedModel):
    application = models.ForeignKey(Application, related_name="stage_transitions")
    user = models.ForeignKey(CustomUser)
    stage = models.ForeignKey(InterviewStage)
    note = models.TextField(blank=True)

    class Meta:
        ordering = "-created",


class ApplicationAnswer(TimeStampedModel):
    answer = models.TextField(blank=True, null=True)

    question = models.ForeignKey(Question)
    application = models.ForeignKey(Application)


class ApplicationMessage(TimeStampedModel):
    application = models.ForeignKey(Application)
    user = models.ForeignKey(CustomUser)
    parent = models.ForeignKey('ApplicationMessage', null=True, blank=True)

    body = models.TextField()

    class Meta:
        ordering = ('-created',)
