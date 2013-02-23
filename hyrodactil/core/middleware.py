class SubdomainMiddleware(object):
    def process_request(self, request):
        domain_parts = request.get_host().split('.')
        if len(domain_parts) > 2:
            request.subdomain = domain_parts[0]
        else:
            request.subdomain = None
