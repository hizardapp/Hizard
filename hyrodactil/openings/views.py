from datetime import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, View

from braces.views import LoginRequiredMixin

from .forms import OpeningForm
from .models import Opening
from core.views import MessageMixin, QuickDeleteView, RestrictedUpdateView
from core.views import RestrictedDetailView, RestrictedListView


class OpeningListView(LoginRequiredMixin, RestrictedListView):
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
        return form_class(self.request.user.company, **self.get_form_kwargs())


class OpeningDeleteView(LoginRequiredMixin, QuickDeleteView):
    model = Opening
    success_url = reverse_lazy('openings:list_openings')
    success_message = _('Opening deleted.')


class OpeningDetailView(LoginRequiredMixin, RestrictedDetailView):
    model = Opening


class OpeningCloseView(LoginRequiredMixin, View):
    success_url = reverse_lazy('openings:list_openings')

    def get(self, request, *args, **kwargs):
        opening = get_object_or_404(Opening, id=self.kwargs['pk'])

        if opening.company != self.request.user.company:
            raise Http404

        if opening.closing_date:
            messages.error(request, _('This opening is already closed.'))
        else:
            opening.closing_date = datetime.now()
            opening.save()
            messages.success(request, _('Opening closed.'))

        return redirect(self.success_url)