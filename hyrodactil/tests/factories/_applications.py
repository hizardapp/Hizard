import factory

import _companysettings
import _openings
from applications.models import Applicant, Application, ApplicationAnswer


class ApplicantFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Applicant

    first_name = 'Bilbon'
    last_name = 'Sacquet'
    email = 'bilbon@shire.com'
    resume = 'resumes/resume.pdf'


class ApplicationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Application

    applicant = factory.SubFactory(ApplicantFactory)
    opening = factory.SubFactory(_openings.OpeningFactory)


class ApplicationAnswerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ApplicationAnswer

    answer = 'Some clever answer'
    application = factory.SubFactory(ApplicationFactory)
    question = factory.SubFactory(_companysettings.SingleLineQuestionFactory)
