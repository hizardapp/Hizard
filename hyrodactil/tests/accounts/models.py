import datetime
import re
import os

from django.core.files import File
from django.test import TestCase

from ..factories._accounts import UserFactory
from accounts.models import CustomUser, get_file_path
from hyrodactil.settings import base


class CustomUserCreationTest(TestCase):
    user_info = {
        'email': 'bob@bob.com',
        'password': 'password'
    }

    inactive_user_info = {
        'email': 'sam@sam.com',
        'password': 'password',
        'active': False
    }

    def test_create_normal_user(self):
        user = CustomUser.objects.create_user(**self.user_info)
        user_found = CustomUser.objects.get(id=1)

        self.assertEqual(user, user_found)
        self.assertEqual(user.is_active, True)

    def test_create_inactive_user(self):
        user = CustomUser.objects.create_user(**self.inactive_user_info)
        user_found = CustomUser.objects.get(id=1)

        self.assertEqual(user, user_found)
        self.assertEqual(user.is_active, False)

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(**self.user_info)
        user_found = CustomUser.objects.get(id=1)

        self.assertEqual(user, user_found)
        self.assertEqual(user.is_staff, True)

    def test_get_file_path(self):
        user = UserFactory.create()
        path = get_file_path(user, 'default_avatar.jpg')
        filename = path.split('/')[-1]

        # The method should generate a 6char filename
        self.assertEqual(len(filename.split('.')[0]), 6)
        # The method should keep the extension from the original file
        self.assertEqual(filename.split('.')[-1], 'jpg')

    def test_add_image_to_user(self):
        user = UserFactory.create()
        default = 'img/default_avatar.jpg'
        default_avatar = os.path.join(base.STATICFILES_DIRS[0], default)

        user.avatar = File(open(default_avatar))
        user.save()

        user_found = CustomUser.objects.get(id=1)
        self.assertTrue(os.path.exists(user_found.avatar.path))

        os.remove(user_found.avatar.path)

    def test_add_information_to_user(self):
        user = UserFactory.create()
        user.save()

        user.first_name = 'Bob'
        user.last_name = 'Marley'
        user.save()

        user_found = CustomUser.objects.get(id=1)

        self.assertEqual(user.first_name, user_found.first_name)
        self.assertEqual(user.last_name, user_found.last_name)

    def test_activate_user(self):
        user = UserFactory.create(is_active=False)
        activated = CustomUser.objects.activate_user(user.activation_key)

        self.assertNotEqual(activated, False)
        self.assertEqual(activated.is_active, True)

    def test_activate_user_past_date(self):
        user = UserFactory.create(is_active=False)

        old_value = base.ACCOUNT_ACTIVATION_DAYS
        base.ACCOUNT_ACTIVATION_DAYS = -1

        activated = CustomUser.objects.activate_user(user.activation_key)

        base.ACCOUNT_ACTIVATION_DAYS = old_value

        self.assertEqual(activated, False)

    def test_activate_user_already_activated(self):
        user = UserFactory.create(is_active=False)
        CustomUser.objects.activate_user(user.activation_key)
        activated = CustomUser.objects.activate_user(user.activation_key)

        self.assertEqual(activated, False)

    def test_activation_key_did_not_expire(self):
        user = UserFactory.create(is_active=False)
        expired = user.activation_key_expired()

        self.assertEqual(expired, False)

    def test_activation_key_did_expire(self):
        user = UserFactory.create(is_active=False)

        old_value = base.ACCOUNT_ACTIVATION_DAYS
        base.ACCOUNT_ACTIVATION_DAYS = -1

        expired = user.activation_key_expired()

        base.ACCOUNT_ACTIVATION_DAYS = old_value

        self.assertEqual(expired, True)

    def test_activation_key_generation(self):
        key = CustomUser.objects._create_activation_token('b@b.com')
        SHA1_RE = re.compile('^[a-f0-9]{40}$')

        self.assertTrue(SHA1_RE.search(key))

    def test_delete_expired_users(self):
        user = UserFactory.create(is_active=False)
        days = datetime.timedelta(days=base.ACCOUNT_ACTIVATION_DAYS + 1)
        user.created -= days
        user.save()

        CustomUser.objects.delete_expired_users()

        count = CustomUser.objects.count()
        self.assertEqual(count, 0)
