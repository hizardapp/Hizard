import os
import uuid

from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from companysettings.models import InterviewStage

from .models import (
    Applicant, Application, ApplicationAnswer, ApplicationStageTransition,
    ApplicationMessage
)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('first_name', 'last_name', 'email', 'resume')

    def __init__(self, *args, **kwargs):
        self.opening = kwargs.pop('opening')
        super(ApplicationForm, self).__init__(*args, **kwargs)

        if not self.opening:
            return

        for question in self.opening.questions.all():
            field_name = 'q_%s' % question.slug

            if question.type_field == 'textbox':
                self.fields[field_name] = forms.CharField(label=question.name)
            elif question.type_field == 'textarea':
                self.fields[field_name] = forms.CharField(
                    label=question.name, widget=forms.Textarea)
            elif question.type_field == 'checkbox':
                self.fields[field_name] = forms.BooleanField(label=question.name)
            elif question.type_field == 'file':
                self.fields[field_name] = forms.FileField(label=question.name)

            self.fields[field_name].required = False

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label += '*'

    def clean_resume(self):
        '''
        Make sure we really have a pdf file
        '''
        resume = self.cleaned_data['resume']

        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError(_('File type is not supported'))

            # mime type of a pdf is application/pdf
            filetype = resume.content_type.split('/')

            if len(filetype) > 1 and filetype[1] != 'pdf':
                raise forms.ValidationError(_('File type is not supported'))

        return resume

    def _assure_directory_exists(self):
        '''
        Creates the company directory in media/uploads if it doesn't exist
        already.
        '''
        path = '%s/uploads/%d' % (settings.MEDIA_ROOT, self.opening.company.id)

        if not os.path.exists(path):
            os.makedirs(path)

    def _get_random_filename(self, filename):
        '''
        Use uuid to generate a unique filename and adds the file extension
        '''
        new_filename = str(uuid.uuid4())
        extension = filename.split('.')[-1]
        new_filename += '.%s' % extension

        return new_filename

    def _save_file(self, file):
        '''
        Saves the files uploaded by an applicant into media/uploads/company_id
        '''
        filename = self._get_random_filename(file.name)
        upload_path = '/uploads/%d/%s' % (self.opening.company.id, filename)
        path = '%s/%s' % (settings.MEDIA_ROOT, upload_path)
        destination = open(path, 'wb+')

        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        return upload_path

    def save(self, commit=True):
        try:
            applicant = Applicant.objects.get(email=self.cleaned_data['email'])
        except Applicant.DoesNotExist:
            applicant = Applicant(
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                resume=self.cleaned_data['resume']
            )
            applicant.save()

        application = Application(
            applicant=applicant,
            opening=self.opening
        )
        application.save()

        stage = InterviewStage.objects.filter(
            company=self.opening.company
        ).order_by('position')[0]

        if stage:
            ApplicationStageTransition.objects.create(
                application=application,
                stage=stage
            )

        questions = self.opening.questions.all()

        for field in self.cleaned_data:
            if field.startswith('q_'):
                question = questions.filter(slug=field[2:])[0]
                answer = None

                if isinstance(self.fields[field], forms.FileField):
                    self._assure_directory_exists()
                    temp_file = self.files.get(field, None)

                    if temp_file:
                        answer = self._save_file(self.files[field])
                else:
                    answer = self.cleaned_data[field]

                if answer is not None:
                    application_answer = ApplicationAnswer()
                    application_answer.application = application
                    application_answer.question = question
                    application_answer.answer = answer
                    application_answer.save()

        return applicant


class ApplicationFilterForm(forms.Form):
    stages = forms.MultipleChoiceField(
        required=False,
        widget=CheckboxSelectMultiple
    )
    openings = forms.MultipleChoiceField(
        required=False,
        widget=CheckboxSelectMultiple
    )

    def __init__(self, company, *args, **kwargs):
        super(ApplicationFilterForm, self).__init__(*args, **kwargs)
        self.fields['stages'].choices = [
            (str(o.pk), o.name) for o in company.interviewstage_set.all()
        ]

        self.fields['openings'].choices = [
            (str(o.pk), o.title) for o in company.opening_set.all()
        ]


class ApplicationStageTransitionForm(forms.ModelForm):
    def __init__(self, company, *args, **kwargs):
        super(ApplicationStageTransitionForm, self).__init__(*args, **kwargs)
        self.fields['stage'].queryset = InterviewStage.objects.filter(
            company=company
        )

    class Meta:
        model = ApplicationStageTransition
        fields = ('stage', 'note')
        widgets = {
            'note': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Additional comment',
                'cols': 55}),
        }


class ApplicationMessageForm(forms.ModelForm):
    class Meta:
        widgets = {
            'parent': forms.HiddenInput(),
        }
        model = ApplicationMessage
        fields = ('body', 'parent')
