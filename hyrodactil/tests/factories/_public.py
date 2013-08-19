import factory

from public.models import Interest


class InterestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Interest

    email = "something@someone.com"
