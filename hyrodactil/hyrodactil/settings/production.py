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

SESSION_COOKIE_SECURE = True

STATIC_ROOT = '/home/app/static/'

RAVEN_CONFIG = {
    'dsn': 'https://440d63c598e04fde809ebb8f64495b7d:e5d86579a5ad4d61855009b0da779a9e@app.getsentry.com/7604',
}

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)

MEDIA_URL = 'https://app.hizard.com/media/'
