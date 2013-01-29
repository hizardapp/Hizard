from django.test import TestCase

from companies.forms import CompanyForm


class FormsTest(TestCase):
    def test_company_form_valid(self):
        form_data = {'name': 'ACME'}
        form = CompanyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_company_form_invalid(self):
        form_data = {'name': ''}
        form = CompanyForm(data=form_data)
        self.assertFalse(form.is_valid())
