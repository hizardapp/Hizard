from django import forms
from django.utils.translation import ugettext_lazy as _

from companysettings.models import Question, Department
from .models import Opening


class OpeningForm(forms.ModelForm):
    new_department = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Opening
        fields = ('title', 'description', 'is_private', 'department',
                  'loc_country', 'loc_city', 'loc_postcode', 'questions',)
        widgets = {'questions': forms.CheckboxSelectMultiple}

    def __init__(self, company, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.company = company

        question_field = self.fields['questions']
        question_field.help_text = ''
        question_field.queryset = Question.objects.filter(company_id=company.id)

        self.fields['is_private'].label = _("Private opening")
        self.fields['questions'].label = _("Included questions")

    def save(self, *args, **kwargs):
        if (self.cleaned_data["new_department"] and
                not self.cleaned_data["department"]):
            self.instance.department = Department.objects.create(
                    name=self.cleaned_data["new_department"],
                    company=self.company)
        self.instance.company = self.company
        return super(OpeningForm, self).save(*args, **kwargs)
