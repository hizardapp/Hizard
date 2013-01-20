from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView

from braces.views import LoginRequiredMixin, SuccessURLRedirectListMixin

from .forms import CompanyForm, DepartmentForm, QuestionForm
from .models import Company, Department, Question


class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm

    def form_valid(self, form):
        company = form.save(commit=False)
        # TODO: remove
        company.owner = User.objects.get(username='vincent')
        #company.user = self.request.user
        company.save()


class DepartmentActionMixin(object):
    def form_valid(self, form):
        msg = 'Department {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(DepartmentActionMixin, self).form_valid(form)


class DepartmentListView(ListView):
    def get_queryset(self):
        # TODO: remove
        self.request.user = User.objects.get(username='vincent')
        company = get_object_or_404(Company, owner=self.request.user)
        return Department.objects.filter(company=company)


class DepartmentCreateView(DepartmentActionMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    action = 'created'
    success_url = reverse_lazy('companies:list_departments')

    def form_valid(self, form):
        department = form.save(commit=False)
        # TODO: remove
        department.company = Company.objects.get(owner=User.objects.get(username='vincent'))
        #department.company = Company.objects.get(owner=self.request.user)
        department.save()
        return super(DepartmentCreateView, self).form_valid(form)


class DepartmentUpdateView(DepartmentActionMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    action = 'updated'
    success_url = reverse_lazy('companies:list_departments')


class QuestionListView(ListView):
    def get_queryset(self):
        # TODO: remove
        self.request.user = User.objects.get(username='vincent')
        company = get_object_or_404(Company, owner=self.request.user)
        return Question.objects.filter(company=company)


class QuestionActionMixin(object):
    def form_valid(self, form):
        msg = 'Question {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(QuestionActionMixin, self).form_valid(form)


class QuestionCreateView(QuestionActionMixin, CreateView):
    model = Question
    form_class = QuestionForm
    action = 'created'
    success_url = reverse_lazy('companies:list_questions')

    def form_valid(self, form):
        question = form.save(commit=False)
        # TODO: remove
        question.company = Company.objects.get(owner=User.objects.get(username='vincent'))
        #department.company = Company.objects.get(owner=self.request.user)
        question.save()
        return super(QuestionCreateView, self).form_valid(form)


class QuestionUpdateView(QuestionActionMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    action = 'updated'
    success_url = reverse_lazy('companies:list_questions')
