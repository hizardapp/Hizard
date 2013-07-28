from django.conf import settings
from django.template import Template, Context
from django.core.mail import send_mail

from customisable_emails.models import EmailTemplate


def get_email_template(code, company):
    try:
        email_template = EmailTemplate.objects.get(code=code, company=company)
        return Template(email_template.subject), Template(email_template.body)
    except EmailTemplate.DoesNotExist:
        return None, None


def send_customised_email(code, company, to, context):
    subject_template, body_template = get_email_template(company=company,
            code=code)

    context = Context(context)
    send_mail(subject_template.render(context),
            body_template.render(context),
            settings.DEFAULT_FROM_EMAIL,
            [to],
            fail_silently=False)
