from django.contrib import messages
from django.core.urlresolvers import reverse

from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateView, View

from applications.forms import ApplicationForm
from companies.models import Company
from core.views import SubdomainRequiredMixin
from customisable_emails import send_customised_email
from openings.models import Opening
from .forms import InterestForm


class LandingPageView(TemplateView):
    template_name = "landing_page.html"


class OpeningList(SubdomainRequiredMixin, TemplateView):
    template_name = "public/opening_list.html"

    def get_context_data(self, **kwargs):
        context = super(OpeningList, self).get_context_data(**kwargs)
        company = get_object_or_404(
            Company,
            subdomain__iexact=self.request.subdomain
        )
        context['company'] = company
        context['openings'] = company.opening_set.filter(
            published_date__isnull=False
        )

        return context


class ApplyView(TemplateView):
    template_name = 'public/apply.html'

    def get(self, request, *args, **kwargs):
        try:
            opening = Opening.objects.get(id=self.kwargs['opening_id'])
        except Opening.DoesNotExist:
            raise Http404

        if not opening.published_date:
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

        if not opening.published_date:
            raise Http404

        form = ApplicationForm(request.POST, request.FILES, opening=opening)

        if form.is_valid():
            applicant = form.save()
            send_customised_email("application_received",
                    company=opening.company,
                    to=applicant.email,
                    context=dict(applicant_first_name=applicant.first_name,
                                 applicant_last_name=applicant.last_name,
                                 company=mark_safe(opening.company.name),
                                 opening=mark_safe(opening.title))
            )
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


class InterestView(View):
    def post(self, request, *args, **kwargs):
        form = InterestForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                _('Thanks for your interest, we will send you a mail on release')
            )
        else:
            messages.error(
                request,
                _('Email seems invalid, please check it again')
            )

        return redirect(reverse('public:landing-page'))
