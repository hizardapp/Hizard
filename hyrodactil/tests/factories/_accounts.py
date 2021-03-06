import factory

from accounts.models import CustomUser

import _companies


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CustomUser

    email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
    name = 'Ann Onymous'
    password = 'bob'
    is_company_admin = False
    is_active = True
    activation_key = '842771118e1d60c103c068280e023bd362af5cc4'
    company = factory.SubFactory(_companies.CompanyFactory)

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
