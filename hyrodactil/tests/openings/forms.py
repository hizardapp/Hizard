from django.test import TestCase

from ..factories._accounts import UserFactory
from ..factories._companies import CompanyFactory
from ..factories._companysettings import SingleLineQuestionFactory
from companysettings.models import Department
from openings.forms import OpeningForm


class OpeningsFormsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.first_question = SingleLineQuestionFactory.create(company=self.user.company)
        SingleLineQuestionFactory.create(company=self.user.company)

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
        form = self.Form(self.user.company,
                         data=self._remove_data(element_to_remove))
        self.assertTrue(form.is_valid())

    def _form_is_invalid_without(self, element_to_remove):
        form = self.Form(self.user.company,
                         data=self._remove_data(element_to_remove))
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
        form = self.Form(self.user.company, data=wrong_data)
        self.assertFalse(form.is_valid())

    def test_opening_form_only_contains_questions_from_same_company(self):
        other_company_question = SingleLineQuestionFactory.create(
            name='Your 5 strenghts and weaknesses',
            company=CompanyFactory())
        form = self.Form(self.user.company, self.user.company)
        questions_qs = form.fields["questions"].queryset
        self.assertFalse(other_company_question in questions_qs)
        self.assertTrue(self.first_question in questions_qs)

    def test_opening_form_create_new_department(self):
        new_dept_data = dict(self.form_data)
        new_dept_data['new_department'] = "HR"
        form = self.Form(self.user.company, data=new_dept_data)
        self.assertTrue(form.is_valid())
        opening = form.save()
        self.assertTrue(Department.objects.filter(name="HR").exists())
        self.assertTrue(opening.department)
        self.assertEqual(opening.department.name, "HR")
