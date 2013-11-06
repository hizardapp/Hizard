from django.conf import settings
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from ..factories._accounts import UserFactory
from ..factories._companies import CompanyFactory
from ..utils import career_site_get


class AppSubdomainRequiredTests(WebTest):
    """
    Test that the middleware correctly adds/remove the url
    """

    def test_should_remove_subdomain_on_public_view(self):
        landing_page_url = reverse('public:landing-page')

        page = self.app.get(
            landing_page_url,
            headers=dict(Host=settings.APP_SITE_DOMAIN)
        ).follow()

        self.assertEqual(
            page.request.host,
            settings.PUBLIC_DOMAIN
        )

    def test_should_add_subdomain_app_view(self):
        login_url = reverse('auth:login')

        page = self.app.get(
            login_url,
            headers=dict(Host=settings.PUBLIC_DOMAIN)
        ).follow()

        self.assertEqual(
            page.request.host,
            settings.APP_SITE_DOMAIN
        )

    def test_should_work_normally_with_opening_list(self):
        company = CompanyFactory(subdomain='blabla')
        user = UserFactory(company=company)
        url = reverse('public:opening-list')
        user.company.subdomain = user.company.subdomain.title()
        user.company.save()
        page = career_site_get(self.app, url, user.company.subdomain.lower())

        self.assertEqual(page.request.host, 'blabla.test.com:80')