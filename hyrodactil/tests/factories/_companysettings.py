import factory

from companysettings.models import Department, Question, InterviewStage
import _companies


class DepartmentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Department

    name = 'Engineering'
    company = factory.SubFactory(_companies.CompanyFactory)


class SingleLineQuestionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Question

    name = 'Single Line'
    type_field = 'textbox'

    company = factory.SubFactory(_companies.CompanyFactory)


class MultiLineQuestionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Question

    name = 'Multi Line'
    type_field = 'textarea'

    company = factory.SubFactory(_companies.CompanyFactory)


class CheckboxQuestionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Question

    name = 'Checkbox'
    type_field = 'checkbox'

    company = factory.SubFactory(_companies.CompanyFactory)


class InterviewStageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = InterviewStage

    name = 'Phone interview'
    accepted = False
    rejected = False
    position = factory.Sequence(lambda n: n)
    company = factory.SubFactory(_companies.CompanyFactory)
