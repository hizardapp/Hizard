from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from braces.views import LoginRequiredMixin

from .forms import OpeningForm
from .models import Opening, OpeningQuestion
from core.views import MessageMixin, RestrictedListView, RestrictedUpdateView
from core.views import RestrictedDeleteView
from companysettings.models import Question


class OpeningRestrictedListView(LoginRequiredMixin, RestrictedListView):
    model = Opening


class OpeningCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Opening
    form_class = OpeningForm
    action = 'created'
    success_url = reverse_lazy('openings:list_openings')
    success_message = _('Opening created.')

    def get_form(self, form_class):
        return form_class(self.request.user.company, **self.get_form_kwargs())


class OpeningUpdateView(LoginRequiredMixin, MessageMixin, RestrictedUpdateView):
    model = Opening
    form_class = OpeningForm
    action = 'updated'
    success_url = reverse_lazy('openings:list_openings')
    success_message = _('Opening updated.')

    def get_form(self, form_class):
        return form_class(
            self.request.user.company, **self.get_form_kwargs()
        )



class OpeningDeleteView(LoginRequiredMixin, RestrictedDeleteView):
    model = Opening
    success_url = reverse_lazy('openings:list_openings')
    success_message = _('Opening deleted.')
