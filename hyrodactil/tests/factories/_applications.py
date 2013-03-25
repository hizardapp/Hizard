import factory

import _companysettings
import _openings
from applications.models import Applicant, Application, ApplicationAnswer


class ApplicantFactory(factory.Factory):
    FACTORY_FOR = Applicant

    first_name = 'Bilbon'
    last_name = 'Sacquet'
    email = 'bilbon@shire.com'
    resume = 'resume.pdf'


class ApplicationFactory(factory.Factory):
    FACTORY_FOR = Application

    applicant = factory.SubFactory(ApplicantFactory)
    opening = factory.SubFactory(_openings.OpeningFactory)


class ApplicationAnswerFactory(factory.Factory):
    FACTORY_FOR = ApplicationAnswer

    answer = 'Some clever answer'
    application = factory.SubFactory(ApplicationFactory)
    question = factory.SubFactory(_companysettings.SingleLineQuestionFactory)
