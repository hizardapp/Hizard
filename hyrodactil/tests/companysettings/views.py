from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._companysettings import (
    DepartmentFactory, QuestionFactory, InterviewStageFactory
)
from companysettings.models import Department, Question, InterviewStage

class CompanySettingsViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory.create()
        self.required = 'This field is required.'

    def test_list_departments(self):
        url = reverse('companysettings:list_departments')

        department = DepartmentFactory.create(company=self.user.company)
        page = self.app.get(url, user=self.user)

        self.assertContains(page, department.name)

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

        self.assertContains(page, dept.name)

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engineering')
        self.assertNotContains(response, 'Sales')

    def test_update_department_invalid(self):
        dept = DepartmentFactory.create(name='Sales', company=self.user.company)
        url = reverse('companysettings:update_department', args=(dept.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['department-form']
        form['name'] = ''

        self.assertContains(page, dept.name)

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_list_questions(self):
        url = reverse('companysettings:list_questions')

        question = QuestionFactory.create(company=self.user.company)

        page = self.app.get(url, user=self.user)

        self.assertContains(page, question.name)

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

        self.assertContains(page, question.name)
        self.assertContains(page, question.label)

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Last Name')
        self.assertNotContains(response, 'First Name')

    def test_update_question_invalid(self):
        question = QuestionFactory.create(company=self.user.company)
        url = reverse('companysettings:update_question', args=(question.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['question-form']
        form['name'] = ''

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

        def setUp(self):
            self.user = UserFactory.create()
        self.required = 'This field is required.'

    def test_list_stages(self):
        url = reverse('companysettings:list_stages')

        stage = InterviewStageFactory.create(company=self.user.company)
        page = self.app.get(url, user=self.user)

        self.assertContains(page, stage.name)

    def test_create_stage_valid(self):
        url = reverse('companysettings:create_stage')

        page = self.app.get(url, user=self.user)
        form = page.forms['stage-form']
        form['name'] = 'Phone interview'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        stage_created = InterviewStage.objects.get()

        self.assertEqual(stage_created.company, self.user.company)
        self.assertEqual(stage_created.name, 'Phone interview')

    def test_create_stage_invalid(self):
        url = reverse('companysettings:create_stage')

        page = self.app.get(url, user=self.user)
        form = page.forms['stage-form']
        form['name'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_update_stage_valid(self):
        stage = InterviewStageFactory.create(name='Phone', company=self.user.company)
        url = reverse('companysettings:update_stage', args=(stage.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['stage-form']
        form['name'] = 'Coding'

        self.assertContains(page, stage.name)

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Coding')
        self.assertNotContains(response, stage.name)

    def test_update_stage_invalid(self):
        stage = InterviewStageFactory.create(name='Phone', company=self.user.company)
        url = reverse('companysettings:update_stage', args=(stage.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['stage-form']
        form['name'] = ''

        self.assertContains(page, stage.name)

        response = form.submit()

        self.assertEqual(response.status_code, 200)
