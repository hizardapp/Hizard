from django.core import mail
from django.core.urlresolvers import reverse

from django_webtest import WebTest

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

        expected_redirect = 'http://testserver%s' % reverse('public:home')
        self.assertRedirects(response, expected_redirect)
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