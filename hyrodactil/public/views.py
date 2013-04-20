from django.views.generic.base import TemplateView
from openings.models import Opening


class HomeView(TemplateView):
    template_name = 'public/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context["opening_list"] = Opening.objects.filter(
                    company=self.request.user.company)
        return context
