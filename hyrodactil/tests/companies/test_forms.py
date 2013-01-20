from django.test import TestCase

from companies.forms import CompanyForm, DepartmentForm, QuestionForm


class FormsTest(TestCase):
    def test_company_form_valid(self):
        form_data = {'name': 'ACME'}
        form = CompanyForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_company_form_invalid(self):
        form_data = {'name': ''}
        form = CompanyForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_department_form_valid(self):
        form_data = {'name': 'Engineering'}
        form = DepartmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_department_form_invalid(self):
        form_data = {'name': ''}
        form = DepartmentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_question_form_valid(self):
        form_data = {'name': 'cover', 'label': 'cover', 'type': 'checkbox'}
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_question_form_invalid(self):
        form_data = {'name': 'cover', 'label': '', 'type': 'checkbox'}
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'name': '', 'label': 'cover', 'type': 'checkbox'}
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())
