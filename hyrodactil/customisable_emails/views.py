from django.core.urlresolvers import reverse_lazy
from django.template import Context, Template, TemplateSyntaxError
from django.utils.safestring import mark_safe
from django.views.generic.base import View
from braces.views import LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin
from core.views import RestrictedListView, RestrictedUpdateView

from .models import EmailTemplate
from .forms import EmailTemplateForm


TEST_CONTEXT = Context(dict(
    applicant_first_name=mark_safe(u"Mayjic"),
    applicant_last_name=mark_safe(u"Eight"),
    opening=mark_safe("Professor of magic"),
    company=mark_safe("Magic & Co.")))


class CustomisableEmailsListView(LoginRequiredMixin, RestrictedListView):
    model = EmailTemplate


class CustomisableEmailsUpdateView(LoginRequiredMixin, RestrictedUpdateView):
    model = EmailTemplate
    form_class = EmailTemplateForm
    success_url = reverse_lazy("customisable_emails:list")

    def get_context_data(self, **kwargs):
        context = super(
                CustomisableEmailsUpdateView, self).get_context_data(**kwargs)
        context["TEST_CONTEXT"] = TEST_CONTEXT
        return context


class TestEmailTemplateRendererView(LoginRequiredMixin, AjaxResponseMixin,
        JSONResponseMixin, View):

    def post_ajax(self, request):
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
