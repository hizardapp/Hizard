from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

from accounts.models import CustomUser
from companysettings.models import Question, InterviewStage
from openings.models import Opening


class Applicant(TimeStampedModel):
    first_name = models.CharField(max_length=770)
    last_name = models.CharField(max_length=770)
    # 254 is the max length of an email
    email = models.EmailField(max_length=254)
    resume = models.FileField(
        upload_to='resumes',
        help_text=_("PDF files only")
    )


class Application(TimeStampedModel):
    applicant = models.ForeignKey(Applicant)
    opening = models.ForeignKey(Opening)

    rating = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(default=0)

    current_stage = models.ForeignKey(InterviewStage, null=True)

    def update_current_stage(self, commit=True):
        transitions = ApplicationStageTransition.objects.filter(
                application=self)
        if transitions:
            last_transistion = transitions[0]
            if last_transistion.stage != self.current_stage:
                self.current_stage = last_transistion.stage
                if commit:
                    self.save()

    def save(self, *args, **kwargs):
        self.update_current_stage(commit=False)
        return super(Application, self).save(*args, **kwargs)

    class Meta:
        ordering = 'position',


class ApplicationStageTransition(TimeStampedModel):
    application = models.ForeignKey(Application, related_name="stage_transitions")
    user = models.ForeignKey(CustomUser, null=True)
    stage = models.ForeignKey(InterviewStage)
    note = models.TextField(blank=True)

    class Meta:
        ordering = "-created",

    def save(self, *args, **kwargs):
        result = super(ApplicationStageTransition, self).save(*args, **kwargs)
        self.application.update_current_stage()
        return result

    def __str__(self):
        return "%s %s %s" % (self.application, self.user, self.stage)

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
