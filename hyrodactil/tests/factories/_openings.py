from datetime import datetime
import factory

import _companies
from openings.models import Opening, OpeningQuestion


class OpeningFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Opening

    title = 'Salesman'
    description = 'Sales stuff'
    is_private = ''
    country = 'FR'
    city = 'Cannes'
    company = factory.SubFactory(_companies.CompanyFactory)


class OpeningQuestionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OpeningQuestion

    title = 'My question'
    opening = factory.SubFactory(OpeningFactory)


class OpeningWithQuestionFactory(OpeningFactory):
    published_date = datetime.now()

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        opening = target_class(*args, **kwargs)
        opening.save()
        OpeningQuestionFactory(opening=opening)
        return opening
