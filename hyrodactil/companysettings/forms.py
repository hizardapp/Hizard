from django import forms

from .models import Department, Question, InterviewStage
from accounts.models import CustomUser


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'type',)


class InterviewStageForm(forms.ModelForm):
    class Meta:
        model = InterviewStage
        fields = ('name',)


class CustomUserInviteForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self, commit=True, company=None):
        """
        Save the user using the manager to make sure it creates the
        activation token and sens the activation email
        """
        email = self.cleaned_data["email"]

        if commit:
            user = CustomUser.objects.create_user(
                    email=email,
                    password=None,
                    active=False,
                    company=company)
            return user
