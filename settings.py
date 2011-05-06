import djcelery
from yukproj.djsecrets import *

djcelery.setup_loader()

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Matt DeBoard', 'matt.deboard@gmail.com'),
)


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pg_links',                     
        'USER': '',                     
        'PASSWORD': '',                 
        'HOST': '',                     
        'PORT': '',                     
    }
}

TIME_ZONE = 'America/Chicago'

DEFAULT_FROM_EMAIL = 'admin@yukmarks.com'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True


USE_L10N = True


MEDIA_ROOT = ''

MEDIA_URL = "http://media.yukmarks.com/"

ADMIN_MEDIA_PREFIX = '/media/'


SECRET_KEY = secret


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'yukproj.urls'

TEMPLATE_DIRS = (
    '/a/mattdeboard.net/src/yukproj/yuk/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "yuk.processors.site_url_processor",
    "yuk.processors.text_area_processor",
    "yuk.processors.search_processor",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'taggit',
    'taggit_templatetags',
    'yuk',
    'registration',
    'south',
    'haystack',
    'django_extensions',
    'djcelery',
)

ACCOUNT_ACTIVATION_DAYS = 7

BLUEPRINT_PATH = MEDIA_URL + "css/blueprint/"

HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_SITECONF = 'yukproj.search_sites'
HAYSTACK_WHOOSH_PATH = '/a/mattdeboard.net/src/yukproj/yuk/whoosh'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 25
HAYSTACK_DEFAULT_OPERATOR = 'OR'

# django-celery config options
#BROKER_HOST = "localhost"
#BROKER_PORT = 5672
#BROKER_USER = celeryuser
#BROKER_PASSWORD = celerypass
#BROKER_VHOST = "/"

SITE_URL = "http://yukmarks.com"
