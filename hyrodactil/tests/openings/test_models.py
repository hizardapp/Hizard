from datetime import datetime

from django.test import TestCase
from applications.models import Application

from ..factories._applications import ApplicationFactory
from ..factories._companies import CompanyFactory
from ..factories._openings import OpeningFactory, OpeningWithQuestionFactory
from ..factories._openings import OpeningQuestionFactory
from ..factories._companysettings import InterviewStageFactory


class OpeningsModelsTests(TestCase):

    def test_get_apply_url(self):
        company = CompanyFactory(subdomain='acme')
        opening = OpeningFactory(company=company)
        self.assertEqual(
            'http://acme.hizard.com/1/apply/',
            opening.get_apply_url()
        )

    def test_get_location_string(self):
        opening = OpeningFactory.build()
        self.assertEqual(opening.get_location_string(), 'Cannes, France')

        opening.city = ''
        self.assertEqual(opening.get_location_string(), 'France')

        opening.city = 'Cannes'
        opening.country = None
        self.assertEqual(opening.get_location_string(), 'Cannes')

    def test_get_status(self):
        opening = OpeningFactory.build()
        self.assertEqual(unicode(opening.get_status()), 'Created')

        opening.is_private = True
        self.assertEqual(unicode(opening.get_status()), 'Private')
        opening.is_private = False

        opening.published_date = datetime.now()
        self.assertEqual(unicode(opening.get_status()), 'Published')

    def test_get_unicode_opening_and_quesionts(self):
        question = OpeningQuestionFactory(title="WPM",
           opening__title="CEO")
        self.assertEqual(unicode(question), u"WPM")
        self.assertEqual(unicode(question.opening), u"CEO")

    def test_question_deletion_keeps_applications(self):
        opening = OpeningWithQuestionFactory()
        ApplicationFactory(opening=opening)
        opening.questions.all().delete()
        self.assertEqual(Application.objects.count(), 1)

    def test_get_stage_counts(self):
        opening = OpeningWithQuestionFactory()
        stage1 = InterviewStageFactory(company=opening.company)
        InterviewStageFactory(company=opening.company)
        application = ApplicationFactory(opening=opening)
        application.current_stage = stage1
        application.save()

        self.assertEqual([1, 0], list(opening.stage_counts()))
