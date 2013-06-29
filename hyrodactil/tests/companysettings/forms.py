from django.test import TestCase

from companysettings.forms import (
    QuestionForm, InterviewStageForm, CompanyInformationForm
)


class CompanySettingsFormsTests(TestCase):
    def test_question_form_valid(self):
        form_data = {'name': 'cover', 'type_field': 'checkbox'}
        form = QuestionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_question_form_invalid(self):
        form_data = {'name': '', 'type_field': 'checkbox'}
        form = QuestionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_stage_form_valid(self):
        form_data = {'name': 'Phone interview'}
        form = InterviewStageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_stage_form_invalid(self):
        form_data = {'name': ''}
        form = InterviewStageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_company_information_valid(self):
        form_data = {
            'name': 'Google Inc',
            'website': 'www.google.com',
            'description': 'We do some cool stuff'
        }
        form = CompanyInformationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_company_information_invalid(self):
        form_data = {
            'name': 'Google Inc',
            'website': 'www.goog',
            'description': 'We do some cool stuff'
        }
        form = CompanyInformationForm(data=form_data)
        self.assertTrue(form.is_valid())
