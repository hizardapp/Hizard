from django.test import TestCase

from ..factories._accounts import UserFactory
from openings.forms import OpeningForm
from openings.models import OpeningQuestion
from tests.factories._openings import OpeningWithQuestionFactory


class OpeningsFormsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.form_data = {'title': 'Software Developer',
                          'description': 'Fait des logiciels.',
                          'is_private': '',
                          'country': 'FR',
                          'city': 'Cannes',
                          'department': 'Vendeur de reve',
                          'employment_type': 'full_time'}

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
        self._form_is_valid_without('country')
        self._form_is_valid_without('city')

    def test_invalid_opening_form(self):
        self._form_is_invalid_without('title')
        self._form_is_invalid_without('description')

    def test_opening_form_clean_valid_question(self):
        data = self.form_data
        data.update({
            'question-1': 'What is your quest?',
            'position-question-1': '1'
        })
        form = self.Form(
            self.user.company,
            data=data
        )
        form._clean_questions()
        self.assertEqual(len(form.questions_present), 1)

        form.save()
        self.assertEqual(OpeningQuestion.objects.count(), 1)

    def test_opening_form_clean_empty_question(self):
        data = self.form_data
        data.update({
            'question-1': '',
            'position-question-1': '1'
        })
        form = self.Form(
            self.user.company,
            data=data
        )
        form._clean_questions()
        self.assertEqual(len(form.questions_present), 0)

        form.save()
        self.assertEqual(OpeningQuestion.objects.count(), 0)

    def test_opening_form_delete_question(self):
        opening = OpeningWithQuestionFactory()

        data = self.form_data
        data.update({
            'question-1': '',
            'position-question-1': '1'
        })
        form = self.Form(
            self.user.company,
            instance=opening,
            data=data
        )
        form._clean_questions()
        self.assertEqual(len(form.questions_present), 0)

        form.save()
        self.assertEqual(OpeningQuestion.objects.count(), 0)

    def test_opening_form_update_question(self):
        opening = OpeningWithQuestionFactory()

        data = self.form_data
        data.update({
            'question-1': 'What is your quest?',
            'position-question-1': '1'
        })
        form = self.Form(
            self.user.company,
            instance=opening,
            data=data
        )
        form._clean_questions()
        self.assertEqual(len(form.questions_present), 1)

        form.save()
        self.assertEqual(OpeningQuestion.objects.count(), 1)
