import os
import shutil

from django.conf import settings
from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._companysettings import SingleLineQuestionFactory, InterviewStageFactory
from ..factories._openings import OpeningWithQuestionsFactory
from applications.models import Application, ApplicationAnswer
from companysettings.models import Question


class ApplicationViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.question = SingleLineQuestionFactory(company=self.user.company)
        self.opening = OpeningWithQuestionsFactory(company=self.user.company)

    def test_get_list_openings(self):
        url = reverse('public_jobs:list_openings')

        page = self.app.get(
            url,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )

        self.assertEqual(page.status_code, 200)
        self.assertContains(page, self.opening.title)

    def test_get_list_openings_inexisting_subdomain(self):
        url = reverse('public_jobs:list_openings')
        self.app.get(url, headers=dict(Host="tralala.h.com"), status=404)

    def test_get_application_form(self):
        url = reverse('public_jobs:apply', args=(self.opening.id,))

        page = self.app.get(url)

        self.assertEqual(page.status_code, 200)
        self.assertContains(page, self.opening.company.name)
        self.assertContains(page, self.opening.description)
        self.assertContains(page, self.opening.title)

        self.assertContains(
            page, self.opening.openingquestion_set.all()[0].question.name
        )

    def test_valid_post_application_form(self):
        url = reverse('public_jobs:apply', args=(self.opening.id,))
        stage = InterviewStageFactory(initial=True, company=self.opening.company)
        form = self.app.get(url).form

        form['first_name'] = 'Bilbon'
        form['last_name'] = 'Sacquet'
        form['email'] = 'bilbon@shire.com'
        # name of file, content of file
        form['resume'] = 'bilbon_cv.pdf', "My resume"
        form['q_single-line'] = 'Lalala'
        form['q_multi-line'] = 'Lalala'
        form['q_file'] = 'mypicture.jpg', "me"
        response = form.submit().follow()

        self.assertEqual(
            response.request.path,
            reverse('public_jobs:confirmation', args=(self.opening.id,))
        )
        self.assertEqual(Application.objects.count(), 1)
        application = Application.objects.get(id=1)
        applicant = application.applicant

        self.assertEqual(applicant.first_name, 'Bilbon')
        self.assertEqual(applicant.resume.url, '/media/resumes/bilbon_cv.pdf')
        self.assertEqual(application.current_stage(), stage)

        # 2 required, 2 not required, we still record the 4 though
        self.assertEqual(ApplicationAnswer.objects.count(), 4)

        # Testing the file has been properly updated
        company_dir = '%s/uploads/%d' % (
            settings.MEDIA_ROOT,
            self.opening.company.id
        )
        file_question = Question.objects.get(type='file')
        filepath = ApplicationAnswer.objects.get(question=file_question).answer
        path = '%s/%s' % (settings.MEDIA_ROOT, filepath)
        self.assertTrue(os.path.exists(path))

        # Remove the uploaded files only
        shutil.rmtree(company_dir)
        # And the resume we just created
        os.unlink(applicant.resume.path)

    def test_invalid_post_application_form(self):
        url = reverse('public_jobs:apply', args=(self.opening.id,))
        form = self.app.get(url).form

        form['first_name'] = 'Software Developer'
        form['last_name'] = 'Fait des logiciels.'
        form['q_single-line'] = 'Lalala'
        form['q_multi-line'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 0)
