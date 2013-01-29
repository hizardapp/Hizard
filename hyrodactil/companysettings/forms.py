from django import forms

from .models import Department, Question


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'label', 'type', 'options',)
