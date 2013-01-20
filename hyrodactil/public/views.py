from django.views.generic.base import TemplateView

from jobs.models import Opening


class HomeView(TemplateView):
    template_name = 'public/home.html'


class JobListView(TemplateView):
    template_name = 'public/job_list.html'

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['openings'] = Opening.objects.filter(company=self.kwargs['company_id'])
        return context