from django.core.urlresolvers import reverse
from django.core import mail
from django_webtest import WebTest

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
        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )

        self.assertContains(page, department.name)

    def test_create_department_valid(self):
        url = reverse('companysettings:create_department')

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = 'Engineering'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        department_created = Department.objects.get()

        self.assertEqual(department_created.company, self.user.company)
        self.assertEqual(department_created.name, 'Engineering')

    def test_create_department_invalid(self):
        url = reverse('companysettings:create_department')

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_update_department_valid(self):
        dept = DepartmentFactory.create(name='Sales', company=self.user.company)
        url = reverse('companysettings:update_department', args=(dept.id,))

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = 'Engineering'

        self.assertContains(page, dept.name)

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Engineering')
        self.assertNotContains(response, 'Sales')

    def test_update_department_invalid(self):
        dept = DepartmentFactory.create(name='Sales', company=self.user.company)
        url = reverse('companysettings:update_department', args=(dept.id,))

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = ''

        self.assertContains(page, dept.name)

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_delete_department(self):
        dept = DepartmentFactory.create(name='Sales', company=self.user.company)
        url = reverse('companysettings:delete_department', args=(dept.id,))

        response = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        ).follow()
        self.assertEqual(response.request.path,
                         reverse('companysettings:list_departments'))
        self.assertNotContains(response, "Sales")
        self.assertContains(response, "Department deleted.")

    def test_list_questions(self):
        url = reverse('companysettings:list_questions')

        question = SingleLineQuestionFactory.create(company=self.user.company)

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )

        self.assertContains(page, question.name)

    def test_create_question_valid(self):
        url = reverse('companysettings:create_question')

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = 'Cover letter'
        form['type'] = 'textbox'

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        question_created = Question.objects.get()

        self.assertEqual(question_created.company, self.user.company)
        self.assertEqual(question_created.name, 'Cover letter')

    def test_create_question_invalid(self):
        url = reverse('companysettings:create_question')

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = ''
        form['type'] = 'textbox'
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_update_question_valid(self):
        question = SingleLineQuestionFactory.create(company=self.user.company)
        url = reverse('companysettings:update_question', args=(question.id,))

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = 'Last Name'

        self.assertContains(page, question.name)

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Last Name')
        self.assertNotContains(response, 'First Name')

    def test_update_question_invalid(self):
        question = SingleLineQuestionFactory.create(company=self.user.company)
        url = reverse('companysettings:update_question', args=(question.id,))

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = ''

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_delete_question(self):
        question = SingleLineQuestionFactory.create(
            name='ninja', company=self.user.company
        )
        url = reverse('companysettings:delete_question', args=(question.id,))

        response = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        ).follow()
        self.assertEqual(response.request.path,
                         reverse('companysettings:list_questions'))
        self.assertNotContains(response, "ninja")
        self.assertContains(response, "Question deleted.")

    def test_list_stages(self):
        url = reverse('companysettings:list_stages')

        stage = InterviewStageFactory.create(company=self.user.company)
        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )

        self.assertContains(page, stage.name)

    def test_create_stage_valid(self):
        url = reverse('companysettings:create_stage')

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = 'Phone interview'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        stage_created = InterviewStage.objects.get()

        self.assertEqual(stage_created.company, self.user.company)
        self.assertEqual(stage_created.name, 'Phone interview')

    def test_create_stage_invalid(self):
        url = reverse('companysettings:create_stage')

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_create_stage_valid_already_one_initial(self):
        initial = InterviewStageFactory(initial=True, company=self.user.company)
        url = reverse('companysettings:create_stage')

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = 'Wrong'
        form['initial'] = True
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(InterviewStage.objects.get(id=initial.id).initial)

    def test_update_stage_valid(self):
        stage = InterviewStageFactory.create(name='Phone', company=self.user.company)
        url = reverse('companysettings:update_stage', args=(stage.id,))

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
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

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = ''

        self.assertContains(page, stage.name)

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', self.required)

    def test_update_stage_valid_already_one_initial(self):
        initial = InterviewStageFactory(initial=True, company=self.user.company)
        stage = InterviewStageFactory.create(name='Phone', company=self.user.company)
        url = reverse('companysettings:update_stage', args=(stage.id,))

        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = page.forms['action-form']
        form['name'] = 'Wrong'
        form['initial'] = True

        self.assertContains(page, stage.name)

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(InterviewStage.objects.get(id=initial.id).initial)

    def test_delete_stage(self):
        stage = InterviewStageFactory.create(name='Interview',
                                             company=self.user.company)
        url = reverse('companysettings:delete_stage', args=(stage.id,))

        response = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        ).follow()
        self.assertEqual(response.request.path,
                         reverse('companysettings:list_stages'))
        self.assertNotContains(response, "Interview")
        self.assertContains(response, "Stage deleted.")

    def test_delete_initial_stage(self):
        stage = InterviewStageFactory.create(initial= True,
            company=self.user.company)
        url = reverse('companysettings:delete_stage', args=(stage.id,))

        response = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        ).follow()

        self.assertEqual(response.request.path,
            reverse('companysettings:list_stages'))
        self.assertContains(response, stage.name)
        self.assertContains(response, "You cannot delete the initial stage.")

    def test_list_users(self):
        url = reverse('companysettings:list_users')
        colleague = UserFactory.create(company=self.user.company,
            first_name="Steve",
            email="steve@example.com")
        not_colleague = UserFactory.create(first_name="Bill",
            email="bill@example.com")
        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )

        self.assertContains(page, colleague.first_name)
        self.assertNotContains(page, not_colleague.first_name)

    def test_invite_user(self):
        url = reverse('companysettings:invite_user')
        page = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )

        form = page.form
        form["email"] = "steve@example.com"
        page = form.submit().follow()
        self.assertTrue(
            CustomUser.objects.filter(email="steve@example.com").exists())
        self.assertEqual(len(mail.outbox), 1)
        new_user = CustomUser.objects.get(email="steve@example.com")
        self.assertEqual(new_user.company, self.user.company)
        self.assertFalse(new_user.is_company_admin)

    def test_user_logins_from_invitation(self):
        new_user = CustomUser.objects.create_user(email="steve@example.com",
            active=False,
            company=self.user.company)
        url = reverse('accounts:activate', args=(new_user.activation_key,))
        response = self.app.get(url,
                headers=dict(Host="%s.h.com" % new_user.company.subdomain))
        form = response.form
        form['password1'] = '1234567'
        form['password2'] = '1234567'
        form.submit().follow()
        new_user = CustomUser.objects.get(pk=new_user.pk)
        self.assertTrue(new_user.is_active)
        self.assertEqual(new_user.company, self.user.company)

    def test_disable_user(self):
        colleague = CustomUser.objects.create_user(email="steve@example.com",
                active=True,
                company=self.user.company)
        toggle_status_url = reverse('accounts:toggle_status',
                args=(colleague.pk,))

        self.app.get(toggle_status_url,
                user=self.user,
                headers=dict(Host="%s.h.com" % colleague.company.subdomain),
                status=302)
        self.assertTrue(CustomUser.objects.filter(pk=colleague.pk,
            is_active=False).exists())

        self.app.get(toggle_status_url,
                user=self.user,
                headers=dict(Host="%s.h.com" % colleague.company.subdomain),
                status=302)
        self.assertTrue(CustomUser.objects.filter(pk=colleague.pk,
            is_active=True).exists())

    def test_disable_user_access(self):
        colleague = CustomUser.objects.create_user(email="steve@example.com",
                active=True,
                is_company_admin=False,
                company=self.user.company)
        toggle_colleague_status_url = reverse('accounts:toggle_status',
                args=(colleague.pk,))
        toggle_self_status_url = reverse('accounts:toggle_status',
                args=(self.user.pk,))
        url = reverse('companysettings:list_users')

        response = self.app.get(url,
                user=self.user,
                headers=dict(Host="%s.h.com" % colleague.company.subdomain))
        self.assertContains(response, toggle_colleague_status_url)
        self.assertNotContains(response, toggle_self_status_url)

        response = self.app.get(url,
                user=colleague,
                headers=dict(Host="%s.h.com" % colleague.company.subdomain))
        self.assertNotContains(response, toggle_colleague_status_url)
        self.assertNotContains(response, toggle_self_status_url)
