import factory

from companysettings.models import Department, Question, InterviewStage
import _companies


class DepartmentFactory(factory.Factory):
    FACTORY_FOR = Department

    name = 'Engineering'
    company = factory.SubFactory(_companies.CompanyFactory)


class SingleLineQuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'Single Line'
    type = 'textbox'

    company = factory.SubFactory(_companies.CompanyFactory)


class MultiLineQuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'Multi Line'
    type = 'textarea'

    company = factory.SubFactory(_companies.CompanyFactory)


class CheckboxQuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'Checkbox'
    type = 'checkbox'

    company = factory.SubFactory(_companies.CompanyFactory)


class FileQuestionFactory(factory.Factory):
    FACTORY_FOR = Question

    name = 'File'
    type = 'file'

    company = factory.SubFactory(_companies.CompanyFactory)


class InterviewStageFactory(factory.Factory):
    FACTORY_FOR = InterviewStage

    name = 'Phone interview'
    position = factory.Sequence(lambda n: n)
    company = factory.SubFactory(_companies.CompanyFactory)
