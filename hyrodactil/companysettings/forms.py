from django import forms
from companies.models import Company

from .models import InterviewStage
from accounts.models import CustomUser


class InterviewStageForm(forms.ModelForm):
    class Meta:
        model = InterviewStage
        fields = ('name',)


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
                name='Invited User',
                password=None,
                active=False,
                is_company_admin=is_company_admin,
                company=company
            )
            return user


class CompanyInformationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'website', 'description')
