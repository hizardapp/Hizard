from base import *

########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = DJANGO_ROOT
TEST_DISCOVER_ROOT = DJANGO_ROOT
TEST_DISCOVER_PATTERN = "*"

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
    'django.contrib.auth.hashers.MD5PasswordHasher',
    )
