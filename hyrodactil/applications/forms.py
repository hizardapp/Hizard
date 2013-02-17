import os
import uuid

from django import forms

from .models import Applicant, Application, ApplicationAnswer


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        self.opening = kwargs.pop('opening')
        super(ApplicationForm, self).__init__(*args, **kwargs)

        if not self.opening:
            return

        for question in self.opening.questions.all():
            field_name = 'q_%s' % question.slug

            if question.type == 'textbox':
                self.fields[field_name] = forms.CharField(label=question.name)
            elif question.type == 'textarea':
                self.fields[field_name] = forms.CharField(label=question.name,
                    widget=forms.Textarea)
            elif question.type == 'checkbox':
                self.fields[field_name] = forms.BooleanField(label=question.name)
            elif question.type == 'file':
                self.fields[field_name] = forms.FileField(label=question.name)

            if not question.is_required:
                self.fields[field_name].required = False

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label += '*'

    def _assure_directory_exists(self):
        """
        Creates the company directory in media/uploads if it doesn't exist
        already.
        """
        path = 'media/uploads/%d' % self.opening.company.id

        if not os.path.exists(path):
            os.makedirs(path)

    def _get_random_filename(self, filename):
        """
        Use uuid to generate a unique filename and adds the file extension
        """
        new_filename = str(uuid.uuid4())
        extension = filename.split('.')[-1]
        new_filename += '.%s' % extension

        return new_filename

    def _save_file(self, file):
        """
        Saves the files uploaded by an applicant into media/uploads/company_id
        """
        filename = self._get_random_filename(file.name)
        path = 'media/uploads/%d/%s' %(self.opening.company.id, filename)
        destination = open(path, 'wb+')

        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        return filename

    def save(self):
        try:
            applicant = Applicant.objects.get(email=self.cleaned_data['email'])
        except Applicant.DoesNotExist:
            applicant = Applicant(
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email']
            )
            applicant.save()

        application = Application(
            applicant=applicant,
            opening=self.opening
        )
        application.save()
        questions = self.opening.questions.all()

        for field in self.cleaned_data:
            if field.startswith('q_'):
                question = questions.filter(slug=field[2:])[0]

                if isinstance(self.fields[field], forms.FileField):
                    self._assure_directory_exists()
                    answer = self._save_file(self.files[field])
                else:
                    answer = self.cleaned_data[field]

                application_answer = ApplicationAnswer()
                application_answer.application = application
                application_answer.question = question
                application_answer.answer = answer
                application_answer.save()
