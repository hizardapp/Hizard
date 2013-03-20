import factory

import _companies
import _companysettings
from openings.models import Opening


class OpeningFactory(factory.Factory):
    FACTORY_FOR = Opening

    title = 'Salesman'
    description = 'Sales stuff'
    is_private = ''
    loc_country = 'FR'
    loc_city = 'Cannes'
    loc_postcode = '93100'
    company = factory.SubFactory(_companies.CompanyFactory)


class OpeningWithQuestionsFactory(OpeningFactory):

    @classmethod
    def _prepare(cls, create, **kwargs):
        opening = super(OpeningWithQuestionsFactory, cls)._prepare(create, **kwargs)

        if opening.id:
            opening.questions.add(
                _companysettings.SingleLineQuestionFactory(
                    company=opening.company),

                _companysettings.MultiLineQuestionFactory(
                    company=opening.company),

                _companysettings.CheckboxQuestionFactory(
                    company=opening.company),

                _companysettings.FileQuestionFactory(
                    company=opening.company)
            )

        return opening
