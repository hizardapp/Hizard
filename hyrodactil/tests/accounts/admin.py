from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from ..factories._accounts import UserFactory
from accounts.models import CustomUser


class ModelAdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_fields(self):
        ma = ModelAdmin(CustomUser, self.site)
        expected = ['password', 'last_login', 'is_superuser', 'groups',
                    'user_permissions', 'email', 'is_active', 'is_admin',
                    'is_staff', 'is_company_admin', 'avatar', 'name',
                    'activation_key', 'company']

        self.assertEqual(expected, ma.get_form(None).base_fields.keys())

    def test_fieldsets(self):
        user = UserFactory()
        ma = ModelAdmin(CustomUser, self.site)
        expected = [
            (None, {
                'fields': [
                    'password', 'last_login', 'is_superuser', 'groups',
                    'user_permissions', 'email', 'is_active', 'is_admin',
                    'is_staff', 'is_company_admin', 'avatar', 'name',
                    'activation_key', 'company']
            })
        ]
        self.assertEqual(expected, ma.get_fieldsets(None, user))
