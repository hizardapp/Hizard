from django.views.generic.base import TemplateView

import django_tables2
from braces.views import LoginRequiredMixin

from openings.models import Opening
from applications.models import Application

from .tables import OpeningTable

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    table_pagination = False

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        config = django_tables2.RequestConfig(self.request, paginate=False)

        company = self.request.user.company
        context['opening_table'] = OpeningTable(company, Opening.objects.all())

        config.configure(context['opening_table'])

        context['last_applications'] = Application.objects.filter(
            opening__company=company
        ).order_by('-created')[:5].select_related('opening', 'applicant')


        context['opening_list'] = company.opening_set.all()
        return context
