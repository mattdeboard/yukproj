from yukproj.settings import *

DEBUG = True

TEMPLATE_DIS = (
    '/a/mattdeboard.net/yukproj/yuk/templates',
)

HAYSTACK_WHOOSH_PATH = '/a/mattdeboard.net/yukproj/yuk/whoosh'

STATIC_DOC_ROOT = "/a/mattdeboard.net/yukproj/yuk/static"

SITE_URL = "http://127.0.0.1:8000"

MEDIA_URL = "/site_media/"

BLUEPRINT_PATH = MEDIA_URL + "css/blueprint/"