from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'subdomain', 'website', 'description')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = _('Company name')
        self.fields['subdomain'].label = _('Url of your career site (***.hizard.com)')
        self.fields['website'].label = _('Company website (will appear on career site)')
        self.fields['description'].label = _('Company description (will appear on career site)')

    def clean_subdomain(self):
        return self.cleaned_data['subdomain'].lower()
