import factory

from companies.models import Company
from ._accounts import UserFactory


class CompanyFactory(factory.Factory):
    FACTORY_FOR = Company

    name = 'ACME'
    owner = factory.SubFactory(UserFactory)
