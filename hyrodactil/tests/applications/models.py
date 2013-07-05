from django.test import TestCase

from ..factories._companysettings import InterviewStageFactory
from ..factories._applications import (
    ApplicationFactory, ApplicantFactory, ApplicationRatingFactory
)
from ..factories._applications import ApplicationStageTransitionFactory
from ..factories._accounts import UserFactory
from ..factories._companies import CompanyFactory


class ApplicationModelTests(TestCase):
    def test_get_full_name(self):
        bob = ApplicantFactory.build()
        self.assertEqual(bob.get_full_name(), 'Bilbon Sacquet')

    def test_get_rating(self):
        company = CompanyFactory()
        admin = UserFactory(company=company, is_company_admin=True)
        normal_user = UserFactory(email='b@b.com', company=company)
        bob_application = ApplicationFactory()

        bob_application.save_rating(admin, -1)
        bob_application.save_rating(normal_user, 1)

        self.assertEqual(bob_application.get_rating(), 0)

    def test_get_rating_without_rating(self):
        bob_application = ApplicationFactory()

        self.assertEqual(bob_application.get_rating(), 0)

    def test_save_rating_valid(self):
        company = CompanyFactory()
        user = UserFactory(company=company)
        bob_application = ApplicationFactory()

        result = bob_application.save_rating(user, -1)

        self.assertTrue(result)
        self.assertEqual(bob_application.get_rating(), -1)

    def test_save_rating_invalid(self):
        company = CompanyFactory()
        user = UserFactory(company=company)
        bob_application = ApplicationFactory()

        result = bob_application.save_rating(user, -1000)

        self.assertFalse(result)
        self.assertEqual(bob_application.get_rating(), 0)

    def test_save_rating_user_change(self):
        company = CompanyFactory()
        user = UserFactory(company=company)
        bob_application = ApplicationFactory()

        result = bob_application.save_rating(user, 1)
        self.assertTrue(result)

        result = bob_application.save_rating(user, 0)
        self.assertTrue(result)

        self.assertEqual(bob_application.get_rating(), 0)

    def test_get_user_rating(self):
        company = CompanyFactory()
        user = UserFactory(company=company)
        bob_application = ApplicationFactory()

        bob_application.save_rating(user, 1)

        self.assertEqual(bob_application.get_user_rating(user), 1)