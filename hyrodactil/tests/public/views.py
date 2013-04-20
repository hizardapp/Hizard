from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory


class PublicViewsTests(WebTest):
    def test_home_page_redirects_to_dashboard_when_logged_in(self):
        url = reverse('public:home')
        user = UserFactory()

        response = self.app.get(
            url,
            user=user,
            headers=dict(Host="%s.h.com" % user.company.subdomain)
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse("dashboard:dashboard") in response["Location"])

    def test_anonymous_can_access_home(self):
        url = reverse('public:home')
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_cannot_stay_in_the_subdomain(self):
        url = reverse('public:home')
        user = UserFactory()

        response = self.app.get(url,
            headers=dict(Host="%s.h.com" % user.company.subdomain)
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("://hizard.com" in response["Location"])
