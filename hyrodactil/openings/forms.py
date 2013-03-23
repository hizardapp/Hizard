
from django import forms
from django.utils.translation import ugettext_lazy as _

from companysettings.models import Question, Department
from .models import Opening, OpeningQuestion


class OpeningQuestionForm(forms.Form):
    included = forms.BooleanField(required=False)
    required = forms.BooleanField(required=False)

    def __init__(self, question, *args, **kwargs):
        super(OpeningQuestionForm, self).__init__(*args, **kwargs)
        self.question = question

    def clean(self):
        cleaned_data = super(OpeningQuestionForm, self).clean()
        if cleaned_data.get('required') and not cleaned_data.get('included'):
            raise forms.ValidationError(_("Can't require a question not included"))

        return cleaned_data


class OpeningQuestionFormset(object):
    def __init__(self, company, data=None):
        self.company = company
        self.questions = company.question_set.all()
        self.forms = []

        for question in self.questions:
            prefix = 'oq-%d' % question.id
            self.forms.append(
                OpeningQuestionForm(question=question, prefix=prefix, data=data)
            )

    def __iter__(self):
        for form in self.forms:
            yield form

    def is_valid(self):
        return all([form.is_valid() for form in self.forms])

    def save(self, opening):
        for form in self.forms:
            if form.cleaned_data.get('included'):
                OpeningQuestion.objects.create(
                    opening=opening,
                    question=form.question,
                    required=form.cleaned_data['required']
                )


class OpeningForm(forms.ModelForm):
    new_department = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Opening
        fields = ('title', 'description', 'is_private', 'department',
                  'loc_country', 'loc_city', 'loc_postcode',)

    def __init__(self, company, opening_questions=None, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.company = company

        self.opening_questions = OpeningQuestionFormset(company=company, data=kwargs.get('data'))

        self.fields['is_private'].label = _("Private opening")

    def is_valid(self):
        is_valid = super(OpeningForm, self).is_valid()

        if self.opening_questions.is_valid() and is_valid:
            return True

        return False

    def save(self, *args, **kwargs):
        if (self.cleaned_data.get("new_department") and
                not self.cleaned_data.get("department")):
            self.instance.department = Department.objects.create(
                    name=self.cleaned_data.get("new_department"),
                    company=self.company)
        self.instance.company = self.company
        opening = super(OpeningForm, self).save(*args, **kwargs)

        self.opening_questions.save(opening)

        return opening
