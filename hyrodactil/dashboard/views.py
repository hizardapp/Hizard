from django.views.generic.base import TemplateView

import django_tables2
from braces.views import LoginRequiredMixin

from openings.models import Opening
from .tables import OpeningTable

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    table_pagination = False

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context["opening_table"] = OpeningTable(Opening.objects.all())
        django_tables2.RequestConfig(self.request).configure(
            context["opening_table"])

        context["opening_list"] = self.request.user.company.opening_set.all()
        return context
