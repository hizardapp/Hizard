from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView
from django.utils.translation import ugettext_lazy as _

from braces.views import LoginRequiredMixin

from .forms import DepartmentForm, QuestionForm, InterviewStageForm
from .models import Department, Question, InterviewStage
from companies.models import Company
from core.views import MessageMixin, RestrictedListView, RestrictedUpdateView
from core.views import RestrictedDeleteView

class DepartmentRestrictedListView(LoginRequiredMixin, RestrictedListView):
    model = Department


class DepartmentCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    action = 'created'
    success_url = reverse_lazy('companysettings:list_departments')
    success_message = _('Department created.')

    def form_valid(self, form):
        department = form.save(commit=False)
        department.company = Company.objects.get(id=self.request.user.company.id)
        department.save()
        return super(DepartmentCreateView, self).form_valid(form)


class DepartmentUpdateView(LoginRequiredMixin, MessageMixin, RestrictedUpdateView):
    model = Department
    form_class = DepartmentForm
    action = 'updated'
    success_url = reverse_lazy('companysettings:list_departments')
    success_message = _('Department updated.')


class DepartmentDeleteView(LoginRequiredMixin, RestrictedDeleteView):
    model = Department
    success_url = reverse_lazy('companysettings:list_departments')
    success_message = _('Department deleted.')


class QuestionRestrictedListView(LoginRequiredMixin, RestrictedListView):
    model = Question


class QuestionCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = Question
    form_class = QuestionForm
    action = 'created'
    success_url = reverse_lazy('companysettings:list_questions')
    success_message = _('Question created.')

    def form_valid(self, form):
        question = form.save(commit=False)
        question.company = Company.objects.get(id=self.request.user.company.id)
        question.save()
        return super(QuestionCreateView, self).form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, MessageMixin, RestrictedUpdateView):
    model = Question
    form_class = QuestionForm
    action = 'updated'
    success_url = reverse_lazy('companysettings:list_questions')
    success_message = _('Question updated.')


class InterviewStageRestrictedListView(LoginRequiredMixin, RestrictedListView):
    model = InterviewStage


class InterviewStageCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    model = InterviewStage
    form_class = InterviewStageForm
    action = 'created'
    success_url = reverse_lazy('companysettings:list_stages')
    success_message = _('Stage created.')

    def form_valid(self, form):
        stage = form.save(commit=False)
        stage.company = self.request.user.company
        stage.save()
        return super(InterviewStageCreateView, self).form_valid(form)


class InterviewStageUpdateView(LoginRequiredMixin, MessageMixin, RestrictedUpdateView):
    model = InterviewStage
    form_class = InterviewStageForm
    action = 'updated'
    success_url = reverse_lazy('companysettings:list_stages')
    success_message = _('Stage updated.')
