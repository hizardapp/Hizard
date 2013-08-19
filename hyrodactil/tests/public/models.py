from django.test import TestCase
from ..factories._public import InterestFactory


class PublicModelsTests(TestCase):

    def test_interest_unicode(self):
        interest = InterestFactory.build()

        self.assertEqual(unicode(interest), interest.email)
