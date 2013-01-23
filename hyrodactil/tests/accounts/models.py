import os

from django.core.files import File
from django.test import TestCase

from accounts.models import CustomUser, get_file_path
from hyrodactil.settings import base


class CustomUserCreationTest(TestCase):
    UserModel = CustomUser

    user_info = {
        'email': 'bob@bob.com',
        'password': 'password'
    }

    def test_create_normal_user(self):
        user = self.UserModel.objects.create_user(**self.user_info)
        user_found = self.UserModel.objects.get(id=1)

        self.assertEqual(user, user_found)

    def test_create_superuser(self):
        user = self.UserModel.objects.create_superuser(**self.user_info)
        user_found = self.UserModel.objects.get(id=1)

        self.assertEqual(user, user_found)
        self.assertEqual(user.is_staff, True)

    def test_get_file_path(self):
        user = self.UserModel.objects.create_superuser(**self.user_info)
        path = get_file_path(user, 'default_avatar.jpg')

        expected = '%s/avatars/%s' % (base.MEDIA_ROOT, 'Ym9iQGJvYi5jb20.jpg')

        self.assertEqual(path, expected)

    def test_add_image_to_user(self):
        user = self.UserModel.objects.create_user(**self.user_info)
        default_avatar = os.path.join(base.STATICFILES_DIRS[0], 'img/default_avatar.jpg')

        user.avatar = File(open(default_avatar))
        user.save()

        user_found = self.UserModel.objects.get(id=1)
        self.assertTrue(os.path.exists(user_found.avatar.path))

        os.remove(user_found.avatar.path)

    def test_add_information_to_user(self):
        user = self.UserModel.objects.create_user(**self.user_info)
        user.save()

        user.first_name = 'Bob'
        user.last_name = 'Marley'
        user.save()

        user_found = self.UserModel.objects.get(id=1)

        self.assertEqual(user.first_name, user_found.first_name)
        self.assertEqual(user.last_name, user_found.last_name)