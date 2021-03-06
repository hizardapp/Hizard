from django.core.urlresolvers import reverse_lazy
from django.template import Context, Template, TemplateSyntaxError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from braces.views import LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin
from core.views import RestrictedListView, RestrictedUpdateView, MessageMixin

from .models import EmailTemplate
from .forms import EmailTemplateForm


TEST_CONTEXT = Context(dict(
    applicant_first_name=mark_safe(u"Quentin"),
    applicant_last_name=mark_safe(u"Potter"),
    opening=mark_safe("Professor of magic"),
    company=mark_safe("Magic & Co.")))


class CustomisableEmailsListView(LoginRequiredMixin, RestrictedListView):
    model = EmailTemplate


class CustomisableEmailsUpdateView(LoginRequiredMixin, MessageMixin, RestrictedUpdateView):
    model = EmailTemplate
    form_class = EmailTemplateForm
    success_url = reverse_lazy("customisable_emails:list")
    success_message = _('Email edited')

    def get_context_data(self, **kwargs):
        context = super(
            CustomisableEmailsUpdateView, self
        ).get_context_data(**kwargs)
        context["TEST_CONTEXT"] = TEST_CONTEXT
        return context


class TestEmailTemplateRendererView(
    LoginRequiredMixin,
    AjaxResponseMixin,
    JSONResponseMixin,
    View
):

    def post_ajax(self, request, *args, **kwargs):
        try:
            subject_template = Template(request.POST.get("subject"))
            subject = subject_template.render(TEST_CONTEXT)
        except TemplateSyntaxError as e:
            subject = str(e)

        try:
            body_template = Template(request.POST.get("body"))
            body = body_template.render(TEST_CONTEXT)
        except TemplateSyntaxError as e:
            body = str(e)

        return self.render_json_response(dict(subject=subject, body=body))
