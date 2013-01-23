from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            msg = _('Email is mandatory')
            raise ValueError(msg)

        user = self.model( email=CustomUserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )

    USERNAME_FIELD = 'email'
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email