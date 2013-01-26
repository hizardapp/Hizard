import factory

from accounts.models import CustomUser


class UserFactory(factory.Factory):
    FACTORY_FOR = CustomUser

    email = 'bob@bob.com'
    password = 'bob'
    activation_key = '842771118e1d60c103c068280e023bd362af5cc4'

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
