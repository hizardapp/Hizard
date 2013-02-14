import factory

from companysettings.models import Department, Question, InterviewStage
from ._companies import CompanyFactory


class DepartmentFactory(factory.Factory):
    FACTORY_FOR = Department

    name = 'Engineering'
    company = factory.SubFactory(CompanyFactory)


class SingleLineQuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'Single Line'
    is_required = True
    type = 'textbox'

    company = factory.SubFactory(CompanyFactory)

class MultiLineQuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'Multi Line'
    is_required = True
    type = 'textarea'

    company = factory.SubFactory(CompanyFactory)

class CheckboxQuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'Checkbox'
    is_required = True
    type = 'checkbox'

    company = factory.SubFactory(CompanyFactory)

class FileQuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'File'
    is_required = True
    type = 'file'

    company = factory.SubFactory(CompanyFactory)

class InterviewStageFactory(factory.Factory):
    FACTORY_FOR = InterviewStage

    name = 'Phone interview'
    company = factory.SubFactory(CompanyFactory)
