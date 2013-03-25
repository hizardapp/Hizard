from django.test import TestCase
from django.db import IntegrityError

from ..factories._companies import CompanyFactory


class CompaniesModelsTest(TestCase):
    def test_subdomain_uniqueness(self):
        CompanyFactory(subdomain='acme')
        with self.assertRaises(IntegrityError):
            CompanyFactory(subdomain='acme')
