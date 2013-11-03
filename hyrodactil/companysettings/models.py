
from django.db import models

from model_utils.models import TimeStampedModel
from companies.models import Company


class InterviewStage(TimeStampedModel):
    name = models.CharField(max_length=100)
    position = models.IntegerField(null=True)
    tag = models.CharField(blank=True, max_length=15)

    company = models.ForeignKey(Company, null=True)

    class Meta:
        ordering = ['position']

    def __unicode__(self):
        return self.name

    def change_position(self, delta):
        delta = int(delta)
        if self.position == 1 and delta == -1:
            return

        try:
            other_stage = InterviewStage.objects.get(
                company=self.company,
                position=self.position + delta
            )
        except InterviewStage.DoesNotExist:
            # Should not happen
            return

        other_stage.position = self.position
        other_stage.save()
        self.position = self.position + delta
        self.save()

    def prepare_for_deletion(self):
        stages_to_modify = InterviewStage.objects.filter(
            company=self.company, position__gt=self.position
        )

        for stage in stages_to_modify:
            stage.position -= 1
            stage.save()
