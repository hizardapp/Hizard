from django.core.urlresolvers import reverse
from django_webtest import WebTest

from tests.factories._accounts import UserFactory
from tests.factories._companies import CompanyFactory
from tests.factories._companysettings import DepartmentFactory, QuestionFactory
from companysettings.models import Department, Question

class ViewsWebTest(WebTest):
    def setUp(self):
        self.user = UserFactory.create()
        self.required = 'This field is required.'

    def test_list_departments(self):
        url = reverse('companysettings:list_departments')

        department = DepartmentFactory.create(company=self.user.company)
        user2 = UserFactory(email='sam@sam.com')
        department2 = DepartmentFactory.create(name='Corp', company=user2.company)

        page = self.app.get(url, user=self.user)

        assert department.name in page
        assert department2.name not in page
        assert 'Create a department' in page

    def test_create_department_valid(self):
        url = reverse('companysettings:create_department')

        page = self.app.get(url, user=self.user)
        form = page.forms['department-form']
        form['name'] = 'Engineering'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        department_created = Department.objects.get()

        self.assertEqual(department_created.company, self.user.company)
        self.assertEqual(department_created.name, 'Engineering')

    def test_create_department_invalid(self):
        url = reverse('companysettings:create_department')

        page = self.app.get(url, user=self.user)
        form = page.forms['department-form']
        form['name'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_update_department_valid(self):
        dept = DepartmentFactory.create(name='Sales', company=self.user.company)
        url = reverse('companysettings:update_department', args=(dept.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['department-form']
        form['name'] = 'Engineering'

        assert dept.name in page

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        assert 'Engineering' in response
        assert 'Sales' not in response

    def test_update_department_invalid(self):
        dept = DepartmentFactory.create(name='Sales', company=self.user.company)
        url = reverse('companysettings:update_department', args=(dept.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['department-form']
        form['name'] = ''

        assert dept.name in page

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_list_questions(self):
        url = reverse('companysettings:list_questions')

        question = QuestionFactory.create(company=self.user.company)
        user2 = UserFactory(email='sam@sam.com')
        question2 = QuestionFactory.create(name='Age', company=user2.company)

        page = self.app.get(url, user=self.user)

        assert question.name in page
        assert question2.name not in page
        assert 'Create a question' in page

    def test_create_question_valid(self):
        url = reverse('companysettings:create_question')

        page = self.app.get(url, user=self.user)
        form = page.forms['question-form']
        form['name'] = 'Cover letter'
        form['label'] = 'Please write a cover letter : '
        form['type'] = 'textbox'

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        question_created = Question.objects.get()

        self.assertEqual(question_created.company, self.user.company)
        self.assertEqual(question_created.name, 'Cover letter')

    def test_create_question_invalid(self):
        url = reverse('companysettings:create_question')

        page = self.app.get(url, user=self.user)
        form = page.forms['question-form']
        form['name'] = ''
        form['label'] = ''
        form['type'] = 'textbox'
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)
        self.assertFormError(response, 'form', 'label', self.required)

    def test_update_question_valid(self):
        question = QuestionFactory.create(company=self.user.company)
        url = reverse('companysettings:update_question', args=(question.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['question-form']
        form['name'] = 'Last Name'

        assert question.name in page
        assert question.label in page

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        assert 'Last Name' in response
        assert 'First Name' not in response

    def test_update_question_invalid(self):
        question = QuestionFactory.create(company=self.user.company)
        url = reverse('companysettings:update_question', args=(question.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['question-form']
        form['name'] = ''

        assert question.name in page
        assert question.label in page

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)
