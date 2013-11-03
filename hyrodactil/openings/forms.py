from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Opening


class OpeningForm(forms.ModelForm):
    class Meta:
        model = Opening
        fields = ('title', 'description', 'employment_type', 'is_private',
                  'department', 'country', 'city',)

    def __init__(self, company, *args, **kwargs):
        super(OpeningForm, self).__init__(*args, **kwargs)
        self.company = company

        if self.instance:
            self.questions = self.instance.questions.all()

        self.fields['is_private'].label = _("Private opening")

    def _clean_questions(self):
        self.questions_present = {}
        for field in self.data:
            if field.startswith('question') and self.data[field]:
                prefix, question_id = field.split("-")
                position = self.data['position-question-%s' % question_id]
                self.questions_present[field] = (position, self.data[field])

    def clean(self):
        self._clean_questions()
        return super(OpeningForm, self).clean()

    def save(self, *args, **kwargs):
        self.instance.company = self.company

        opening = super(OpeningForm, self).save(*args, **kwargs)

        if self.instance:
            for question in self.questions:
                field_name = 'question-' + str(question.id)
                if field_name not in self.questions_present:
                    question.delete()
                else:
                    present_position, present_title =\
                            self.questions_present[field_name]
                    if (question.title != present_title or
                        question.position != question.position):
                        question.position = present_position
                        question.title = present_title
                        question.save()
                    del self.questions_present[field_name]

            for field in self.questions_present:
                present_position, present_title = self.questions_present[field]
                opening.questions.create(title=present_title,
                                         position=present_position)

        return opening
