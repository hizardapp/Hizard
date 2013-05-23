from django.test import TestCase

from ..factories._companysettings import InterviewStageFactory
from ..factories._applications import ApplicationFactory
from ..factories._applications import ApplicationStageTransitionFactory


class ApplicationModelTests(TestCase):
    def test_application_has_current_stage(self):
        s1 = InterviewStageFactory.create(name="1D")
        s2 = InterviewStageFactory.create(name="Vacuum")
        application = ApplicationFactory()
        self.assertFalse(application.current_stage)

        ApplicationStageTransitionFactory.create(application=application,
                stage=s1)
        self.assertEqual(application.current_stage, s1)

        ApplicationStageTransitionFactory.create(application=application,
                stage=s2)
        self.assertEqual(application.current_stage, s2)
