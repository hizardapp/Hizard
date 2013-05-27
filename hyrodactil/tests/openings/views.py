from datetime import datetime

from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._openings import OpeningFactory
from ..factories._companysettings import SingleLineQuestionFactory
from ..factories._companies import CompanyFactory

from openings.models import Opening


class OpeningsViewsTests(WebTest):

    def setUp(self):
        self.user = UserFactory()
        self.question = SingleLineQuestionFactory(company=self.user.company)

    def test_arriving_on_opening_creation_page(self):
        url = reverse('openings:create_opening')

        response = self.app.get(url, user=self.user)

        self.assertEqual(response.status_code, 200)

    def test_opening_creation(self):
        url = reverse('openings:create_opening')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]

        form['title'] = 'Software Developer'
        form['description'] = 'Fait des logiciels.'
        form['is_private'] = ''
        form['loc_country'] = 'FR'
        form['loc_city'] = 'Cannes'
        form['oq-1-included'] = True
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Opening created.")

        opening_created = Opening.objects.get()

        self.assertEqual(opening_created.company, self.user.company)
        self.assertEqual(opening_created.title, 'Software Developer')
        self.assertEqual(opening_created.openingquestion_set.count(), 1)

    def test_opening_form_only_contains_questions_from_same_company(self):
        same_company_question = SingleLineQuestionFactory(
            name='To be or not to be?',
            company=self.user.company)
        other_company_question = SingleLineQuestionFactory(
            name='Your 5 strenghts and weaknesses',
            company=CompanyFactory())

        url = reverse('openings:create_opening')
        page = self.app.get(url, user=self.user)
        self.assertContains(page, same_company_question.name)
        self.assertNotContains(page, other_company_question.name)

    def test_opening_creation_invalid(self):
        url = reverse('openings:create_opening')

        page = self.app.get(url, user=self.user)
        form = page.forms[0]
        form['title'] = 'Software Developer'
        form['description'] = ''
        form['is_private'] = ''
        form['loc_country'] = 'FR'
        form['loc_city'] = 'Cannes'
        form['oq-1-included'] = True
        response = form.submit()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Opening.objects.count(), 0)

    def test_opening_edit(self):
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        url = reverse('openings:update_opening', args=(opening.id,))

        page = self.app.get(url, user=self.user)
        form = page.forms[0]
        form['title'] = 'Software Developer'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Developer')
        self.assertNotContains(response, 'DevOps')

    def test_cant_edit_other_company_opening(self):
        opening = OpeningFactory(title='DevOps', company=CompanyFactory())
        url = reverse('openings:update_opening', args=(opening.id,))
        self.app.get(url, user=self.user, status=404)

    def test_opening_delete(self):
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        url = reverse('openings:delete_opening', args=(opening.id,))

        response = self.app.get(url, user=self.user).follow()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.path,
            reverse('openings:list_openings'))
        self.assertNotContains(response, 'DevOps')
        self.assertContains(response, 'Opening deleted.')

    def test_opening_listing(self):
        url = reverse('openings:list_openings')
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        response = self.app.get(url, user=self.user)
        self.assertContains(response, opening.title)

    def test_opening_detail_view(self):
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        url = reverse('openings:detail_opening', args=(opening.id,))
        response = self.app.get(url, user=self.user)
        self.assertContains(response, opening.title)

    def test_close_opening_valid(self):
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        url = reverse('openings:close_opening', args=(opening.id,))
        self.app.get(url, user=self.user)

        self.assertEqual(
            Opening.objects.filter(closing_date__isnull=True).count(), 0
        )

    def test_close_opening_already_closed(self):
        opening = OpeningFactory(
            title='DevOps', company=self.user.company, closing_date=datetime.now()
        )
        url = reverse('openings:close_opening', args=(opening.id,))
        response = self.app.get(url, user=self.user).follow()

        self.assertEqual(
            Opening.objects.filter(closing_date__isnull=True).count(), 0
        )
        self.assertContains(response, 'already closed')

    def test_publish_opening(self):
        opening = OpeningFactory(company=self.user.company)
        url = reverse('openings:publish_opening', args=(opening.id,))
        self.app.get(url, user=self.user)

        self.assertIsNotNone(Opening.objects.get().published_date)

    def test_unpublish_opening(self):
        opening = OpeningFactory(company=self.user.company, published_date=datetime.now())
        url = reverse('openings:publish_opening', args=(opening.id,))
        self.app.get(url, user=self.user)

        self.assertIsNone(Opening.objects.get().published_date)
