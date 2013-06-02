from django.db import models
from model_utils.models import TimeStampedModel


class Interest(TimeStampedModel):
    email = models.EmailField()
