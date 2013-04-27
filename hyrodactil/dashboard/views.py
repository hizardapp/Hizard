from django.views.generic.base import TemplateView

from braces.views import LoginRequiredMixin

from openings.models import Opening


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context["opening_list"] = Opening.objects.filter(
                    company=self.request.user.company)
        return context
