from django.core.urlresolvers import reverse
from django_webtest import WebTest

from tests.factories._accounts import UserFactory
from tests.factories._jobs import ApplicationFactory, OpeningFactory
from tests.factories._companies import CompanyFactory, QuestionFactory

from jobs.models import Application, Opening


class ViewsWebTest(WebTest):
    csrf_checks = False

    def setUp(self):
        self.user = UserFactory()
        self.company = CompanyFactory(owner=self.user)
        self.question = QuestionFactory(company=self.company)

    def test_arriving_on_opening_creation_page(self):
        url = reverse('jobs:create_opening')

        page = self.app.get(url, user=self.user)

        assert 'Title' in page
        assert 'Description' in page
        assert 'Department' in page
        assert 'Questions' in page
        #Should check the title of the page

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

        self.assertEqual(opening_created.company, self.company)
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
        opening = OpeningFactory.create(title='DevOps', company=self.company)
        url = reverse('jobs:update_opening', args=(opening.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms['job-form']
        form['title'] = 'Software Developer'
        response = form.submit().follow()

        self.assertEqual(page.status_code, 200)
        assert 'Software Developer' in response
        assert 'DevOps' not in response

    def test_opening_listing(self):
        url = reverse('jobs:list_openings')

        opening = OpeningFactory.create(title='DevOps', company=self.company)
        user2 = UserFactory(email='sam@sam.com')
        company2 = CompanyFactory(name='Corp', owner=user2)
        opening2 = OpeningFactory.create(company=company2)

        page = self.app.get(url, user=self.user)

        assert opening.title in page
        assert opening2.title not in page

    def tofix_test_applying_using_get(self):
        url = reverse('jobs:apply', args=(1,))
        page = self.app.get(url)

        self.assertEqual(page.response_code, 405)

    def test_apply_to_existing_opening(self):
        opening = OpeningFactory.create(company=self.company)
        question = QuestionFactory.create(company=self.company)
        question2 = QuestionFactory.create(name='are you a ninja?',
            company=self.company)

        opening.questions.add(question)
        opening.questions.add(question2)

        opening.save()

        url = reverse('jobs:apply', args=(opening.id,))
        application_data = {'first-name': 'Vincent',
                            'last-name': 'Prouillet',
                            question.name: 'This is me.',
                            question2.name: 'Yes'}

        response = self.app.post(url, application_data)

        assert 'applied' in response

        application = Application.objects.get()
        self.assertEqual(application.opening, opening)
        self.assertEqual(application.first_name, 'Vincent')
        self.assertEqual(application.last_name, 'Prouillet')

        app_answers = application.applicationanswer_set.all()

        self.assertEqual(app_answers[0].answer, 'Yes')
        self.assertEqual(app_answers[1].answer, 'This is me.')

    def test_apply_to_nonexisting_opening(self):
        url = reverse('jobs:apply', args=(7777,))
        application_data = {'first-name': 'Vincent',
                            'last-name': 'Prouillet'}

        response = self.app.post(url, application_data)

        assert 'fail' in response

        number_application = Application.objects.count()
        self.assertEqual(number_application, 0)

    def test_listing_applicants(self):
        opening = OpeningFactory.create(company=self.company)
        application = ApplicationFactory.create(opening=opening)

        url = reverse('jobs:list_applications', args=(opening.id,))

        page = self.app.get(url, user=self.user)

        self.assertEqual(page.status_code, 200)
        assert application.first_name in page
        assert application.last_name in page

    def test_applicant_details(self):
        opening = OpeningFactory.create(company=self.company)
        application = ApplicationFactory.create(opening=opening)
        #answer = ApplicationAnswerFactory.create(application=application)

        url = reverse('jobs:application_detail', args=(application.id,))
        page = self.app.get(url, user=self.user)

        self.assertEqual(page.status_code, 200)
        assert application.first_name in page
        assert application.last_name in page
        #assert answer.question.label in page
        #assert answer.answer in page
