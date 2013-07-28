from django.views.generic.base import View
from django.template import Context, Template, TemplateSyntaxError
from django.core.urlresolvers import reverse_lazy
from braces.views import LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin
from core.views import RestrictedListView, RestrictedUpdateView

from .models import EmailTemplate
from .forms import EmailTemplateForm


class CustomisableEmailsListView(LoginRequiredMixin, RestrictedListView):
    model = EmailTemplate


class CustomisableEmailsUpdateView(LoginRequiredMixin, RestrictedUpdateView):
    model = EmailTemplate
    form_class = EmailTemplateForm
    success_url = reverse_lazy("customisable_emails:list")

    def get_context_data(self, **kwargs):
        return super(
                CustomisableEmailsUpdateView, self).get_context_data(**kwargs)


class TestEmailTemplateRendererView(LoginRequiredMixin, AjaxResponseMixin,
        JSONResponseMixin, View):
    TEST_CONTEXT = Context(dict(applicant=u"Bob"))

    def post_ajax(self, request):
        print "post_ajax"
        try:
            subject_template = Template(request.POST.get("subject"))
            subject = subject_template.render(
                    TestEmailTemplateRendererView.TEST_CONTEXT)
        except TemplateSyntaxError as e:
            subject = str(e)

        try:
            body_template = Template(request.POST.get("body"))
            body = body_template.render(
                    TestEmailTemplateRendererView.TEST_CONTEXT)
        except TemplateSyntaxError as e:
            body = str(e)

        return self.render_json_response(dict(subject=subject, body=body))
