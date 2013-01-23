import factory

from companies.models import Company, Department, Question
from ._accounts import UserFactory


class CompanyFactory(factory.Factory):
    FACTORY_FOR = Company

    name = 'ACME'
    owner = factory.SubFactory(UserFactory)


class DepartmentFactory(factory.Factory):
    FACTORY_FOR = Department

    name = 'Engineering'
    company = factory.SubFactory(CompanyFactory)


class QuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'Cover letter'
    label = 'Please write a cover letter'
    type = 'TEXTAREA'

    company = factory.SubFactory(CompanyFactory)
