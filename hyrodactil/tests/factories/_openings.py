import factory

import _companies
import _companysettings
from openings.models import Opening, OpeningQuestion


class OpeningFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Opening

    title = 'Salesman'
    description = 'Sales stuff'
    is_private = ''
    loc_country = 'FR'
    loc_city = 'Cannes'
    loc_postcode = '93100'
    company = factory.SubFactory(_companies.CompanyFactory)


class OpeningQuestionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OpeningQuestion

    question = factory.SubFactory(_companysettings.Question)
    opening = factory.SubFactory(OpeningFactory)
    required = False


class OpeningWithQuestionsFactory(OpeningFactory):

    @classmethod
    def _prepare(cls, create, **kwargs):
        opening = super(OpeningWithQuestionsFactory, cls)._prepare(create, **kwargs)

        if opening.id:
            OpeningQuestionFactory(
                opening=opening,
                question=_companysettings.SingleLineQuestionFactory(
                    company=opening.company),
                required=True
            )

            OpeningQuestionFactory(
                opening=opening,
                question=_companysettings.MultiLineQuestionFactory(
                    company=opening.company)
            )

            OpeningQuestionFactory(
                opening=opening,
                question=_companysettings.CheckboxQuestionFactory(
                    company=opening.company),
                required=True
            )

            OpeningQuestionFactory(
                opening=opening,
                question=_companysettings.FileQuestionFactory(
                    company=opening.company)
            )

        return opening
