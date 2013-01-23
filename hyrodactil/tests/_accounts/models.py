from django.test import TestCase

from accounts.models import CustomUser


class CustomUserCreationTest(TestCase):
    UserModel = CustomUser

    user_info = {
        'email': 'bob@bob.com',
        'password': 'password'
    }

    def test_create_normal_user(self):
        user = self.UserModel.objects.create_user(**self.user_info)
        user_found = self.UserModel.objects.all()[0]

        self.assertEqual(user, user_found)

    def test_create_superuser(self):
        user = self.UserModel.objects.create_superuser(**self.user_info)
        user_found = self.UserModel.objects.all()[0]

        self.assertEqual(user, user_found)
        self.assertEqual(user.is_staff, True)