from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView

from braces.views import LoginRequiredMixin

from .forms import CompanyForm, DepartmentForm, QuestionForm
from .models import Company, Department, Question


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    success_url = reverse_lazy('jobs:list_openings')

    def form_valid(self, form):
        company = form.save(commit=False)
        company.owner = self.request.user
        company.save()
        return super(CompanyCreateView, self).form_valid(form)


class DepartmentActionMixin(object):
    def form_valid(self, form):
        msg = 'Department {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(DepartmentActionMixin, self).form_valid(form)


class DepartmentListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        company = get_object_or_404(Company, owner=self.request.user)
        return Department.objects.filter(company=company)


class DepartmentCreateView(LoginRequiredMixin, DepartmentActionMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    action = 'created'
    success_url = reverse_lazy('companies:list_departments')

    def form_valid(self, form):
        department = form.save(commit=False)
        department.company = Company.objects.get(owner=self.request.user)
        department.save()
        return super(DepartmentCreateView, self).form_valid(form)


class DepartmentUpdateView(LoginRequiredMixin, DepartmentActionMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    action = 'updated'
    success_url = reverse_lazy('companies:list_departments')


class QuestionListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        company = get_object_or_404(Company, owner=self.request.user)
        return Question.objects.filter(company=company)


class QuestionActionMixin(object):
    def form_valid(self, form):
        msg = 'Question {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(QuestionActionMixin, self).form_valid(form)


class QuestionCreateView(LoginRequiredMixin, QuestionActionMixin, CreateView):
    model = Question
    form_class = QuestionForm
    action = 'created'
    success_url = reverse_lazy('companies:list_questions')

    def form_valid(self, form):
        question = form.save(commit=False)
        question.company = Company.objects.get(owner=self.request.user)
        question.save()
        return super(QuestionCreateView, self).form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, QuestionActionMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    action = 'updated'
    success_url = reverse_lazy('companies:list_questions')
