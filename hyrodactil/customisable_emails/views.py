from braces.views import LoginRequiredMixin
from core.views import RestrictedListView, RestrictedUpdateView

from .models import EmailTemplate
from .forms import EmailTemplateForm


class CustomisableEmailsListView(LoginRequiredMixin, RestrictedListView):
    model = EmailTemplate


class CustomisableEmailsUpdateView(LoginRequiredMixin, RestrictedUpdateView):
    model = EmailTemplate
    form_class = EmailTemplateForm

    def get_context_data(self, **kwargs):
        return super(
                CustomisableEmailsUpdateView, self).get_context_data(**kwargs)
