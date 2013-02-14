import factory

from _companies import CompanyFactory
import _companysettings
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


class OpeningWithQuestionsFactory(OpeningFactory):

    @classmethod
    def _prepare(cls, create, **kwargs):
        opening = super(OpeningWithQuestionsFactory, cls)._prepare(create, **kwargs)
        if opening.id:
            question1 = _companysettings.SingleLineQuestionFactory(company=opening.company)
            question2 = _companysettings.MultiLineQuestionFactory(company=opening.company)
            question3 = _companysettings.CheckboxQuestionFactory(is_required=False, company=opening.company)
            question4 = _companysettings.FileQuestionFactory(is_required=False, company=opening.company)
            opening.questions.add(question1)
            opening.questions.add(question2)
            opening.questions.add(question3)
            opening.questions.add(question4)
        return opening


class ApplicationFactory(factory.Factory):
    FACTORY_FOR = Application

    first_name = 'Bilbon'
    last_name = 'Sacquet'
    opening = factory.SubFactory(OpeningFactory)


class ApplicationAnswerFactory(factory.Factory):
    FACTORY_FOR = ApplicationAnswer

    answer = 'Some clever answer'
    application = factory.SubFactory(ApplicationFactory)
    question = factory.SubFactory(_companysettings.SingleLineQuestionFactory)
