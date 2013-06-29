from braces.views import LoginRequiredMixin
from core.views import RestrictedListView

from models import EmailTemplate


class CustomisableEmailsListView(LoginRequiredMixin, RestrictedListView):
    model = EmailTemplate

    def get_queryset(self):
        return EmailTemplate.objects.filter(company=self.request.user.company)
