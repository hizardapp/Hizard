from django.contrib.auth.forms import AuthenticationForm
from django.core import mail
from django.core.urlresolvers import reverse

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
        self.assertFormError(response, 'form', 'password2', 'Passwords don\'t match')
        self.assertEqual(CustomUser.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_valid_activation(self):
        pass

    def test_invalid_activation(self):
        pass

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
        self.assertRedirects(response, reverse('public:home'))