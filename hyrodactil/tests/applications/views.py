import json
import os
import shutil

from django.conf import settings
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
from applications.models import ApplicationMessage, Application, Applicant


class ApplicationViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()
        self.question = SingleLineQuestionFactory(company=self.user.company)
        self.opening = OpeningWithQuestionsFactory(company=self.user.company)

    def test_listing_all_applicants(self):
        application = ApplicationFactory.create(opening=self.opening)

        url = reverse('applications:list_applications')

        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)
        self.assertContains(response, application.applicant.last_name)

    def test_filter_applicants(self):
        phoned = InterviewStageFactory.create(
            company=self.user.company,
            name="phoned"
        )
        hired = InterviewStageFactory.create(
            company=self.user.company,
            name="hired"
        )
        opening2 = OpeningWithQuestionsFactory(company=self.user.company)
        application = ApplicationFactory.create(
            opening=self.opening,
            current_stage=phoned
        )
        url = reverse('applications:list_applications')

        response = self.app.get(url, dict(stages=[phoned.pk]), user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)

        response = self.app.get(url, dict(
            stages=[phoned.pk],
            opening=self.opening.pk
        ), user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)

        response = self.app.get(url, dict(stages=[hired.pk]), user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, application.applicant.first_name)

        response = self.app.get(
            url, dict(openings=[opening2.pk]), user=self.user
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, application.applicant.first_name)

    def test_get_applicant_details(self):
        application = ApplicationFactory.create(opening=self.opening)
        ApplicationAnswerFactory.create(
            application=application, question=self.question, answer="Man"
        )

        url = reverse(
            'applications:application_detail', args=(application.id,)
        )
        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.applicant.first_name)
        self.assertContains(response, "Man")

    def test_get_applicant_details_different_company(self):
        application = ApplicationFactory.create(opening=self.opening)
        user = UserFactory.create(email='red@red.com')

        url = reverse(
            'applications:application_detail', args=(application.id,)
        )

        self.app.get(url, user=user, status=404)

    def test_applicant_details_update_stage(self):
        application = ApplicationFactory.create(opening=self.opening)
        phoned = InterviewStageFactory.create(company=self.user.company)

        url = reverse(
            'applications:application_detail', args=(application.id,)
        )
        response = self.app.get(url, user=self.user)
        self.assertEqual(response.status_code, 200)
        response = self.app.get(url)
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

    def test_discuss_an_application(self):
        application = ApplicationFactory.create(opening=self.opening)
        colleague = UserFactory.create(
            email='bill@company.com', company=self.user.company
        )
        url = reverse(
            'applications:application_detail', args=(application.id,)
        )

        response = self.app.get(url, user=self.user)

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
        application = ApplicationFactory.create(opening=self.opening)
        attacker = UserFactory.create(email='red@red.com')
        url = reverse(
            'applications:application_detail', args=(application.id,)
        )

        response = self.app.get(url, user=self.user)

        form = response.forms['new-message-form']
        form['body'] = 'This guy is good'
        form['parent'] = ''
        response = form.submit(user=attacker, status=404)
        self.assertFalse(ApplicationMessage.objects.all().exists())

    def test_create_manual_application(self):
        InterviewStageFactory(company=self.user.company)
        url = reverse('applications:manual_application')
        self.fail('Need to rewrite manual application from/view')
        page = self.app.get(url, user=self.user)
        form = page.forms['action-form']
        form['first_name'] = 'Bilbo'
        form['last_name'] = 'Sacquet'
        form['email'] = 'bilbo@shire.com'
        form['resume'] = 'bilbon_cv.pdf', "My resume"

        response = form.submit().follow()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Application.objects.count(), 1)
        company_dir = '%s/uploads/%d' % (
            settings.MEDIA_ROOT,
            self.opening.company.id
        )
        shutil.rmtree(company_dir)
        os.unlink(Applicant.objects.get(id=1).resume.path)


class ApplicationAjaxViewsTests(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.question = SingleLineQuestionFactory(company=self.user.company)
        self.opening = OpeningWithQuestionsFactory(company=self.user.company)

    def test_saving_position_applications_valid_with_stage(self):
        application1 = ApplicationFactory(opening=self.opening)
        application2 = ApplicationFactory(opening=self.opening)
        stage = InterviewStageFactory(company=self.user.company)

        url = reverse('applications:update_positions')
        data = {
            'stage': stage.id,
            'positions': [(application1.id, 0), (application2.id, 1)]
        }

        response = self.app.post(
            url,
            {'data': json.dumps(data)},
            user=self.user,
            extra_environ=dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        )

        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], 'success')

        application1 = Application.objects.get(id=application1.id)
        application2 = Application.objects.get(id=application2.id)

        self.assertEqual(0, application1.position)
        self.assertEqual(stage.id, application1.current_stage_id)

        self.assertEqual(1, application2.position)
        self.assertEqual(stage.id, application1.current_stage_id)

    def test_saving_position_applications_valid_without_stage(self):
        application1 = ApplicationFactory(opening=self.opening)
        application2 = ApplicationFactory(opening=self.opening)

        url = reverse('applications:update_positions')
        data = {
            'stage': None,
            'positions': [(application1.id, 0), (application2.id, 1)]
        }

        response = self.app.post(
            url,
            {'data': json.dumps(data)},
            user=self.user,
            extra_environ=dict(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        )

        json_response = json.loads(response.content)
        self.assertEqual(json_response['status'], 'success')
        self.assertEqual(
            0, Application.objects.get(id=application1.id).position
        )
        self.assertEqual(
            1, Application.objects.get(id=application2.id).position
        )
