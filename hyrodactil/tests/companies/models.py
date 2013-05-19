from django.test import TestCase
from django.db import IntegrityError

from ..factories._companies import CompanyFactory


class CompaniesModelsTest(TestCase):
    def test_subdomain_uniqueness(self):
        CompanyFactory(subdomain='acme')
        with self.assertRaises(IntegrityError):
            CompanyFactory(subdomain='acme')

    def test_get_career_site_url(self):
        company = CompanyFactory(subdomain='acme')
        self.assertEqual(
            'http://acme.hizard.com/opening_list/',
            company.get_career_site_url()
        )

