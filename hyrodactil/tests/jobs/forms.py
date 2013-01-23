from django.test import TestCase

from tests.factories._companies import UserFactory, CompanyFactory, QuestionFactory

from jobs.forms import OpeningForm


class FormsTest(TestCase):
    def setUp(self):
        user = UserFactory()
        company = CompanyFactory(owner=user)
        QuestionFactory.create(company=company)
        QuestionFactory.create(company=company)

        self.form_data = {'title': 'Software Developer',
                          'description': 'Fait des logiciels.',
                          'is_private': '',
                          'loc_country': 'FR',
                          'loc_city': 'Cannes',
                          'loc_postcode': '93100',
                          'questions': [1, 2]}

        self.Form = OpeningForm

    def _remove_data(self, element):
        result = dict(self.form_data)
        if element == '':
            return result
        result[element] = ''
        return result

    def _form_is_valid_without(self, element_to_remove=''):
        form = self.Form(data=self._remove_data(element_to_remove))
        self.assertTrue(form.is_valid())

    def _form_is_invalid_without(self, element_to_remove):
        form = self.Form(data=self._remove_data(element_to_remove))
        self.assertFalse(form.is_valid())
        self.assertTrue(element_to_remove in form.errors)

    def test_valid_opening_form(self):
        self._form_is_valid_without()
        self._form_is_valid_without('loc_country')
        self._form_is_valid_without('loc_city')
        self._form_is_valid_without('loc_postcode')
        self._form_is_valid_without('questions')

    def test_invalid_opening_form(self):
        self._form_is_invalid_without('title')
        self._form_is_invalid_without('description')

    def test_invalid_opening_form_nonexisting_question(self):
        wrong_data = dict(self.form_data)
        wrong_data['questions'] = [1, 2, 3]
        form = self.Form(data=wrong_data)
        self.assertFalse(form.is_valid())
