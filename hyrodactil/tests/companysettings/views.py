import json

from django.core.urlresolvers import reverse
from django.core import mail
from django_webtest import WebTest
from companies.models import Company

from ..factories._accounts import UserFactory
from ..factories._companysettings import InterviewStageFactory
from companysettings.models import InterviewStage
from accounts.models import CustomUser
from tests.utils import subdomain_get, subdomain_post_ajax


class CompanySettingsViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory(is_company_admin=True)

    def test_list_stages(self):
        url = reverse('companysettings:list_stages')

        stage = InterviewStageFactory(company=self.user.company)
        page = subdomain_get(self.app, url, user=self.user)

        self.assertContains(page, stage.name)

    def test_ajax_create_stage_valid(self):
        url = reverse('companysettings:ajax_stage')
        data = {'name': 'Cooking'}

        response = subdomain_post_ajax(
            self.app, url, data, user=self.user
        )
        result = json.loads(response.body)
        self.assertEqual(result['result'], 'success')
        self.assertEqual(result['id'], 1)
        self.assertTrue(InterviewStage.objects.filter(name='Cooking').exists())

    def test_ajax_create_stage_invalid(self):
        url = reverse('companysettings:ajax_stage')
        data = {'name': ''}

        response = subdomain_post_ajax(
            self.app, url, data, user=self.user
        )
        result = json.loads(response.body)
        self.assertEqual(
            result['errors'], {'name': ['This field is required.']}
        )
        self.assertFalse(InterviewStage.objects.filter(name='Cooking').exists())

    def test_ajax_update_stage_valid(self):
        url = reverse('companysettings:ajax_stage')
        stage = InterviewStageFactory()
        data = {'id': stage.id,'name': 'Cooking'}

        response = subdomain_post_ajax(
            self.app, url, data, user=self.user
        )
        result = json.loads(response.body)
        self.assertEqual(result['result'], 'success')
        self.assertTrue(InterviewStage.objects.filter(name='Cooking').exists())

    def test_ajax_update_stage_invalid(self):
        url = reverse('companysettings:ajax_stage')
        stage = InterviewStageFactory()
        data = {'id': stage.id, 'name': ''}

        response = subdomain_post_ajax(
            self.app, url, data, user=self.user
        )
        result = json.loads(response.body)
        self.assertEqual(
            result['errors'], {'name': ['This field is required.']}
        )
        self.assertFalse(InterviewStage.objects.filter(name='Cooking').exists())

    def test_ajax_update_stage_inexisting(self):
        url = reverse('companysettings:ajax_stage')
        data = {'id': 42, 'name': ''}

        response = subdomain_post_ajax(
            self.app, url, data, user=self.user
        )
        result = json.loads(response.body)
        self.assertEqual(result['result'], 'error')
        self.assertFalse(InterviewStage.objects.filter(name='Cooking').exists())
        
    def test_delete_stage(self):
        InterviewStageFactory(company=self.user.company)
        stage = InterviewStageFactory(
            name='Interview',
            company=self.user.company
        )
        url = reverse('companysettings:delete_stage', args=(stage.id,))

        response = subdomain_get(self.app, url, user=self.user)
        self.assertEqual(response.request.path,
                         reverse('companysettings:list_stages'))
        self.assertNotContains(response, "Interview")
        self.assertContains(response, "Stage deleted.")

    def test_reorder_stage_valid_up(self):
        stage1 = InterviewStageFactory(company=self.user.company)
        stage2 = InterviewStageFactory(company=self.user.company)
        url = reverse('companysettings:reorder_stage', args=(stage2.id, 'up'))

        response = subdomain_get(self.app, url, user=self.user)

        self.assertEqual(
            response.request.path,
            reverse('companysettings:list_stages')
        )
        self.assertEqual(InterviewStage.objects.get(id=1).position, 2)

    def test_reorder_stage_valid_down(self):
        stage1 = InterviewStageFactory(company=self.user.company)
        stage2 = InterviewStageFactory(company=self.user.company)
        url = reverse(
            'companysettings:reorder_stage', args=(stage1.id, 'down')
        )

        response = subdomain_get(self.app, url, user=self.user)

        self.assertEqual(
            response.request.path,
            reverse('companysettings:list_stages')
        )
        self.assertEqual(InterviewStage.objects.get(id=1).position, 2)

    def test_reorder_stage_invalid(self):
        stage1 = InterviewStageFactory(company=self.user.company)
        stage2 = InterviewStageFactory(company=self.user.company)
        url = reverse(
            'companysettings:reorder_stage', args=(stage2.id, 'down')
        )

        response = subdomain_get(self.app, url, user=self.user)

        self.assertEqual(
            response.request.path,
            reverse('companysettings:list_stages')
        )
        self.assertEqual(InterviewStage.objects.get(id=1).position, 1)
    def test_list_users(self):
        url = reverse('companysettings:list_users')
        colleague = UserFactory(
            company=self.user.company,
            name="Steve",
            email="steve@example.com"
        )
        not_colleague = UserFactory(
            name="Bill",
            email="bill@example.com"
        )
        page = subdomain_get(self.app, url, user=self.user)

        self.assertContains(page, colleague.name)
        self.assertNotContains(page, not_colleague.name)

    def test_invite_user(self):
        url = reverse('companysettings:list_users')
        page = subdomain_get(self.app, url, user=self.user)

        self.assertEqual(len(mail.outbox), 0)
        form = page.form
        form.action = reverse('companysettings:list_users')
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
            name='Steve',
            active=False,
            company=self.user.company
        )
        url = reverse('accounts:activate', args=(new_user.activation_key,))
        response = subdomain_get(self.app, url)
        form = response.form
        form['password1'] = '1234567'
        form['password2'] = '1234567'
        form.submit().follow()
        new_user = CustomUser.objects.get(pk=new_user.pk)
        self.assertTrue(new_user.is_active)
        self.assertEqual(new_user.company, self.user.company)

        user = CustomUser.objects.get(email="steve@example.com")
        self.assertTrue(user.check_password("1234567"))

    def test_modify_company_information_valid(self):
        url = reverse('companysettings:update_information')

        page = subdomain_get(self.app, url, user=self.user)
        form = page.forms[0]
        form['website'] = 'www.google.com'
        form['description'] = 'Cool stuff.'
        form['name'] = 'Google Incorporated'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        company = Company.objects.get(id=1)

        self.assertEqual(company.name, 'Google Incorporated')
        self.assertEqual(company.website, 'http://www.google.com/')
        self.assertEqual(company.description, 'Cool stuff.')

    def test_modify_company_information_invalid(self):
        url = reverse('companysettings:update_information')

        page = subdomain_get(self.app, url, user=self.user)
        form = page.forms[0]
        form['website'] = 'goog'
        form['description'] = 'Cool stuff.'
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'website', 'Enter a valid URL.')
