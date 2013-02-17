import os
import shutil

from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._applications import ApplicationFactory
from ..factories._companysettings import SingleLineQuestionFactory
from ..factories._jobs import OpeningFactory, OpeningWithQuestionsFactory

from applications.models import Application, ApplicationAnswer
from companysettings.models import Question


class ApplicationViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.question = SingleLineQuestionFactory(company=self.user.company)
        self.opening = OpeningWithQuestionsFactory(company=self.user.company)

    def test_get_list_openings(self):
        url = reverse('applications:list_openings', args=(self.user.company.id,))

        page = self.app.get(url)

        self.assertEqual(page.status_code, 200)
        self.assertContains(page, self.opening.title)

    def test_get_application_form(self):
        url = reverse('applications:apply', args=(self.opening.id,))

        page = self.app.get(url)

        self.assertEqual(page.status_code, 200)
        self.assertContains(page, self.opening.company.name)
        self.assertContains(page, self.opening.description)
        self.assertContains(page, self.opening.title)
        self.assertContains(page, self.opening.questions.all()[0].name)

    def test_valid_post_application_form(self):
        url = reverse('applications:apply', args=(self.opening.id,))
        form = self.app.get(url).form

        form['first_name'] = 'Bilbon'
        form['last_name'] = 'Sacquet'
        form['email'] = 'bilbon@shire.com'
        form['q_single-line'] = 'Lalala'
        form['q_multi-line'] = 'Lalala'
        # name of file, content of file
        form['q_file'] = 'resume.pdf', "My resume"
        response = form.submit().follow()

        self.assertEqual(response.request.path, reverse('public:home'))
        self.assertEqual(Application.objects.count(), 1)
        # 2 required, 2 not required, we still record the 4 though
        self.assertEqual(ApplicationAnswer.objects.count(), 4)

        # Testing the file has been properly updated
        dir = 'media/uploads/%d' % self.opening.company.id
        file_question = Question.objects.get(type='file')
        filename = ApplicationAnswer.objects.get(question=file_question).answer
        path = dir + '/%s' % filename
        self.assertTrue(os.path.exists(path))

        # Making sure we delete the folder and the files inside
        shutil.rmtree(dir)

    def test_invalid_post_application_form(self):
        url = reverse('applications:apply', args=(self.opening.id,))
        form = self.app.get(url).form

        form['first_name'] = 'Software Developer'
        form['last_name'] = 'Fait des logiciels.'
        form['q_single-line'] = 'Lalala'
        form['q_multi-line'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 0)


    def test_listing_applicants(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)

        url = reverse('applications:list_applications', args=(opening.id,))

        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)
        self.assertContains(response, application.applicant.last_name)

    def test_listing_all_applicants(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)

        url = reverse('applications:list_all_applications')

        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)
        self.assertContains(response, application.applicant.last_name)

    def test_get_applicant_details(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)
        #answer = ApplicationAnswerFactory.create(application=application)

        url = reverse('applications:application_detail', args=(application.id,))
        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)

    def test_get_applicant_details_different_company(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)
        rival = UserFactory.create(email='red@red.com')

        url = reverse('applications:application_detail', args=(application.id,))

        self.client.login(username='red@red.com', password='bob')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
