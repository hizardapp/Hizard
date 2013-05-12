from django.core.urlresolvers import reverse
from django.core import mail
from django_webtest import WebTest
from companies.models import Company

from ..factories._accounts import UserFactory
from ..factories._companysettings import (
    DepartmentFactory, SingleLineQuestionFactory, InterviewStageFactory
)
from companysettings.models import Department, Question, InterviewStage
from accounts.models import CustomUser


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
        url = reverse('companysettings:list_departments')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]
        form.action = reverse('companysettings:create_department')
        form['name'] = 'Engineering'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        department_created = Department.objects.get()

        self.assertEqual(department_created.company, self.user.company)
        self.assertEqual(department_created.name, 'Engineering')

    def test_create_department_invalid(self):
        url = reverse('companysettings:list_departments')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]
        form.action = reverse('companysettings:create_department')
        form['name'] = ''
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_update_department_valid(self):
        dept = DepartmentFactory.create(name='Sales', company=self.user.company)
        url = reverse('companysettings:list_departments')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]
        form.action = reverse('companysettings:update_department', args=(dept.id,))
        form['name'] = 'Engineering'

        self.assertContains(page, dept.name)

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engineering')
        self.assertNotContains(response, 'Sales')

    def test_update_department_invalid(self):
        dept = DepartmentFactory.create(name='Sales', company=self.user.company)
        url = reverse('companysettings:list_departments')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]

        form.action = reverse('companysettings:update_department', args=(dept.id,))
        form['name'] = ''

        self.assertContains(page, dept.name)

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_delete_department(self):
        dept = DepartmentFactory.create(name='Sales', company=self.user.company)
        url = reverse('companysettings:delete_department', args=(dept.id,))

        response = self.app.get(url, user=self.user).follow()
        self.assertEqual(response.request.path,
                         reverse('companysettings:list_departments'))
        self.assertNotContains(response, "Sales")
        self.assertContains(response, "Department deleted.")

    def test_list_questions(self):
        url = reverse('companysettings:list_questions')
        question = SingleLineQuestionFactory.create(company=self.user.company)
        page = self.app.get(url, user=self.user)
        self.assertContains(page, question.name)

    def test_create_question_valid(self):
        url = reverse('companysettings:list_questions')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]
        form.action = reverse('companysettings:create_question')
        form['name'] = 'Cover letter'
        form['type'] = 'textbox'

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        question_created = Question.objects.get()

        self.assertEqual(question_created.company, self.user.company)
        self.assertEqual(question_created.name, 'Cover letter')

    def test_create_question_invalid(self):
        url = reverse('companysettings:list_questions')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]
        form.action = reverse('companysettings:create_question')
        form['name'] = ''
        form['type'] = 'textbox'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_update_question_valid(self):
        question = SingleLineQuestionFactory.create(company=self.user.company)
        url = reverse('companysettings:list_questions')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]
        form.action = reverse('companysettings:update_question', args=(question.id,))
        form['name'] = 'Last Name'

        self.assertContains(page, question.name)

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Last Name')
        self.assertNotContains(response, 'First Name')

    def test_update_question_invalid(self):
        question = SingleLineQuestionFactory.create(company=self.user.company)
        url = reverse('companysettings:list_questions')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]
        form.action = reverse('companysettings:update_question', args=(question.id,))
        form['name'] = ''

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_delete_question(self):
        question = SingleLineQuestionFactory.create(
            name='ninja', company=self.user.company
        )
        url = reverse('companysettings:delete_question', args=(question.id,))

        response = self.app.get(url, user=self.user).follow()
        self.assertEqual(response.request.path,
                         reverse('companysettings:list_questions'))
        self.assertNotContains(response, "ninja")
        self.assertContains(response, "Question deleted.")

    def test_list_stages(self):
        url = reverse('companysettings:list_stages')

        stage = InterviewStageFactory.create(company=self.user.company)
        page = self.app.get(url, user=self.user)

        self.assertContains(page, stage.name)

    def test_create_stage_valid(self):
        url = reverse('companysettings:create_stage')

        page = self.app.get(url, user=self.user)
        form = page.forms['action-form']
        form['name'] = 'Phone interview'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        stage_created = InterviewStage.objects.get()

        self.assertEqual(stage_created.company, self.user.company)
        self.assertEqual(stage_created.name, 'Phone interview')
        self.assertEqual(stage_created.position, 1)

    def test_create_stage_invalid(self):
        url = reverse('companysettings:create_stage')

        page = self.app.get(url, user=self.user)
        form = page.forms['action-form']
        form['name'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_update_stage_valid(self):
        stage = InterviewStageFactory.create(name='Phone', company=self.user.company)
        url = reverse('companysettings:update_stage', args=(stage.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['action-form']
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
        form = page.forms['action-form']
        form['name'] = ''

        self.assertContains(page, stage.name)

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_delete_stage(self):
        InterviewStageFactory(company=self.user.company)
        stage = InterviewStageFactory(
            name='Interview',
            company=self.user.company
        )
        url = reverse('companysettings:delete_stage', args=(stage.id,))

        response = self.app.get(url, user=self.user).follow()
        self.assertEqual(response.request.path,
                         reverse('companysettings:list_stages'))
        self.assertNotContains(response, "Interview")
        self.assertContains(response, "Stage deleted.")

    def test_delete_last_stage(self):
        stage = InterviewStageFactory.create(company=self.user.company)
        url = reverse('companysettings:delete_stage', args=(stage.id,))

        response = self.app.get(url, user=self.user).follow()

        self.assertEqual(
            response.request.path,
            reverse('companysettings:list_stages')
        )
        self.assertContains(response, stage.name)
        self.assertContains(response, "You need to have at least one stage.")

    def test_reorder_stage_valid_up(self):
        stage1 = InterviewStageFactory.create(company=self.user.company)
        stage2 = InterviewStageFactory.create(company=self.user.company)
        url = reverse('companysettings:reorder_stage', args=(stage2.id, 'up'))

        response = self.app.get(url, user=self.user).follow()

        self.assertEqual(
            response.request.path,
            reverse('companysettings:list_stages')
        )
        self.assertEqual(InterviewStage.objects.get(id=1).position, 2)

    def test_reorder_stage_valid_down(self):
        stage1 = InterviewStageFactory.create(company=self.user.company)
        stage2 = InterviewStageFactory.create(company=self.user.company)
        url = reverse('companysettings:reorder_stage', args=(stage1.id, 'down'))

        response = self.app.get(url, user=self.user).follow()

        self.assertEqual(
            response.request.path,
            reverse('companysettings:list_stages')
        )
        self.assertEqual(InterviewStage.objects.get(id=1).position, 2)

    def test_reorder_stage_invalid(self):
        stage1 = InterviewStageFactory.create(company=self.user.company)
        stage2 = InterviewStageFactory.create(company=self.user.company)
        url = reverse('companysettings:reorder_stage', args=(stage2.id, 'down'))

        response = self.app.get(url, user=self.user).follow()

        self.assertEqual(
            response.request.path,
            reverse('companysettings:list_stages')
        )
        self.assertEqual(InterviewStage.objects.get(id=1).position, 1)

    def test_list_users(self):
        url = reverse('companysettings:list_users')
        colleague = UserFactory.create(
            company=self.user.company,
            first_name="Steve",
            email="steve@example.com"
        )
        not_colleague = UserFactory.create(
            first_name="Bill",
            email="bill@example.com"
        )
        page = self.app.get(url, user=self.user)

        self.assertContains(page, colleague.first_name)
        self.assertNotContains(page, not_colleague.first_name)

    def test_invite_user(self):
        url = reverse('companysettings:list_users')
        page = self.app.get(url, user=self.user)

        form = page.form
        form.action = reverse('companysettings:invite_user')
        form["email"] = "steve@example.com"
        page = form.submit().follow()
        self.assertTrue(
            CustomUser.objects.filter(email="steve@example.com").exists())
        self.assertEqual(len(mail.outbox), 1)
        new_user = CustomUser.objects.get(email="steve@example.com")
        self.assertEqual(new_user.company, self.user.company)
        self.assertFalse(new_user.is_company_admin)

    def test_user_logins_from_invitation(self):
        new_user = CustomUser.objects.create_user(
            email="steve@example.com",
            active=False,
            company=self.user.company
        )
        url = reverse('accounts:activate', args=(new_user.activation_key,))
        response = self.app.get(url)
        form = response.form
        form['password1'] = '1234567'
        form['password2'] = '1234567'
        form.submit().follow()
        new_user = CustomUser.objects.get(pk=new_user.pk)
        self.assertTrue(new_user.is_active)
        self.assertEqual(new_user.company, self.user.company)

        user = CustomUser.objects.get(email="steve@example.com")
        self.assertTrue(user.check_password("1234567"))

    def test_disable_user(self):
        colleague = CustomUser.objects.create_user(
            email="steve@example.com",
            active=True,
            company=self.user.company
        )
        toggle_status_url = reverse(
            'accounts:toggle_status',
            args=(colleague.pk,)
        )

        self.app.get(toggle_status_url, user=self.user, status=302)
        self.assertTrue(
            CustomUser.objects.filter(pk=colleague.pk, is_active=False).exists()
        )

        self.app.get(toggle_status_url, user=self.user, status=302)
        self.assertTrue(
            CustomUser.objects.filter(pk=colleague.pk, is_active=True).exists()
        )

    def test_disable_user_access(self):
        colleague = CustomUser.objects.create_user(
            email="steve@example.com",
            active=True,
            is_company_admin=False,
            company=self.user.company
        )
        toggle_colleague_status_url = reverse(
            'accounts:toggle_status',
            args=(colleague.pk,)
        )
        toggle_self_status_url = reverse(
            'accounts:toggle_status',
            args=(self.user.pk,)
        )
        url = reverse('companysettings:list_users')

        response = self.app.get(url, user=self.user)
        self.assertContains(response, toggle_colleague_status_url)
        self.assertNotContains(response, toggle_self_status_url)

        response = self.app.get(url, user=colleague)
        self.assertNotContains(response, toggle_colleague_status_url)
        self.assertNotContains(response, toggle_self_status_url)

    def test_modify_company_information_valid(self):
        url = reverse('companysettings:update_information')

        page = self.app.get(url, user=self.user)
        form = page.forms['action-form']
        form['website'] = 'www.google.com'
        form['description'] = 'Cool stuff.'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        company = Company.objects.get(id=1)

        self.assertEqual(company.website, 'http://www.google.com/')
        self.assertEqual(company.description, 'Cool stuff.')

    def test_modify_company_information_invalid(self):
        url = reverse('companysettings:update_information')

        page = self.app.get(url, user=self.user)
        form = page.forms['action-form']
        form['website'] = 'goog'
        form['description'] = 'Cool stuff.'
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'website', 'Enter a valid URL.')
