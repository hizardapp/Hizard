from django.test import TestCase

from companies.forms import CompanyForm


class CompaniesFormsTest(TestCase):
    def test_company_form_valid(self):
        form_data = {'name': 'ACME', 'subdomain': 'acmebob'}
        form = CompanyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_company_form_invalid_name(self):
        form_data = {'name': '', 'subdomain': 'acmebob'}
        form = CompanyForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_company_form_invalid_subdomain(self):
        form_data = {'name': 'Bob Company Ltd', 'subdomain': 'google.acme.job'}
        form = CompanyForm(data=form_data)
        self.assertFalse(form.is_valid())
