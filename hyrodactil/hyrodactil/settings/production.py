"""Production settings and globals."""

from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hyrodactil',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

STATIC_ROOT = '/home/app/static/'
MEDIA_URL = 'http://hizard.com/media/'
