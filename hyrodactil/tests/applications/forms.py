import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from ..factories._applications import ApplicantFactory
from ..factories._companysettings import InterviewStageFactory
from ..factories._companies import CompanyFactory
from ..factories._openings import OpeningFactory, OpeningWithQuestionFactory
from applications.forms import (
    ApplicationForm, ApplicationStageTransitionForm
)
from applications.models import Applicant


class ApplicationFormTests(TestCase):
    form_data = {
        'first_name': 'Bob',
        'last_name': 'Marley',
        'email': 'bob@marley.jah'
    }

    question_data = {
        'question-1': 'Lalala'
    }

    def _get_temporary_file(self, type='application/pdf', extension='pdf'):
        io = StringIO.StringIO()
        io.write('foo')
        text_file = InMemoryUploadedFile(
            io, None, 'foo.%s' % extension, type, io.len, None
        )
        text_file.seek(0)
        return text_file

    def test_application_without_questions_valid(self):
        opening = OpeningFactory()

        files = {'resume': self._get_temporary_file()}
        form = ApplicationForm(self.form_data, files, opening=opening)

        self.assertTrue(form.is_valid())

    def test_application_without_questions_invalid(self):
        opening = OpeningFactory()
        invalid = dict(self.form_data)
        del invalid['first_name']

        files = {'resume': self._get_temporary_file()}
        form = ApplicationForm(invalid, files, opening=opening)
        self.assertFalse(form.is_valid())

    def test_application_with_questions_valid(self):
        opening = OpeningWithQuestionFactory()
        data = dict(self.form_data)
        data.update(self.question_data)

        files = {'resume': self._get_temporary_file()}
        form = ApplicationForm(data, files, opening=opening)

        self.assertTrue(form.is_valid())

    def test_application_with_missing_required_valid(self):
        opening = OpeningWithQuestionFactory()
        data = dict(self.form_data)
        data.update(self.question_data)
        del data['question-1']

        files = {'resume': self._get_temporary_file()}
        form = ApplicationForm(data, files, opening=opening)

        self.assertFalse(form.is_valid())

    def test_should_be_valid_if_resume_is_doc_docx(self):
        opening = OpeningFactory()
        files = {'resume': self._get_temporary_file(
          type='application/msword', extension='.DOC')}
        form = ApplicationForm(self.form_data, files, opening=opening)
        self.assertTrue(form.is_valid())

        files = {'resume': self._get_temporary_file(
          type='application/vnd.oasis.opendocument.text', extension='.dOcX')}
        form = ApplicationForm(self.form_data, files, opening=opening)
        self.assertTrue(form.is_valid())

    def test_should_not_be_valid_if_resume_not_pdf(self):
        opening = OpeningFactory()

        files = {'resume': self._get_temporary_file(type='evil/hacker')}
        form = ApplicationForm(self.form_data, files, opening=opening)
        self.assertFalse(form.is_valid())

        files = {'resume': self._get_temporary_file(extension='py')}
        form = ApplicationForm(self.form_data, files, opening=opening)
        self.assertFalse(form.is_valid())

    def test_should_not_create_new_applicant_if_exists(self):
        ApplicantFactory(email='bob@marley.jah')
        company = CompanyFactory()
        opening = OpeningFactory(company=company)
        stage = InterviewStageFactory(tag='RECEIVED')

        files = {'resume': self._get_temporary_file()}
        form = ApplicationForm(self.form_data, files, opening=opening)
        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(Applicant.objects.count(), 1)

    def test_only_show_company_stages(self):
        coca_cola = CompanyFactory()
        s_ic = InterviewStageFactory(name="S-IC", company=coca_cola)
        s_ii = InterviewStageFactory(name="S-II", company=CompanyFactory())
        form = ApplicationStageTransitionForm(coca_cola)

        def just_pks(choices):
            return [pk for pk, choice in choices]
        pks = just_pks(form["stage"].field.choices)
        self.assertTrue(s_ic.pk in pks)
        self.assertTrue(s_ii.pk not in pks)
