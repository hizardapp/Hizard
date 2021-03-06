from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect


class AppSubdomainRequired(object):
    """
    Make sure we can only access the accounts/app views using the subdomain
    with HTTPS on live.
    """

    public_urls = ['/landing_page/', '/add_interest/', '/favicon.ico']

    def process_request(self, request):
        # Do nothing if it's a career site
        host = request.get_host()
        # Remove the port if there's one
        host = host.split(':')[0]
        host_split = host.split('.')
        # If we have a subdomain and it's different from app, continue
        if len(host_split) == 3:
            subdomain = host_split[0]
            if subdomain != 'app':
                return None

        if request.path in self.public_urls:
            if request.get_host() == settings.PUBLIC_DOMAIN:
                return None

            # If url was in public and it was using the subdomain
            # redirect to the page without the subdomain
            return HttpResponsePermanentRedirect(
                settings.PUBLIC_URL + request.path
            )

        # If a app page was request without the subdomain, redirect to the
        # same page with the subdomain added
        if request.get_host() != settings.APP_SITE_DOMAIN:
            return HttpResponsePermanentRedirect(
                settings.APP_SITE_URL + request.path
            )

        return None

class CompanyRequired(object):
    "Make sure the user has a company."

    def process_request(self, request):
        if (not request.path.startswith(reverse("auth:logout")) and
            not request.path.startswith("/admin") and
            request.user.is_authenticated() and
            request.user.company is None and
            not request.path.startswith(reverse("companies:create"))):
            return HttpResponseRedirect(reverse("companies:create"))
