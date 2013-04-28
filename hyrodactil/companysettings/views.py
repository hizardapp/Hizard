from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView, View
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from .forms import DepartmentForm, QuestionForm, InterviewStageForm, CompanyInformationForm
from .forms import CustomUserInviteForm
from .models import Department, Question, InterviewStage
from companies.models import Company
from accounts.models import CustomUser
from core.views import MessageMixin, QuickDeleteView, RestrictedUpdateView
from core.views import RestrictedListView


class SettingsHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'companysettings/settings.html'


class ListViewWithDropdown(LoginRequiredMixin, RestrictedListView):
    def get_context_data(self, **kwargs):
        context = super(ListViewWithDropdown, self).get_context_data(**kwargs)
        form_with_errors = self.request.session.get('used_form', None)
        if form_with_errors:
            context['form'] = form_with_errors
            context['has_errors'] = True
            del self.request.session['used_form']
            object_id = self.request.session.get('object_id', None)

            if object_id:
                context['error_object_id'] = object_id
                del self.request.session['object_id']

        else:
            context['form'] = self.form()

        return context


class DepartmentRestrictedListView(ListViewWithDropdown):
    model = Department
    form = DepartmentForm


class DepartmentCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    success_url = reverse_lazy('companysettings:list_departments')
    success_message = _('Department created.')

    def form_valid(self, form):
        department = form.save(commit=False)
        department.company = Company.objects.get(id=self.request.user.company.id)
        department.save()
        return super(DepartmentCreateView, self).form_valid(form)

    def form_invalid(self, form):
        self.request.session['used_form'] = form
        return redirect(self.success_url)


class DepartmentUpdateView(LoginRequiredMixin, MessageMixin,
        RestrictedUpdateView):
    model = Department
    form_class = DepartmentForm
    success_url = reverse_lazy('companysettings:list_departments')
    success_message = _('Department updated.')

    def form_invalid(self, form):
        self.request.session['used_form'] = form
        self.request.session['object_id'] = self.object.id
        return redirect(self.success_url)


class DepartmentDeleteView(LoginRequiredMixin, QuickDeleteView):
    model = Department
    success_url = reverse_lazy('companysettings:list_departments')
    success_message = _('Department deleted.')

class QuestionRestrictedListView(ListViewWithDropdown):
    model = Question
    form = QuestionForm


class QuestionCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('companysettings:list_questions')
    success_message = _('Question created.')

    def form_valid(self, form):
        question = form.save(commit=False)
        question.company = Company.objects.get(id=self.request.user.company.id)
        question.save()
        return super(QuestionCreateView, self).form_valid(form)

    def form_invalid(self, form):
        self.request.session['used_form'] = form
        return redirect(self.success_url)


class QuestionUpdateView(LoginRequiredMixin, MessageMixin,
        RestrictedUpdateView):
    model = Question
    form_class = QuestionForm
    success_url = reverse_lazy('companysettings:list_questions')
    success_message = _('Question updated.')

    def form_invalid(self, form):
        self.request.session['used_form'] = form
        self.request.session['object_id'] = self.object.id
        return redirect(self.success_url)


class QuestionDeleteView(LoginRequiredMixin, QuickDeleteView):
    model = Question
    success_url = reverse_lazy('companysettings:list_questions')
    success_message = _('Question deleted.')


class InterviewStageListView(LoginRequiredMixin, RestrictedListView):
    model = InterviewStage


class InterviewStageCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = InterviewStage
    form_class = InterviewStageForm
    success_url = reverse_lazy('companysettings:list_stages')
    success_message = _('Stage created.')

    def get_form_kwargs(self):
        kwargs = super(InterviewStageCreateView, self).get_form_kwargs()
        kwargs.update({'company': self.request.user.company})
        return kwargs

    def form_valid(self, form):
        stage = form.save(commit=False)
        stage.company = self.request.user.company
        stage.save()
        return super(InterviewStageCreateView, self).form_valid(form)


class InterviewStageUpdateView(LoginRequiredMixin, MessageMixin,
        RestrictedUpdateView):
    model = InterviewStage
    form_class = InterviewStageForm
    success_url = reverse_lazy('companysettings:list_stages')
    success_message = _('Stage updated.')

    def get_form_kwargs(self):
        kwargs = super(InterviewStageUpdateView, self).get_form_kwargs()
        kwargs.update({'company': self.request.user.company})
        return kwargs


class InterviewStageDeleteView(LoginRequiredMixin, QuickDeleteView):
    model = InterviewStage
    success_url = reverse_lazy('companysettings:list_stages')
    success_message = _('Stage deleted.')

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        count_stages = InterviewStage.objects.filter(
                company=self.request.user.company).count()
        if count_stages > 1:
            return super(InterviewStageDeleteView, self).get(*args, **kwargs)
        else:
            messages.error(
                self.request, _('You need to have at least one stage.')
            )
            return redirect(self.success_url)


class InterviewStageReorderView(LoginRequiredMixin, MessageMixin, View):
    def get(self, request, *args, **kwargs):
        stage = InterviewStage.objects.get(id=kwargs.pop('pk'))
        direction = kwargs.pop('direction')

        if direction == 'up':
            swapping_stage = stage.get_previous_stage()
        else:
            swapping_stage = stage.get_next_stage()

        if stage.swap_position(swapping_stage):
            messages.info(self.request, 'Stages reordered.')
        else:
            messages.info(self.request, "Couldn't reorder the stages.")
        return HttpResponseRedirect(reverse('companysettings:list_stages'))


class UsersListView(ListViewWithDropdown):
    template_name = "companysettings/customuser_list.html"
    model = CustomUser
    form = CustomUserInviteForm


class InviteUserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserInviteForm
    success_url = reverse_lazy('companysettings:list_users')

    def form_valid(self, form):
        form.save(company=self.request.user.company)
        return redirect(self.success_url)


class UpdateCompanyInformationView(LoginRequiredMixin, MessageMixin,
        RestrictedUpdateView):
    model = Company
    form_class = CompanyInformationForm
    success_url = reverse_lazy('companysettings:settings_home')
    success_message = _('Company informations updated.')
    template_name = 'companysettings/information_form.html'

    def get_object(self):
        return self.request.user.company
