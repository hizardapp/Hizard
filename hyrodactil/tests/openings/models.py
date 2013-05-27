from datetime import datetime

from django.test import TestCase

from ..factories._companies import CompanyFactory
from ..factories._openings import OpeningFactory


class OpeningsModelsTests(TestCase):

    def test_get_apply_url(self):
        company = CompanyFactory(subdomain='acme')
        opening = OpeningFactory(company=company)
        self.assertEqual(
            'http://acme.hizard.com/1/apply/',
            opening.get_apply_url()
        )

    def test_get_location_string(self):
        opening = OpeningFactory.build()
        self.assertEqual(opening.get_location_string(), 'Cannes, France')

    def test_get_status(self):
        opening = OpeningFactory.build()
        self.assertEqual(unicode(opening.get_status()), 'Created')

        opening.is_private = True
        self.assertEqual(unicode(opening.get_status()), 'Private')
        opening.is_private = False

        opening.closing_date = datetime.now()
        self.assertEqual(unicode(opening.get_status()), 'Closed')
        opening.closing_date = None

        opening.published_date = datetime.now()
        self.assertEqual(unicode(opening.get_status()), 'Published')
