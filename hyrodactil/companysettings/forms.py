from django import forms

from .models import Department, Question, InterviewStage


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'label', 'type', 'options',)


class InterviewStageForm(forms.ModelForm):
    class Meta:
        model = InterviewStage
        fields = ('name',)
