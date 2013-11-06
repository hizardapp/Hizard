from django.core.urlresolvers import reverse
from django_webtest import WebTest

from tests.utils import subdomain_get, subdomain_post_ajax

from ..factories._accounts import UserFactory
from ..factories._customisable_emails import EmailTemplateFactory
from customisable_emails.models import EmailTemplate


class CustomisableEmailsViewsTests(WebTest):
    def setUp(self):
        self.user = UserFactory()

    def test_list_emails(self):
        template = EmailTemplateFactory(company=self.user.company,
                code="application_received",
                name="Application received")
        response = subdomain_get(self.app,
                reverse('customisable_emails:list'),
                user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Application received")

        edit_email_url = reverse("customisable_emails:edit",
                args=[template.pk])
        self.assertContains(response, edit_email_url)

    def test_edit_template(self):
        template = EmailTemplateFactory(company=self.user.company,
                code="application_received")

        edit_email_url = reverse("customisable_emails:edit",
                args=[template.pk])

        response = subdomain_get(self.app, edit_email_url, user=self.user)
        self.assertEqual(response.status_code, 200)

        form = response.forms[0]
        form['subject'] = 'Received'
        form['body'] = 'Hi, '
        response = form.submit()
        self.assertEqual(response.status_code, 302)

        template = EmailTemplate.objects.get()
        self.assertEqual(template.body, "Hi, ")
        self.assertEqual(template.subject, "Received")

    def test_test_renderer(self):
        render_test_template_url = reverse("customisable_emails:test_render")

        response = subdomain_post_ajax(self.app,
                render_test_template_url,
                dict(subject=u"hi {{ applicant_first_name }}",
                     body=u"{% if True %}Hey!{% endif %}"),
                user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict(subject="hi Quentin", body="Hey!"), response.json)

    def test_test_renderer_syntax_error(self):
        render_test_template_url = reverse("customisable_emails:test_render")

        response = subdomain_post_ajax(self.app,
                render_test_template_url,
                dict(subject=u"hi {% a%}", body=u"{% if True %}Hey!"),
                user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["subject"], "Invalid block tag: 'a'")
        self.assertEqual(response.json["body"],
                "Unclosed tags: elif, else, endif ")
