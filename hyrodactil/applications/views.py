from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView

from braces.views import LoginRequiredMixin

from .forms import ApplicationStageTransitionForm
from applications.models import Application, ApplicationAnswer
from core.views import RestrictedListView
from openings.models import Opening


class ApplicationListView(LoginRequiredMixin, RestrictedListView):
    def get_context_data(self, **kwargs):
        kwargs['context_opening'] = get_object_or_404(
            Opening, pk=self.kwargs['opening_id']
        )
        return super(ApplicationListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        opening = get_object_or_404(Opening, pk=self.kwargs['opening_id'])
        return Application.objects.filter(opening=opening)


class AllApplicationListView(LoginRequiredMixin, RestrictedListView):
    def get_queryset(self):
        return Application.objects.filter(
            opening__company=self.request.user.company).order_by("opening")


class ApplicationDetailView(LoginRequiredMixin, FormView):
    model = Application
    form_class = ApplicationStageTransitionForm
    template_name = "applications/application_detail.html"

    def get_application(self):
        try:
            return Application.objects.get(
                pk=self.kwargs["pk"],
                opening__company=self.request.user.company
            )
        except Application.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['application'] = self.get_application()
        context['answers'] = ApplicationAnswer.objects.filter(
            application=context['application'])
        return context

    def form_valid(self, form):
        transition = form.save(commit=False)
        transition.application = self.get_application()
        transition.user = self.request.user
        transition.save()
        return redirect('applications:application_detail', pk=self.kwargs['pk'])
