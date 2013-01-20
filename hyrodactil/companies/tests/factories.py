import factory

from django.contrib.auth.models import User

from ..models import Company, Department, Question


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = 'bob'
    email = 'bob@bob.com'
    password = 'bob'

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


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
