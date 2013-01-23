import factory

from hyrodactil.settings import base


class UserFactory(factory.Factory):
    FACTORY_FOR = base.AUTH_USER_MODEL

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
