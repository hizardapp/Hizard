from django.views.generic.base import TemplateView

from braces.views import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context["opening_list"] = self.request.user.company.opening_set.all()
        return context
