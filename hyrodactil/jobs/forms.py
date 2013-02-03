from django import forms

from companysettings.models import Question
from .models import Opening


class OpeningForm(forms.ModelForm):
    class Meta:
        model = Opening
        fields = ('title', 'description', 'is_private', 'department',
                  'loc_country', 'loc_city', 'loc_postcode', 'questions',)
        widgets = {'questions': forms.CheckboxSelectMultiple}

    def __init__(self, company, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        question_field = self.fields['questions']
        question_field.help_text = ''
        question_field.queryset = Question.objects.filter(company_id=company.id)
