from django.test import TestCase
from django.core import mail

from ..factories._companies import CompanyFactory
from ..factories._customisable_emails import EmailTemplateFactory
from customisable_emails.utils import get_email_template, send_customised_email


class UtilsTest(TestCase):
    def test_get_template(self):
        company = CompanyFactory()
        EmailTemplateFactory(code="confirmation", company=company)
        subject_template, body_template = get_email_template(
            company=company,
            code="confirmation"
        )
        self.assertTrue(subject_template)
        self.assertTrue(body_template)

    def test_get_template_failure(self):
        company = CompanyFactory()
        subject_template, body_template = get_email_template(
            company=company,
            code="confirmation"
        )
        self.assertIsNone(subject_template)
        self.assertIsNone(body_template)

    def test_send_template(self):
        company = CompanyFactory()
        EmailTemplateFactory(company=company,
                subject="Hi {{applicant}}",
                body="Dear {{applicant}} XXX",
                code="confirmation")

        send_customised_email("confirmation",
                company=company,
                to="henry@example.com",
                context=dict(applicant="Henry")
        )

        self.assertEqual(len(mail.outbox), 1)
        email, = mail.outbox
        self.assertTrue("henry@example.com" in email.to)
        self.assertEqual(email.subject, "Hi Henry")
        self.assertTrue(email.body, "Dear Henry XXX")
