from django_webtest import WebTest

from ..factories._companies import CompanyFactory
from accounts.models import CustomUser
from companies.models import Company
from companysettings.models import InterviewStage
from core import utils
from customisable_emails.models import EmailTemplate
from openings.models import Opening


class SetupCompanyTests(WebTest):
    """
    Test what happens when a company is created.
    Here, it should add some default question and stages in the database
    """

    def test_should_add_default_data(self):
        company = CompanyFactory()

        utils.setup_company(company)

        # Not asserting exact number since it can vary if we want to add some
        self.assertTrue(
            InterviewStage.objects.filter(company=company).exists()
        )
        self.assertTrue(
            InterviewStage.objects.filter(company=company, tag="RECEIVED").exists()
        )
        self.assertTrue(
            InterviewStage.objects.filter(company=company, tag="HIRED").exists()
        )
        self.assertTrue(
            InterviewStage.objects.filter(company=company, tag="REJECTED").exists()
        )
        self.assertTrue(Opening.objects.filter(company=company).exists())
        self.assertEqual(EmailTemplate.objects.all().count(), 3)


class SetupDemoAccountTest(WebTest):
    def test_add_demo_account(self):
        demo_user = utils.create_demo_account()
        self.assertTrue(demo_user.check_password("demo"))
        self.assertTrue(demo_user.company)
        self.assertEqual(EmailTemplate.objects.filter(
          company=demo_user.company).count(), 3)

    def test_reset_existing_demo_account(self):
        demo_user = utils.create_demo_account()
        # add documents


        utils.delete_demo_company()
        self.assertFalse(CustomUser.objects.filter(pk=demo_user.pk))
        self.assertFalse(Company.objects.filter(pk=demo_user.company.pk))
        self.assertEqual(EmailTemplate.objects.all().count(), 0)
