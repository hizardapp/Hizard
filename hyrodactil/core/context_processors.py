from django.core.urlresolvers import reverse

from core.utils import build_subdomain_url

def opening_lists(request):
    if request.user.is_authenticated() and request.user.company is not None:
        return dict(opening_list_url=
                build_subdomain_url(request, reverse('public:home')))
    return dict()
