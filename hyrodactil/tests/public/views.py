from datetime import datetime
import os
import shutil

from django.conf import settings
from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._companysettings import (
    SingleLineQuestionFactory, InterviewStageFactory
)
from ..factories._openings import OpeningWithQuestionsFactory

from applications.models import Application, ApplicationAnswer
from companysettings.models import Question
from tests.utils import subdomain_get, career_site_get


class PublicViewsTests(WebTest):
    def test_anonymous_can_access_landing_page(self):
        url = reverse('public:landing-page')
        response = subdomain_get(self.app, url)
        self.assertEqual(response.status_code, 200)


class ApplicationViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.question = SingleLineQuestionFactory(company=self.user.company)
        self.opening = OpeningWithQuestionsFactory(company=self.user.company)

    def test_get_list_openings(self):
        url = reverse('public:opening-list')
        self.user.company.subdomain = self.user.company.subdomain.title()
        self.user.company.save()

        page = career_site_get(self.app, url, self.user.company.subdomain.lower())

        self.assertEqual(page.status_code, 200)
        self.assertContains(page, self.opening.title)

    def test_get_list_openings_inexisting_subdomain(self):
        url = reverse('public:opening-list')
        self.app.get(url, headers=dict(Host="tralala.h.com"), status=404)

    def test_get_list_openings_with_an_unpublished_one(self):
        OpeningWithQuestionsFactory(
            title="Dreamer",
            company=self.user.company,
            published_date=None
        )
        url = reverse('public:opening-list')
        page = career_site_get(self.app, url, self.user.company.subdomain.lower())
        self.assertNotContains(page, 'Dreamer')

    def test_get_application_form(self):
        url = reverse('public:apply', args=(self.opening.id,))

        page = career_site_get(self.app, url, self.user.company.subdomain.lower())

        self.assertEqual(page.status_code, 200)
        self.assertContains(page, self.opening.company.name)
        self.assertContains(page, self.opening.description)
        self.assertContains(page, self.opening.title)

        self.assertContains(
            page, self.opening.openingquestion_set.all()[0].question.name
        )

    def test_valid_post_application_form(self):
        url = reverse('public:apply', args=(self.opening.id,))
        stage1 = InterviewStageFactory(
            company=self.opening.company,
            position=0, name="Received"
        )
        InterviewStageFactory(
            company=self.opening.company,
            position=1, name="Accepted"
        )
        form = career_site_get(self.app, url, self.user.company.subdomain.lower()).form

        form['first_name'] = 'Bilbon'
        form['last_name'] = 'Sacquet'
        form['email'] = 'bilbon@shire.com'
        # name of file, content of file
        form['resume'] = 'bilbon_cv.pdf', "My resume"
        form['q_single-line'] = 'Lalala'
        form['q_multi-line'] = 'Lalala'
        form['q_checkbox'] = True
        response = form.submit().follow()

        self.assertEqual(
            response.request.path,
            reverse('public:confirmation', args=(self.opening.id,))
        )
        self.assertEqual(Application.objects.count(), 1)
        application = Application.objects.get(id=1)
        applicant = application.applicant

        self.assertEqual(applicant.first_name, 'Bilbon')
        self.assertEqual(applicant.resume.url,
                '/media/resumes/%d/bilbon_cv.pdf' % self.opening.company.id)
        self.assertEqual(application.current_stage, stage1)

        # 2 required, 1 not required, we still record the 3 though
        self.assertEqual(ApplicationAnswer.objects.count(), 3)

        # And the resume we just created
        os.unlink(applicant.resume.path)

    def test_invalid_post_application_form(self):
        url = reverse('public:apply', args=(self.opening.id,))
        form = career_site_get(self.app, url, self.user.company.subdomain.lower()).form

        form['first_name'] = 'Software Developer'
        form['last_name'] = 'Fait des logiciels.'
        form['q_single-line'] = 'Lalala'
        form['q_multi-line'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 0)
