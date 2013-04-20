from django.core.urlresolvers import reverse
from django.conf import settings
from django_webtest import WebTest

from tests.factories._accounts import UserFactory
from companies.models import Company


class CompaniesViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory.create(company=None)
        self.required = 'This field is required.'

    def test_get_company(self):
        url = reverse('companies:create')

        page = self.app.get(url, user=self.user)

        self.assertEqual(page.status_code, 200)
        self.assertIn('action-form', page.forms)

    def test_post_create_company_invalid(self):
        url = reverse('companies:create')

        page = self.app.get(url, user=self.user)
        form = page.forms['action-form']
        form['name'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_post_create_company_valid(self):
        url = reverse('companies:create')

        page = self.app.get(url, user=self.user)
        form = page.forms['action-form']
        form['name'] = 'ACME'
        form['subdomain'] = 'acmememe'
        response = form.submit()
        expected = "http://acmememe.%s%s" % (
            settings.SITE_URL, reverse("dashboard:dashboard")
        )
        self.assertEqual(response["Location"], expected)
        self.assertEqual(response.status_code, 302)

        response = response.follow()

        company_created = Company.objects.get()

        self.assertEqual(company_created.employees.all()[0], self.user)
        self.assertEqual(company_created.name, 'ACME')

        self.assertTrue(len(company_created.question_set.all()) > 0)
        self.assertTrue(len(company_created.interviewstage_set.all()) > 0)
