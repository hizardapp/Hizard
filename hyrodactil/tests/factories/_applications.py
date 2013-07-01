import factory


from applications.models import (
    Applicant, Application, ApplicationAnswer, ApplicationStageTransition,
    ApplicationRating
)
from ._accounts import UserFactory
from ._companysettings import InterviewStageFactory
from ._openings import OpeningQuestionFactory, OpeningFactory


class ApplicantFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Applicant

    first_name = 'Bilbon'
    last_name = 'Sacquet'
    email = 'bilbon@shire.com'
    resume = 'tmp_resumes/resume.pdf'


class ApplicationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Application

    applicant = factory.SubFactory(ApplicantFactory)
    opening = factory.SubFactory(OpeningFactory)

class ApplicationAnswerFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ApplicationAnswer

    answer = 'Some clever answer'
    application = factory.SubFactory(ApplicationFactory)
    question = factory.SubFactory(OpeningQuestionFactory)


class ApplicationStageTransitionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ApplicationStageTransition

    application = factory.SubFactory(ApplicationFactory)
    stage = factory.SubFactory(InterviewStageFactory)


class ApplicationRatingFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ApplicationRating

    application = factory.SubFactory(ApplicationFactory)
    user = factory.SubFactory(UserFactory)
    rating = 0
