from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._jobs import ApplicationFactory, OpeningFactory
from ..factories._companysettings import QuestionFactory
from ..factories._companies import CompanyFactory

from jobs.models import Application, Opening


class JobsViewsTests(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.question = QuestionFactory(company=self.user.company)

    def test_arriving_on_opening_creation_page(self):
        url = reverse('jobs:create_opening')

        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)

    def test_opening_creation(self):
        url = reverse('jobs:create_opening')

        page = self.app.get(url, user=self.user)
        form = page.forms['job-form']
        form['title'] = 'Software Developer'
        form['description'] = 'Fait des logiciels.'
        form['is_private'] = ''
        form['loc_country'] = 'FR'
        form['loc_city'] = 'Cannes'
        form['loc_postcode'] = '93100'
        form['questions'] = [self.question]
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)

        opening_created = Opening.objects.get()

        self.assertEqual(opening_created.company, self.user.company)
        self.assertEqual(opening_created.title, 'Software Developer')
        self.assertEqual(opening_created.questions.count(), 1)

    def test_opening_creation_invalid(self):
        url = reverse('jobs:create_opening')

        page = self.app.get(url, user=self.user)
        form = page.forms['job-form']
        form['title'] = 'Software Developer'
        form['description'] = ''
        form['is_private'] = ''
        form['loc_country'] = 'FR'
        form['loc_city'] = 'Cannes'
        form['loc_postcode'] = '93100'
        form['questions'] = [1]
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        # Should check that there is an error
        opening_count = Opening.objects.count()

        self.assertEqual(opening_count, 0)

    def test_opening_edit(self):
        opening = OpeningFactory.create(title='DevOps', company=self.user.company)
        url = reverse('jobs:update_opening', args=(opening.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['job-form']
        form['title'] = 'Software Developer'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Developer')
        self.assertNotContains(response, 'DevOps')

    def test_opening_delete(self):
        opening = OpeningFactory.create(title='DevOps',
                                        company=self.user.company)
        url = reverse('jobs:delete_opening', args=(opening.id,))

        response = self.app.get(url, user=self.user).follow()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, reverse('jobs:list_openings'))
        self.assertNotContains(response, 'DevOps')

    def test_can_only_edit_from_the_same_company(self):
        opening = OpeningFactory.create(title='Op', company=CompanyFactory())
        url = reverse('jobs:update_opening', args=(opening.id,))
        self.app.get(url, user=self.user, status=404)

    def test_can_only_delete_from_the_same_company(self):
        opening = OpeningFactory.create(title='Op', company=CompanyFactory())
        url = reverse('jobs:delete_opening', args=(opening.id,))
        self.app.get(url, user=self.user, status=404)
        self.assertTrue(opening in Opening.objects.all())

    def test_opening_listing(self):
        url = reverse('jobs:list_openings')
        opening = OpeningFactory.create(title='DevOps', company=self.user.company)
        response = self.app.get(url, user=self.user)
        self.assertContains(response, opening.title)

    def test_apply_to_existing_opening(self):
        opening = OpeningFactory.create(company=self.user.company)
        question = QuestionFactory.create(company=self.user.company)
        question2 = QuestionFactory.create(name='are you a ninja?',
            company=self.user.company)

        opening.questions.add(question)
        opening.questions.add(question2)

        opening.save()

        url = reverse('jobs:apply', args=(opening.id,))
        application_data = {'first-name': 'Vincent',
                            'last-name': 'Prouillet',
                            question.name: 'This is me.',
                            question2.name: 'Yes'}

        self.app.post(url, application_data)

        application = Application.objects.get()
        self.assertEqual(application.opening, opening)
        self.assertEqual(application.first_name, 'Vincent')
        self.assertEqual(application.last_name, 'Prouillet')

        app_answers = application.applicationanswer_set.all()

        self.assertEqual(app_answers[0].answer, 'Yes')
        self.assertEqual(app_answers[1].answer, 'This is me.')

    def test_apply_to_non_existing_opening(self):
        url = reverse('jobs:apply', args=(7777,))
        application_data = {'first-name': 'Vincent',
                            'last-name': 'Prouillet'}

        self.app.post(url, application_data)

        number_application = Application.objects.count()
        self.assertEqual(number_application, 0)

    def test_listing_applicants(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)

        url = reverse('jobs:list_applications', args=(opening.id,))

        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.first_name)
        self.assertContains(response, application.last_name)

    def test_get_applicant_details(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)
        #answer = ApplicationAnswerFactory.create(application=application)

        url = reverse('jobs:application_detail', args=(application.id,))
        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, application.first_name)

    def test_get_applicant_details_different_company(self):
        opening = OpeningFactory.create(company=self.user.company)
        application = ApplicationFactory.create(opening=opening)
        rival = UserFactory.create(email='red@red.com')

        url = reverse('jobs:application_detail', args=(application.id,))

        self.client.login(username='red@red.com', password='bob')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
