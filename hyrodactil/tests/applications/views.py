from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._applications import ApplicationFactory
from ..factories._companysettings import SingleLineQuestionFactory
from ..factories._jobs import OpeningFactory


class ApplicationViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.question = SingleLineQuestionFactory(company=self.user.company)

    def test_listing_applicants(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)

        url = reverse('applications:list_applications', args=(opening.id,))

        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.first_name)
        self.assertContains(response, application.last_name)

    def test_listing_all_applicants(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)

        url = reverse('applications:list_all_applications')

        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.first_name)
        self.assertContains(response, application.last_name)

    def test_get_applicant_details(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)
        #answer = ApplicationAnswerFactory.create(application=application)

        url = reverse('applications:application_detail', args=(application.id,))
        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.first_name)

    def test_get_applicant_details_different_company(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)
        rival = UserFactory.create(email='red@red.com')

        url = reverse('applications:application_detail', args=(application.id,))

        self.client.login(username='red@red.com', password='bob')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
