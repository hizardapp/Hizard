import base64
import datetime
import os

from django.contrib.auth.forms import (
    AuthenticationForm, PasswordResetForm, SetPasswordForm
)
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36

from django_webtest import WebTest

from ..factories._accounts import UserFactory
from accounts.forms import UserCreationForm
from accounts.models import CustomUser
from tests.utils import subdomain_get

SMALL_GIF = base64.decodestring(
    'R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
)


class AccountsViewsTests(WebTest):
    def test_get_registration_view(self):
        """
        Simple GET to the registration view that should use the correct
        template and have form in its context
        """
        response = subdomain_get(self.app, reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/registration_form.html')
        self.failUnless(isinstance(response.context['form'], UserCreationForm))

    def test_post_registration_view_success(self):
        """
        POST to this view should create an user and redirect to the home page
        """
        page = subdomain_get(self.app, reverse('accounts:register'))

        form = page.forms[0]
        form['email'] = 'bob@bob.com'
        form['name'] = 'Bob S.'
        form['password1'] = 'password'
        form['password2'] = 'password'

        form.submit().follow()

        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(settings.APP_SITE_URL in mail.outbox[0].body)
        new_user = CustomUser.objects.get()
        self.assertTrue(new_user.is_company_admin)

    def test_post_registration_view_failure(self):
        """
        POST to this view with an error in the form should display this form
        again with the error
        """
        page = subdomain_get(self.app, reverse('accounts:register'))

        form = page.forms[0]
        form['email'] = 'bob@bob.com'
        form['name'] = 'Bob S.'
        form['password1'] = 'password'
        form['password2'] = 'wrong'

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        error = "The two password fields didn't match."
        self.assertFormError(response, 'form', 'password2', error)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_get_valid_activation(self):
        user = UserFactory(is_active=False, company=None)
        url = reverse('accounts:activate', args=(user.activation_key,))

        response = subdomain_get(self.app, url)
        user_found = CustomUser.objects.get()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You can now login')
        self.assertTrue(user_found.is_active)

    def test_get_invalid_activation(self):
        """
        GET the activation page with an invalid activation key
        Should raise a 404, using client instead of app since app would fail
        """
        url = reverse('accounts:activate', args=('FAKE',))
        response = subdomain_get(self.app, url, status=404)
        self.assertEqual(response.status_code, 404)

    def test_get_expired_activation(self):
        """
        GET the activation page with an expired activation key
        Should raise a 404, using client instead of app since app would fail
        """
        user = UserFactory(is_active=False,
                created=datetime.datetime.now() - datetime.timedelta(
                                days=settings.ACCOUNT_ACTIVATION_DAYS+1),
                company=None
        )
        url = reverse('accounts:activate', args=(user.activation_key,))
        response = subdomain_get(self.app, url, status=404)
        self.assertEqual(response.status_code, 404)

    def test_get_login_view(self):
        """
        GET the login auth view (from django itself)
        """
        response = subdomain_get(self.app, reverse('auth:login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.failUnless(
            isinstance(response.context['form'], AuthenticationForm)
        )

    def test_get_demo_login_view(self):
        response = subdomain_get(self.app, reverse('auth:login'),
            data=dict(demo=1))
        self.assertEqual(response.status_code, 200)
        form = response.forms[0]
        self.assertEqual(form['username'].value, "demo")
        self.assertEqual(form['password'].value, "demo")

    def test_post_login_view_success_without_company(self):
        """
        POST to the view to login
        Testing to make sure it works with email/activated user and it
        redirects the user to the company creation form
        """
        user = UserFactory(company=None)
        page = subdomain_get(self.app, reverse('auth:login'))

        form = page.forms[0]
        form['username'] = user.email
        form['password'] = 'bob'

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'companies/company_form.html')
        self.assertIn('_auth_user_id', self.app.session)

    def test_post_login_view_success(self):
        """
        POST to the view to login
        Testing to make sure it works with email/activated user
        """
        user = UserFactory()
        page = subdomain_get(self.app, reverse('auth:login'))

        form = page.forms[0]
        form['username'] = user.email
        form['password'] = 'bob'

        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertIn('_auth_user_id', self.app.session)

    def test_already_logged_in(self):
        """
        Testing that logged in users get redirected to the dashboard
        """
        user = UserFactory()
        response = subdomain_get(self.app, reverse('auth:login'), user=user)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')

    def test_post_login_view_failure_inactive_user(self):
        """
        POST to the view to login
        Testing to make sure it works with email/activated user
        """
        user = UserFactory(is_active=False)
        page = subdomain_get(self.app, reverse('auth:login'))

        form = page.forms[0]
        form['username'] = user.email
        form['password'] = 'bob'

        response = form.submit()
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', '', 'This account is inactive.')
        self.assertNotIn('_auth_user_id', self.app.session)

    def test_get_logout_while_logged_in(self):
        """
        GET the logout view while logged in
        Should redirect to the login page and be logged out
        """
        user = UserFactory()
        response = subdomain_get(self.app, reverse('auth:logout'), user=user)
        self.assertEqual(response.request.path, reverse("auth:login"))
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertNotIn('_auth_user_id', self.app.session)

    def test_get_logout_while_logged_out(self):
        """
        GET the logout view while logged out
        Should redirect to the home page since it's not allowed to access this
        page without being logged in
        """
        subdomain_get(self.app, reverse('auth:logout'))

        self.assertTemplateUsed('accounts/login.html')

    def test_get_change_password(self):
        """
        GET the change password page (accessible only while logged in)
        """
        user = UserFactory()
        response = subdomain_get(self.app, reverse('accounts:change_details'), user=user)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'accounts/change_details_form.html'
        )

    def test_post_change_password_success(self):
        """
        POST the change password page
        Should change the password and redirects to home
        """
        user = UserFactory()

        page = subdomain_get(self.app, reverse('accounts:change_details'), user=user)
        form = page.forms[1]
        form['old_password'] = 'bob'
        form['new_password1'] = 'a secure password'
        form['new_password2'] = 'a secure password'
        response = form.submit().follow()

        user_found = CustomUser.objects.get()
        self.assertTemplateUsed(
            response, 'accounts/change_details_form.html'
        )
        self.assertTrue(user_found.check_password('a secure password'))

    def test_post_change_password_failure_too_short(self):
        """
        POST the change password page
        Should display the error and not change the password
        """
        user = UserFactory()

        page = subdomain_get(self.app, reverse('accounts:change_details'), user=user)
        form = page.forms[1]
        form['old_password'] = 'bob'
        form['new_password1'] = 'nop'
        form['new_password2'] = 'nop'
        response = form.submit()

        user_found = CustomUser.objects.get()
        self.assertTemplateUsed(
            response, 'accounts/change_details_form.html'
        )
        self.assertFalse(user_found.check_password('nop'))

    def test_post_change_password_failure_not_matching(self):
        """
        POST the change password page
        Should display the error and not change the password
        """
        user = UserFactory()

        page = subdomain_get(self.app, reverse('accounts:change_details'), user=user)
        form = page.forms[1]
        form['old_password'] = 'bob'
        form['new_password1'] = 'new'
        form['new_password2'] = 'wrong'
        response = form.submit()

        user_found = CustomUser.objects.get()
        self.assertTemplateUsed(
            response, 'accounts/change_details_form.html'
        )
        self.assertFalse(user_found.check_password('new'))
        self.assertFalse(user_found.check_password('wrong'))

    def test_get_password_reset(self):
        """
        GET the reset password page
        """
        response = subdomain_get(self.app, reverse('auth:reset_password'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_form.html')
        self.failUnless(
            isinstance(response.context['form'], PasswordResetForm)
        )

    def test_post_password_reset_success(self):
        """
        POST the reset password page
        Should send a mail
        """
        user = UserFactory()

        page = subdomain_get(self.app, reverse('auth:reset_password'))
        form = page.forms[0]
        form['email'] = user.email
        response = form.submit().follow()

        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertEqual(len(mail.outbox), 1)

    def test_post_password_reset_failure(self):
        """
        POST the reset password page
        Should ask for a confirmation
        """
        UserFactory()

        page = subdomain_get(self.app, reverse('auth:reset_password'))
        form = page.forms[0]
        form['email'] = 'wrong@email.com'
        response = form.submit()

        self.assertContains(response, 'have an associated user account')

    def test_get_password_confirm_valid(self):
        """
        GET the reset password confirmation page
        Should display a form to change password without entering the current
        """
        user = UserFactory()
        uidb36 = int_to_base36(user.pk)
        token = default_token_generator.make_token(user)
        response = subdomain_get(
            self.app,
            reverse(
                'auth:confirm_reset_password',
                kwargs={
                    'uidb36': uidb36,
                    'token': token
                }
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'accounts/password_reset_confirm.html'
        )
        self.failUnless(isinstance(response.context['form'], SetPasswordForm))

    def test_get_password_confirm_invalid(self):
        """
        GET the reset password confirmation page with invalid uidb36/token
        Should display an error
        """
        UserFactory()
        response = subdomain_get(
            self.app,
            reverse(
                'auth:confirm_reset_password',
                kwargs={
                    'uidb36': 'wrong',
                    'token': 'fake'
                }
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'accounts/password_reset_confirm.html'
        )
        self.assertContains(response, 'Password reset failed')

    def test_post_password_confirm_success(self):
        """
        POST the reset password confirmation page
        Should change the password and redirects to home page
        """
        user = UserFactory()
        uidb36 = int_to_base36(user.pk)
        token = default_token_generator.make_token(user)
        page = subdomain_get(
            self.app,
            reverse(
                'auth:confirm_reset_password',
                kwargs={
                    'uidb36': uidb36,
                    'token': token
                }
            )
        )
        form = page.forms[0]
        form['new_password1'] = 'password'
        form['new_password2'] = 'password'
        response = form.submit().follow()

        user_found = CustomUser.objects.get()
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.assertTrue(user_found.check_password('password'))
        self.assertFalse(user_found.check_password('bob'))

    def test_post_password_confirm_failure_short_password(self):
        """
        POST the reset password confirmation page
        Should not change the password and shows the errors
        """
        user = UserFactory()
        uidb36 = int_to_base36(user.pk)
        token = default_token_generator.make_token(user)
        page = subdomain_get(
            self.app,
            reverse(
                'auth:confirm_reset_password',
                kwargs={
                    'uidb36': uidb36,
                    'token': token
                }
            )
        )
        form = page.forms[0]
        form['new_password1'] = 'bad'
        form['new_password2'] = 'bad'
        response = form.submit()

        user_found = CustomUser.objects.get()

        self.assertContains(response, 'Password is too short')
        self.assertFalse(user_found.check_password('bad'))
        self.assertTrue(user_found.check_password('bob'))

    def test_post_password_confirm_failure_password_mismatch(self):
        """
        POST the reset password confirmation page
        Should not change the password and shows the errors
        """
        user = UserFactory()
        uidb36 = int_to_base36(user.pk)
        token = default_token_generator.make_token(user)
        page = subdomain_get(
            self.app,
            reverse(
                'auth:confirm_reset_password',
                kwargs={
                    'uidb36': uidb36,
                    'token': token
                }
            )
        )
        form = page.forms[0]
        form['new_password1'] = 'password'
        form['new_password2'] = 'wrong'
        response = form.submit()

        user_found = CustomUser.objects.get()

        self.assertContains(response, 'The two password fields')
        self.assertFalse(user_found.check_password('password'))
        self.assertTrue(user_found.check_password('bob'))

    def test_change_personal_details(self):
        url = reverse("accounts:change_details")
        user = UserFactory(name='Nikola Tesla')
        page = subdomain_get(self.app, url, user=user)

        self.assertTrue(user.name)
        self.assertContains(page, user.name)

        form = page.forms[0]
        form['name'] = "Henry IV"
        form['avatar'] = 'avatar.gif', SMALL_GIF

        response = form.submit()
        self.assertEqual(response.status_code, 302)

        user = CustomUser.objects.get(pk=user.pk)
        self.assertEqual(user.name, "Henry IV")
        self.assertTrue(user.avatar.url)
        os.unlink(user.avatar.path)

    def test_promote_to_admin_valid(self):
        admin = UserFactory(is_company_admin=True)
        user = UserFactory(company=admin.company)

        url = reverse('accounts:promote', kwargs={'user_pk': user.id})

        subdomain_get(self.app, url, user=admin)
        self.assertTrue(CustomUser.objects.get(id=user.id).is_company_admin)

    def test_promote_to_admin_without_being_admin(self):
        fake_admin = UserFactory()
        user = UserFactory(company=fake_admin.company)

        url = reverse('accounts:promote', kwargs={'user_pk': user.id})

        subdomain_get(self.app, url, user=fake_admin, status=404)

    def test_promote_to_admin_different_company(self):
        admin = UserFactory(is_company_admin=True)
        user = UserFactory()

        url = reverse('accounts:promote', kwargs={'user_pk': user.id})

        subdomain_get(self.app, url, user=admin, status=404)

    def test_delete_user_valid(self):
        admin = UserFactory(is_company_admin=True)
        user = UserFactory(company=admin.company)

        url = reverse('accounts:delete', kwargs={'user_pk': user.id})

        subdomain_get(self.app, url, user=admin)
        self.assertEqual(len(CustomUser.objects.filter(id=user.id)), 0)

    def test_user_without_company_is_redirected(self):
        url = reverse('dashboard:dashboard')
        subdomain_get(self.app, url, user=UserFactory(company=None), status=302)
