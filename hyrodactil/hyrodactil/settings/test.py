from base import *

########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
# Default is test*.py
TEST_DISCOVER_PATTERN = "*"

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'core.middlewares.AppSubdomainRequired',
    'core.middlewares.CompanyRequired'
)

########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

######### FAST HASHING FOR PASSWORDS
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
)
SOUTH_TESTS_MIGRATE = False

MEDIA_ROOT = normpath(join(SITE_ROOT, 'tests/media'))

APP_SITE_DOMAIN = 'app.test.com:80'
APP_SITE_URL = 'http://app.test.com'
PUBLIC_DOMAIN = 'test.com:80'
PUBLIC_URL = 'http://test.com'
