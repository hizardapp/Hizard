from django.core.urlresolvers import reverse
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView

from core.utils import build_host_part


class HomeView(TemplateView):
    template_name = 'public/home.html'

    def get(self, *args, **kwargs):
        if self.request.subdomain:
            if self.request.user.is_authenticated():
                return HttpResponseRedirect(reverse("dashboard:dashboard"))
            else:
                return HttpResponseRedirect(
                    build_host_part(self.request, settings.SITE_URL)
                )
        return super(HomeView, self).get(*args, **kwargs)
