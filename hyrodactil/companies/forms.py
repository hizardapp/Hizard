from django import forms

from .models import Company, Department


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name',)