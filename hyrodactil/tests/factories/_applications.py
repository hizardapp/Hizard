import factory

import _companysettings
import _jobs
from applications.models import Applicant, Application, ApplicationAnswer


class ApplicantFactory(factory.Factory):
    FACTORY_FOR = Applicant

    first_name = 'Bilbon'
    last_name = 'Sacquet'
    email = 'bilbon@shire.com'

class ApplicationFactory(factory.Factory):
    FACTORY_FOR = Application

    applicant = factory.SubFactory(ApplicantFactory)
    opening = factory.SubFactory(_jobs.OpeningFactory)


class ApplicationAnswerFactory(factory.Factory):
    FACTORY_FOR = ApplicationAnswer

    answer = 'Some clever answer'
    application = factory.SubFactory(ApplicationFactory)
    question = factory.SubFactory(_companysettings.SingleLineQuestionFactory)
