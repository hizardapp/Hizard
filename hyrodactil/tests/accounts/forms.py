from django.test import TestCase

from accounts.forms import UserCreationForm

from ..factories._accounts import UserFactory


class UserCreationFormTests(TestCase):
    user_data = {
        'email': 'bob@bob.com',
        'password1': 'password',
        'password2': 'password'
    }

    def test_form_invalid_without_email(self):
        invalid = dict(self.user_data)
        del(invalid['email'])
        form = UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())

    def test_invalid_email(self):
        invalid = dict(self.user_data)
        invalid['email'] = 'wrong.wrong.com'
        form = UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())

    def test_using_already_registered_email(self):
        user = UserFactory.create()
        invalid = dict(self.user_data)
        invalid['email'] = user.email
        form = UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())

    def test_form_invalid_without_identical_passwords(self):
        invalid = dict(self.user_data)
        invalid['password2'] = 'wrong'
        form = UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors.keys())

    def test_form_valid(self):
        form = UserCreationForm(data=self.user_data)
        self.assertTrue(form.is_valid())
