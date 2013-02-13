from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView

from braces.views import LoginRequiredMixin
from core.utils import save_file

from .forms import OpeningForm
from .models import Application, ApplicationAnswer, Opening
from core.views import MessageMixin, RestrictedListView, RestrictedUpdateView
from core.views import RestrictedDeleteView
from public.forms import ApplicationForm


class OpeningRestrictedListView(LoginRequiredMixin, RestrictedListView):
    model = Opening


class OpeningCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Opening
    form_class = OpeningForm
    action = 'created'
    success_url = reverse_lazy('jobs:list_openings')
    success_message = _('Opening created.')

    def get_form(self, form_class):
        return form_class(self.request.user.company, **self.get_form_kwargs())

    def form_valid(self, form):
        opening = form.save(commit=False)
        opening.company = self.request.user.company
        opening.save()
        form.save_m2m()
        return super(OpeningCreateView, self).form_valid(form)


class OpeningUpdateView(LoginRequiredMixin, MessageMixin, RestrictedUpdateView):
    model = Opening
    form_class = OpeningForm
    action = 'updated'
    success_url = reverse_lazy('jobs:list_openings')
    success_message = _('Opening updated.')

    def get_form(self, form_class):
        return form_class(self.request.user.company, **self.get_form_kwargs())


class OpeningDeleteView(LoginRequiredMixin, RestrictedDeleteView):
    model = Opening
    success_url = reverse_lazy('jobs:list_openings')
    success_message = _('Opening deleted.')


class ApplicationListView(LoginRequiredMixin, RestrictedListView):
    def get_queryset(self):
        opening = get_object_or_404(Opening, pk=self.kwargs['opening_id'])
        return Application.objects.filter(opening=opening)


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application

    def get_object(self, queryset=None):
        object = super(ApplicationDetailView, self).get_object()
        if object.opening.company == self.request.user.company:
            return object
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['answers'] = ApplicationAnswer.objects.filter(application=context['application'])
        return context
