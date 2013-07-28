import os

from django.core import mail
from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._companysettings import (
    InterviewStageFactory
)
from ..factories._openings import OpeningWithQuestionFactory

from applications.models import Application, ApplicationAnswer
from public.models import Interest
from tests.utils import subdomain_get, career_site_get
from customisable_emails.models import EmailTemplate


class PublicViewsTests(WebTest):
    def test_anonymous_can_access_landing_page(self):
        url = reverse('public:landing-page')
        response = subdomain_get(self.app, url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_can_add_email(self):
        url = reverse('public:landing-page')
        form = subdomain_get(self.app, url).form
        form['email'] =  'aston@martin.com'
        form.submit()
        self.assertEqual(Interest.objects.count(), 1)

class ApplicationViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.opening = OpeningWithQuestionFactory(company=self.user.company)

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
        OpeningWithQuestionFactory(
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
            page, self.opening.questions.all()[0].title
        )

    def test_valid_post_application_form(self):
        stage = InterviewStageFactory(tag='RECEIVED', company=self.user.company)
        url = reverse('public:apply', args=(self.opening.id,))

        EmailTemplate.objects.create(
            company=self.user.company,
            code="application_received",
            subject="Thank your for applying for {{ opening }}",
            body="Dear {{applicant_first_name}}, Best regards",
        )

        form = career_site_get(self.app, url, self.user.company.subdomain.lower()).form

        form['first_name'] = 'Bilbon'
        form['last_name'] = 'Sacquet'
        form['email'] = 'bilbon@shire.com'
        # name of file, content of file
        form['resume'] = 'bilbon_cv.pdf', "My resume"
        form['question-1'] = 'Lalala'
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
        self.assertEqual(application.current_stage, stage)
        self.assertEqual(len(mail.outbox), 1)
        email, = mail.outbox
        self.assertTrue("Bilbon" in email.body)
        self.assertTrue(self.opening.title in email.subject)

        # 2 required, 1 not required, we still record the 3 though
        self.assertEqual(ApplicationAnswer.objects.count(), 1)

        # And the resume we just created
        os.unlink(applicant.resume.path)

    def test_invalid_post_application_form(self):
        url = reverse('public:apply', args=(self.opening.id,))
        form = career_site_get(self.app, url, self.user.company.subdomain.lower()).form

        form['first_name'] = 'Software Developer'
        form['last_name'] = 'Fait des logiciels.'
        form['question-1'] = ''
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 0)

    def test_get_apply_form_unpublished(self):
        opening = OpeningWithQuestionFactory(company=self.user.company, published_date=None)
        url = reverse('public:apply', args=(opening.id,))
        career_site_get(self.app, url, self.user.company.subdomain.lower(), status=404)
