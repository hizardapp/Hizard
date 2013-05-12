from datetime import datetime

from django.test import TestCase

from ..factories._applications import ApplicationFactory
from ..factories._companysettings import InterviewStageFactory
from ..factories._openings import OpeningFactory

from openings.models import Opening


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
