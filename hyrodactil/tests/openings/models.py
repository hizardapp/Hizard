from datetime import datetime

from django.test import TestCase

from ..factories._applications import ApplicationFactory
from ..factories._companies import CompanyFactory
from ..factories._companysettings import InterviewStageFactory
from ..factories._openings import OpeningFactory



class OpeningsModelsTests(TestCase):

    def test_applicants_stats(self):
        opening = OpeningFactory()
        self.assertEqual(opening.applicants_stats(), [])
        s1 = InterviewStageFactory(name="L220", company=opening.company)
        s2 = InterviewStageFactory(name="L33", company=opening.company)
        self.assertEqual(opening.applicants_stats(),
                [[s1.name, 0], [s2.name, 0]])

        application = ApplicationFactory.create(opening=opening)
        application.stage_transitions.create(stage=s1)
        self.assertEqual(opening.applicants_stats(),
                [[s1.name, 1], [s2.name, 0]])

    def test_get_apply_url(self):
        company = CompanyFactory(subdomain='acme')
        opening = OpeningFactory(company=company)
        self.assertEqual(
            'http://acme.hizard.com/1/apply/',
            opening.get_apply_url()
        )
