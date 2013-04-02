from django import forms
from django.utils.translation import ugettext_lazy as _

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
            ).count()
            if existing_initial > 0:
                raise forms.ValidationError(
                    _('You can only one initial stage at a given time')
                )

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
