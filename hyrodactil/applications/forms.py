import os

from django import forms
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

        for opening_question in self.opening.openingquestion_set.all().select_related('question'):
            question = opening_question.question
            field_name = 'q_%s' % question.slug

            if question.type_field == 'textbox':
                self.fields[field_name] = forms.CharField(label=question.name)
            elif question.type_field == 'textarea':
                self.fields[field_name] = forms.CharField(
                    label=question.name, widget=forms.Textarea)
            elif question.type_field == 'checkbox':
                self.fields[field_name] = forms.BooleanField(label=question.name)


            self.fields[field_name].required = opening_question.required

    def clean_resume(self):
        '''
        Make sure we really have a pdf file
        '''
        resume = self.cleaned_data['resume']

        if resume:
            if not any(resume.name.lower().endswith(extension)
                    for extension in Applicant.ALLOWED_EXTENSIONS):
                raise forms.ValidationError(_('File type is not supported'))

            if resume.content_type not in Applicant.ALLOWED_CONTENT_TYPES:
                raise forms.ValidationError(_('File type is not supported'))

        return resume

    def save(self, commit=True):
        try:
            applicant = Applicant.objects.get(email=self.cleaned_data['email'])
        except Applicant.DoesNotExist:
            applicant = Applicant.objects.create(
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                resume=self.cleaned_data['resume']
            )

        application = Application.objects.create(
            applicant=applicant,
            opening=self.opening
        )

        tmp_resume = application.applicant.resume.path
        base_name = os.path.basename(tmp_resume)

        final_resume = os.path.join('resumes',
                str(application.opening.company.id),
                base_name)
        absolute_final_resume = os.path.join(settings.MEDIA_ROOT, final_resume)

        try:
            os.makedirs(os.path.dirname(absolute_final_resume))
        except OSError:
            pass

        if os.path.exists(tmp_resume):
            os.rename(tmp_resume, absolute_final_resume)

        application.applicant.resume = final_resume
        application.applicant.save()

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
                answer = self.cleaned_data[field]

                if answer is not None:
                    application_answer = ApplicationAnswer()
                    application_answer.application = application
                    application_answer.question = question
                    application_answer.answer = answer
                    application_answer.save()

        return applicant


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
