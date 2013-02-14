from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from braces.views import LoginRequiredMixin

from .models import Opening
from applications.models import Application, ApplicationAnswer
from core.views import  RestrictedListView


class ApplicationListView(LoginRequiredMixin, RestrictedListView):
    def get_queryset(self):
        opening = get_object_or_404(Opening, pk=self.kwargs['opening_id'])
        return Application.objects.filter(opening=opening)


class AllApplicationListView(LoginRequiredMixin, RestrictedListView):
    def get_queryset(self):
        return Application.objects.filter(
            opening__company=self.request.user.company).order_by("opening")


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
