from django.db import models

from accounts.models import CustomUser
from companies.models import Company

from model_utils.models import TimeStampedModel


class EmailTemplate(TimeStampedModel):
    code = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    company = models.ForeignKey(Company)

    subject = models.CharField(max_length=512)
    body = models.TextField()
    last_edited_by = models.ForeignKey(CustomUser, null=True, blank=True)
