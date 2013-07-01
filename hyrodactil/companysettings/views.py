from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic import CreateView, TemplateView, View
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin

from .forms import (
    InterviewStageForm, CompanyInformationForm
)
from .forms import CustomUserInviteForm
from .models import InterviewStage
from companies.models import Company
from accounts.models import CustomUser
from core.views import MessageMixin, QuickDeleteView, RestrictedUpdateView
from core.views import RestrictedListView


class CreateUpdateAjaxView(
    LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View
):
    def post_ajax(self, request, *args, **kwargs):
        data = request.POST.copy()

        if 'id' in data:
            obj_to_update = self.model.objects.filter(id=int(data['id']))
            if obj_to_update:
                form = self.form(data, instance=obj_to_update[0])
            else:
                return self.render_json_response({
                    'result': 'error',
                    'message': unicode(self.message_not_exist)
                })
        else:
            form = self.form(data)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.company = self.request.user.company
            obj.save()
            return self.render_json_response({
                'result': 'success',
                'id': obj.id,
                'message': unicode(self.message_success)
            })
        else:
            return self.render_json_response({
                'result': 'error',
                'errors': form.errors,
                'message': unicode(self.message_errors)
            })


class InterviewStageListView(LoginRequiredMixin, TemplateView):
    model = InterviewStage
    template_name = 'companysettings/interviewstage_list.html'

    def get_context_data(self, **kwargs):
        stages = InterviewStage.objects.filter(
            company=self.request.user.company, position__isnull=False
        )
        context = super(InterviewStageListView, self).get_context_data(**kwargs)
        context['stages'] = stages

        return context


class InterviewStageCreateUpdateView(CreateUpdateAjaxView):
    model = InterviewStage
    form = InterviewStageForm
    message_success = _('Stage saved.')
    message_errors = _('Please correct the errors below.')
    message_not_exist = _('The stage does not exist.')


class InterviewStageDeleteView(LoginRequiredMixin, QuickDeleteView):
    model = InterviewStage
    success_url = reverse_lazy('companysettings:list_stages')
    success_message = _('Stage deleted.')

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        # Can't delete those 2, we use them to classify
        if self.object.accepted or self.object.rejected:
            raise Http404

        count_stages = InterviewStage.objects.filter(
            company=self.request.user.company
        ).count()
        if count_stages > 1:
            return super(InterviewStageDeleteView, self).get(*args, **kwargs)
        else:
            messages.error(
                self.request, _('You need to have at least one stage.')
            )
            return redirect(self.success_url)


class InterviewStageReorderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        stage = InterviewStage.objects.get(id=kwargs.pop('pk'))
        direction = kwargs.pop('direction')

        if direction == 'up':
            swapping_stage = stage.get_previous_stage()
        else:
            swapping_stage = stage.get_next_stage()

        if stage.swap_position(swapping_stage):
            messages.success(self.request, 'Stages reordered.')
        else:
            messages.info(self.request, "Couldn't reorder the stages.")
        return HttpResponseRedirect(reverse('companysettings:list_stages'))


class InviteUserCreateView(LoginRequiredMixin, CreateView):
    template_name = "companysettings/customuser_list.html"
    model = CustomUser
    form_class = CustomUserInviteForm
    success_url = reverse_lazy('companysettings:list_users')

    def get_context_data(self, **kwargs):
        context = super(InviteUserCreateView, self).get_context_data(**kwargs)
        context['users'] = CustomUser.objects.filter(
            company=self.request.user.company
        )
        return context

    def form_valid(self, form):
        form.save(company=self.request.user.company)
        return redirect(self.success_url)


class UpdateCompanyInformationView(
    LoginRequiredMixin, MessageMixin, RestrictedUpdateView
):
    model = Company
    form_class = CompanyInformationForm
    success_url = reverse_lazy('dashboard:dashboard')
    success_message = _('Company information updated.')
    template_name = 'companysettings/information_form.html'

    def get_object(self):
        return self.request.user.company
