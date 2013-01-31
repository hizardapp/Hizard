from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from braces.views import LoginRequiredMixin

from .forms import DepartmentForm, QuestionForm, InterviewStageForm
from .models import Department, Question, InterviewStage
from companies.models import Company
from core.views import ListCompanyObjectsMixin, UserAllowedActionMixin


class DepartmentListView(LoginRequiredMixin, ListCompanyObjectsMixin, ListView):
    model = Department


class DepartmentActionMixin(object):
    def form_valid(self, form):
        msg = 'Department {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(DepartmentActionMixin, self).form_valid(form)


class DepartmentCreateView(LoginRequiredMixin, DepartmentActionMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    action = 'created'
    success_url = reverse_lazy('companysettings:list_departments')

    def form_valid(self, form):
        department = form.save(commit=False)
        department.company = Company.objects.get(id=self.request.user.company.id)
        department.save()
        return super(DepartmentCreateView, self).form_valid(form)


class DepartmentUpdateView(LoginRequiredMixin, UserAllowedActionMixin, DepartmentActionMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    action = 'updated'
    success_url = reverse_lazy('companysettings:list_departments')


class QuestionListView(LoginRequiredMixin, ListCompanyObjectsMixin, ListView):
    model = Question


class QuestionActionMixin(object):
    def form_valid(self, form):
        msg = 'Question {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(QuestionActionMixin, self).form_valid(form)


class QuestionCreateView(LoginRequiredMixin, QuestionActionMixin, CreateView):
    model = Question
    form_class = QuestionForm
    action = 'created'
    success_url = reverse_lazy('companysettings:list_questions')

    def form_valid(self, form):
        question = form.save(commit=False)
        question.company = Company.objects.get(id=self.request.user.company.id)
        question.save()
        return super(QuestionCreateView, self).form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, UserAllowedActionMixin, QuestionActionMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    action = 'updated'
    success_url = reverse_lazy('companysettings:list_questions')


class InterviewStageListView(LoginRequiredMixin, ListCompanyObjectsMixin, ListView):
    model = InterviewStage


class InterviewStageActionMixin(object):
    def form_valid(self, form):
        msg = 'Stage {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(InterviewStageActionMixin, self).form_valid(form)


class InterviewStageCreateView(LoginRequiredMixin, InterviewStageActionMixin, CreateView):
    model = InterviewStage
    form_class = InterviewStageForm
    action = 'created'
    success_url = reverse_lazy('companysettings:list_stages')

    def form_valid(self, form):
        stage = form.save(commit=False)
        stage.company = self.request.user.company
        stage.save()
        return super(InterviewStageCreateView, self).form_valid(form)


class InterviewStageUpdateView(LoginRequiredMixin, UserAllowedActionMixin, InterviewStageActionMixin, UpdateView):
    model = InterviewStage
    form_class = InterviewStageForm
    action = 'updated'
    success_url = reverse_lazy('companysettings:list_stages')
