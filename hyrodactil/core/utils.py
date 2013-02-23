from django.conf import settings


def build_subdomain_url(request, url):
    scheme = "https" if request.is_secure() else "http"
    server_port = int(request.environ['SERVER_PORT'])
    if server_port not in (80, 443):
        host_part = "%s://%s.%s:%s" % (scheme,
            request.user.company.subdomain,
            settings.SITE_URL,
            server_port)
    else:
        host_part = "%s://%s.%s" % (scheme,
            request.user.company.subdomain,
            settings.SITE_URL)

    return "%s%s" % (host_part, url)

