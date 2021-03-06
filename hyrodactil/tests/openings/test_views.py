from datetime import datetime

from django.core.urlresolvers import reverse
from django_webtest import WebTest

from ..factories._accounts import UserFactory
from ..factories._openings import OpeningFactory
from ..factories._companies import CompanyFactory

from openings.models import Opening
from tests.utils import subdomain_get


class OpeningsViewsTests(WebTest):

    def setUp(self):
        self.user = UserFactory()

    def test_arriving_on_opening_creation_page(self):
        url = reverse('openings:create_opening')
        response = subdomain_get(self.app, url, user=self.user)
        self.assertEqual(response.status_code, 200)

    def test_opening_creation(self):
        url = reverse('openings:create_opening')

        page = subdomain_get(self.app, url, user=self.user)
        form = page.forms[0]

        form['title'] = 'Software Developer'
        form['description'] = 'Fait des logiciels.'
        form['is_private'] = ''
        form['country'] = 'FR'
        form['city'] = 'Cannes'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Opening created.")

        opening_created = Opening.objects.get()

        self.assertEqual(opening_created.company, self.user.company)
        self.assertEqual(opening_created.title, 'Software Developer')

    def test_opening_creation_invalid(self):
        url = reverse('openings:create_opening')

        page = subdomain_get(self.app, url, user=self.user)
        form = page.forms[0]
        form['title'] = 'Software Developer'
        form['description'] = ''
        form['is_private'] = ''
        form['country'] = 'FR'
        form['city'] = 'Cannes'
        response = form.submit()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Opening.objects.count(), 0)

    def test_opening_edit(self):
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        url = reverse('openings:update_opening', args=(opening.id,))

        page = subdomain_get(self.app, url, user=self.user)
        form = page.forms[0]
        form['title'] = 'Software Developer'
        response = form.submit().follow()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Developer')
        self.assertNotContains(response, 'DevOps')

    def test_cant_edit_other_company_opening(self):
        opening = OpeningFactory(title='DevOps', company=CompanyFactory())
        url = reverse('openings:update_opening', args=(opening.id,))
        subdomain_get(self.app, url, user=self.user, status=404)

    def test_opening_delete(self):
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        url = reverse('openings:delete_opening', args=(opening.id,))

        response = subdomain_get(self.app, url, user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.request.path,
            reverse('openings:list_openings')
        )
        self.assertNotContains(response, 'DevOps')
        self.assertContains(response, 'Opening deleted.')

    def test_opening_listing(self):
        url = reverse('openings:list_openings')
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        response = subdomain_get(self.app, url, user=self.user)
        self.assertContains(response, opening.title)

    def test_opening_detail_view(self):
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        url = reverse('openings:detail_opening', args=(opening.id,))
        response = subdomain_get(self.app, url, user=self.user)
        self.assertContains(response, opening.title)

    def test_close_opening_valid(self):
        opening = OpeningFactory(title='DevOps', company=self.user.company)
        url = reverse('openings:publish_opening', args=(opening.id,))
        subdomain_get(self.app, url, user=self.user)

        self.assertEqual(
            Opening.objects.filter(published_date__isnull=True).count(), 0
        )

    def test_publish_opening(self):
        opening = OpeningFactory(company=self.user.company)
        url = reverse('openings:publish_opening', args=(opening.id,))
        subdomain_get(self.app, url, user=self.user)

        self.assertIsNotNone(Opening.objects.get().published_date)

    def test_unpublish_opening(self):
        opening = OpeningFactory(
            company=self.user.company, published_date=datetime.now()
        )
        url = reverse('openings:publish_opening', args=(opening.id,))
        subdomain_get(self.app, url, user=self.user)

        self.assertIsNone(Opening.objects.get().published_date)

    def test_publish_another_company_opening(self):
        opening = OpeningFactory(
            company=self.user.company, published_date=datetime.now()
        )
        user2 = UserFactory()
        url = reverse('openings:publish_opening', args=(opening.id,))
        subdomain_get(self.app, url, user=user2, status=404)
