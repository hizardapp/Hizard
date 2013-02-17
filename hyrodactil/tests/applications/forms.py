import os
import shutil
import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from ..factories._applications import ApplicantFactory
from ..factories._jobs import OpeningFactory, OpeningWithQuestionsFactory
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

    def _get_temporary_text_file(self):
        io = StringIO.StringIO()
        io.write('foo')
        text_file = InMemoryUploadedFile(io, None, 'foo.txt', 'text', io.len, None)
        text_file.seek(0)
        return text_file

    def test_application_without_questions_valid(self):
        opening = OpeningFactory()

        form = ApplicationForm(data=self.form_data, opening=opening)
        self.assertTrue(form.is_valid())

    def test_application_without_questions_invalid(self):
        opening = OpeningFactory()
        invalid = dict(self.form_data)
        del invalid['first_name']

        form = ApplicationForm(data=invalid, opening=opening)
        self.assertFalse(form.is_valid())

    def test_application_with_questions_valid(self):
        opening = OpeningWithQuestionsFactory()
        data = dict(self.form_data)
        data.update(self.question_data)

        form = ApplicationForm(data=data, opening=opening)
        self.assertTrue(form.is_valid())

    def test_application_with_questions_invalid(self):
        opening = OpeningWithQuestionsFactory()
        data = dict(self.form_data)
        data.update(self.question_data)
        del data['q_single-line']

        form = ApplicationForm(data=data, opening=opening)
        self.assertFalse(form.is_valid())

    def test_assure_directory_exists(self):
        opening = OpeningFactory()
        path = 'media/uploads/%d' % opening.company.id
        form = ApplicationForm(opening=opening)

        self.assertFalse(os.path.exists(path))
        form._assure_directory_exists()
        self.assertTrue(os.path.exists(path))

        # Making sure we delete the folder
        os.rmdir(path)

    def test_get_random_filename(self):
        opening = OpeningFactory()
        form = ApplicationForm(opening=opening)
        file = self._get_temporary_text_file()
        filename = form._get_random_filename(file.name)

        self.assertNotEqual(filename, 'foo.txt')
        self.assertEqual(filename.split('.')[-1], 'txt')

    def test_save_file(self):
        opening = OpeningFactory()
        dir = 'media/uploads/%d' % opening.company.id

        form = ApplicationForm(opening=opening)
        file = self._get_temporary_text_file()

        form._assure_directory_exists()
        self.assertEqual(len(os.listdir(dir)), 0)
        filename = form._save_file(file)
        path = dir + '/%s' % filename
        self.assertTrue(os.path.exists(path))

        # Making sure we delete the folder and the files inside
        shutil.rmtree(dir)

    def test_should_not_create_new_applicant_if_exists(self):
        ApplicantFactory(email='bob@marley.jah')
        opening = OpeningFactory()

        form = ApplicationForm(data=self.form_data, opening=opening)
        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(Applicant.objects.count(), 1)