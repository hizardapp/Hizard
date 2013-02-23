from django_webtest import WebTest
from django.core.urlresolvers import reverse

class CoreMiddlewareTests(WebTest):
    def test_middleware_adds_subdomain_to_request(self):
        url = reverse('accounts:register')
        response = self.app.get(url,
                extra_environ=dict(HTTP_HOST="google.hyrodactil.com"))
        request = response.context["request"]
        self.assertTrue(hasattr(request, "subdomain"))
        self.assertEqual(request.subdomain, "google")

    def test_middleware_without_subdomain(self):
        url = reverse('accounts:register')
        response = self.app.get(url)
        request = response.context["request"]
        self.assertTrue(hasattr(request, "subdomain"))
        self.assertFalse(request.subdomain)
