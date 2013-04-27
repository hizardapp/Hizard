from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from applications.forms import ApplicationForm
from companies.models import Company
from core.views import SubdomainMixin
from openings.models import Opening


class HomeView(SubdomainMixin, TemplateView):
    def job_list(self, request):
        context = super(HomeView, self).get_context_data()
        company = get_object_or_404(Company, subdomain=self.request.subdomain)
        context['company'] = company
        context['openings'] = Opening.objects.filter(company=company)

        return TemplateResponse(
                request=request,
                template="public/opening_list.html",
                context=context
        )

    def home_view(self, request):
        return TemplateResponse(
                request=self.request,
                template="public/home.html"
        )

    def get(self, request, *args, **kwargs):
        if self.request.subdomain:
            return self.job_list(request)
        else:
            return self.home_view(request)


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
