from django import forms

from .models import Application, ApplicationAnswer


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        self.opening = kwargs.pop('opening')
        super(ApplicationForm, self).__init__(*args, **kwargs)

        for question in self.opening.questions.all():
            field_name = 'q_%s' % question.slug

            if question.type == 'textbox':
                self.fields[field_name] = forms.CharField(label=question.name)
            elif question.type == 'textarea':
                self.fields[field_name] = forms.CharField(label=question.name, widget=forms.Textarea)
            elif question.type == 'checkbox':
                self.fields[field_name] = forms.BooleanField(label=question.name)
            elif question.type == 'file':
                self.fields[field_name] = forms.FileField(label=question.name)

            if not question.is_required:
                self.fields[field_name].required = False

    def save(self):
        application = Application(
            first_name=self.cleaned_data['first_name'], last_name=self.cleaned_data['last_name'],
            opening=self.opening
        )
        application.save()
        questions = self.opening.questions.all()

        for field in self.cleaned_data:
            if field.startswith('q_'):
                question = questions.filter(slug=field[2:])[0]

                if isinstance(self.fields[field], forms.FileField):
                    answer = 'look into self.files and save the file'
                else:
                    answer = self.cleaned_data[field]

                application_answer = ApplicationAnswer()
                application_answer.application = application
                application_answer.question = question
                application_answer.answer = answer
                application_answer.save()
