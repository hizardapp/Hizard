import factory

from companysettings.models import InterviewStage
import _companies


class InterviewStageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = InterviewStage

    name = 'Phone interview'
    accepted = False
    rejected = False
    position = factory.Sequence(lambda n: n)
    company = factory.SubFactory(_companies.CompanyFactory)
