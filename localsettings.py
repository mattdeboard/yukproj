from yukproj.settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yukdb',                     
        'USER': '',                     
        'PASSWORD': '',                 
        'HOST': '',                     
        'PORT': '',                     
    }
}

TEMPLATE_DIRS = (
    '/a/mattdeboard.net/yukproj/yuk/templates',
)

STATIC_DOC_ROOT = 'a/mattdeboard.net/yukproj/yuk/static'