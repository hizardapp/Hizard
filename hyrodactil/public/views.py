from django.views.generic.base import TemplateView

from .forms import ApplicationForm
from jobs.models import Opening


class HomeView(TemplateView):
    template_name = 'public/home.html'


class JobListView(TemplateView):
    template_name = 'public/job_list.html'

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context['openings'] = Opening.objects.filter(company=self.kwargs['company_id'])
        return context


class JobList2View(TemplateView):
    template_name = 'public/job_list2.html'


    def get(self, request, *args, **kwargs):
        context = {}

        openings = Opening.objects.filter(company=self.kwargs['company_id'])
        context['openings'] = []

        for opening in openings:
            job = {
                'ad': opening,
                'form': ApplicationForm(opening=opening)
            }
            context['openings'].append(job)
        return self.render_to_response(context)


    def post(self, request, *args, **kwargs):
        context = {}

        openings = Opening.objects.filter(company=self.kwargs['company_id'])
        context['openings'] = []

        opening_id = int(request.POST['opening'])
        form = ApplicationForm(request.POST, request.FILES, opening=Opening.objects.get(id=opening_id))

        opening_ids = [opening.id for opening in openings]

        if form.is_valid() and opening_id in opening_ids:
            form.save()
            return self.render_to_response(context)
        else:
            for opening in openings:
                if opening.id in opening_ids and opening.id == opening_id:
                    new_form = ApplicationForm(request.POST, request.FILES, opening=opening)
                else:
                    new_form = ApplicationForm(opening=opening)

                job = {
                    'ad': opening,
                    'form': new_form
                }

                context['openings'].append(job)

            return self.render_to_response(context)