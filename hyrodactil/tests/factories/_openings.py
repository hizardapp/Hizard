import factory

import _companies
import _companysettings
from openings.models import Opening, OpeningQuestion


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
            OpeningQuestion(
                opening=opening,
                question=_companysettings.SingleLineQuestionFactory(
                    company=opening.company),
                required=True
            )

            OpeningQuestion(
                opening=opening,
                question=_companysettings.MultiLineQuestionFactory(
                    company=opening.company)
            )

            OpeningQuestion(
                opening=opening,
                question=_companysettings.CheckboxQuestionFactory(
                    company=opening.company),
                required=True
            )

            OpeningQuestion(
                opening=opening,
                question=_companysettings.CheckboxQuestionFactory(
                    company=opening.company)
            )

        return opening
