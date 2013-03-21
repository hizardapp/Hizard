from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._openings import OpeningFactory
from ..factories._companysettings import SingleLineQuestionFactory
from ..factories._companies import CompanyFactory

from openings.models import Opening, OpeningQuestion


class JobsViewsTests(WebTest):

    def setUp(self):
        self.user = UserFactory()
        self.question = SingleLineQuestionFactory(company=self.user.company)

    def test_arriving_on_opening_creation_page(self):
        url = reverse('openings:create_opening')

        response = self.app.get(url, user=self.user,
                headers=dict(Host="%s.h.com" % self.user.company.subdomain))

        self.assertEqual(response.status_code, 200)

    def test_opening_creation(self):
        url = reverse('openings:create_opening')

        page = self.app.get(url, user=self.user,
                headers=dict(Host="%s.h.com" % self.user.company.subdomain))
        form = page.forms['action-form']

        form['title'] = 'Software Developer'
        form['description'] = 'Fait des logiciels.'
        form['is_private'] = ''
        form['loc_country'] = 'FR'
        form['loc_city'] = 'Cannes'
        form['loc_postcode'] = '93100'
        form['questions'] = [True]
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Opening created.")

        opening_created = Opening.objects.get()
        #print OpeningQuestion.objects.all()
        self.assertEqual(opening_created.company, self.user.company)
        self.assertEqual(opening_created.title, 'Software Developer')
        self.assertEqual(opening_created.questions.count(), 1)

    def test_opening_form_only_contains_questions_from_same_company(self):
        same_company_question = SingleLineQuestionFactory.create(
            name='To be or not to be?',
            company=self.user.company)
        other_company_question = SingleLineQuestionFactory.create(
            name='Your 5 strenghts and weaknesses',
            company=CompanyFactory())

        url = reverse('openings:create_opening')
        page = self.app.get(url, user=self.user,
                headers=dict(Host="%s.h.com" % self.user.company.subdomain))
        self.assertContains(page, same_company_question.name)
        self.assertNotContains(page, other_company_question.name)

    def test_opening_creation_invalid(self):
        url = reverse('openings:create_opening')

        page = self.app.get(url, user=self.user,
                headers=dict(Host="%s.h.com" % self.user.company.subdomain))
        form = page.forms['action-form']
        form['title'] = 'Software Developer'
        form['description'] = ''
        form['is_private'] = ''
        form['loc_country'] = 'FR'
        form['loc_city'] = 'Cannes'
        form['loc_postcode'] = '93100'
        form['questions'] = [1]
        response = form.submit()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Opening.objects.count(), 0)

    def test_opening_edit(self):
        opening = OpeningFactory.create(title='DevOps', company=self.user.company)
        url = reverse('openings:update_opening', args=(opening.id,))

        page = self.app.get(url, user=self.user,
                headers=dict(Host="%s.h.com" % self.user.company.subdomain))
        form = page.forms['action-form']
        form['title'] = 'Software Developer'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Developer')
        self.assertNotContains(response, 'DevOps')

    def test_opening_delete(self):
        opening = OpeningFactory.create(title='DevOps',
                                        company=self.user.company)
        url = reverse('openings:delete_opening', args=(opening.id,))

        response = self.app.get(url, user=self.user,
                headers=dict(Host="%s.h.com" % self.user.company.subdomain)
                ).follow()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path, reverse('openings:list_openings'))
        self.assertNotContains(response, 'DevOps')
        self.assertContains(response, 'Opening deleted.')

    def test_can_only_edit_from_the_same_company(self):
        opening = OpeningFactory.create(title='Op', company=CompanyFactory())
        url = reverse('openings:update_opening', args=(opening.id,))
        self.app.get(url, user=self.user, status=404,
                headers=dict(Host="%s.h.com" % self.user.company.subdomain))

    def test_can_only_delete_from_the_same_company(self):
        opening = OpeningFactory.create(title='Op', company=CompanyFactory())
        url = reverse('openings:delete_opening', args=(opening.id,))
        self.app.get(url, user=self.user, status=404,
                headers=dict(Host="%s.h.com" % self.user.company.subdomain))
        self.assertTrue(opening in Opening.objects.all())

    def test_opening_listing(self):
        url = reverse('openings:list_openings')
        opening = OpeningFactory.create(title='DevOps', company=self.user.company)
        response = self.app.get(url, user=self.user,
                headers=dict(Host="%s.h.com" % self.user.company.subdomain))
        self.assertContains(response, opening.title)
