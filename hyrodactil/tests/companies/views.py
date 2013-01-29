from django.core.urlresolvers import reverse
from django_webtest import WebTest

from tests.factories._accounts import UserFactory
from companies.models import Company


class ViewsWebTest(WebTest):
    def setUp(self):
        self.user = UserFactory.create()
        self.required = 'This field is required.'

    def test_get_company(self):
        url = reverse('companies:create')

        page = self.app.get(url, user=self.user)

        self.assertEqual(page.status_code, 200)
        self.assertIn('company-form', page.forms)

    def test_create_company_invalid(self):
        url = reverse('companies:create')

        page = self.app.get(url, user=self.user)
        form = page.forms['company-form']
        form['name'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_create_company_valid(self):
        url = reverse('companies:create')

        page = self.app.get(url, user=self.user)
        form = page.forms['company-form']
        form['name'] = 'ACME'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)

        company_created = Company.objects.get()

        self.assertEqual(company_created.owner, self.user)
        self.assertEqual(company_created.name, 'ACME')

