from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView

from applications.forms import ApplicationForm
from companies.models import Company
from openings.models import Opening

class OpeningListView(TemplateView):
    template_name = 'public_jobs/opening_list.html'

    def get_context_data(self, **kwargs):
        context = super(OpeningListView, self).get_context_data(**kwargs)
        company = get_object_or_404(Company, subdomain=self.request.subdomain)
        context['company'] = company
        context['openings'] = Opening.objects.filter(company=company)
        return context


class ApplyView(TemplateView):
    template_name = 'public_jobs/apply.html'

    def get(self, request, *args, **kwargs):
        try:
            opening = Opening.objects.get(id=self.kwargs['opening_id'])
        except Opening.DoesNotExist:
            raise Http404

        context = {
            'opening': opening,
            'form': ApplicationForm(opening=opening)
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        try:
            opening = Opening.objects.get(id=self.kwargs['opening_id'])
        except Opening.DoesNotExist:
            raise Http404
        form = ApplicationForm(request.POST, request.FILES, opening=opening)

        if form.is_valid():
            form.save()
            return redirect('public:home')
        else:
            context = {
                'opening': opening,
                'form': form
            }
            return self.render_to_response(context)


