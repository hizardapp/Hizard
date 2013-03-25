from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._applications import (
    ApplicationFactory, ApplicationAnswerFactory
)
from ..factories._companysettings import (
    SingleLineQuestionFactory, InterviewStageFactory
)
from ..factories._openings import OpeningWithQuestionsFactory


class ApplicationViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.question = SingleLineQuestionFactory(company=self.user.company)
        self.opening = OpeningWithQuestionsFactory(company=self.user.company)

    def test_listing_applicants(self):
        application = ApplicationFactory.create(opening=self.opening)

        url = reverse(
            'applications:list_applications',
            args=(self.opening.id,)
        )

        response = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)
        self.assertContains(response, application.applicant.last_name)

    def test_listing_all_applicants(self):
        application = ApplicationFactory.create(opening=self.opening)

        url = reverse('applications:list_all_applications')

        response = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)
        self.assertContains(response, application.applicant.last_name)

    def test_get_applicant_details(self):
        application = ApplicationFactory.create(opening=self.opening)
        ApplicationAnswerFactory.create(
            application=application, question=self.question, answer="Man"
        )

        url = reverse('applications:application_detail', args=(application.id,))
        response = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.opening.company.subdomain)
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)
        self.assertContains(response, "Man")

    def test_get_applicant_details_different_company(self):
        application = ApplicationFactory.create(opening=self.opening)
        user = UserFactory.create(email='red@red.com')

        url = reverse('applications:application_detail', args=(application.id,))

        self.app.get(
            url,
            user=user,
            status=404,
            headers=dict(Host="%s.h.com" % self.opening.company.subdomain)
        )

    def test_applicant_details_update_stage(self):
        application = ApplicationFactory.create(opening=self.opening)
        phoned = InterviewStageFactory.create(company=self.user.company)

        url = reverse(
            'applications:application_detail', args=(application.id,)
        )
        response = self.app.get(
            url,
            user=self.user,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        self.assertEqual(response.status_code, 200)
        response = self.app.get(
            url,
            headers=dict(Host="%s.h.com" % self.user.company.subdomain)
        )
        form = response.form
        form['stage'] = '%s' % phoned.pk
        response = form.submit().follow()

        transition = application.stage_transitions.get()
        self.assertEqual(transition.user, self.user)
        self.assertEqual(transition.stage, phoned)

        self.assertContains(response, transition.user)
        self.assertContains(response, transition.stage)
