from collections import defaultdict
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, CreateView, TemplateView
from braces.views import LoginRequiredMixin

from .forms import ApplicationStageTransitionForm, ApplicationMessageForm
from .models import Application, ApplicationAnswer, ApplicationMessage
from .threaded_discussion import group
from companysettings.models import InterviewStage
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


class ApplicationMessageCreateView(LoginRequiredMixin, CreateView):
    model = ApplicationMessage
    form_class = ApplicationMessageForm
    action = 'created'

    def dispatch(self, request, application_id, **kwargs):
        self.application = get_object_or_404(Application,
                opening__company=self.request.user.company,
                pk=application_id)
        return super(ApplicationMessageCreateView, self).dispatch(
                request, application_id, **kwargs)

    def get_success_url(self):
        return "%s#notes" % reverse('applications:application_detail',
                args=(self.application.id,))

    def form_valid(self, form):
        new_message = form.save(commit=False)
        new_message.application = self.application
        new_message.user = self.request.user
        return super(ApplicationMessageCreateView, self).form_valid(form)


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
        context['user'] = self.request.user
        application = self.get_application()
        context['application'] = application
        context['discussion'] = group(application.applicationmessage_set.all())
        context['new_message_form'] = ApplicationMessageForm()
        context['answers'] = ApplicationAnswer.objects.filter(
            application=context['application'])
        return context

    def form_valid(self, form):
        transition = form.save(commit=False)
        transition.application = self.get_application()
        transition.user = self.request.user
        transition.save()
        return redirect('applications:application_detail',
            pk=self.kwargs['pk'])


class BoardView(LoginRequiredMixin, TemplateView):
    template_name = "applications/_kanban.html"

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)

        board_data = defaultdict(list)

        stages = InterviewStage.objects.filter(company=self.request.user.company)
        applications = Application.objects.filter(opening__company=self.request.user.company).prefetch_related("stage_transitions__stage")

        for stage in stages:
            board_data[stage] = []
            for application in applications:
                if stage == application.current_stage():
                    board_data[stage].append(application)

        context['board'] = board_data

        return context
