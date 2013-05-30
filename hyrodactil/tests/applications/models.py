from django.test import TestCase

from ..factories._companysettings import InterviewStageFactory
from ..factories._applications import (
    ApplicationFactory, ApplicantFactory, ApplicationRatingFactory
)
from ..factories._applications import ApplicationStageTransitionFactory
from ..factories._accounts import UserFactory
from ..factories._companies import CompanyFactory


class ApplicationModelTests(TestCase):
    def test_application_has_current_stage(self):
        s1 = InterviewStageFactory.create(name="1D")
        s2 = InterviewStageFactory.create(name="Vacuum")
        application = ApplicationFactory()
        self.assertFalse(application.current_stage)

        ApplicationStageTransitionFactory.create(
            application=application,
            stage=s1
        )
        self.assertEqual(application.current_stage, s1)

        ApplicationStageTransitionFactory.create(
            application=application,
            stage=s2
        )
        self.assertEqual(application.current_stage, s2)

    def test_get_full_name(self):
        bob = ApplicantFactory.build()
        self.assertEqual(bob.get_full_name(), 'Bilbon Sacquet')

    def test_rating(self):
        company = CompanyFactory()
        admin = UserFactory(company=company, is_company_admin=True)
        normal_user = UserFactory(email='b@b.com', company=company)
        bob_application = ApplicationFactory()

        ApplicationRatingFactory(
            user=admin,
            application=bob_application,
            rating=6
        )

        ApplicationRatingFactory(
            user=normal_user,
            application=bob_application,
            rating=9
        )

        self.assertEqual(bob_application.get_rating(), 7)
