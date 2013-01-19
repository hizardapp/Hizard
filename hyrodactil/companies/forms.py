from django import forms

from .models import Company, Department, Question


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'label', 'type', 'options',)