import os
import shutil
import StringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from ..factories._applications import ApplicantFactory
from ..factories._openings import OpeningFactory, OpeningWithQuestionsFactory
from applications.forms import ApplicationForm
from applications.models import Applicant


class ApplicationFormTests(TestCase):
    form_data = {
        'first_name': 'Bob',
        'last_name': 'Marley',
        'email': 'bob@marley.jah'
    }

    question_data = {
        'q_single-line': 'Lalala',
        'q_multi-line': 'Lololo'
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

        files = { 'resume': self._get_temporary_file() }
        form = ApplicationForm(self.form_data, files, opening=opening)
        self.assertTrue(form.is_valid())

    def test_application_without_questions_invalid(self):
        opening = OpeningFactory()
        invalid = dict(self.form_data)
        del invalid['first_name']

        files = { 'resume': self._get_temporary_file() }
        form = ApplicationForm(invalid, files, opening=opening)
        self.assertFalse(form.is_valid())

    def test_application_with_questions_valid(self):
        opening = OpeningWithQuestionsFactory()
        data = dict(self.form_data)
        data.update(self.question_data)

        files = { 'resume': self._get_temporary_file() }
        form = ApplicationForm(data, files, opening=opening)
        self.assertTrue(form.is_valid())

    def test_application_with_questions_invalid(self):
        opening = OpeningWithQuestionsFactory()
        data = dict(self.form_data)
        data.update(self.question_data)
        del data['q_single-line']

        files = { 'resume': self._get_temporary_file() }
        form = ApplicationForm(data, files, opening=opening)
        self.assertFalse(form.is_valid())

    def test_should_not_be_valid_if_resume_not_pdf(self):
        opening = OpeningFactory()

        files = { 'resume': self._get_temporary_file(type='evil/hacker') }
        form = ApplicationForm(self.form_data, files, opening=opening)
        self.assertFalse(form.is_valid())

        files = { 'resume': self._get_temporary_file(extension='py') }
        form = ApplicationForm(self.form_data, files, opening=opening)
        self.assertFalse(form.is_valid())

    def test_assure_directory_exists(self):
        opening = OpeningFactory()
        path = '%s/uploads/%d' % (settings.MEDIA_ROOT, opening.company.id)
        form = ApplicationForm(opening=opening)

        self.assertFalse(os.path.exists(path))
        form._assure_directory_exists()
        self.assertTrue(os.path.exists(path))

        # Making sure we delete the folder
        os.rmdir(path)

    def test_get_random_filename(self):
        opening = OpeningFactory()
        form = ApplicationForm(opening=opening)
        file = self._get_temporary_file()
        filename = form._get_random_filename(file.name)

        self.assertNotEqual(filename, 'foo.pdf')
        self.assertEqual(filename.split('.')[-1], 'pdf')

    def test_save_file(self):
        opening = OpeningFactory()
        dir = '%s/uploads/%d' % (settings.MEDIA_ROOT, opening.company.id)

        form = ApplicationForm(opening=opening)
        file = self._get_temporary_file()

        form._assure_directory_exists()
        self.assertEqual(len(os.listdir(dir)), 0)
        filepath = form._save_file(file)
        path = '%s/%s' % (settings.MEDIA_ROOT, filepath)
        self.assertTrue(os.path.exists(path))

        # Making sure we delete the folder and the files inside
        shutil.rmtree(dir)

    def test_should_not_create_new_applicant_if_exists(self):
        ApplicantFactory(email='bob@marley.jah')
        opening = OpeningFactory()

        files = { 'resume': self._get_temporary_file() }
        form = ApplicationForm(self.form_data, files, opening=opening)
        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(Applicant.objects.count(), 1)
