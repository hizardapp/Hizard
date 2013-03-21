from django.http.response import HttpResponseRedirect
from core.utils import build_subdomain_url


class SubdomainMiddleware(object):
    def process_request(self, request):
        domain_parts = request.get_host().split('.')
        if len(domain_parts) > 2:
            request.subdomain = domain_parts[0]
        else:
            request.subdomain = None

        if (request.user.is_authenticated()
                and request.user.company
                and not request.subdomain):
            url = build_subdomain_url(request, request.get_full_path())
            return HttpResponseRedirect(url)
