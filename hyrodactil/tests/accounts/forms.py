from django.conf import settings
from django.test import TestCase

from ..factories._accounts import UserFactory
from accounts import forms as account_forms


class UserCreationFormTests(TestCase):
    user_data = {
        'email': 'bob@bob.com',
        'password1': 'password',
        'password2': 'password'
    }

    def test_form_invalid_without_email(self):
        invalid = dict(self.user_data)
        del(invalid['email'])
        form = account_forms.UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())

    def test_invalid_email(self):
        invalid = dict(self.user_data)
        invalid['email'] = 'wrong.wrong.com'
        form = account_forms.UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())

    def test_using_already_registered_email(self):
        user = UserFactory()
        invalid = dict(self.user_data)
        invalid['email'] = user.email
        form = account_forms.UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())

    def test_form_invalid_passwords_mismatch(self):
        invalid = dict(self.user_data)
        invalid['password2'] = 'wrongpassword'
        form = account_forms.UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors.keys())

    def test_password_too_short(self):
        invalid = dict(self.user_data)
        invalid['password1'] = 'short'
        invalid['password2'] = 'short'
        form = account_forms.UserCreationForm(data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors.keys())

    def test_password_same_length_as_limit(self):
        valid = dict(self.user_data)
        valid_password = 'a' * settings.MIN_PASSWORD_LENGTH
        valid['password1'] = valid_password
        valid['password2'] = valid_password
        form = account_forms.UserCreationForm(data=valid)
        self.assertTrue(form.is_valid())

    def test_form_valid(self):
        form = account_forms.UserCreationForm(data=self.user_data)
        self.assertTrue(form.is_valid())


class MinLengthSetPasswordFormTests(TestCase):
    form_data = {
        'new_password1': 'a secure password',
        'new_password2': 'a secure password'
    }

    def test_passwords_mismatch(self):
        invalid = dict(self.form_data)
        invalid['new_password2'] = 'wrongpassword'
        form = account_forms.MinLengthSetPasswordForm(user={}, data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors.keys())

    def test_short_password(self):
        invalid_password = 'a' * (settings.MIN_PASSWORD_LENGTH - 1)
        invalid = {
            'new_password1': invalid_password,
            'new_password2': invalid_password
        }
        form = account_forms.MinLengthSetPasswordForm(user={}, data=invalid)
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors.keys())

    def test_password_same_length_as_limit(self):
        valid_password = 'a' * settings.MIN_PASSWORD_LENGTH
        valid = {
            'new_password1': valid_password,
            'new_password2': valid_password
        }
        form = account_forms.MinLengthSetPasswordForm(user={}, data=valid)
        self.assertTrue(form.is_valid())

    def test_form_valid(self):
        form = account_forms.MinLengthSetPasswordForm(user={}, data=self.form_data)
        self.assertTrue(form.is_valid())


class MinLengthChangePasswordFormTests(TestCase):

    form_data = {
        'old_password': 'bob',
        'new_password1': 'a secure password',
        'new_password2': 'a secure password'
    }

    def setUp(self):
        self.user = UserFactory()

    def test_passwords_mismatch(self):
        invalid = dict(self.form_data)
        invalid['new_password2'] = 'wrongpassword'
        form = account_forms.MinLengthChangePasswordForm(
            user=self.user, data=invalid
        )
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors.keys())

    def test_short_password(self):
        invalid_password = 'a' * (settings.MIN_PASSWORD_LENGTH - 1)
        invalid = {
            'old_password': 'bob',
            'new_password1': invalid_password,
            'new_password2': invalid_password
        }
        form = account_forms.MinLengthChangePasswordForm(
            user=self.user, data=invalid
        )
        self.assertFalse(form.is_valid())
        self.assertIn('new_password2', form.errors.keys())

    def test_password_same_length_as_limit(self):
        valid_password = 'a' * settings.MIN_PASSWORD_LENGTH
        valid = {
            'old_password': 'bob',
            'new_password1': valid_password,
            'new_password2': valid_password
        }
        form = account_forms.MinLengthChangePasswordForm(
            user=self.user, data=valid
        )
        self.assertTrue(form.is_valid())

    def test_form_valid(self):
        form = account_forms.MinLengthChangePasswordForm(
            user=self.user, data=self.form_data
        )
        form.is_valid()
        self.assertTrue(form.is_valid())
