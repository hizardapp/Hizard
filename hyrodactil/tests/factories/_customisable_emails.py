import factory

from customisable_emails.models import EmailTemplate

import _companies

class EmailTemplateFactory(factory.DjangoModelFactory):
    FACTORY_FOR = EmailTemplate

    code = "confirmation"
    name = "Confirmation email"
    company = factory.SubFactory(_companies.CompanyFactory)
    subject = "Hi {{applicant}}"
    body = "Dear {{applicant}}, bla bla"
