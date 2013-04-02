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
        fields = ('name', 'initial',)

    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company')
        super(InterviewStageForm, self).__init__(*args, **kwargs)

    def clean_initial(self):
        data = self.cleaned_data['initial']

        if data:
            existing_initial = InterviewStage.objects.filter(
                company=self.company, initial=True
            )
            # Should never have more than 1 but safer to loop there, in case
            for stage in existing_initial:
                stage.initial = False
                stage.save()

        return data


class CustomUserInviteForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def save(self, commit=True, company=None, is_company_admin=False):
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
                    is_company_admin=is_company_admin,
                    company=company)
            return user
