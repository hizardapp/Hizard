import factory

from _companies import CompanyFactory
from _companysettings import QuestionFactory
from jobs.models import Application, ApplicationAnswer, Opening


class OpeningFactory(factory.Factory):
    FACTORY_FOR = Opening

    title = 'Salesman'
    description = 'Sales stuff'
    is_private = ''
    loc_country = 'FR'
    loc_city = 'Cannes'
    loc_postcode = '93100'
    company = factory.SubFactory(CompanyFactory)
    #questions = factory.SubFactory(QuestionFactory)


class ApplicationFactory(factory.Factory):
    FACTORY_FOR = Application

    first_name = 'Bilbon'
    last_name = 'Sacquet'
    opening = factory.SubFactory(OpeningFactory)


class ApplicationAnswerFactory(factory.Factory):
    FACTORY_FOR = ApplicationAnswer

    answer = "Some clever answer"
    application = factory.SubFactory(ApplicationFactory)
    question = factory.SubFactory(QuestionFactory)
