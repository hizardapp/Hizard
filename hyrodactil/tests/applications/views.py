import os

from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._applications import (
    ApplicationFactory, ApplicationAnswerFactory
)
from ..factories._companysettings import InterviewStageFactory
from ..factories._openings import OpeningWithQuestionFactory
from applications.models import ApplicationMessage, Application, Applicant
from tests.utils import subdomain_get


class ApplicationViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.opening = OpeningWithQuestionFactory(company=self.user.company)

    def test_listing_all_applicants(self):
        application = ApplicationFactory.create(opening=self.opening)

        url = reverse('applications:list_applications')

        response = subdomain_get(self.app, url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)
        self.assertContains(response, application.applicant.last_name)

    def test_get_applicant_details(self):
        application = ApplicationFactory(opening=self.opening)
        ApplicationAnswerFactory(
            question=self.opening.questions.get(), application=application,
            answer="Man"
        )

        url = reverse(
            'applications:application_detail', args=(application.id,)
        )
        response = subdomain_get(self.app, url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)
        self.assertContains(response, "Man")

    def test_get_applicant_details_different_company(self):
        application = ApplicationFactory(opening=self.opening)
        user = UserFactory(email='red@red.com')

        url = reverse(
            'applications:application_detail', args=(application.id,)
        )
        subdomain_get(self.app, url, user=user, status=404)

    def test_applicant_details_update_stage(self):
        application = ApplicationFactory(opening=self.opening)
        phoned = InterviewStageFactory(company=self.user.company)

        url = reverse(
            'applications:application_detail', args=(application.id,)
        )
        response = subdomain_get(self.app, url, user=self.user)

        form = response.forms['transition-form']
        form['stage'] = '%s' % phoned.pk
        form['note'] = 'Yep, looks good'
        response = form.submit().follow()

        transition = application.stage_transitions.get()
        self.assertEqual(transition.user, self.user)
        self.assertEqual(transition.stage, phoned)
        self.assertEqual(transition.note, "Yep, looks good")

        self.assertContains(response, transition.user.name)
        self.assertContains(response, transition.stage)

        # test email here?

    def test_discuss_an_application(self):
        application = ApplicationFactory(opening=self.opening)
        colleague = UserFactory(
            email='bill@company.com', company=self.user.company
        )
        url = reverse(
            'applications:application_detail', args=(application.id,)
        )

        response = subdomain_get(self.app, url, user=self.user)

        form = response.forms['new-message-form']
        form['body'] = 'This guy is good'
        form['parent'] = ''
        response = form.submit().follow()
        self.assertContains(response, "This guy is good")
        parent_message = ApplicationMessage.objects.get()
        self.assertEqual(self.user, parent_message.user)

        form = response.forms['new-message-form']
        form['body'] = "I beg to differ"
        form['parent'] = parent_message.pk
        response = form.submit(user=colleague).follow(user=colleague)
        self.assertContains(response, "This guy is good")
        self.assertContains(response, "I beg to differ")
        new_message = ApplicationMessage.objects.get(parent=parent_message)
        self.assertEqual(colleague, new_message.user)

    def test_only_allowed_user_can_participate_to_application_discussion(self):
        application = ApplicationFactory(opening=self.opening)
        attacker = UserFactory(email='red@red.com')
        url = reverse(
            'applications:application_detail', args=(application.id,)
        )

        response = subdomain_get(self.app, url, user=self.user)

        form = response.forms['new-message-form']
        form['body'] = 'This guy is good'
        form['parent'] = ''
        response = form.submit(user=attacker, status=404)
        self.assertFalse(ApplicationMessage.objects.all().exists())

    def test_create_manual_application(self):
        InterviewStageFactory(tag='RECEIVED')
        url = reverse(
            'applications:manual_application', args=[self.opening.pk]
        )
        page = subdomain_get(self.app, url, user=self.user)

        form = page.forms['action-form']
        form['first_name'] = 'Bilbo'
        form['last_name'] = 'Sacquet'
        form['email'] = 'bilbo@shire.com'
        form['resume'] = 'bilbon_cv.pdf', "My resume"
        form['question-1'] = 'lala'

        response = form.submit().follow()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Application.objects.count(), 1)
        applicant = Applicant.objects.get()
        self.assertEqual(applicant.first_name, "Bilbo")
        self.assertEqual(applicant.last_name, "Sacquet")
        os.unlink(applicant.resume.path)

    def test_vote_application_valid(self):
        application = ApplicationFactory(opening=self.opening)
        url = reverse(
            'applications:rate', args=(application.pk, -1,)
        )
        page = subdomain_get(self.app, url, user=self.user)
        self.assertTemplateUsed(page, 'applications/application_detail.html')
        self.assertNotContains(page, 'class="alert-error"')

    def test_vote_application_invalid(self):
        application = ApplicationFactory(opening=self.opening)
        url = reverse(
            'applications:rate', args=(application.pk, -42,)
        )
        page = subdomain_get(self.app, url, user=self.user)
        self.assertTemplateUsed(page, 'applications/application_detail.html')
        self.assertContains(page, 'class="alert-error"')

    def test_hire_applicant(self):
        InterviewStageFactory(tag='HIRED')
        application = ApplicationFactory(opening=self.opening)
        url = reverse(
            'applications:hire', args=(application.pk, )
        )
        subdomain_get(self.app, url, user=self.user)
