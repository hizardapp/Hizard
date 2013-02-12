import factory

from companysettings.models import Department, Question, InterviewStage
from ._companies import CompanyFactory


class DepartmentFactory(factory.Factory):
    FACTORY_FOR = Department

    name = 'Engineering'
    company = factory.SubFactory(CompanyFactory)


class QuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'Cover letter'
    is_required = True
    type = 'Single Line'

    company = factory.SubFactory(CompanyFactory)


class InterviewStageFactory(factory.Factory):
    FACTORY_FOR = InterviewStage

    name = 'Phone interview'
    company = factory.SubFactory(CompanyFactory)