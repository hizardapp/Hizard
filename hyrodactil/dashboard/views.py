from django.views.generic.base import TemplateView

from braces.views import LoginRequiredMixin

from openings.models import Opening
from applications.models import Application
from companysettings.models import InterviewStage


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    table_pagination = False

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        company = self.request.user.company
        context['opening_list'] = Opening.objects.filter(
            company=company,
            published_date__isnull=False
        )

        context['interview_stages'] = InterviewStage.objects.filter(company=company)

        context['last_applications'] = Application.objects.filter(
            opening__company=company
        ).select_related("opening", "applicant").order_by('-created')[:5]

        return context
