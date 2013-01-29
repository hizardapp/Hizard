from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
)
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36

from django_webtest import WebTest

from ..factories._accounts import UserFactory
from accounts.forms import UserCreationForm
from accounts.models import CustomUser


class AccountsViewsTests(WebTest):
    def test_get_registration_view(self):
        """
        Simple GET to the registration view that should use the correct
        template and have form in its context
        """
        response = self.client.get(reverse('accounts:register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/registration_form.html')
        self.failUnless(isinstance(response.context['form'], UserCreationForm))

    def test_post_registration_view_success(self):
        """
        POST to this view should create an user and redirect to the home page
        """
        page = self.app.get(reverse('accounts:register'))

        form = page.forms['register-form']
        form['email'] = 'bob@bob.com'
        form['password1'] = 'password'
        form['password2'] = 'password'

        response = form.submit()

        self.assertRedirects(response, reverse('public:home'))
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_post_registration_view_failure(self):
        """
        POST to this view with an error in the form should display this form
        again with the error
        """
        page = self.app.get(reverse('accounts:register'))

        form = page.forms['register-form']
        form['email'] = 'bob@bob.com'
        form['password1'] = 'password'
        form['password2'] = 'wrong'

        response = form.submit()

        self.assertEqual(response.status_code, 200)
        error = "Passwords don't match"
        self.assertFormError(response, 'form', 'password2', error)
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_get_valid_activation(self):
        user = UserFactory(is_active=False)
        url = reverse('accounts:activate', args=(user.activation_key,))

        response = self.client.get(url)
        user_found = CustomUser.objects.get(id=1)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(user_found.is_active)

    def test_get_invalid_activation(self):
        """
        GET the activation page with an invalid activation key
        Should raise a 404, using client instead of app since app would fail
        """
        url = reverse('accounts:activate', args=('FAKE',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_login_view(self):
        """
        GET the login auth view (from django itself)
        """
        response = self.app.get(reverse('auth:login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        self.failUnless(isinstance(response.context['form'], AuthenticationForm))

    def test_post_login_view_success(self):
        """
        POST to the view to login
        Testing to make sure it works with email/activated user
        """
        user = UserFactory.create()
        page = self.app.get(reverse('auth:login'))

        form = page.forms['login-form']
        form['username'] = user.email
        form['password'] = 'bob'

        response = form.submit()
        self.assertRedirects(response, reverse('public:home'))
        self.assertIn('_auth_user_id', self.app.session)

    def test_post_login_view_failure_inactive_user(self):
        """
        POST to the view to login
        Testing to make sure it works with email/activated user
        """
        user = UserFactory.create(is_active=False)
        page = self.app.get(reverse('auth:login'))

        form = page.forms['login-form']
        form['username'] = user.email
        form['password'] = 'bob'

        response = form.submit()
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', '', 'This account is inactive.')
        self.assertNotIn('_auth_user_id', self.app.session)

    def test_get_logout_while_logged_in(self):
        """
        GET the logout view while logged in
        Should redirect to the home page and be logged out
        """
        user = UserFactory.create()
        response = self.app.get(reverse('auth:logout'), user=user)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('public:home'))
        self.assertNotIn('_auth_user_id', self.app.session)

    def test_get_logout_while_logged_out(self):
        """
        GET the logout view while logged out
        Should redirect to the home page since it's not allowed to access this
        page without being logged in
        """
        response = self.app.get(reverse('auth:logout'))

        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('accounts/login.html')

    def test_get_change_password(self):
        """
        GET the change password page (accessible only while logged in)
        """
        user = UserFactory.create()
        response = self.app.get(reverse('auth:change_password'), user=user)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_change_form.html')
        self.failUnless(isinstance(response.context['form'], PasswordChangeForm))

    def test_post_change_password_success(self):
        """
        POST the change password page
        Should change the password and redirects to home
        """
        user = UserFactory.create()

        page = self.app.get(reverse('auth:change_password'), user=user)
        form = page.forms['change-password-form']
        form['old_password'] = 'bob'
        form['new_password1'] = 'new'
        form['new_password2'] = 'new'
        response = form.submit()

        user_found = CustomUser.objects.get(id=1)
        self.assertRedirects(response, reverse('public:home'))
        self.assertTrue(user_found.check_password('new'))

    def test_post_change_password_failure(self):
        """
        POST the change password page
        Should display the error and not change the password
        """
        user = UserFactory.create()

        page = self.app.get(reverse('auth:change_password'), user=user)
        form = page.forms['change-password-form']
        form['old_password'] = 'bob'
        form['new_password1'] = 'new'
        form['new_password2'] = 'wrong'
        response = form.submit()

        user_found = CustomUser.objects.get(id=1)
        error = "The two password fields didn't match."
        self.assertFormError(response, 'form', 'new_password2', error)
        self.assertFalse(user_found.check_password('new'))
        self.assertFalse(user_found.check_password('wrong'))

    def test_get_password_reset(self):
        """
        GET the reset password page
        """
        response = self.app.get(reverse('auth:reset_password'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_form.html')
        self.failUnless(isinstance(response.context['form'], PasswordResetForm))

    def test_post_password_reset_success(self):
        """
        POST the reset password page
        Should send a mail
        """
        user = UserFactory.create()

        page = self.app.get(reverse('auth:reset_password'))
        form = page.forms['reset-password-form']
        form['email'] = user.email
        response = form.submit()

        self.assertRedirects(response, reverse('public:home'))
        self.assertEqual(len(mail.outbox), 1)

    def test_post_password_reset_failure(self):
        """
        POST the reset password page
        Should ask for a confirmation
        """
        user = UserFactory.create()

        page = self.app.get(reverse('auth:reset_password'))
        form = page.forms['reset-password-form']
        form['email'] = 'wrong@email.com'
        response = form.submit()

        self.assertContains(response, 'have an associated user account')

    def test_get_password_confirm_valid(self):
        """
        GET the reset password confirmation page
        Should display a form to change password without entering the current
        """
        user = UserFactory.create()
        uidb36 = int_to_base36(user.pk)
        token = default_token_generator.make_token(user)
        response = self.app.get(
            reverse(
                'auth:confirm_reset_password',
                kwargs={
                    'uidb36': uidb36,
                    'token': token
                }
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_confirm.html')
        self.failUnless(isinstance(response.context['form'], SetPasswordForm))

    def test_get_password_confirm_invalid(self):
        """
        GET the reset password confirmation page with invalid uidb36/token
        Should display an error
        """
        user = UserFactory.create()
        response = self.app.get(
            reverse(
                'auth:confirm_reset_password',
                kwargs={
                    'uidb36': 'wrong',
                    'token': 'fake'
                }
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_confirm.html')
        self.assertContains(response, 'Password reset failed')

    def test_post_password_confirm_success(self):
        """
        POST the reset password confirmation page
        Should change the password and redirects to home page
        """
        user = UserFactory.create()
        uidb36 = int_to_base36(user.pk)
        token = default_token_generator.make_token(user)
        page = self.app.get(
            reverse(
                'auth:confirm_reset_password',
                kwargs={
                    'uidb36': uidb36,
                    'token': token
                }
            )
        )
        form = page.forms['confirm-reset-password-form']
        form['new_password1'] = 'password'
        form['new_password2'] = 'password'
        response = form.submit()

        user_found = CustomUser.objects.get(id=1)
        self.assertRedirects(response, reverse('public:home'))
        self.assertTrue(user_found.check_password('password'))
        self.assertFalse(user_found.check_password('bob'))

    def test_post_password_confirm_failure(self):
        """
        POST the reset password confirmation page
        Should not change the password and shows the errors
        """
        user = UserFactory.create()
        uidb36 = int_to_base36(user.pk)
        token = default_token_generator.make_token(user)
        page = self.app.get(
            reverse(
                'auth:confirm_reset_password',
                kwargs={
                    'uidb36': uidb36,
                    'token': token
                }
            )
        )
        form = page.forms['confirm-reset-password-form']
        form['new_password1'] = 'password'
        form['new_password2'] = 'wrong'
        response = form.submit()

        user_found = CustomUser.objects.get(id=1)

        self.assertContains(response, 'The two password fields')
        self.assertFalse(user_found.check_password('password'))
        self.assertTrue(user_found.check_password('bob'))
