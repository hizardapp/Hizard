from django.conf import settings
from django.test import TestCase

from ..factories._accounts import UserFactory
from accounts.forms import UserCreationForm


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
        invalid['password2'] = 'wrongpassword'
        form = UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors.keys())

    def test_form_password_too_short(self):
        invalid = dict(self.user_data)
        invalid['password1'] = 'short'
        invalid['password2'] = 'short'
        form = UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors.keys())

    def test_form_password_same_length_as_limit(self):
        valid = dict(self.user_data)
        valid_password = 'a' * settings.MIN_PASSWORD_LENGTH
        valid['password1'] = valid_password
        valid['password2'] = valid_password
        form = UserCreationForm(data=valid)
        self.assertTrue(form.is_valid())

    def test_form_valid(self):
        form = UserCreationForm(data=self.user_data)
        self.assertTrue(form.is_valid())
