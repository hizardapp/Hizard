from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateView

from applications.forms import ApplicationForm
from companies.models import Company
from openings.models import Opening
from core.views import SubdomainRequiredMixin


class LandingPageView(TemplateView):
    template_name = "public/home.html"


class OpeningList(SubdomainRequiredMixin, TemplateView):
    template_name = "public/opening_list.html"

    def get_context_data(self, **kwargs):
        context = super(OpeningList, self).get_context_data(**kwargs)
        company = get_object_or_404(Company, subdomain=self.request.subdomain)
        context["company"] = company
        context["openings"] = company.opening_set.all()
        return context


class ApplyView(TemplateView):
    template_name = 'public/apply.html'

    def get(self, request, *args, **kwargs):
        try:
            opening = Opening.objects.get(id=self.kwargs['opening_id'])
        except Opening.DoesNotExist:
            raise Http404

        context = {
            'opening': opening,
            'company': opening.company,
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
            return redirect('public:confirmation', opening_id=opening.id)
        else:
            context = {
                'opening': opening,
                'company': opening.company,
                'form': form
            }
            return self.render_to_response(context)


class ApplicationConfirmationView(TemplateView):
    template_name = 'public/confirmation.html'

    def get(self, request, *args, **kwargs):
        try:
            opening = Opening.objects.get(id=self.kwargs['opening_id'])
        except Opening.DoesNotExist:
            raise Http404

        context = {
            'opening': opening,
            'company': opening.company
        }
        return self.render_to_response(context)
