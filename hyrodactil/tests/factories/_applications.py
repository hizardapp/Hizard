import factory

import _companysettings
import _jobs
from applications.models import Application, ApplicationAnswer


class ApplicationFactory(factory.Factory):
    FACTORY_FOR = Application

    first_name = 'Bilbon'
    last_name = 'Sacquet'
    opening = factory.SubFactory(_jobs.OpeningFactory)


class ApplicationAnswerFactory(factory.Factory):
    FACTORY_FOR = ApplicationAnswer

    answer = 'Some clever answer'
    application = factory.SubFactory(ApplicationFactory)
    question = factory.SubFactory(_companysettings.SingleLineQuestionFactory)
