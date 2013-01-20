from django import forms

from .models import Opening


class OpeningForm(forms.ModelForm):
    class Meta:
        model = Opening
        fields = ('title', 'description', 'is_private', 'department',
                  'loc_country', 'loc_city', 'loc_postcode', 'questions',)
        widgets = {'questions': forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.fields['questions'].help_text = ''
