from django import forms
from django.utils.translation import ugettext_lazy as _

from companysettings.models import Question, Department
from .models import Opening


class OpeningForm(forms.ModelForm):
    new_department = forms.CharField(required=False, widget=forms.HiddenInput)
    questions = forms.MultipleChoiceField(required=False, widget=forms.CheckboxInput())
    questions_required = forms.MultipleChoiceField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Opening
        fields = ('title', 'description', 'is_private', 'department',
                  'loc_country', 'loc_city', 'loc_postcode',)

    def __init__(self, company, opening_questions=None, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.company = company

        self.saved_questions =  {}
        self.editing = False

        if opening_questions:
            for opening_question in opening_questions:
                self.saved_questions[opening_question.id] = opening_question.required
                self.editing = True

        self.questions_objects = Question.objects.filter(company_id=company.id)

        self.fields['is_private'].label = _("Private opening")

    def save(self, *args, **kwargs):
        #print self.cleaned_data['questions']
        if (self.cleaned_data["new_department"] and
                not self.cleaned_data["department"]):
            self.instance.department = Department.objects.create(
                    name=self.cleaned_data["new_department"],
                    company=self.company)
        self.instance.company = self.company
        return super(OpeningForm, self).save(*args, **kwargs)
