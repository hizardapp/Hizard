import os

from django.core.urlresolvers import reverse
from django.core import mail
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._applications import (
    ApplicationFactory, ApplicationAnswerFactory
)
from ..factories._companysettings import InterviewStageFactory
from ..factories._companies import CompanyFactory
from ..factories._customisable_emails import EmailTemplateFactory
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
        response = form.submit().follow()

        transition = application.stage_transitions.get()
        self.assertEqual(transition.user, self.user)
        self.assertEqual(transition.stage, phoned)

        self.assertContains(response, transition.user.name)
        self.assertContains(response, transition.stage)

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
        InterviewStageFactory(tag='RECEIVED', company=self.user.company)
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
        InterviewStageFactory(tag='HIRED', company=CompanyFactory())
        hired_stage = InterviewStageFactory(tag='HIRED',
                company=self.user.company)
        EmailTemplateFactory(code="candidate_hired",
            company=self.user.company,
            subject="Congrats {{ applicant_first_name }}")
        application = ApplicationFactory(opening=self.opening)
        url = reverse(
            'applications:application_detail', args=(application.pk,)
        )
        response = subdomain_get(self.app, url, user=self.user)

        form = response.forms['transition-form']
        form['stage'] = '%s' % hired_stage.pk
        response = form.submit().follow()

        self.assertEqual(len(mail.outbox), 1)
        email, = mail.outbox
        self.assertTrue("Bilbon" in email.subject)

        application = Application.objects.get(pk=application.pk)
        self.assertEqual(application.current_stage, hired_stage)

        transition = application.stage_transitions.get()
        self.assertEqual(transition.user, self.user)
        self.assertEqual(transition.stage, hired_stage)

    def test_reject_applicant(self):
        application = ApplicationFactory(opening=self.opening)
        EmailTemplateFactory(code="application_rejected",
            company=self.user.company,
            subject="Sorry {{ applicant_first_name }}")
        goodbye = InterviewStageFactory(company=self.user.company,
            tag="REJECTED")

        url = reverse(
            'applications:application_detail', args=(application.id,)
        )
        response = subdomain_get(self.app, url, user=self.user)

        form = response.forms['transition-form']
        form['stage'] = '%s' % goodbye.pk
        response = form.submit().follow()
        self.assertEqual(len(mail.outbox), 1)
        email, = mail.outbox
        self.assertTrue("Bilbon" in email.subject)

    def test_can_only_rate_own_company_opening(self):
        application = ApplicationFactory(opening=self.opening)
        other_user = UserFactory()
        url = reverse(
            'applications:rate', args=(application.pk, -1,)
        )
        subdomain_get(self.app, url, other_user, status=404)
