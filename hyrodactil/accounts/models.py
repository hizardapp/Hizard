import base64
import datetime
import hashlib
import random

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

from hyrodactil.settings import base


class CustomUserManager(BaseUserManager):
    """
    Manager for the custom user, responsible for creating new users and
    activating them
    """
    def create_user(self, email, password=None, active=True):
        """
        Creates a basic user which is active by default.
        If we want to create an inactive one, an activation key is generated
        """
        if not email:
            msg = _('Email is mandatory')
            raise ValueError(msg)

        user = self.model(email=CustomUserManager.normalize_email(email))
        user.set_password(password)

        if not active:
            # create token here
            user.activation_key = self._create_activation_token(email)
            user.is_active = False

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates an active superuser
        """
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


    def activate_user(self, activation_key):
        """
        Activates an user account by its activation key.
        If the activation key doesn't exist (someone typed a random one or
        the user has already been activated), return False.
        Otherwise, return the updated user object.
        """
        if not activation_key:
            return False
        try:
            user = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False

        if not user.activation_key_expired():
            user.activation_key = ''
            user.is_active = True
            user.save()
            return user

        return False

    def delete_expired_users(self):
        """
        Deletes all users that have an expired activation token
        """
        for user in self.all():
            if user.activation_key_expired():
                user.delete()

    def _create_activation_token(self, email):
        """
        Generates an activation token based on a random salt + the user's email
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        return hashlib.sha1(salt + email).hexdigest()


def get_file_path(instance, filename):
    """
    Used by the avatar field in the CustomUser model
    Base64 the name of the file and returns the path where it should be
    saved to
    """
    ext = filename.split('.')[-1]
    hash = base64.urlsafe_b64encode(instance.email).rstrip("=")
    filename = "%s.%s" % (hash, ext)

    return '%s/avatars/%s' % (base.MEDIA_ROOT, filename)


class CustomUser(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom user using the django 1.5 customisable users.
    Uses email as username field and adds optional avatar, first name, last
    name and an activation key
    """
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
        db_index=True,
    )

    USERNAME_FIELD = 'email'

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    avatar = models.ImageField(
        verbose_name=_('Avatar'),
        blank=True,
        upload_to=get_file_path
    )
    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=255,
        blank=True
    )
    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=255,
        blank=True
    )
    activation_key = models.CharField(
        verbose_name=_('Activation key'),
        max_length=40,
        blank=True
    )


    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def activation_key_expired(self):
        """
        Determines if the activation key is expired.
        This is known by checking if the current date is after the date
        the user created its account + the ACCOUNT_ACTIVATION_DAYS period
        defined in the settings
        """
        delta = datetime.timedelta(days=base.ACCOUNT_ACTIVATION_DAYS)
        now = datetime.datetime.now()

        if now > self.created + delta:
            'print expired'
            return True
        else:
            return False

    def __unicode__(self):
        return self.email
