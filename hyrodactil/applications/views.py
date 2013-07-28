from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, CreateView, TemplateView

from braces.views import LoginRequiredMixin

from .forms import ApplicationStageTransitionForm, ApplicationMessageForm
from .forms import ApplicationForm
from .models import (
    Application, ApplicationMessage,
    ApplicationStageTransition, Applicant
)
from .threaded_discussion import group
from companysettings.models import InterviewStage
from core.views import MessageMixin, RestrictedListView
from customisable_emails import send_customised_email
from openings.models import Opening


class ApplicationListView(LoginRequiredMixin, RestrictedListView):
    model = Application

    def get_context_data(self, **kwargs):
        context = super(ApplicationListView, self).get_context_data(**kwargs)
        context['stages'] = InterviewStage.objects.filter(
            company=self.request.user.company
        )

        opening_id = self.kwargs.get('pk', None)

        if opening_id:
            opening = get_object_or_404(Opening, id=opening_id)
            context['application_list'] = context['application_list'].filter(
                opening=opening
            )
            context['opening'] = opening

        return context

    def get_queryset(self):
        qs = Application.objects.filter(
            opening__company=self.request.user.company
        ).order_by('opening').select_related(
            'applicant', 'opening', 'current_stage'
        )
        return qs


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
        return reverse(
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
    template_name = 'applications/application_detail.html'

    def get_application(self):
        try:
            return Application.objects.get(
                pk=self.kwargs['pk'],
                opening__company=self.request.user.company
            )
        except Application.DoesNotExist:
            raise Http404

    def get_form_kwargs(self):
        default_kwargs = super(ApplicationDetailView, self).get_form_kwargs()
        default_kwargs['company'] = self.request.user.company
        return default_kwargs

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        application = self.get_application()
        context['application'] = application
        context['discussion'] = group(application.applicationmessage_set.all())
        context['new_message_form'] = ApplicationMessageForm()
        context['user_rating'] = application.get_user_rating(context['user'])
        context['rating'] = application.get_rating()
        context['answers'] = application.answers.all()
        return context

    def form_valid(self, form):
        application = self.get_application()
        transition = form.save(commit=False)
        transition.application = application
        transition.user = self.request.user
        transition.save()
        application.current_stage = transition.stage
        application.save()

        if transition.stage.tag == "REJECTED":
            applicant = application.applicant
            opening = application.opening
            send_customised_email("application_rejected",
                company=opening.company,
                to=applicant.email,
                context=dict(applicant_first_name=applicant.first_name,
                  applicant_last_name=applicant.last_name,
                  company=mark_safe(opening.company.name),
                  opening=mark_safe(opening.title))
            )

        return redirect(
            'applications:application_detail',
            pk=self.kwargs['pk']
        )


class ManualApplicationView(LoginRequiredMixin, MessageMixin, FormView):
    model = Applicant
    form_class = ApplicationForm
    template_name = 'applications/manual_application.html'
    success_message = _('Application manually added.')

    def get_context_data(self, **kwargs):
        context = super(ManualApplicationView, self).get_context_data(**kwargs)
        context["opening"] = self.opening
        return context

    def get_form_kwargs(self):
        default_kwargs = super(ManualApplicationView, self).get_form_kwargs()
        self.opening = Opening.objects.get(
            pk=self.kwargs["opening_id"]
        )
        default_kwargs['opening'] = self.opening
        return default_kwargs

    def form_valid(self, form):
        self.success_url = reverse(
            'applications:list_applications_opening',
            args=[self.opening.id]
        )
        form.save()
        return super(ManualApplicationView, self).form_valid(form)


class RateView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        application = get_object_or_404(
            Application.objects.select_related('opening', 'opening__company'),
            id=self.kwargs['application_id']
        )
        if application.opening.company != request.user.company:
            raise Http404

        result = application.save_rating(request.user, self.kwargs['rating'])
        if result:
            messages.success(request, _('Application rated.'))
        else:
            messages.error(request, _("Couldn't rate the application"))

        return redirect(
            reverse('applications:application_detail', args=(application.id,))
        )


class HireView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        application = get_object_or_404(
            Application.objects.select_related('opening', 'opening__company'),
            id=self.kwargs['application_id']
        )
        if application.opening.company != request.user.company:
            raise Http404

        hired_stage = InterviewStage.objects.get(tag='HIRED')

        ApplicationStageTransition(
            application=application,
            user=request.user,
            stage=hired_stage
        ).save()

        applicant = application.applicant
        opening = application.opening
        send_customised_email("candidate_hired",
            company=request.user.company,
            to=applicant.email,
            context=dict(applicant_first_name=applicant.first_name,
              applicant_last_name=applicant.last_name,
              company=mark_safe(opening.company.name),
              opening=mark_safe(opening.title))
        )

        messages.success(request, _('Applicant marked as hired.'))

        return redirect(
            reverse('applications:application_detail', args=(application.id,))
        )
