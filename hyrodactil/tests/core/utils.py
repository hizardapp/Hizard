from django_webtest import WebTest

from ..factories._companies import CompanyFactory
from companysettings.models import Question, InterviewStage
from openings.models import Opening
from core import utils


class SetupCompanyTests(WebTest):
    """
    Test what happens when a company is created.
    Here, it should add some default question and stages in the database
    """

    def test_should_add_default_data(self):
        company = CompanyFactory()

        utils.setup_company(company)

        # Not asserting exact number since it can vary if we want to add some
        self.assertTrue(Question.objects.filter(company=company).exists())
        self.assertTrue(InterviewStage.objects.filter(company=company).exists())
        self.assertTrue(Opening.objects.filter(company=company).exists())
