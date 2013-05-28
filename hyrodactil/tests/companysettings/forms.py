from django.test import TestCase

from companysettings.forms import (
    DepartmentForm, QuestionForm, InterviewStageForm,
    CompanyInformationForm)
from ..factories._companies import CompanyFactory


class CompanySettingsFormsTests(TestCase):
    def test_department_form_valid(self):
        form_data = {'name': 'Engineering'}
        form = DepartmentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_department_form_invalid(self):
        form_data = {'name': ''}
        form = DepartmentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_question_form_valid(self):
        form_data = {'name': 'cover', 'type': 'checkbox'}
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_question_form_invalid(self):
        form_data = {'name': '', 'type': 'checkbox'}
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_stage_form_valid(self):
        company = CompanyFactory()
        form_data = {'name': 'Phone interview'}
        form = InterviewStageForm(data=form_data, **{'company': company})
        self.assertTrue(form.is_valid())

    def test_stage_form_invalid(self):
        company = CompanyFactory()
        form_data = {'name': ''}
        form = InterviewStageForm(data=form_data, **{'company': company})
        self.assertFalse(form.is_valid())

    def test_company_information_valid(self):
        form_data = {
            'website': 'www.google.com',
            'description': 'We do some cool stuff'
        }
        form = CompanyInformationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_company_information_invalid(self):
        form_data = {
            'website': 'www.goog',
            'description': 'We do some cool stuff'
        }
        form = CompanyInformationForm(data=form_data)
        self.assertTrue(form.is_valid())
