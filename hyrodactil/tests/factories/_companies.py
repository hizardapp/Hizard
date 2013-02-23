import factory

from companies.models import Company


class CompanyFactory(factory.Factory):
    FACTORY_FOR = Company

    name = 'ACME'
    website = 'http://www.acme.com'
