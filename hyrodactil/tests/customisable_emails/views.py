from django.core.urlresolvers import reverse
from django_webtest import WebTest

from tests.utils import subdomain_get

from ..factories._accounts import UserFactory
from ..factories._customisable_emails import EmailTemplateFactory


class CustomisableEmailsViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()

    def test_list_emails(self):
        EmailTemplateFactory(company=self.user.company,
                name="application_received")
        response = subdomain_get(self.app,
                reverse('customisable_emails:list'),
                user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "application_received")
