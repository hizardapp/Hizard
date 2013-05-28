from django.test import TestCase

from ..factories._accounts import UserFactory
from ..factories._companies import CompanyFactory
from ..factories._openings import OpeningFactory, OpeningQuestionFactory
from ..factories._companysettings import (
    SingleLineQuestionFactory, MultiLineQuestionFactory, DepartmentFactory
)
from companysettings.models import Department
from openings.forms import OpeningForm, OpeningQuestionFormset
from openings.models import OpeningQuestion


class OpeningsFormsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.first_question = SingleLineQuestionFactory(
            company=self.user.company
        )
        SingleLineQuestionFactory(company=self.user.company)

        self.form_data = {'title': 'Software Developer',
                          'description': 'Fait des logiciels.',
                          'is_private': '',
                          'country': 'FR',
                          'city': 'Cannes',
                          'employment_type': 'full_time',
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
        self._form_is_valid_without('country')
        self._form_is_valid_without('city')
        self._form_is_valid_without('questions')

    def test_invalid_opening_form(self):
        self._form_is_invalid_without('title')
        self._form_is_invalid_without('description')

    def test_opening_form_create_new_department(self):
        new_dept_data = dict(self.form_data)
        new_dept_data['new_department'] = "HR"
        form = self.Form(self.user.company, data=new_dept_data)
        self.assertTrue(form.is_valid())
        opening = form.save()
        self.assertTrue(Department.objects.filter(name="HR").exists())
        self.assertTrue(opening.department)
        self.assertEqual(opening.department.name, "HR")
        self.assertEqual(opening.department.company, self.user.company)

    def test_opening_form_only_list_company_department(self):
        form = self.Form(self.user.company)
        capcom = DepartmentFactory.create(
            company=self.user.company,
            name="CAPCOM"
        )
        control = DepartmentFactory.create(
            company=CompanyFactory(),
            name="CONTROL"
        )

        def just_pks(choices):
            return (pk for pk, choice in choices)
        pks = just_pks(form.fields["department"].choices)
        self.assertTrue(capcom.pk in pks)
        self.assertTrue(control.pk not in pks)

    def test_opening_form_save_opening_questions(self):
        data = dict(self.form_data)

        data.update(
            {
                'oq-2-included': True,
                'oq-2-required': True,
            }
        )

        form = self.Form(self.user.company, data=data)
        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(1, OpeningQuestion.objects.count())

    def test_opening_update_related_questions(self):
        opening = OpeningFactory(company=self.user.company)
        OpeningQuestionFactory(question=self.first_question, opening=opening)
        form = self.Form(self.user.company, instance=opening)
        self.assertEqual(
            form.opening_questions.forms[0].initial,
            {'included': True, 'required': False}
        )


class OpeningQuestionFormsetTests(TestCase):

    def setUp(self):
        self.company = CompanyFactory()
        self.question1 = SingleLineQuestionFactory(company=self.company)
        self.question2 = MultiLineQuestionFactory(company=self.company)

    def test_initialize_with_company(self):
        formset = OpeningQuestionFormset(company=self.company)

        self.assertEqual(
            len(formset.questions), self.company.question_set.count()
        )
        self.assertEqual(len(formset.forms), self.company.question_set.count())

        self.assertEqual(formset.forms[0].prefix, 'oq-1')
        self.assertEqual(formset.forms[1].prefix, 'oq-2')

    def test_iterate_opening_question_formset(self):
        formset = OpeningQuestionFormset(company=self.company)

        self.assertEqual(2, len(list(formset)))

    def test_save_invalid_opening_questions(self):
        data = {
            'oq-2-required': True,
        }

        formset = OpeningQuestionFormset(company=self.company, data=data)

        self.assertFalse(formset.is_valid())
        self.assertEqual(1, len(formset.forms[1].errors))

    def test_empty_is_valid(self):
        formset = OpeningQuestionFormset(company=self.company, data={})

        self.assertTrue(formset.is_valid())

    def test_save_opening_questions(self):
        data = {
            'oq-2-included': True,
            'oq-2-required': True,
        }
        opening = OpeningFactory(company=self.company)
        formset = OpeningQuestionFormset(company=self.company, data=data)
        formset.is_valid()
        formset.save(opening)

        self.assertEqual(1, OpeningQuestion.objects.count())

    def test_initialize_with_opening(self):
        opening = OpeningFactory(company=self.company)
        OpeningQuestionFactory(opening=opening, question=self.question1)

        formset = OpeningQuestionFormset(company=self.company, opening=opening)

        self.assertEqual(len(formset.forms), self.company.question_set.count())

        self.assertEqual(formset.forms[0].initial, {'included': True,
                                                    'required': False})
        self.assertEqual(formset.forms[1].initial, {})

        self.assertEqual(
            formset.forms[1].fields['required'].widget.attrs['disabled'],
            'disabled'
        )

    def test_update_opening_questions(self):
        data = {
            'oq-1-included': True,
            'oq-1-required': True,
        }
        opening = OpeningFactory(company=self.company)
        OpeningQuestionFactory(opening=opening, question=self.question1)

        formset = OpeningQuestionFormset(
            company=self.company, opening=opening, data=data
        )
        formset.is_valid()
        formset.save(opening)

        self.assertEqual(1, OpeningQuestion.objects.count())
        self.assertEqual(True, OpeningQuestion.objects.get().required)
