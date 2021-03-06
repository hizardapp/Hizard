from django.contrib import messages
from django.core.urlresolvers import reverse

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template import loader, Context
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
    template_name = "public/landing_page.html"

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        context["hizard_prefix"] = settings.COMPANY_URL_PREFIX % "hizard"
        return context


def get_context_for_subdomain(context, subdomain):
    company = get_object_or_404(
        Company,
        subdomain__iexact=subdomain
    )
    context['company'] = company
    context['openings'] = company.opening_set.filter(
        published_date__isnull=False
    )

    return context


class OpeningList(SubdomainRequiredMixin, TemplateView):
    template_name = "public/opening_list.html"

    def get_context_data(self, **kwargs):
        context = super(OpeningList, self).get_context_data(**kwargs)
        return get_context_for_subdomain(context, self.request.subdomain)


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


class EmbedView(SubdomainRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super(EmbedView, self).get_context_data(**kwargs)
        return get_context_for_subdomain(context, self.request.subdomain)

    def get(self, request, *args, **kwargs):
        context = Context(self.get_context_data(**kwargs))
        embed_template = loader.get_template('public/embed.html')
        embed_html = embed_template.render(context)

        context = Context({'embed_html': embed_html})
        embed_template_js = loader.get_template('public/embed.js')
        embed_js = embed_template_js.render(context)

        return HttpResponse(embed_js)
