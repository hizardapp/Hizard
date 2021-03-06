from django.core.urlresolvers import reverse
from django_webtest import WebTest

from tests.factories._accounts import UserFactory
from companies.models import Company
from tests.utils import subdomain_get


class CompaniesViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory.create(company=None)
        self.required = 'This field is required.'

    def test_get_company(self):
        url = reverse('companies:create')

        page = subdomain_get(self.app, url, user=self.user)

        self.assertEqual(page.status_code, 200)
        self.assertIn(0, page.forms)

    def test_get_company_with_already_a_company(self):
        """Should be redirect to dashboard"""
        user = UserFactory(email="mac@gyver.com")
        url = reverse('companies:create')

        page = subdomain_get(self.app, url, user=user)

        self.assertTemplateUsed(page, 'dashboard/dashboard.html')

    def test_post_create_company_invalid(self):
        url = reverse('companies:create')

        page = subdomain_get(self.app, url, user=self.user)
        form = page.forms[0]
        form['name'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_post_create_company_valid(self):
        url = reverse('companies:create')

        page = subdomain_get(self.app, url, user=self.user)
        form = page.forms[0]
        form['name'] = 'ACME'
        form['subdomain'] = 'acmememe'
        form['website'] = 'acmememe.com'
        form['description'] = 'Tidadou'
        response = form.submit()
        self.assertTrue(reverse("dashboard:dashboard") in response["Location"])
        self.assertEqual(response.status_code, 302)

        response = response.follow()

        company_created = Company.objects.get()

        self.assertEqual(company_created.employees.all()[0], self.user)
        self.assertEqual(company_created.name, 'ACME')

        self.assertTrue(len(company_created.interviewstage_set.all()) > 0)
