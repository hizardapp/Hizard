from collections import defaultdict
import json

from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, CreateView, TemplateView, View
from braces.views import LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin

from .forms import ApplicationStageTransitionForm, ApplicationMessageForm, ApplicationForm
from .models import Application, ApplicationAnswer, ApplicationMessage, ApplicationStageTransition, Applicant
from .threaded_discussion import group
from companysettings.models import InterviewStage
from core.views import MessageMixin, RestrictedListView
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
            opening__company=self.request.user.company
        ).order_by("opening").prefetch_related("applicant", "opening")


class ApplicationMessageCreateView(LoginRequiredMixin, CreateView):
    model = ApplicationMessage
    form_class = ApplicationMessageForm
    action = 'created'

    def dispatch(self, request, application_id, **kwargs):
        self.application = get_object_or_404(
            Application,
            opening__company=self.request.user.company,
            pk=application_id
        )
        return super(ApplicationMessageCreateView, self).dispatch(
            request, application_id, **kwargs)

    def get_success_url(self):
        return "%s#notes" % reverse(
            'applications:application_detail',
            args=(self.application.id,)
        )

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

    def get_form_kwargs(self):
        default_kwargs = super(ApplicationDetailView, self).get_form_kwargs()
        default_kwargs["company"] = self.request.user.company
        return default_kwargs

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
        return redirect(
            'applications:application_detail',
            pk=self.kwargs['pk']
        )


class ManualApplicationView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Applicant
    form_class = ApplicationForm
    template_name = 'applications/manual_application.html'
    success_message = _('Application manually added.')

    def get_form_kwargs(self):
        kwargs = super(ManualApplicationView, self).get_form_kwargs()
        kwargs.update(
            {'opening': get_object_or_404(Opening, id=self.kwargs['opening_id'])}
        )
        return kwargs

    def form_valid(self, form):
        self.success_url = reverse(
            'applications:list_applications',
            kwargs={'opening_id': form.opening.id}
        )
        return super(ManualApplicationView, self).form_valid(form)


class BoardView(LoginRequiredMixin, TemplateView):
    template_name = 'applications/kanban.html'

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)

        board_data = defaultdict(list)

        stages = InterviewStage.objects.filter(company=self.request.user.company)
        applications = Application.objects.filter(
            opening__company=self.request.user.company
        ).prefetch_related('stage_transitions__stage', 'applicant')
        for stage in stages:
            board_data[stage] = []
            for application in applications:
                if stage == application.current_stage():
                    board_data[stage].append(application)

        context['board'] = board_data
        context['full_width'] = True
        return context


class UpdatePositionsAjaxView(JSONResponseMixin, AjaxResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        data = json.loads(request.POST.get('data'))

        if data.get('stage'):
            stage = int(data.get('stage'))

        positions = data.get('positions')

        if positions:
            for position in positions:
                application_id, new_position = position

                application = Application.objects.filter(
                    id=int(application_id),
                    opening__company=self.request.user.company
                ).prefetch_related("stage_transitions__stage")[0]

                application.position = new_position
                application.save()

                if data.get('stage'):
                    current_stage = application.current_stage()
                    if not current_stage or current_stage.id != stage:
                        ApplicationStageTransition.objects.create(
                            application=application,
                            user=self.request.user,
                            stage=InterviewStage.objects.get(id=stage)
                        )

                result = {'status': 'success'}
        else:
            result = {'status': 'error'}

        return self.render_json_response(result)
