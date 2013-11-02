from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

from accounts.models import CustomUser
from companysettings.models import InterviewStage
from openings.models import Opening, OpeningQuestion


class Applicant(TimeStampedModel):
    first_name = models.CharField(max_length=770)
    last_name = models.CharField(max_length=770)
    # 254 is the max length of an email
    email = models.EmailField(max_length=254)
    resume = models.FileField(
        upload_to="tmp_resumes",
        help_text=_('PDF/doc files only')
    )

    ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx']
    ALLOWED_CONTENT_TYPES = ['application/pdf',
        'application/msword',
        'application/vnd.oasis.opendocument.text']

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
        return self.get_full_name()


class Application(TimeStampedModel):
    applicant = models.ForeignKey(Applicant)
    opening = models.ForeignKey(Opening)
    current_stage = models.ForeignKey(InterviewStage, null=True)

    def get_rating(self):
        ratings = ApplicationRating.objects.filter(
            application=self
        ).select_related('CustomUser')

        rating = 0

        for user_rating in ratings:
            rating += user_rating.rating

        return rating

    def save_rating(self, user, rating):
        int_rating = int(rating)

        if int_rating not in [-1, 0, 1]:
            return False

        rating_obj = ApplicationRating.objects.filter(
            application=self,
            user=user
        ).select_related('CustomUser')

        if rating_obj:
            rating_obj = rating_obj[0]
            if rating_obj.rating == int_rating:
                return True
            rating_obj.rating = int_rating
            rating_obj.save()
            return True

        ApplicationRating.objects.create(
            application=self,
            user=user,
            rating=int_rating
        ).save()

        return True

    def get_user_rating(self, user):
        rating_obj = ApplicationRating.objects.filter(
            application=self,
            user=user
        ).select_related('CustomUser')

        if rating_obj:
            return rating_obj[0].rating

        return 0

    def __unicode__(self):
        return self.applicant.get_full_name()


class ApplicationAnswer(TimeStampedModel):
    application = models.ForeignKey(Application, related_name='answers')
    question = models.ForeignKey(OpeningQuestion)

    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Answer to: %s' % self.question.title

class ApplicationStageTransition(TimeStampedModel):
    application = models.ForeignKey(
        Application, related_name='stage_transitions'
    )
    user = models.ForeignKey(CustomUser, null=True)
    stage = models.ForeignKey(InterviewStage)

    class Meta:
        ordering = '-created',

    def __str__(self):
        return "%s %s %s" % (self.application, self.user, self.stage)


class ApplicationMessage(TimeStampedModel):
    application = models.ForeignKey(Application)
    user = models.ForeignKey(CustomUser)
    parent = models.ForeignKey('ApplicationMessage', null=True, blank=True)

    body = models.TextField()

    class Meta:
        ordering = ('-created',)


class ApplicationRating(TimeStampedModel):
    application = models.ForeignKey(Application)
    user = models.ForeignKey(CustomUser)
    rating = models.IntegerField(default=0)
