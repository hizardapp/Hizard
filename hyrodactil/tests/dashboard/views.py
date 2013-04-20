from django.core.urlresolvers import reverse

from django_webtest import WebTest

from ..factories._accounts import UserFactory


class DashboardViewsTests(WebTest):
    def test_anonymous_is_redirect_out_of_domain(self):
        user = UserFactory.create()
        response = self.client.get(reverse('dashboard:dashboard'),
            headers=dict(Host="%s.h.com" % user.company.subdomain)
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue("://hizard.com" in response["Location"])
