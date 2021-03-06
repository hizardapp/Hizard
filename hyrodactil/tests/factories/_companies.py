import factory

from companies.models import Company


class CompanyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Company

    name = 'ACME'
    website = 'http://www.acme.com'
    subdomain = factory.Sequence(lambda n: 'domain%s' % n)
